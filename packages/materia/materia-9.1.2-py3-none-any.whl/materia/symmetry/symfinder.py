from __future__ import annotations
from typing import Iterable, List

import itertools
import materia as mtr
import numpy as np
import scipy.linalg

__all__ = [
    "search_symmetries_automorphism",
    "search_symmetries_explicit",
    "plot_symmetries",
]

# def generate_axes(structure, symprec=5, seed=None):
#     symmetries = tuple(
#         R.matrix
#         for R in materia.symmetry.GraphSymmetryFinder().symmetry_operations(
#             structure=structure, symprec=symprec
#         )
#         if not (np.allclose(R.matrix, np.eye(3)) or np.allclose(R.matrix, np.eye(3)))
#     )

#     num_symmetries = len(symmetries)

# FIXME: is there an easy way to check if R1 == -R2
# when R1 and R2 are SymmetryOperation objects?
#     excluded_generator = (
#         (R1, R2, _excluded_circles(A=R1, B=R2))
#         for R1, R2 in itertools.product(symmetries, symmetries)
#         if (not np.allclose(R1, R2) and not np.allclose(R1, -R2))
#     )  # R1 != R2)#
#     try:
#         R1, R2, excluded_circles = next(excluded_generator)
#         intersections = np.hstack(
#             [
#                 materia.utils.perpendicular_vector(a=n1, b=n2)
#                 for n1, n2 in itertools.combinations(
#                     excluded_circles.T[:, :, None], r=2
#                 )
#             ]
#         )
#         A, B, C = materia.utils.closest_trio(points=intersections).T[:, :, None]
#         sin_alpha = scipy.linalg.norm(A)
#         sin_beta = scipy.linalg.norm(B)
#         sin_gamma = scipy.linalg.norm(C)
#         # triangle vertices
#         A /= sin_alpha
#         B /= sin_beta
#         C /= sin_gamma

#         q = materia.utils.sample_spherical_triangle(
#             A=A,
#             B=B,
#             C=C,
#             sin_alpha=sin_alpha,
#             sin_beta=sin_beta,
#             sin_gamma=sin_gamma,
#             seed=seed,
#         )
#         r = R1 @ q
#         s = R2 @ q

#         axes = np.hstack([q, r, s])
#     except StopIteration:
#         if num_symmetries > 0:
#             R1 = symmetries[0]
#             R2 = None

#             q = materia.utils.make_nontrivial_vector(R=R1, seed=seed)
#             r = R1 @ q
#             s = materia.utils.perpendicular_vector(a=q, b=r)

#             axes = np.hstack([q, r, s])
#         else:
#             R1 = R2 = None
#             axes = np.eye(3)

#     if _validate_axes(axes=axes):
#         # FIXME: this wprime line is wrong - replace the conditional with something
# which can tell whether or not the three axes are all symmetry related
#         # wprime = (A.T@axes[:,-1])[:,None] if wprime is not None else wprime
#         return axes, R1, R2
#     else:
#         print("Error validating vectors!")
#         return np.eye(3), None, None


# def _excluded_circles(A, B):
#     """
#     Construct list of excluded circles on unit sphere.

#     Parameters
#     ----------
#     A,B : numpy.ndarray
#         3x3 Numpy arrays representating the two symmetry
#         operations whose excluded circles are being calculated.

#     Returns
#     -------
#     numpy.ndarray:
#         3xNc Numpy array representing the normal vectors
#         of excluded circles, where Nc is the number of excluded circles.
#     """
#     identity = np.eye(3)
#     null_bases = [
#         scipy.linalg.null_space(M)
#         for M in (
#             (A + identity, A - identity, B + identity, B - identity, A + B, A - B)
#             if B is not None
#             else (A + identity, A - identity)
#         )
#     ]

#     # each null basis with geometric multiplicity two results
#       in a circle of excluded points whose normal vector
#       is the cross product of the null basis
#     fixed_excluded_circles = [
#         materia.utils.perpendicular_vector(*nb.T[:, :, None])
#         for nb in null_bases
#         if nb.shape[1] == 2
#     ]
#     # create additional circles which encompass all excluded
#       points and which go through the selected intersection
#     additional_excluded_circles = _extend_points_to_circles(
#         _intersection(*fixed_excluded_circles),
#         *(nb for nb in null_bases if nb.shape[1] == 1)
#     )
#     excluded_circles = materia.utils.linearly_independent(
#         vectors=np.hstack(fixed_excluded_circles + additional_excluded_circles)
#     )

#     # if there are still fewer than three excluded circles,
#       generate additional circles perpendicular to
#       the previous circle(s)
#     while excluded_circles.shape[1] < 3:
#         excluded_circles = np.hstack(
#             [
#                 excluded_circles,
#                 materia.utils.perpendicular_vector(*excluded_circles.T[:, :, None]),
#             ]
#         )

