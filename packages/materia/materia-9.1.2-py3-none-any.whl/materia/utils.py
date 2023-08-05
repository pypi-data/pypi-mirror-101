from __future__ import annotations
from typing import Iterable, Optional

import collections
import contextlib
import copy
import functools
import itertools
import networkx as nx
import numpy as np
import os
import pathlib
import tempfile
import rdkit
import rdkit.Chem
import rdkit.Chem.AllChem
import scipy.interpolate
import scipy.spatial


__all__ = [
    "expand",
    "extrapolate",
    "interpolate",
    "IO",
    "memoize",
    "mkdir_safe",
    "NestedDictionary",
    "Settings",
    "temporary_seed",
    "work_dir",
    "xyz2mol",
]


def expand(path: str, dir: Optional[str] = None) -> str:
    p = pathlib.Path(path).expanduser()
    if dir is not None:
        p = pathlib.Path(dir).joinpath(p)
    return str(p.expanduser().resolve())


def extrapolate(x, y, x_extrap_to):
    # simple linear extrapolation
    x_lb, x_nlb, *_, x_nub, x_ub = x
    y_lb, y_nlb, *_, y_nub, y_ub = y

    # extrapolate down
    m_lb = (y_nlb - y_lb) / (x_nlb - x_lb)
    x_down = x_extrap_to[np.where(x_extrap_to < x_lb)]
    y_down = y_lb + m_lb * (x_down - x_lb)

    # extrapolate up
    m_ub = (y_ub - y_nub) / (x_ub - x_nub)
    x_up = x_extrap_to[np.where(x_extrap_to > x_ub)]
    y_up = y_ub + m_ub * (x_up - x_ub)

    return np.hstack((x_down, x, x_up)), np.hstack((y_down, y, y_up))


def interpolate(x, y, x_interp_to, method="cubic_spline"):
    if method == "sprague":
        return interpolate_sprague(x=x, y=y, x_interp_to=x_interp_to)
    elif method == "cubic_spline":
        return interpolate_cubic_spline(x=x, y=y, x_interp_to=x_interp_to)
    elif method == "linear_spline":
        return interpolate_linear_spline(x=x, y=y, x_interp_to=x_interp_to)
    else:
        raise ValueError(f"Interpolation method {method} not recognized.")


def interpolate_cubic_spline(x, y, x_interp_to):
    x_lb, *_, x_ub = x
    x_interp = x_interp_to[(x_interp_to >= x_lb) & (x_interp_to <= x_ub)]
    y_interp = scipy.interpolate.CubicSpline(x=x, y=y)(x_interp)

    return x_interp, y_interp


def interpolate_linear_spline(x, y, x_interp_to):
    x_lb, *_, x_ub = x
    x_interp = x_interp_to[(x_interp_to >= x_lb) & (x_interp_to <= x_ub)]
    y_interp = np.interp(x=x_interp, xp=x, fp=y)

    return x_interp, y_interp


def interpolate_sprague(x, y, x_interp_to):
    # FIXME: this implementation of Sprague interpolation is broken somehow!
    # data taken from
    # https://link.springer.com/content/pdf/10.1007/978-3-642-27851-8_366-1.pdf
    # FIXME: we have to convert spec to wavelength spec with nanometer units first
    interp_coeffs = np.array(
        [
            [0, 0, 24, 0, 0, 0],
            [2, -16, 0, 16, -2, 0],
            [-1, -16, -30, 16, -1, 0],
            [-9, 39, 70, 66, -33, 7],
            [13, -64, 126, -124, 61, -12],
            [-5, 25, -50, 50, -25, 5],
        ]
    )
    # Sprague boundary points
    sbp1 = np.dot([884, -1960, 3033, -2648, 1080, 180], y[:6]) / 209
    sbp2 = np.dot([508, -540, 488, -367, 144, -24], y[:6]) / 209
    sbp3 = np.dot([-24, 144, -367, 488, -540, 508], y[-6:]) / 209
    sbp4 = np.dot([-180, 1080, -2648, 3033, -1960, 884], y[-6:]) / 209

    sprague_y = np.hstack([[sbp1, sbp2], y, [sbp3, sbp4]])[:, None]

    poly_c_mat = np.hstack(
        [
            (interp_coeffs @ np.roll(sprague_y, -i)[:6])
            for i in range(len(sprague_y) - 5)
        ]
    )  # [::-1]

    def interp(x_to):
        lower_bound_indices = np.searchsorted(x, x_to) - 1
        scaled_x = (x_to - x[lower_bound_indices]) / (
            x[lower_bound_indices + 1] - x[lower_bound_indices]
        )
        scaled_x_powers = np.vander(x=scaled_x, N=6)
        poly_coeffs = poly_c_mat[:, lower_bound_indices]
        # print(poly_coeffs.shape)
        # print(scaled_x.shape)
        return np.array(
            [
                np.polyval(p=coeffs[::-1], x=X)
                for coeffs, X in zip(poly_coeffs.T, scaled_x)
            ]
        )
        return (scaled_x_powers * poly_coeffs.T).sum(axis=1)

    y_interp = interp(x=x_interp_to)

    return x_interp_to, y_interp


