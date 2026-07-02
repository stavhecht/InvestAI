"""Quote facade — capability-level fallback over the source chain.

Tool names and payload shapes differ per source, so fallback happens HERE
(per capability), not at the raw tool level. Each parser normalizes its
source's payload into a currency-aware Quote.

Yahoo hazard (discovered 2026-07-02): get_current_stock_price returns a BARE
float with no currency field — 'LUMI.TA' -> 6693.0 is agorot, unlabeled. The
currency is inferred from the spike-verified registry rule: TASE equities
quote in agorot (ILA), TA indices in ILS, everything else USD (v1 scope is
US + IL only).
"""

from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

from investai.dataaccess.interface import DataSource, DataSourceError
from investai.dataaccess.models import Currency, Quote
from investai.dataaccess.registry import FALLBACK_CHAINS, is_israeli, is_ta_index


def infer_currency(symbol: str) -> Currency:
    if not is_israeli(symbol):
        return Currency.USD  # v1 scope: US + IL markets only
    return Currency.ILS if is_ta_index(symbol) else Currency.ILA


async def _yahoo_quote(source: DataSource, symbol: str) -> Quote:
    payload = await source.call_tool("get_current_stock_price", {"symbol": symbol})
    try:
        price = Decimal(str(payload))
    except (InvalidOperation, ValueError) as err:
        msg = f"yahoo returned non-numeric price for {symbol}: {payload!r}"
        raise DataSourceError(msg) from err
    return Quote(
        symbol=symbol,
        price=price,
        currency=infer_currency(symbol),
        as_of=datetime.now(UTC),  # tool exposes no timestamp; treat as "now, delayed"
        is_delayed=True,
        source=source.name,
    )


async def _alpha_vantage_quote(source: DataSource, symbol: str) -> Quote:
    # Official AV MCP tools map 1:1 to API endpoints; GLOBAL_QUOTE returns
    # {"Global Quote": {"05. price": ..., "07. latest trading day": ...}}.
    # TODO(phase-1): verify live once ALPHAVANTAGE_API_KEY is configured.
    payload: Any = await source.call_tool("GLOBAL_QUOTE", {"symbol": symbol})
    block = payload.get("Global Quote") if isinstance(payload, dict) else None
    if not block:
        raise DataSourceError(f"alpha_vantage returned no quote for {symbol}: {payload!r}")
    try:
        price = Decimal(str(block["05. price"]))
    except (KeyError, InvalidOperation, ValueError) as err:
        raise DataSourceError(f"alpha_vantage quote unparseable for {symbol}: {block!r}") from err
    return Quote(
        symbol=symbol,
        price=price,
        currency=infer_currency(symbol),
        as_of=datetime.now(UTC),
        is_delayed=True,
        source=source.name,
    )


_QUOTE_PARSERS = {
    "yahoo": _yahoo_quote,
    "alpha_vantage": _alpha_vantage_quote,
}


async def get_quote(
    symbol: str,
    sources: dict[str, DataSource],
    *,
    profile: str = "local",
) -> Quote:
    """Walk the profile's market-data chain; first source that answers wins."""
    errors: list[str] = []
    for name in FALLBACK_CHAINS[profile]["market_data"]:
        source = sources.get(name)
        parser = _QUOTE_PARSERS.get(name)
        if source is None or parser is None:
            continue
        try:
            return await parser(source, symbol)
        except DataSourceError as err:
            errors.append(str(err))
        except Exception as err:  # noqa: BLE001 — transport failure -> try next source
            errors.append(f"{name}: {type(err).__name__}: {err}")
    raise DataSourceError(f"no source could quote {symbol}: {errors}")