#     assert excluded_circles.shape[1] < 4

#     return excluded_circles


# def _intersection(*normals):
#     if (
#         len(normals) > 1
#     ):  # pick two fixed circles and choose their intersection axis
#           as the intersection axis for subsequent circles
#           (excepting the third fixed circle);
#           if there are two fixed circles, choose their intersection axis
#         a, b, *_ = normals
#         return materia.utils.perpendicular_vector(a=a, b=b)
#     elif (
#         len(normals) == 1
#     ):  # if there is one fixed circle, choose a vector in
#           the circle as the intersection axis for subsequent circles
#         [a] = normals
#         return materia.utils.perpendicular_vector(a=a)
#     else:  # if there are no fixed circles, then choose the north pole
#         return np.array([[0, 0, 1]]).T


# def _extend_points_to_circles(intersection, *excluded_points):
#     return [
#         materia.utils.perpendicular_vector(a=p, b=intersection)
#         for p in excluded_points
#         if not np.allclose(p, intersection) and not np.allclose(p, -intersection)
#     ]


# def _validate_axes(axes):
#     """
#     Checks whether or not three vectors span R^3.

#     Parameters
#     ----------
#     axes: numpy.ndarray
#         3x3 Numpy array whose columns are the vectors whose span is to be checked.

#     Returns
#     -------
#     bool
#         True if the columns of vector_array span R^3, else False.
#     """
#     return scipy.linalg.null_space(axes).shape[1] == 0


# SEARCHING FOR PLANES
# a mirror plane must map every atom to an atom of the same element
# if a mirror plane goes through no atoms, then it must
# map every atom to a different atom, so its normal is the
# difference of two isoelemental atoms
# if a mirror plane goes through at least one atom but
# not all atoms of any element, then it must map every
# other atom to a different atom, so its normal
# is the difference of two isoelemental atoms
# if a mirror plane goes through all atoms of an element,
# then it must map all atoms of that element to themselves,
# and the plane is simply the plane of those atoms
# so all mirror planes can be found by listing all mirror planes
# separating isoelemental atoms and all mirror planes containing
# all atoms of an element
# SEARCHING FOR PROPER ROTATION AXES
# a rotation axis must map every atom to an atom of the same element
# if a rotation axis goes through no atoms, then it must be at the
# center of n atoms where n is the order of the axis
# if these n atoms are coplanar, then the rotation axis is the
# normal to the plane
# otherwise, the rotation axis is the centroid of the n atoms
# if a rotation axis goes through at least one atom, then the axis
# is the vector from the COM to that atom
# so all rotation axes can be found by checking all atomic position
# vectors and the centroid/plane normal of all sets of
# n isoelemental atoms
# SEARCHING FOR IMPROPER ROTATION AXES
# SEARCHING FOR INVERSION
# if inversion symmetry exists, then the center of mass
# is the center of inversion

# def sea_sets(structure: mtr.Structure):
#     return tuple(
#         materia.Structure(*atoms)
#         for Z, atoms in itertools.groupby(
#             sorted(structure.atoms, key=lambda a: a.Z), lambda a: a.Z
#         )
#     )

# def symmetry_operations(structure, symprec):
#     seas = fragment_seas(structure=structure).values()
#     candidate_operations = find_operations(structure=seas, symprec=symprec) + [
#         materia.symmetry.Inversion()
#     ]


# def find_operations(structure, symprec):
#     if structure.is_linear:
#         return _find_rotations_linear(structure=structure, symprec=symprec)
#     elif structure.is_planar:
#         normal = structure.principal_axes[np.argmax(structure.principal_moments)]
#         overall_reflection = materia.symmetry.Reflection(axis=normal)

#         rotations = [
#             _find_rotations_planar(structure=sea, symprec=symprec) for sea in seas
#         ]
#         reflections = [
#             _find_reflections_planar(structure=structure, symprec=symprec)
#             for sea in seas
#         ]
#         # FIXME: improper? no need for inversion
#         return rotations + reflections + [overall_reflection]
#     else:
#         # FIXME: write this
#         return None


# def _find_rotations_planar(structure, symprec):
#     divisors = factors(n=structure.num_atoms)
#     rs = []
#     m1, m2, m3 = structure.principal_moments
#     if m1 == m2:
#         normal = structure.principal_axes[2]
#     elif m1 == m3:
#         normal = structure.principal_axes[1]
#     else:  # m2 == m3
#         normal = structure.principal_axes[0]
#     for p1, p2 in itertools.combinations(
#         structure.centered_atomic_positions.value.T, r=2
#     ):
#         Rs = (
#             materia.symmetry.ProperRotation(
#                 order=d, axis=materia.utils.normalize(p1 + p2)
#             )
#             for d in divisors
#         )
#         rs.extend(
#             [R for R in Rs if R.is_symmetry_of(structure=structure, symprec=symprec)]
#         )
#         Rs = (materia.symmetry.ProperRotation(order=d, axis=normal) for d in divisors)
#         rs.extend(
#             [R for R in Rs if R.is_symmetry_of(structure=structure, symprec=symprec)]
#         )

