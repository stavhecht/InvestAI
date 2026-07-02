"""Analyst — weighs evidence and writes the cited ResearchBrief (Sonnet).

Numeric computation (overlap %, fee diffs) is done by calling the deterministic
tools in investai.analysis — NEVER by LLM arithmetic. That is the last mile of
the grounding guarantee.
"""

from investai.orchestration.state import RunState


class AnalystAgent:
    async def __call__(self, state: RunState) -> RunState:
        # Phase 3: tool-use loop with analysis.overlap / analysis.fees as tools,
        # producing a ResearchBrief with inline citations on state.brief
        raise NotImplementedError("Phase 3: analysis + brief synthesis")
