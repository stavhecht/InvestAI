from datetime import UTC, datetime
from decimal import Decimal

from investai.api.schemas import DISCLAIMER, ResearchBrief
from investai.dataaccess.models import Currency, Quote
from investai.dataaccess.registry import is_israeli
from investai.orchestration.state import RunState


def test_brief_always_carries_disclaimer():
    brief = ResearchBrief(question="q", generated_at=datetime.now(UTC))
    assert brief.disclaimer == DISCLAIMER
    assert "NOT investment advice" in brief.model_dump()["disclaimer"]


def test_agorot_normalizes_to_ils():
    q = Quote(
        symbol="LUMI.TA",
        price=Decimal("3500"),
        currency=Currency.ILA,
        as_of=datetime.now(UTC),
        source="yahoo",
    )
    price, currency = q.price_normalized()
    assert price == Decimal("35")
    assert currency is Currency.ILS


def test_usd_passes_through_unchanged():
    q = Quote(
        symbol="SOXX",
        price=Decimal("225.10"),
        currency=Currency.USD,
        as_of=datetime.now(UTC),
        source="alpha_vantage",
    )
    assert q.price_normalized() == (Decimal("225.10"), Currency.USD)


def test_israeli_symbol_routing():
    assert is_israeli("LUMI.TA")
    assert is_israeli("^TA125.TA")
    assert not is_israeli("SOXX")


def test_run_state_survives_json_roundtrip():
    """The Step Functions constraint: state must be JSON-serializable."""
    state = RunState(run_id="r1", question="compare SOXX vs SMH")
    assert RunState.model_validate_json(state.model_dump_json()) == state