#     return rs


def unique(op: mtr.SymmetryOperation, ops: Iterable[mtr.SymmetryOperation]) -> bool:
    for _op in ops:
        if op.order == _op.order and np.abs(np.dot(op.axis, _op.axis).round(3)) == 1:
            return False
    return True


def search_symmetries_explicit(
    structure: mtr.Structure,
    tolerance: float,
) -> List[mtr.SymmetryOperation]:
    round_to = round(-np.log(tolerance) / np.log(10))

    # "symmetrically equivalent atoms" - although they are actually just isoelemental
    seas = (structure.element_substructure(Z) for Z in set(structure.atomic_numbers))
    # center of mass
    com = structure.center_of_mass

    rots = []
    refs = []
    imps = []
    points = [mtr.Identity()]

    inv = mtr.Inversion()
    if inv.is_symmetry_of(structure, round_to):
        points.append(inv)

    for s in seas:
        X = (s.atomic_positions - com).value.T

        # possible proper rotation orders
        _, *divisors = mtr.divisors(s.num_atoms)

        (m1, m2, m3) = s.principal_moments.value / sum(s.principal_moments.value)
        n1, n2, n3 = s.principal_axes.T

        # check if linear

        if round(m1, round_to) == 0 and round(m2, round_to) == round(m3, round_to):
            # FIXME
            # linear along n1
            pass
        if round(m2, round_to) == 0 and round(m1, round_to) == round(m3, round_to):
            # FIXME
            # linear along n2
            pass
        if round(m3, round_to) == 0 and round(m1, round_to) == round(m2, round_to):
            # FIXME
            # linear along n3
            pass

        # check if planar

        if round(m1 + m2, round_to) == round(m3, round_to):
            for k in divisors:
                rot = mtr.ProperRotation(k, n3)
                if unique(rot, rots) and rot.is_symmetry_of(structure, round_to):
                    rots.append(rot)
        if round(m1 + m3, round_to) == round(m2, round_to):
            for k in divisors:
                rot = mtr.ProperRotation(k, n2)
                if unique(rot, rots) and rot.is_symmetry_of(structure, round_to):
                    rots.append(rot)
        if round(m2 + m3, round_to) == round(m1, round_to):
            for k in divisors:
                rot = mtr.ProperRotation(k, n1)
                if unique(rot, rots) and rot.is_symmetry_of(structure, round_to):
                    rots.append(rot)

        for p in X:
            # proper rotational axes through atoms
            for k in divisors:
                rot = mtr.ProperRotation(k, p)
                if unique(rot, rots) and rot.is_symmetry_of(structure, round_to):
                    rots.append(rot)

        for p1, p2 in itertools.combinations(X, r=2):
            # proper rotational axes of order 2 through atom pair midpoints

            rot = mtr.ProperRotation(2, p1 + p2)
            if unique(rot, rots) and rot.is_symmetry_of(structure, round_to):
                rots.append(rot)

            # reflections

            n = mtr.normalize(p1 - p2)

            ref = mtr.Reflection(n)
            if unique(ref, refs) and ref.is_symmetry_of(structure, round_to):
                refs.append(ref)

            n1 = mtr.normalize(np.cross(p1, p2))

            ref = mtr.Reflection(n1)
            if unique(ref, refs) and ref.is_symmetry_of(structure, round_to):
                refs.append(ref)

            n2 = mtr.normalize(np.cross(n, n1))

            ref = mtr.Reflection(n2)
            if unique(ref, refs) and ref.is_symmetry_of(structure, round_to):
                refs.append(ref)

        for p1, p2, p3 in itertools.combinations(X, r=3):
            # proper rotatoinal axes of higher order
            a = p2 - p1
            b = p3 - p2
            theta = np.arccos(np.dot(mtr.normalize(a), mtr.normalize(b)))
            n = round(2 / (1 - theta / np.pi))

            rot = mtr.ProperRotation(n, np.cross(a, b))
            if n > 1 and unique(rot, rots) and rot.is_symmetry_of(structure, round_to):
                rots.append(rot)

    # FIXME: surely missing some impropers?
    for rot in rots:
        for k in divisors:
            imp = mtr.ImproperRotation(k, rot.axis)
            if imp.axis is not None and imp.is_symmetry_of(structure, round_to):
                imps.append(imp)

            imp = mtr.ImproperRotation(2 * k, rot.axis)
            if imp.axis is not None and imp.is_symmetry_of(structure, round_to):
                imps.append(imp)

    return rots + refs + imps + points


