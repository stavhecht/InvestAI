"""Phase 0 spike: empirically verify Yahoo symbol resolution for Israeli assets.

Checks: .TA equities, dual-listed pairs, TA-index candidate tickers, and the
agorot-vs-ILS currency question. Run: uv run python scripts/spike_symbols.py
Record results in CLAUDE.md's decisions log and dataaccess/registry.py.
"""

import yfinance as yf

from investai.dataaccess.registry import TA_INDEX_CANDIDATES

EQUITIES = ["LUMI.TA", "ESLT.TA", "TEVA.TA", "TEVA", "CHKP", "NICE", "CYBR"]


def probe(symbol: str) -> str:
    try:
        info = yf.Ticker(symbol).fast_info
        price = info.get("lastPrice")
        currency = info.get("currency")
        exchange = info.get("exchange")
        if price is None:
            return f"  {symbol:12} -> NO DATA"
        return f"  {symbol:12} -> price={price:<12.2f} currency={currency:<4} exchange={exchange}"
    except Exception as err:  # noqa: BLE001 — spike script, report and continue
        return f"  {symbol:12} -> ERROR: {err}"


def main() -> None:
    print("== Equities (watch the currency field: ILA = agorot!) ==")
    for symbol in EQUITIES:
        print(probe(symbol))

    print("\n== TA index candidates (first working form wins -> registry.py) ==")
    for index, candidates in TA_INDEX_CANDIDATES.items():
        print(f"{index}:")
        for symbol in candidates:
            print(probe(symbol))


if __name__ == "__main__":
    main()
