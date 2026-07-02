"""Planner — decomposes the research question into subtasks (Haiku)."""

from investai.orchestration.state import RunState


class PlannerAgent:
    async def __call__(self, state: RunState) -> RunState:
        # Phase 3: LlmClient(role="planner") -> structured Subtask list on state.plan
        raise NotImplementedError("Phase 3: planner decomposition")