def search_symmetries_automorphism(
    structure: mtr.Structure,
    tolerance: float,
) -> List[mtr.SymmetryOperation]:
    # permutations = {}

    symmetries = []

    X = structure.centered_atomic_positions.value
    pinv_X = np.linalg.pinv(X)

    for P in _automorphisms(structure, tolerance):

        matrix, _ = scipy.linalg.polar(X @ P @ pinv_X)
        R = mtr.SymmetryOperation(matrix=matrix)
        if R.is_symmetry_of(structure, tolerance) and unique(R, symmetries):
            symmetries.append(R)
        # permutations[hash(P.data.tobytes())] = P

    # for P in permutations.values():
    #     permutations[hash(P.T.data.tobytes())] = P.T

    # for P1, P2 in itertools.combinations(permutations.values(), r=2):
    #     P3 = P1 @ P2
    #     permutations[hash(P3.data.tobytes())] = P3
    #     permutations[hash(P3.T.data.tobytes())] = P3.T

    # for P in permutations.values():
    #     matrix, _ = scipy.linalg.polar(X @ P @ pinv_X)
    #     R = mtr.SymmetryOperation(matrix=matrix)
    #     if R.is_symmetry_of(structure, tolerance) and unique(R, symmetries):
    #         symmetries.append(R)

    return symmetries


def _automorphisms(structure: mtr.Structure, tolerance: float):
    import networkx as nx

    round_to = round(-np.log(tolerance) / np.log(10))

    g = nx.Graph()

    # node with label num_atoms represents COM node
    nodes = tuple(range(structure.num_atoms + 1))

    # make edge between COM node and every non-COM node
    edges = tuple((structure.num_atoms, i) for i in nodes[:-1])

    # 'COM' is the "atomic symbol" for the COM node
    atomic_symbols = (
        *structure.atomic_symbols,
        "COM",
    )
    com_distances = (
        np.linalg.norm(p).round(round_to)
        for p in structure.centered_atomic_positions.value.T
    )

    g.add_edges_from(edges)
    nx.set_node_attributes(
        G=g, values={n: {"Z": v} for n, v in zip(nodes, atomic_symbols)}
    )
    nx.set_edge_attributes(
        G=g, values={e: {"dist": v} for e, v in zip(edges, com_distances)}
    )

    perms = nx.algorithms.isomorphism.GraphMatcher(
        G1=g,
        G2=g,
        node_match=lambda n1, n2: n1["Z"] == n2["Z"],
        edge_match=lambda e1, e2: e1["dist"] == e2["dist"],
    ).isomorphisms_iter()

    for p in perms:
        n = len(p) - 1  # number of atoms
        p.pop(n)  # remove the COM

        iden = np.eye(n, dtype=int)
        yield np.hstack(
            [iden[:, col_ind].reshape(n, -1) for _, col_ind in sorted(p.items())]
        )


def plot_symmetries(
    structure: mtr.Structure, symmetries: Iterable[mtr.SymmetryOperation]
) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection

    # from mpl_toolkits.mplot3d import Axes3D

    # plt3d = plt.figure().gca(projection="3d")
    ax = plt.gca()

    rots = [s for s in symmetries if type(s) == mtr.ProperRotation]
    imps = [s for s in symmetries if type(s) == mtr.ImproperRotation]
    refs = [s for s in symmetries if type(s) == mtr.Reflection]
    # points = [
    #     s for s in symmetries if type(s) == mtr.Identity or type(s) == mtr.Inversion
    # ]

    print(
        f"""Found {len(rots)} proper rotations,
             {len(imps)} improper rotations,
             and {len(refs)} reflections."""
    )

    for s in symmetries:
        if type(s) == mtr.Reflection:
            n1, n2, n3 = s.axis

            _l = [(0, 0), (n1, n2)]
            lines = LineCollection((_l, _l))
            ax.add_collection3d(lines, zs=0)

            # if round(n3, 3) == 0:
            #     xx, zz = np.meshgrid(range(-10, 10), range(-10, 10))
            #     y = (-n1 * xx - n3 * zz) / n2
            #     plt3d.plot_surface(xx, y, zz, alpha=0.2)
            # else:
            #     xx, yy = np.meshgrid(range(-10, 10), range(-10, 10))
            #     z = (-n1 * xx - n2 * yy) / n3
            #     plt3d.plot_surface(xx, yy, z, alpha=0.2)
            # break

    xs, ys, zs = structure.centered_atomic_positions.value
    ax.scatter(xs, ys, zs)
    ax.set_xlim3d(-10, 10)
    ax.set_ylim3d(-10, 10)
    ax.set_zlim3d(-10, 10)
    plt.show()