_IO = collections.namedtuple("IOParams", ["work_dir", "inp", "out"])


class IO:
    def __init__(
        self,
        inp: Optional[str] = None,
        out: Optional[str] = None,
        work_dir: Optional[str] = ".",
        temp: Optional[bool] = False,
    ) -> None:
        self.inp = inp
        self.out = out
        self.work_dir = expand(work_dir)
        self.temp = temp

    @contextlib.contextmanager
    def __call__(self):
        mkdir_safe(self.work_dir)

        if self.temp:
            cm = tempfile.TemporaryDirectory(dir=self.work_dir)
        else:
            cm = contextlib.nullcontext(self.work_dir)

        with cm as wd:
            try:
                old_temp, self.temp = copy.copy(self.temp), False
                old_work_dir, self.work_dir = copy.copy(self.work_dir), wd

                yield _IO(
                    wd,
                    expand(self.inp, wd) if self.inp is not None else None,
                    expand(self.out, wd) if self.out is not None else None,
                )
            finally:
                self.temp, self.work_dir = old_temp, old_work_dir


class _Cache(collections.OrderedDict):
    def last_result(self, n=1):
        return tuple(self.values())[-n]

    def last_args(self, n=1):
        args, kwarg_items = tuple(self.keys())[-n]
        return args, dict(kwarg_items)


def memoize(func):
    func.cache = _Cache()

    @functools.wraps(func)
    def memoized(*args, **kwargs):
        k = (args, frozenset(kwargs.items()))
        if k not in func.cache:
            func.cache[k] = func(*args, **kwargs)

        return func.cache[k]

    return memoized


def mkdir_safe(directory: str) -> None:
    with contextlib.suppress(FileExistsError):
        os.makedirs(directory)


@contextlib.contextmanager
def temporary_seed(seed: int) -> None:
    # adapted from https://stackoverflow.com/a/49557127
    state = np.random.get_state()
    if seed is not None:
        np.random.seed(seed)
    try:
        yield
    finally:
        np.random.set_state(state)


@contextlib.contextmanager
def work_dir(dir: Optional[str] = None):
    # FIXME: learn how to type annotation yields
    with contextlib.nullcontext(
        expand(dir)
    ) if dir is not None else tempfile.TemporaryDirectory(dir=dir) as wd:
        try:
            mkdir_safe(dir=wd)
            yield wd
        finally:
            pass


class NestedDictionary(collections.abc.MutableMapping):
    def __init__(self, *args, **kwargs) -> None:
        self.d = dict(*args, **kwargs)

    def __getitem__(self, keys) -> NestedDictionary:
        if not isinstance(keys, tuple):
            keys = (keys,)

        branch = self.d
        for k in keys:
            branch = branch[k]

        return NestedDictionary(branch) if isinstance(branch, dict) else branch

    def __setitem__(self, keys, value) -> None:
        if not isinstance(keys, tuple):
            keys = (keys,)

        *most_keys, last_key = keys

        branch = self.d
        for k in most_keys:
            if k not in branch:
                branch[k] = {}
            branch = branch[k]

        branch[last_key] = value

    def __delitem__(self, keys) -> None:
        if not isinstance(keys, tuple):
            keys = (keys,)

        *most_keys, last_key = keys

        branch = self.d
        for k in most_keys:
            # FIXME: does this really need to be here? if we're deleting the item,
            # we shouldn't ever need to make branches on the way to the item...
            if k not in branch:
                branch[k] = {}
            branch = branch[k]

        del branch[last_key]

    def __iter__(self, d=None, prepath=()):
        if d is None:
            d = self.d
        for k, v in d.items():
            if hasattr(v, "items"):
                for keys in self.__iter__(d=v, prepath=prepath + (k,)):
                    yield keys
            else:
                yield prepath + (k,)

    def __len__(self) -> int:
        return sum(1 for _ in self)

    def __str__(self) -> str:
        return str(self.d)

    def __repr__(self) -> str:
        return repr(self.d)


