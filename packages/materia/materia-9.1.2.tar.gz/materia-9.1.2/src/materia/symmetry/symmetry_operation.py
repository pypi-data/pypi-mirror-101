from __future__ import annotations
from typing import Iterable, Optional, Union

import materia as mtr
import numpy as np
import scipy.linalg


__all__ = [
    "Identity",
    "Inversion",
    "Reflection",
    "ProperRotation",
    "ImproperRotation",
    "SymmetryOperation",
]


class SymmetryOperation:
    def __init__(
        self,
        matrix: Optional[np.ndarray] = None,
        determinant: Optional[Union[int, float]] = None,
        trace: Optional[float] = None,
        axis: Optional[np.ndarray] = None,
    ) -> None:
        if matrix is not None:
            self.matrix, _ = scipy.linalg.polar(matrix)
        elif determinant is not None and trace is not None:
            if axis is None:
                self.matrix, _ = scipy.linalg.polar(
                    determinant * np.eye(3).astype("float64")
                )
            else:
                a = mtr.normalize(axis)

                cos_theta = (trace - determinant) / 2
                cos_theta = max(min(cos_theta, 1), -1)
                theta = np.arccos(cos_theta)

                self.matrix = mtr.rotation_matrix(
                    axis=a, theta=theta, improper=(determinant == -1)
                )
        else:
            raise ValueError

    def __eq__(self, other: SymmetryOperation) -> bool:
        return hasattr(other, "matrix") and np.allclose(
            self.matrix, other.matrix, atol=1e-3
        )

    @property
    def det(self) -> int:
        return int(round(np.linalg.det(self.matrix)))

    @property
    def tr(self) -> float:
        return np.trace(self.matrix)

    @property
    def cos_theta(self) -> float:
        return max(min((self.tr - np.sign(self.det)) / 2, 1.0), -1.0)

    @property
    def axis(self) -> np.ndarray:
        # algorithm from scipp.ucsc.edu/~haber/ph116A/rotation_11.pdf
        if np.isclose(abs(self.tr), 3):
            return None

        if np.isclose(self.tr * self.det, -1):
            S = (np.eye(3) + self.det * self.matrix) / 2
            for i in range(3):
                signs = np.sign(S[:, i])
                if not np.allclose(signs, [0, 0, 0]):
                    return signs * np.sqrt(np.abs(np.diag(S)))

        inds = np.triu_indices(3, k=1)
        return mtr.normalize(
            (self.matrix.T - self.matrix)[inds][::-1] * np.array([1, -1, 1])
        )

    @property
    def inverse(self) -> SymmetryOperation:
        return SymmetryOperation(matrix=self.matrix.T)

    def apply(self, structure: mtr.Structure):
        return self.matrix @ structure.centered_atomic_positions.value

    def error(self, structure: mtr.Structure):
        kdt = scipy.spatial.KDTree(structure.centered_atomic_positions.value.T)
        dists, _ = np.abs(kdt.query(self.apply(structure).T))
        rs = np.abs(self.axis @ structure.centered_atomic_positions.value)
        return dists / rs

    def is_symmetry_of(self, structure: mtr.Structure, tolerance: float) -> bool:
        round_to = round(-np.log(tolerance) / np.log(10))
        X = structure.centered_atomic_positions.value

        return set(
            tuple(row) for row in self.apply(structure).T.round(round_to)
        ) == set(tuple(row) for row in X.T.round(round_to))

    @property
    def order(self) -> int:
        return mtr.periodicity(self.matrix)

    def __mul__(self, other):
        return SymmetryOperation(matrix=self.matrix @ other.matrix)


class Identity(SymmetryOperation):
    def __init__(self) -> None:
        determinant = 1
        trace = 3
        axis = None
        super().__init__(determinant=determinant, trace=trace, axis=axis)


class Inversion(SymmetryOperation):
    def __init__(self) -> None:
        determinant = -1
        trace = -3
        axis = None
        super().__init__(determinant=determinant, trace=trace, axis=axis)


class Reflection(SymmetryOperation):
    def __init__(self, axis: Iterable[Union[float, int]]) -> None:
        determinant = -1
        trace = 1
        super().__init__(determinant=determinant, trace=trace, axis=axis)


class ProperRotation(SymmetryOperation):
    def __init__(self, order: int, axis: Iterable[Union[float, int]]) -> None:
        determinant = 1
        trace = 2 * np.cos(2 * np.pi / order) + determinant
        super().__init__(determinant=determinant, trace=trace, axis=axis)

    def __repr__(self) -> str:
        return f"ProperRotation(order={self.order})"


class ImproperRotation(SymmetryOperation):
    def __init__(self, order: int, axis: Iterable[Union[float, int]]) -> None:
        determinant = -1
        trace = 2 * np.cos(2 * np.pi / order) + determinant
        super().__init__(determinant=determinant, trace=trace, axis=axis)
