"""The state-machine definition — data, not code.

LocalRunner executes this in-process today; Phase 5's asl_compiler translates
the SAME structure to Step Functions ASL (task states, one Parallel state,
per-state Retry). Handlers are dotted import strings so the compiler can map
each state to a Lambda without importing anything.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class StateDef:
    name: str
    handler: str  # dotted path to an AgentStep class ("" for parallel states)
    next: str | None  # None = terminal state
    retry_attempts: int = 2
    branches: tuple[str, ...] = ()  # non-empty => parallel fan-out (SFN Parallel)


MACHINE: tuple[StateDef, ...] = (
    StateDef(name="plan", handler="investai.agents.planner.PlannerAgent", next="gather"),
    StateDef(
        name="gather",
        handler="",
        next="analyze",
        branches=(
            "investai.agents.market_data.MarketDataAgent",
            "investai.agents.filings_rag.FilingsRagAgent",
        ),
    ),
    StateDef(name="analyze", handler="investai.agents.analyst.AnalystAgent", next=None),
)
