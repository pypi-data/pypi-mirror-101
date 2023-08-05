from __future__ import annotations
from typing import Any, Callable, Iterable, Optional, Tuple, Union

import dlib
import functools
import materia as mtr
from materia.utils import memoize
import re
import subprocess

__all__ = [
    "ExternalTask",
    "FunctionTask",
    "InputTask",
    "MaxLIPOTR",
    "ShellCommand",
    "Task",
    "task",
]


class Task:
    """Function with dependencies.

    Attributes
    ----------
    name : str
        Name for use in Workflows.
    requirements : list
        List of Tasks required as args in compute.
    named_requirements : dict
        Dicionary of Tasks required as kwargs in compute.
    """

    def __init__(
        self,
        name: Optional[str] = None,
    ) -> None:
        """Initialize Task.

        Parameters
        ----------
        name : Optional[str], optional
            Name for use in Workflows, by default None
        """
        self.name = (
            name
            or re.match("<class '(?P<cls>.*)'>", str(self.__class__))
            .group("cls")
            .rsplit(".")[-1]
            + f"-{id(self)}"
        )

        self.requirements = []
        self.named_requirements = {}

    def requires(self, *args: Task, **kwargs: Task) -> None:
        """Register Task dependencies."""
        new_reqs = [a if isinstance(a, Task) else InputTask(a) for a in args]
        new_named_reqs = {
            k: v if isinstance(v, Task) else InputTask(v) for k, v in kwargs.items()
        }

        self.requirements += new_reqs
        self.named_requirements = dict(**self.named_requirements, **new_named_reqs)

    def compute(self, **kwargs: Any) -> Any:
        """Execute Task using requirements as inputs.

        Returns
        -------
        Any
            [description]

        Raises
        ------
        NotImplementedError
            [description]
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """Return string representation.

        Returns
        -------
        str
            String representation (i.e. name) of Task.
        """
        return self.name


class ExternalTask(Task):
    """Task which runs external code.

    Attributes
    ----------
    engine : materia.Engine
        Engine to run external code.
    io : materia.IO
        Manager for external code input and output files.
    name : str
        Name for use in Workflows.
    requirements : list
        List of Tasks required as args in compute.
    named_requirements : dict
        Dicionary of Tasks required as kwargs in compute.
    """

    def __init__(
        self,
        engine: mtr.Engine,
        io: mtr.IO,
        name: Optional[str] = None,
    ) -> None:
        self.engine = engine
        self.io = io
        super().__init__(name=name)


class FunctionTask(Task):
    """Task which runs a Python function.

    Attributes
    ----------
    f : callable
        Function to be run by compute.
    name : str
        Name for use in Workflows.
    requirements : list
        List of Tasks required as args in compute.
    named_requirements : dict
        Dicionary of Tasks required as kwargs in compute.
    """

    def __init__(
        self,
        f: Callable,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(name=name)
        self.f = f

    def compute(self, **kwargs) -> None:
        return self.f(**kwargs)


class InputTask(Task):
    """Task which returns a fixed value.

    Attributes
    ----------
    value : Any
        Fixed value returned by compute.
    name : str
        Name for use in Workflows.
    requirements : list
        List of Tasks required as args in compute.
    named_requirements : dict
        Dicionary of Tasks required as kwargs in compute.
    """

    def __init__(
        self,
        value: Any,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(name=name)
        self.value = value

    def compute(self, *args, **kwargs) -> Any:
        return self.value


class ShellCommand(Task):
    def __init__(
        self,
        command: str,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(name=name)
        self.command = command

    def compute(self) -> None:
        subprocess.call(self.command.split())


def task(
    f: Callable = None,
    name: Optional[str] = None,
) -> FunctionTask:
    if f is None:
        return functools.partial(task, name=name)

    return FunctionTask(f=f, name=name)


T = Union[int, float]


class MaxLIPOTR(Task):
    def __init__(
        self,
        objective_function: Callable[T, T],
        name: Optional[str] = None,
    ) -> None:
        super().__init__(name)
        self.objective_function = objective_function

    @memoize
    def _evaluate_objective(self, *args: T) -> T:
        return self.objective_function(*args)

    def compute(
        self,
        x_min: Union[T, Iterable[T]],
        x_max: Union[T, Iterable[T]],
        num_evals: int,
        epsilon: Optional[float] = 0,
    ) -> Tuple[T, Union[int, float]]:

        return dlib.find_min_global(
            self._evaluate_objective,
            x_min if isinstance(x_min, list) else [x_min],
            x_max if isinstance(x_max, list) else [x_max],
            num_evals,
            solver_epsilon=epsilon,
        )

    # def plot_results(self):
    #     x, y = zip(*sorted(self.evaluate_objective.cache.items()))
    #     plt.plot(x, y)
    #     plt.show()
