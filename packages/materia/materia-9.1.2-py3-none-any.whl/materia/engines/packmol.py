from __future__ import annotations
from typing import Iterable, Optional, Tuple

import contextlib
import materia as mtr
import numpy as np

from .engine import Engine
from ..tasks import ExternalTask

__all__ = ["Packmol", "PackmolInput"]


class Packmol(Engine):
    def __init__(self, executable: Optional[str] = "packmol") -> None:
        super().__init__(executable=executable)

    def solvate(
        self,
        io: mtr.IO,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> PackmolSolvate:
        return PackmolSolvate(engine=self, io=io, handlers=handlers, name=name)


class PackmolSolvate(ExternalTask):
    def _packing_params(
        self, shells: int, number_density: Optional[mtr.Quantity] = None
    ) -> Tuple[int, mtr.Quantity]:
        # these are the ideal gas packing values:
        n = int((2 / 3) * shells ** 3)
        sphere_radius = shells * (2 * np.pi * number_density) ** (-1 / 3)

        return n, sphere_radius

    def compute(
        self,
        solute: mtr.Molecule,
        solvent: mtr.Molecule,
        shells: int,
        tolerance: float,
        solvent_density: mtr.Quantity,
    ) -> mtr.Molecule:
        if solvent_density.dimension == mtr.Dimension(M=1, L=-3):
            number_density = solvent_density / solvent.mass
        else:
            number_density = solvent_density

        n, sphere_radius = self._packing_params(
            shells=shells, number_density=number_density
        )

        with self.io() as io:
            inp = mtr.PackmolInput(
                tolerance=tolerance,
                filetype="xyz",
                output_name=mtr.expand(path="packed", dir=io.work_dir),
            )

            if isinstance(solute, str):
                solute_cm = contextlib.nullcontext(solute)
            else:
                solute_cm = solute.tempfile(suffix=".xyz", dir=io.work_dir)

            if isinstance(solvent, str):
                solvent_cm = contextlib.nullcontext(solvent)
            else:
                solvent_cm = solvent.tempfile(suffix=".xyz", dir=io.work_dir)

            with solute_cm as f, solvent_cm as g:
                inp.add_structure(
                    structure_filepath=mtr.expand(
                        path=f.name if hasattr(f, "name") else f, dir=io.work_dir
                    ),
                    number=1,
                    instructions=["fixed 0. 0. 0. 0. 0. 0."],
                )
                r = sphere_radius.convert(mtr.angstrom).value
                inp.add_structure(
                    structure_filepath=mtr.expand(
                        path=g.name if hasattr(g, "name") else g, dir=io.work_dir
                    ),
                    number=n - 1,
                    instructions=[f"inside sphere 0. 0. 0. {r}"],
                )

                inp.write(io.inp)

                self.engine.execute(self.io)

                return mtr.Molecule(mtr.expand(path="packed.xyz", dir=io.work_dir))


# ------------------------- INPUT ---------------------------- #


class PackmolInput:
    def __init__(
        self,
        tolerance: float,
        filetype: str,
        output_name: str,
        instructions: Optional[Iterable[str]] = None,
    ) -> None:
        self.tolerance = tolerance
        self.filetype = filetype
        self.output_name = output_name
        self.instructions = instructions or []
        self.structures = []

    def add_structure(
        self,
        structure_filepath: str,
        number: int,
        instructions: Optional[Iterable[str]] = None,
    ) -> None:
        self.structures.append((structure_filepath, number, instructions or []))

    def __str__(self) -> str:
        return (
            f"tolerance {self.tolerance}\n"
            + f"output {self.output_name}.{self.filetype}\n"
            + f"filetype {self.filetype}\n\n"
            + "\n".join(
                f"structure {sfp}\n  number {n}\n"
                + "".join(f"  {i}\n" for i in inst)
                + "end structure\n"
                for sfp, n, inst in self.structures
            )
        )

    def write(self, filepath: str) -> None:
        with open(mtr.expand(filepath), "w") as f:
            f.write(str(self))