class Settings(NestedDictionary):
    def update(self, settings: Settings) -> None:
        for k, v in settings.items():
            self.__setitem__(keys=k, value=v)


# ------------------------------------------------------ #

##
# Written by Jan H. Jensen based on this paper Yeonjoon Kim and Woo Youn Kim
# "Universal Structure Conversion Method for Organic Molecules: From Atomic Connectivity
# to Three-Dimensional Geometry" Bull. Korean Chem. Soc. 2015,
# Vol. 36, 1769-1777 DOI: 10.1002/bkcs.10334
#


def xyz2mol(
    atomic_numbers, charge, atomic_positions, charged_fragments: Optional[bool] = True
) -> rdkit.Chem.rdchem.Mol:
    # alternatively radicals are made if charged_fragments=False

    # Get atom connectivity (ac) matrix, list of atomic numbers, molecular charge,
    # and mol object with no connectivity information
    ac, mol = _atom_connectivity(atomic_numbers, atomic_positions)

    # Convert ac to bond order matrix and add connectivity and charge info to mol object
    new_mol = _connected_mol(mol, ac, atomic_numbers, charge, charged_fragments)

    # Check for stereocenters and chiral centers
    new_mol = _chiral_stereo_check(new_mol)

    # # Canonical hack
    # smiles = Chem.MolToSmiles(mol, isomericSmiles=True)
    # m = Chem.MolFromSmiles(smiles)
    # smiles = Chem.MolToSmiles(m, isomericSmiles=True)

    return new_mol


def _atom_connectivity(atomic_numbers: Iterable[int], atomic_positions):
    # generate proto molecule
    first, *rest = atomic_numbers

    mol = rdkit.Chem.MolFromSmarts("[#" + str(first) + "]")
    rwMol = rdkit.Chem.RWMol(mol)

    for Z in rest:
        rwMol.AddAtom(rdkit.Chem.Atom(Z))

    mol = rwMol.GetMol()

    # compute atom connectivity matrix

    dmat = scipy.spatial.distance_matrix(atomic_positions, atomic_positions)
    pt = rdkit.Chem.GetPeriodicTable()

    num_atoms = len(atomic_numbers)
    ac = np.zeros((num_atoms, num_atoms)).astype(int)

    for i in range(num_atoms):
        a_i = mol.GetAtomWithIdx(i)
        Rcov_i = pt.GetRcovalent(a_i.GetAtomicNum()) * 1.30
        for j in range(i + 1, num_atoms):
            a_j = mol.GetAtomWithIdx(j)
            Rcov_j = pt.GetRcovalent(a_j.GetAtomicNum()) * 1.30
            if dmat[i, j] <= Rcov_i + Rcov_j:
                ac[i, j] = 1
                ac[j, i] = 1

    return ac, mol


def _connected_mol(
    mol: rdkit.Chem.rdchem.Mol,
    ac,
    atomic_numbers: Iterable[int],
    charge: int,
    charged_fragments: bool,
) -> rdkit.Chem.rdchem.Mol:
    # convert ac matrix to bond order (BO) matrix
    BO, atomic_valence_electrons = _bond_order(
        ac, atomic_numbers, charge, charged_fragments
    )

    # add BO connectivity and charge info to mol object
    mol = _bond_order_to_mol(
        mol, BO, atomic_numbers, atomic_valence_electrons, charge, charged_fragments
    )

    return mol