# # SEE
# https://iopscience.iop.org/book/978-1-6817-4637-1/chapter/bk978-1-6817-4637-1ch1,
# https://math.stackexchange.com/questions/693414/reflection-across-the-plane,
# https://github.com/psi4/psi4/blob/master/psi4/src/psi4/libmints/molecule.cc,
# http://www.pci.tu-bs.de/aggericke/PC4e/Kap_IV/Matrix_Symm_Op.htm


# class SymmetryAnalyzer:
#     def symmetry_operations(self, molecule, symprec=5):
#         I = molecule.structure.inertia_tensor / np.trace(
#             molecule.structure.inertia_tensor
#         )
#         principal_moments, principal_axes = scipy.linalg.eig(I)
#         (m1, m2, m3) = principal_moments.round(symprec)

#         symmetry_operations = []

#         for p1, p2 in itertools.combinations(
#             molecule.structure.centered_atomic_positions.value.T, r=2
#         ):
#             axis = p1 - p2
#             axis /= scipy.linalg.norm(axis)

#             R = Reflection(axis=axis)

#             if R.is_symmetry_of(molecule, symprec=symprec):
#                 symmetry_operations.append(R)
#             print(len(symmetry_operations))
#             axis = p1 + p2
#             axis_norm = scipy.linalg.norm(axis)
#             if not np.isclose(axis_norm, 0):
#                 axis /= axis_norm
#                 R2 = ProperRotation(order=2, axis=axis)
#                 R3 = ProperRotation(order=2, axis=axis)
#                 R4 = ProperRotation(order=2, axis=axis)
#                 R5 = ProperRotation(order=2, axis=axis)

#                 if R2.is_symmetry_of(molecule, symprec=symprec):
#                     symmetry_operations.append(R2)
#                 if R3.is_symmetry_of(molecule, symprec=symprec):
#                     symmetry_operations.append(R3)
#                 if R4.is_symmetry_of(molecule, symprec=symprec):
#                     symmetry_operations.append(R4)
#                 if R5.is_symmetry_of(molecule, symprec=symprec):
#                     symmetry_operations.append(R5)

#             print(len(symmetry_operations))
#         print(len({hash(R.matrix.data.tobytes()): R for R in symmetry_operations}))
#         if np.isclose(np.prod((m1, m2, m3)), 0):  # one of the eigenvalues is zero
#             return self._analyze_linear_molecule(molecule=molecule)
#         elif np.allclose((m1 - m2, m2 - m3), 0):  # all eigenvalues are the same
#             return self._analyze_spherical_top(molecule=molecule)
#         elif (
#             np.sum(np.isclose((m1 - m2, m2 - m3, m1 - m3), 0)) == 0
#         ):  # all eigenvalues are different
#             # possible groups: C1, Ci, Cs, C2, C2v, C2h, D2, D2h
#             for axis in principal_axes.T:
#                 R = ProperRotation(order=2, axis=axis)
#                 if R.is_symmetry_of(molecule=molecule, symprec=symprec):
#                     symmetry_operations.append(R)
#             if len(symmetry_operations) == 0:
#                 # possible groups: C1, Ci, Cs
#                 inv = Inversion()
#                 if inv.is_symmetry_of(molecule=molecule, symprec=symprec):
#                     # Ci
#                     symmetry_operations.append(inv)
#                 # elif Reflection(axis=)# check for mirror plane
#             elif len(symmetry_operations) == 1:
#                 # possible groups: C2, C2v, C2h
#                 pass
#             else:
#                 # possible groups: D2, D2h
#                 pass
#             print(symmetry_operations)
#             return self._analyze_asymmetrical_top(molecule=molecule)
#         else:  # two eigenvalues are the same, one is different
#             return self._analyze_symmetrical_top(molecule=molecule)

#     def _analyze_linear_molecule(self, molecule):
#         inv = Inversion()
#         if inv.is_symmetry_of(molecule):
#             pass  # FIXME: what to return for infinite point group Dinfh?
#         else:
#             pass  # FIXME: what to return for infinite point group Cinfv?

#     # def asymmetrical_top(self, molecule):
#     #     for

# class SymmetryFinder:
#     def __init__(self):
#         pass

#     def molecular_pointgroup(self, coordinates, atomic_numbers):
#         min_x, min_y, min_z = [min(p) for p in coordinates.T]
#         # the 0.1 ensures that the fractional
#         # positions are sufficiently smaller than 1,
#         # which appears to be necessary for accurate
#         # symmetry determination, and it
#         # also ensures that max_x,max_y,max_z are all
#         # > 0 so that scipy.linalg.inv(lattice)
#         # is well-defined
#         max_x, max_y, max_z = [
#             max(abs(p) - min) + 0.1
#             for p, min in zip(coordinates.T, (min_x, min_y, min_z))
#         ]

