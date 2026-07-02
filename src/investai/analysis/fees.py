"""Deterministic fee math — Analyst tool, never LLM arithmetic."""

from decimal import Decimal

from investai.dataaccess.models import ExpenseRatio


def expense_ratio_diff_bps(a: ExpenseRatio, b: ExpenseRatio) -> Decimal:
    """Difference (a - b) in basis points. 0.0035 - 0.0035 -> 0bps."""
    return (a.ratio - b.ratio) * Decimal(10_000)