def _bond_order(
    ac, atomic_numbers: Iterable[int], charge: int, charged_fragments: bool
):
    # TODO
    atomic_valence = collections.defaultdict(list)
    atomic_valence[1] = [1]
    atomic_valence[6] = [4]
    atomic_valence[7] = [4, 3]
    atomic_valence[8] = [2, 1]
    atomic_valence[9] = [1]
    atomic_valence[14] = [4]
    atomic_valence[15] = [5, 4, 3]
    atomic_valence[16] = [6, 4, 2]
    atomic_valence[17] = [1]
    atomic_valence[32] = [4]
    atomic_valence[35] = [1]
    atomic_valence[53] = [1]

    atomic_valence_electrons = {}
    atomic_valence_electrons[1] = 1
    atomic_valence_electrons[6] = 4
    atomic_valence_electrons[7] = 5
    atomic_valence_electrons[8] = 6
    atomic_valence_electrons[9] = 7
    atomic_valence_electrons[14] = 4
    atomic_valence_electrons[15] = 5
    atomic_valence_electrons[16] = 6
    atomic_valence_electrons[17] = 7
    atomic_valence_electrons[32] = 4
    atomic_valence_electrons[35] = 7
    atomic_valence_electrons[53] = 7

    # make a list of valences, e.g. for CO: [[4],[2,1]]
    valences_list_of_lists = [atomic_valence[Z] for Z in atomic_numbers]

    # convert [[4],[2,1]] to [[4,2],[4,1]]
    valences_list = itertools.product(*valences_list_of_lists)

    best_BO = ac.copy()

    # implemenation of algorithm shown in Figure 2
    # ua: unsaturated atoms
    # du: degree of unsaturation (u matrix in Figure)
    # best_BO: Bcurr in Figure
    #

    for valences in valences_list:
        ac_valence = list(ac.sum(axis=1))
        ua, du_from_ac = _get_unsaturated_atoms(valences, ac_valence)

        if len(ua) == 0 and _bond_order_is_ok(
            ac,
            ac,
            charge,
            du_from_ac,
            atomic_valence_electrons,
            atomic_numbers,
            charged_fragments,
        ):
            return ac, atomic_valence_electrons

        for ua_pairs in _get_ua_pairs(ua, ac):
            BO = _get_bond_orders(ac, ua, du_from_ac, valences, ua_pairs)
            if _bond_order_is_ok(
                BO,
                ac,
                charge,
                du_from_ac,
                atomic_valence_electrons,
                atomic_numbers,
                charged_fragments,
            ):
                return BO, atomic_valence_electrons

            elif BO.sum() >= best_BO.sum() and (BO.sum(axis=1) <= valences).all():
                best_BO = BO.copy()

    return best_BO, atomic_valence_electrons


def _get_unsaturated_atoms(max_valences, valences):
    diffs = np.array(max_valences) - np.array(valences)
    inds = diffs > 0

    unsatured_atoms = np.flatnonzero(inds)
    degree_of_unsaturation = diffs[inds]

    return unsatured_atoms, degree_of_unsaturation


def _bond_order_is_ok(
    BO,
    ac,
    charge: int,
    du,
    atomic_valence_electrons,
    atomic_numbers: Iterable[int],
    charged_fragments: bool,
) -> bool:
    Q = 0  # total charge
    q_list = []
    if charged_fragments:
        BO_valences = list(BO.sum(axis=1))
        for i, atom in enumerate(atomic_numbers):
            q = _get_atomic_charge(atom, atomic_valence_electrons[atom], BO_valences[i])
            Q += q
            if atom == 6:
                number_of_single_bonds_to_C = list(BO[i, :]).count(1)
                if number_of_single_bonds_to_C == 2 and BO_valences[i] == 2:
                    Q += 1
                    q = 2
                if number_of_single_bonds_to_C == 3 and Q + 1 < charge:
                    Q += 2
                    q = 1

            if q != 0:
                q_list.append(q)

    return (BO - ac).sum() == sum(du) and charge == Q and len(q_list) <= abs(charge)


def _get_bond_orders(ac, ua, du, valences, ua_pairs):
    BO = ac.copy()
    du_save = []

    while du_save != list(du):
        for i, j in ua_pairs:
            BO[i, j] += 1
            BO[j, i] += 1

        BO_valence = list(BO.sum(axis=1))
        du_save = list(copy.copy(du))
        ua, du = _get_unsaturated_atoms(valences, BO_valence)
        ua_pairs, *_ = _get_ua_pairs(ua, ac)

    return BO


