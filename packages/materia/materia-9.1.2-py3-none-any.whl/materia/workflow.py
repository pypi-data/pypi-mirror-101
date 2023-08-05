from __future__ import annotations
from typing import Any, Dict, List, Optional

import dask
import dask.distributed
import json
import materia as mtr
import pickle

__all__ = ["Workflow", "WorkflowResults"]


class WorkflowResults:
    def __init__(self, results: Dict[str, Any]) -> None:
        self.results = results

    def __getitem__(self, key: str) -> Any:
        return self.results[key]

    def __str__(self) -> str:
        return json.dumps(self.results, sort_keys=True, indent=2, default=str)

    def save(self, filepath) -> None:
        with open(filepath, "wb") as f:
            pickle.dump(self, f)


def _discover_tasks(*tasks: mtr.Task) -> List[mtr.Task]:
    discovered = list(tasks)

    for t in tasks:
        requirements = list(t.requirements) + list(t.named_requirements.values())
        discovered.extend(requirements + _discover_tasks(*requirements))

    return list(set(discovered))


def _build_delayed(
    task: mtr.Task,
    delayeds: Optional[Dict[str, dask.delayed.Delayed]],
    restart: Optional[WorkflowResults] = None,
) -> Dict[str, dask.delayed.Delayed]:
    if restart is not None and task.name in restart.results:
        delayeds[task.name] = dask.delayed(mtr.InputTask(restart[task.name]).compute)()
    elif delayeds[task.name] is None:
        args = (_build_delayed(v, delayeds) for v in task.requirements)
        kwargs = {
            k: _build_delayed(v, delayeds) for k, v in task.named_requirements.items()
        }
        delayeds[task.name] = dask.delayed(task.compute)(*args, **kwargs)

    return delayeds[task.name]


class Workflow:
    def __init__(self, *tasks: mtr.Task) -> None:
        # traverse task dependencies to find all tasks
        # required to compute the provided tasks
        self.tasks = _discover_tasks(*tasks)

    def compute(
        self,
        restart: Optional[WorkflowResults] = None,
    ) -> WorkflowResults:
        # create a registry of dask delayed objects
        # using this in _build_delayed prevents
        # creation of duplicate delayeds for a given task
        delayeds = {t.name: None for t in self.tasks}

        # build each delayed object
        for t in self.tasks:
            delayeds[t.name] = _build_delayed(t, delayeds, restart)

        # compute results
        (results,) = dask.compute(delayeds)

        return WorkflowResults(results)
