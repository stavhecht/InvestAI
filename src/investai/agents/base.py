"""Agent seam. Every agent is a pure step: (RunState) -> RunState.

Purity + JSON-serializable state is what makes each state mappable to a
Lambda handler in Phase 5.
"""

from typing import Protocol

from investai.orchestration.state import RunState


class AgentStep(Protocol):
    async def __call__(self, state: RunState) -> RunState: ...