def _chiral_stereo_check(mol: rdkit.Chem.rdchem.Mol) -> rdkit.Chem.rdchem.Mol:
    rdkit.Chem.SanitizeMol(mol)
    rdkit.Chem.DetectBondStereochemistry(mol, -1)
    rdkit.Chem.AssignStereochemistry(mol, flagPossibleStereoCenters=True, force=True)
    rdkit.Chem.AssignAtomChiralTagsFromStructure(mol, -1)

    return mol


def _get_atomic_charge(atom, atomic_valence_electrons, BO_valence) -> int:
    if atom == 1:
        charge = 1 - BO_valence
    elif atom == 5:
        charge = 3 - BO_valence
    elif atom == 15 and BO_valence == 5:
        charge = 0
    elif atom == 16 and BO_valence == 6:
        charge = 0
    else:
        charge = atomic_valence_electrons - 8 + BO_valence

    return charge


def _clean_charges(mol: rdkit.Chem.rdchem.Mol) -> rdkit.Chem.rdchem.Mol:
    rdkit.Chem.SanitizeMol(mol)
    # rxn_smarts = ['[N+:1]=[*:2]-[C-:3]>>[N+0:1]-[*:2]=[C-0:3]',
    #              '[N+:1]=[*:2]-[O-:3]>>[N+0:1]-[*:2]=[O-0:3]',
    #              '[N+:1]=[*:2]-[*:3]=[*:4]-[O-:5]>>[N+0:1]-[*:2]=[*:3]-[*:4]=[O-0:5]',
    #              '[#8:1]=[#6:2]([!-:6])[*:3]=[*:4][#6-:5]>>[*-:1][*:2]([*:6])=[*:3][*:4]=[*+0:5]',
    #              '[O:1]=[c:2][c-:3]>>[*-:1][*:2][*+0:3]',
    #              '[O:1]=[C:2][C-:3]>>[*-:1][*:2]=[*+0:3]']

    rxn_smarts = [
        "[#6,#7:1]1=[#6,#7:2][#6,#7:3]=[#6,#7:4][CX3-,NX3-:5][#6,#7:6]1=[#6,#7:7]>>\
        [#6,#7:1]1=[#6,#7:2][#6,#7:3]=[#6,#7:4][-0,-0:5]=[#6,#7:6]1[#6-,#7-:7]",
        "[#6,#7:1]1=[#6,#7:2][#6,#7:3](=[#6,#7:4])[#6,#7:5]=[#6,#7:6][CX3-,NX3-:7]1>>\
        [#6,#7:1]1=[#6,#7:2][#6,#7:3]([#6-,#7-:4])=[#6,#7:5][#6,#7:6]=[-0,-0:7]1",
    ]

    fragments = rdkit.Chem.GetMolFrags(mol, asMols=True, sanitizeFrags=False)

    for i, fragment in enumerate(fragments):
        for smarts in rxn_smarts:
            patt = rdkit.Chem.MolFromSmarts(smarts.split(">>")[0])
            while fragment.HasSubstructMatch(patt):
                rxn = rdkit.Chem.AllChem.ReactionFromSmarts(smarts)
                ps = rxn.RunReactants((fragment,))
                fragment = ps[0][0]
                rdkit.Chem.SanitizeMol(fragment)

        mol = fragment if i == 0 else rdkit.Chem.CombineMols(mol, fragment)

    return mol


