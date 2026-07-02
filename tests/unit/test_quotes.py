"""Quote facade tests against RECORDED payloads (captured live 2026-07-02 via
scripts/smoke_mcp.py) — no network in CI."""

from decimal import Decimal
from typing import Any

import pytest

from investai.dataaccess.interface import DataSourceError, ToolSpec
from investai.dataaccess.models import Currency
from investai.dataaccess.quotes import get_quote, infer_currency

# Payloads exactly as returned by the live servers on 2026-07-02.
YAHOO_RECORDED: dict[str, Any] = {
    "SOXX": 599.7,
    "LUMI.TA": 6693.0,  # agorot — Yahoo gives NO currency field
    "^TA125.TA": 4080.11,  # index — quotes in ILS
}
AV_RECORDED_SOXX = {  # documented GLOBAL_QUOTE shape (verify live when key lands)
    "Global Quote": {"01. symbol": "SOXX", "05. price": "599.7000"}
}


class FakeSource:
    def __init__(self, name: str, responses: dict[str, Any], fail: bool = False) -> None:
        self.name = name
        self._responses = responses
        self._fail = fail
        self.calls: list[tuple[str, dict]] = []

    async def list_tools(self) -> list[ToolSpec]:
        return []

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        self.calls.append((name, arguments))
        if self._fail:
            raise DataSourceError(f"{self.name} is down")
        return self._responses[arguments["symbol"]]


async def test_us_quote_is_usd():
    sources = {"yahoo": FakeSource("yahoo", YAHOO_RECORDED)}
    quote = await get_quote("SOXX", sources)
    assert quote.price == Decimal("599.7")
    assert quote.currency is Currency.USD
    assert quote.source == "yahoo"
    assert quote.is_delayed


async def test_tase_equity_is_agorot_and_normalizes():
    sources = {"yahoo": FakeSource("yahoo", YAHOO_RECORDED)}
    quote = await get_quote("LUMI.TA", sources)
    assert quote.currency is Currency.ILA
    price_ils, currency = quote.price_normalized()
    assert price_ils == Decimal("66.93")
    assert currency is Currency.ILS


async def test_ta_index_is_ils_not_agorot():
    sources = {"yahoo": FakeSource("yahoo", YAHOO_RECORDED)}
    quote = await get_quote("^TA125.TA", sources)
    assert quote.currency is Currency.ILS
    assert quote.price_normalized() == (Decimal("4080.11"), Currency.ILS)


async def test_fallback_walks_chain_on_failure():
    sources = {
        "yahoo": FakeSource("yahoo", {}, fail=True),
        "alpha_vantage": FakeSource("alpha_vantage", {"SOXX": AV_RECORDED_SOXX}),
    }
    quote = await get_quote("SOXX", sources)
    assert quote.source == "alpha_vantage"
    assert quote.price == Decimal("599.7000")


async def test_all_sources_failing_raises_with_details():
    sources = {"yahoo": FakeSource("yahoo", {}, fail=True)}
    with pytest.raises(DataSourceError, match="no source could quote"):
        await get_quote("SOXX", sources)


async def test_non_numeric_payload_is_a_source_error_not_a_crash():
    sources = {"yahoo": FakeSource("yahoo", {"SOXX": "N/A"})}
    with pytest.raises(DataSourceError):
        await get_quote("SOXX", sources)


def test_currency_inference_rules():
    assert infer_currency("SOXX") is Currency.USD
    assert infer_currency("LUMI.TA") is Currency.ILA
    assert infer_currency("TA35.TA") is Currency.ILS  # index WITHOUT caret
    assert infer_currency("^TA125.TA") is Currency.ILS
    assert infer_currency("ESLT.TA") is Currency.ILA
