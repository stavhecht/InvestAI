from decimal import Decimal

from investai.analysis.overlap import holdings_overlap
from investai.dataaccess.models import Holding


def test_weight_overlap_uses_min_rule():
    a = [
        Holding(symbol="NVDA", weight=Decimal("0.10")),
        Holding(symbol="AVGO", weight=Decimal("0.05")),
    ]
    b = [
        Holding(symbol="NVDA", weight=Decimal("0.08")),
        Holding(symbol="TSM", weight=Decimal("0.07")),
    ]
    result = holdings_overlap(a, b)
    assert result.shared_symbols == ["NVDA"]
    assert result.weight_overlap == Decimal("0.08")
    assert result.count_a == 2 and result.count_b == 2


def test_symbols_match_case_insensitively():
    a = [Holding(symbol="nvda", weight=Decimal("0.10"))]
    b = [Holding(symbol="NVDA", weight=Decimal("0.10"))]
    assert holdings_overlap(a, b).shared_symbols == ["NVDA"]


def test_disjoint_portfolios_have_zero_overlap():
    a = [Holding(symbol="AAPL", weight=Decimal("1"))]
    b = [Holding(symbol="MSFT", weight=Decimal("1"))]
    result = holdings_overlap(a, b)
    assert result.shared_symbols == []
    assert result.weight_overlap == Decimal(0)