def _bond_order_to_mol(
    mol: rdkit.Chem.rdchem.Mol,
    BO_matrix,
    atomic_numbers: Iterable[int],
    atomic_valence_electrons,
    mol_charge,
    charged_fragments: bool,
):
    # based on code written by Paolo Toscani

    l1 = len(BO_matrix)
    l2 = len(atomic_numbers)
    BO_valences = list(BO_matrix.sum(axis=1))

    if l1 != l2:
        raise RuntimeError(
            "sizes of adjMat ({0:d}) and atomic_numbers " "{1:d} differ".format(l1, l2)
        )

    rwMol = rdkit.Chem.RWMol(mol)

    bondTypeDict = {
        1: rdkit.Chem.BondType.SINGLE,
        2: rdkit.Chem.BondType.DOUBLE,
        3: rdkit.Chem.BondType.TRIPLE,
    }

    for i in range(l1):
        for j in range(i + 1, l1):
            bo = int(round(BO_matrix[i, j]))
            if bo == 0:
                continue
            bt = bondTypeDict.get(bo, rdkit.Chem.BondType.SINGLE)
            rwMol.AddBond(i, j, bt)
    mol = rwMol.GetMol()

    if charged_fragments:
        mol = set_atomic_charges(
            mol,
            atomic_numbers,
            atomic_valence_electrons,
            BO_valences,
            BO_matrix,
            mol_charge,
        )
    else:
        mol = set_atomic_radicals(
            mol, atomic_numbers, atomic_valence_electrons, BO_valences
        )

    return mol


def set_atomic_charges(
    mol: rdkit.Chem.rdchem.Mol,
    atomic_numbers: Iterable[int],
    atomic_valence_electrons,
    BO_valences,
    BO_matrix,
    mol_charge,
) -> rdkit.Chem.rdchem.Mol:
    q = 0
    for i, atom in enumerate(atomic_numbers):
        a = mol.GetAtomWithIdx(i)
        charge = _get_atomic_charge(
            atom, atomic_valence_electrons[atom], BO_valences[i]
        )
        q += charge
        if atom == 6:
            number_of_single_bonds_to_C = list(BO_matrix[i, :]).count(1)
            if number_of_single_bonds_to_C == 2 and BO_valences[i] == 2:
                q += 1
                charge = 0
            if number_of_single_bonds_to_C == 3 and q + 1 < mol_charge:
                q += 2
                charge = 1

        if abs(charge) > 0:
            a.SetFormalCharge(int(charge))

    mol = _clean_charges(mol)

    return mol


def set_atomic_radicals(
    mol: rdkit.Chem.rdchem.Mol,
    atomic_numbers: Iterable[int],
    atomic_valence_electrons,
    BO_valences,
) -> rdkit.Chem.rdchem.Mol:
    # The number of radical electrons = absolute atomic charge
    for i, atom in enumerate(atomic_numbers):
        a = mol.GetAtomWithIdx(i)
        charge = _get_atomic_charge(
            atom, atomic_valence_electrons[atom], BO_valences[i]
        )

        if abs(charge) > 0:
            a.SetNumRadicalElectrons(abs(int(charge)))

    return mol


def _get_ua_pairs(ua, ac):
    bonds = []

    for k, i in enumerate(ua):
        for j in ua[k + 1 :]:
            if ac[i, j] == 1:
                bonds.append(tuple(sorted([i, j])))

    if len(bonds) == 0:
        return [()]

    G = nx.Graph()
    G.add_edges_from(bonds)
    ua_pairs = [list(nx.max_weight_matching(G))]

    return ua_pairs


# ----------------------------------------------------- #

# def plot_lune(self, samples):
#     import matplotlib.pyplot as plt
#     from mpl_toolkits.mplot3d import Axes3D
#     xs,ys,zs = samples
#     fig = plt.figure()
#     ax = Axes3D(fig)
#     phigrid,thetagrid = np.mgrid[0.0:np.pi:100j,0.0:2.0*np.pi:100j]
#     xgrid = np.sin(phigrid)*np.cos(thetagrid)
#     ygrid = np.sin(phigrid)*np.sin(thetagrid)
#     zgrid = np.cos(phigrid)
#     ax.plot_surface(xgrid,ygrid,zgrid,rstride=1,cstride=1,color='c',alpha=0.1,linewidth=0)
#     ax.scatter(xs,ys,zs)
#     ax.quiver([0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[1,0,0,-1,0,0],[0,1,0,0,-1,0],[0,0,1,0,0,-1],arrow_length_ratio=0.1,linewidths=[2,2,2,2,2,2])
#     #ax.set_aspect('equal')
#     ax.xaxis._axinfo['juggled'] = (0,0,0)
#     ax.yaxis._axinfo['juggled'] = (1,1,1)
#     ax.zaxis._axinfo['juggled'] = (2,2,2)
#     plt.show(block=True)