#         lattice = np.diag([max_x, max_y, max_z])
#         fractional_positions = coordinates @ scipy.linalg.inv(lattice)

#         cell = (lattice, fractional_positions, atomic_numbers)

#         return spglib.get_spacegroup_type(
#             spglib.get_symmetry_dataset(cell=cell)["hall_number"]
#         )["pointgroup_international"]

#     def get_rotations(self, pointgroup_symbol):
#         """
#         Generates two lists of rotations, one proper and
#         one improper, which are symmetries corresponding
#         to the given point group symbol.

#         Parameters
#         ----------
#         pointgroup_symbol: str
#             String denoting a Schoenflies point group symbol.

#         Returns
#         -------
#         list of numpy.ndarrays:
#             List of unique proper rotation matrices
#             corresponding to pointgroup_symbol,
#             excluding the identity matrix.
#         list of numpy.ndarrays:
#             List of unique improper rotation matrices
#             corresponding to pointgroup_symbol,
#             excluding the negative identity matrix.
#         """
#         representative_numbers = {
#             spglib.get_spacegroup_type(i)["pointgroup_international"]: i
#             for i in range(1, 531)
#         }
#         hall_number = representative_numbers[
#             pointgroup_symbol
#         ]  # lowest Hall number of a space group which contains the given point group.
# hall_number = self.get_representative_hall_number(pointgroup_symbol=pointgroup_symbol)
#         ## lowest Hall number of a space group which contains the given point group.

#         # symmetry_dict = spglib.get_symmetry_from_database(hall_number)
#         # rotations = symmetry_dict['rotations']
#         # inds = (symmetry_dict['translations'] == 0).sum(axis=1) == 3
#         # rotations = rotations[inds]
#         rotations = spglib.get_symmetry_from_database(hall_number)["rotations"]
#         _, unique_indices = np.unique(ar=rotations, axis=0, return_index=True)
#         unique_rotations = rotations[sorted(unique_indices)]

#         # exact (as opposed to np.isclose) conditions on determinant and
#         # identity-ness are fine since spglib gives rotation matrices
#         # with integer elements
#         determinants = np.linalg.det(unique_rotations)
#         proper_rotations = tuple(
#             R
#             for R, det in zip(unique_rotations, determinants)
#   if det == 1 and (R @ R.T == np.eye(3)).all() and not (R == np.eye(3)).all()
#         )
#         improper_rotations = tuple(
#             R
#             for R, det in zip(unique_rotations, determinants)
#             if det == -1
#             and (R @ R.T == np.eye(3)).all()
#             and not (R == -np.eye(3)).all()
#         )

#         return proper_rotations, improper_rotations


# class AxesGenerator:
#     def __init__(self, seed=None):
#         self.sf = SymmetryFinder()
#         self.geometry = Geometry(seed=seed)

#     def generate_axes(self, pointgroup_symbol, inertia_tensor):
#   axes, A, B = self._generate_unaligned_axes(pointgroup_symbol=pointgroup_symbol)

#    alignment_matrix = self._align_axes_with_molecule(inertia_tensor=inertia_tensor)
#         axes = alignment_matrix.T @ axes if not (axes == np.eye(3)).all() else axes
#         A = alignment_matrix.T @ A if A is not None else A
#         B = alignment_matrix.T @ B if B is not None else B
#         wprime = (A.T @ axes[:, -1])[:, None] if wprime is not None else wprime

#         return axes, A, B, wprime
#         # if A is not None and B is not None:

#     #            wprime = (A.T@axes[:,-1])[:,None]
#     #        aligned_wprime = alignment_matrix.T@wprime #FIXME: is this correct??
#     # else:
#     #    aligned_prime = None

#     # if self._validate_axes(axes=axes):
#     #     return aligned_axes,aligned_A,aligned_B,aligned_wprime
#     # else:
#     #     print('Error validating vectors!')
#     #     return np.eye(3),None,None,None

#     def _generate_unaligned_axes(self, pointgroup_symbol):
#         proper, improper = self.sf.get_rotations(pointgroup_symbol=pointgroup_symbol)

#         num_proper = len(proper)
#         num_improper = len(improper)

