"""Deterministic holdings-overlap math.

The Analyst agent calls this as a tool — numeric claims are NEVER produced by
LLM arithmetic (grounding non-negotiable, see CLAUDE.md).
"""

from decimal import Decimal

from pydantic import BaseModel

from investai.dataaccess.models import Holding


class OverlapResult(BaseModel):
    shared_symbols: list[str]
    count_a: int
    count_b: int
    # Sum of min(w_a, w_b) over shared symbols — the standard portfolio-overlap metric.
    weight_overlap: Decimal


def holdings_overlap(a: list[Holding], b: list[Holding]) -> OverlapResult:
    wa = {h.symbol.upper(): h.weight for h in a}
    wb = {h.symbol.upper(): h.weight for h in b}
    shared = sorted(wa.keys() & wb.keys())
    return OverlapResult(
        shared_symbols=shared,
        count_a=len(wa),
        count_b=len(wb),
        weight_overlap=sum((min(wa[s], wb[s]) for s in shared), Decimal(0)),
    )
