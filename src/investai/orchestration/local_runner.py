"""Executes MACHINE in-process — the local twin of Step Functions (Phase 5).

Semantics are deliberately restricted to what translates 1:1 to ASL:
sequential task states, one level of parallel fan-out, per-state retry.
"""

import asyncio
import importlib

from investai.orchestration.machine import MACHINE, StateDef
from investai.orchestration.state import RunState


def _resolve(dotted: str):
    module, _, cls = dotted.rpartition(".")
    return getattr(importlib.import_module(module), cls)()


class LocalRunner:
    def __init__(self, machine: tuple[StateDef, ...] = MACHINE) -> None:
        self._states = {s.name: s for s in machine}
        self._start = machine[0].name

    async def run(self, state: RunState) -> RunState:
        name: str | None = self._start
        while name is not None:
            spec = self._states[name]
            state.current_state = name
            state = await self._run_with_retry(spec, state)
            name = spec.next
        return state

    async def _run_with_retry(self, spec: StateDef, state: RunState) -> RunState:
        last_err: Exception | None = None
        for _ in range(spec.retry_attempts + 1):
            try:
                if spec.branches:
                    # Each branch gets a copy of the input state (SFN Parallel
                    # semantics); results are merged below.
                    results = await asyncio.gather(
                        *(_resolve(b)(state.model_copy(deep=True)) for b in spec.branches)
                    )
                    return self._merge(state, list(results))
                return await _resolve(spec.handler)(state)
            except NotImplementedError:
                raise  # unbuilt phase — fail loudly, don't retry
            except Exception as err:  # noqa: BLE001 — mirrors SFN Retry-on-any
                last_err = err
        state.errors.append(f"{spec.name}: {last_err}")
        return state

    @staticmethod
    def _merge(base: RunState, branch_states: list[RunState]) -> RunState:
        updated = {t.id: t for bs in branch_states for t in bs.plan if t.status != "pending"}
        base.plan = [updated.get(t.id, t) for t in base.plan]
        for bs in branch_states:
            base.evidence_refs.extend(r for r in bs.evidence_refs if r not in base.evidence_refs)
            base.errors.extend(bs.errors)
        return base