#         if num_proper == 0 and num_improper == 0:
#             # print('No usable symmetries found. Returning Cartesian axes.')
#             axes, A, B = self._generate_unaligned_axes_no_symmetries()
#         elif num_proper == 0 and num_improper == 1:
#             # print('One rotoflection found. Generating two axes...')
#             axes, A, B = self._generate_unaligned_axes_one_symmetry(R=improper[0])
#         elif num_proper == 1 and num_improper == 0:
#             # print('One rotation found. Generating two axes...')
#             axes, A, B = self._generate_unaligned_axes_one_symmetry(R=proper[0])
#         elif num_proper == 0 and num_improper > 1:
#             # print('Multiple symmetries found. Generating three axes...')
#             # print('All symmetries have degnerate span.')
#             # print('Generating two axes...')
#             axes, A, B = self._generate_unaligned_axes_multiple_symmetries(
#                 symmetries=improper
#             )
#         elif num_proper > 1 and num_improper == 0:
#             # print('Multiple symmetries found. Generating three axes...')
#             # print('All symmetries have degnerate span. Generating two axes...')
#             axes, A, B = self._generate_unaligned_axes_multiple_symmetries(
#                 symmetries=proper
#             )
#         else:
#             # print('Multiple symmetries found. Generating three axes...')
#             # print('All symmetries have degnerate span. Generating two axes...')
#             axes, A, B = self._generate_unaligned_axes_multiple_symmetries(
#                 symmetries=proper + improper
#             )

#         if self._validate_axes(axes=axes):
#             return axes, A, B
#         else:
#             print("Error validating vectors!")
#             return np.eye(3), None, None

#     def _generate_unaligned_axes_no_symmetries(self):
#         return np.eye(3), None, None

#     def _generate_unaligned_axes_one_symmetry(self, R):
#         q = self.geometry.make_nontrivial_vector(R=R)
#         r = R @ q
#         s = self.geometry.perpendicular_vector(a=q, b=r)

#         return np.hstack([q, r, s]), R, None

#     def _generate_unaligned_axes_multiple_symmetries(self, symmetries):
#         excluded_generator = (
#             (a, b, *self._excluded_points_and_circles(A=a, B=b))
#             for a, b in itertools.product(symmetries, symmetries)
#             if (not (a == b).all() and not (a == -b).all())
#         )
#         try:
#             A, B, excluded_points, excluded_circles = next(
#                 (
#                     (a, b, xp, xc)
#                     for (a, b, xp, xc) in excluded_generator
#                     if (
#                         xc.shape[1] == 0
#                         or (xc.shape[1] > 0 and np.linalg.matrix_rank(xc) < 3)
#                     )
#                 )
#             )
#             self.geometry.add_excluded_points(excluded_points=excluded_points)
#             self.geometry.add_excluded_circles(excluded_circles=excluded_circles)
#             q = self.geometry.sample_axis()
#             r = A @ q
#             s = B @ q

#             return np.hstack([q, r, s]), A, B
#         except StopIteration:
#             return self._generate_unaligned_axes_one_symmetry(R=symmetries[0])

#     def _align_axes_with_molecule(self, inertia_tensor):
#         """
#         Computes the unique rotation matrix which maps the two highest-inertia
#         principal vectors to the z- and y-axes, respectively.

#         Parameters
#         ----------
#         numpy.ndarray: inertia_tensor
#             3x3 numpy array specifying the inertia tensor in arbitrary units.

#         Returns
#         -------
#         numpy.ndarray:
#             3x3 numpy array representing the rotation matrix which maps the
#             first two principal vectors to the z- and y-axes.
#         """
#         principal_moments, principal_directions = scipy.linalg.eigh(inertia_tensor)

#         # FIXME: this is currently broken for monomers
#         sorted_moments, sorted_directions = zip(
#             *sorted(zip(principal_moments, principal_directions.T), reverse=True)
#         )
#         u, v, _ = sorted_directions

#         Ru = self.geometry.rotation_matrix_m_to_n(m=u, n=np.array([[0, 0, 1]]).T)
#         Rv = self.geometry.rotation_matrix_m_to_n(m=Ru @ v, n=np.array([[0, 1, 0]]).T)
#         R = Rv @ Ru

#         return R

#     def _excluded_points_and_circles(self, A, B):
#         """
#         Construct list of excluded points and circles on unit sphere.

#         Parameters
#         ----------
#         A,B : numpy.ndarray
#             3x3 numpy arrays representating the
#             two symmetry operations whose excluded
#             points are being calculated.

#         Returns
#         -------
#         numpy.ndarray:
#             3xNp Numpy array representing excluded
#             points on a unit sphere, where Np is
#             the number of excluded points.
#         numpy.ndarray:
#             3xNc Numpy array representing the normal
#             vectors of excluded circles, where Nc is
#             the number of excluded circles.
#         """
#         identity = np.eye(3)
#         null_bases = [
#             scipy.linalg.null_space(M)
#             for M in (
#                 A + identity,
#                 A - identity,
#                 B + identity,
#                 B - identity,
#                 A + B,
#                 A - B,
#             )
#         ]
#         geometric_multiplicities = [null_basis.shape[1] for null_basis in null_bases]

#         # each null basis with geometric multiplicity two
#         # results in a circle of excluded points whose
#         # normal vector is the cross product of the null basis
#         excluded_circles = [
#             self.geometry.perpendicular_vector(*nb.T[:, :, None])
#             for nb in null_bases
#             if nb.shape[1] == 2
#         ]
#         excluded_circles = (
#             np.unique(np.hstack(excluded_circles).round(decimals=10), axis=1)
#             if len(excluded_circles) > 0
#             else np.array([[], [], []])
#         )

#         # only get excluded points which do not lie on an excluded circle
#         excluded_points = [
#             nb
#             for nb in null_bases
#             if nb.shape[1] == 1 and not np.isclose(nb.T @ excluded_circles, 0).any()
#         ]
#         excluded_points = (
#             np.unique(np.hstack(excluded_points).round(decimals=10), axis=1)
#             if len(excluded_points) > 0
#             else np.array([[], [], []])
#         )

#         return excluded_points, excluded_circles

#     def _validate_axes(self, axes):
#         """
#         Checks whether or not three vectors span R^3.

#         Parameters
#         ----------
#         axes: numpy.ndarray
#             3x3 Numpy array whose columns are the vectors whose span is to be checked.

#         Returns
#         -------
#         bool
#             True if the columns of vector_array span R^3, else False.
#         """
#         return scipy.linalg.null_space(axes).shape[1] == 0

# def add_excluded_points(self, excluded_points):
#         self.excluded_points = excluded_points

# def add_excluded_circles(self, excluded_circles):
#     self.excluded_circles = excluded_circles

# def points_to_circles(self):
#     new_circles = np.hstack(
#         [self.perpendicular_vector(m=p) for p in self.excluded_points[:, :, None]]
#     )
#     self.excluded_circles = np.hstack([self.excluded_circles, new_circles])


# def sample_axis(self):
#     self.points_to_circles()
#     n1, n2 = self.closest_pair(points=self.excluded_circles)

#     return self.sample_from_lune(n1=n1, n2=n2)

# def _equivalent_atoms(molecule):
#     mol_dict = {
#         tuple(p.squeeze()): symb
#         for symb, p in zip(
#             molecule.structure.atomic_symbols,
#             molecule.structure.centered_atomic_positions.value.T,
#         )
#     }
#     elements = tuple(set(mol_dict.values()))

#     yield from (
#         [position for position, element in mol_dict.items() if element == el]
#         for el in elements
#     )


# def find_symmetry(mol):
#     # FIXME: first align principal axes, center on COM
#     possible_lines_of_symmetry = _candidate_symmetry_axes(molecule=mol)
#     if mol.structure.is_linear:
#         if Inversion().is_symmetry_of(mol=mol):
#             print("D-infh")
#         else:
#             print("C-infv")
#     if (
#         sum(
#             CnU(n=5, axis=line).is_symmetry_of(molecule=mol)
#             for line in possible_lines_of_symmetry
#         )
#         >= 2
#     ):
#         if mol.has_symmetry(symmetry_op=Inversion()):
#             print("Ih")
#         else:
#             print("I")
#     if (
#         sum(
#             CnU(n=4, axis=line).is_symmetry_of(molecule=mol)
#             for line in possible_lines_of_symmetry
#         )
#         >= 2
#     ):
#         if mol.has_symmetry(symmetry_op=Inversion()):
#             print("Oh")
#         else:
#             print("O")
#     if (
#         sum(
#             CnU(n=3, axis=line).is_symmetry_of(molecule=mol)
#             for line in possible_lines_of_symmetry
#         )
#         == 4
#     ):
#         if (
#             sum(
#                 mol.has_symmetry(symmetry_op=Sigma(axis=plane_normal))
#                 for plane_normal in mol.atom_planes
#             )
#             >= 1
#         ):
#             if mol.has_symmetry(symmetry_op=Inversion()):
#                 print("Th")
#             else:
#                 print("Td")
#         else:
#             print("T")
#     print(
#         [
#             CnU(n=2, axis=line).is_symmetry_of(molecule=mol)
#             for line in possible_lines_of_symmetry
#         ]
#     )
#     print(possible_lines_of_symmetry)
#     has_cs = [
#         sum(
#             CnU(n=n, axis=line).is_symmetry_of(molecule=mol)
#             for line in possible_lines_of_symmetry
#         )
#         for n in (2, 3, 4, 5, 6)
#     ]
#     if sum(has_cs) == 0:
#         if (
#             sum(
#                 mol.has_symmetry(symmetry_op=Sigma(axis=plane_normal))
#                 for plane_normal in mol.atom_planes
#             )
#             >= 1
#         ):
#             print("Cs")
#         else:
#             if mol.has_symmetry(symmetry_op=Inversion()):
#                 print("Ci")
#             else:
#                 print("C1")
#     else:
#         max_n = 6 - np.argmax(has_cs[::-1])
#         if max_n <= 1:
#             pass
