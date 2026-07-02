"""Symbol routing + primary->fallback source chains.

Israeli listings use the '.TA' suffix (LUMI.TA, ESLT.TA) and TA-index tickers.
Exact index symbol forms are verified empirically by scripts/spike_symbols.py —
do not trust TA_INDEX_CANDIDATES until the spike passes.
"""

TA_SUFFIX = ".TA"

# VERIFIED 2026-07-02 by scripts/spike_symbols.py — note the inconsistency:
# TA-35/TA-90 take no caret, TA-125 requires one. Indices quote in ILS;
# equities quote in agorot (ILA).
TA_INDEX_SYMBOLS: dict[str, str] = {
    "TA-35": "TA35.TA",
    "TA-90": "TA90.TA",
    "TA-125": "^TA125.TA",
}

# Kept for the spike script — candidates that were probed.
TA_INDEX_CANDIDATES: dict[str, list[str]] = {
    "TA-35": ["TA35.TA", "^TA35.TA"],
    "TA-90": ["TA90.TA", "^TA90.TA"],
    "TA-125": ["^TA125.TA", "TA125.TA"],
}

# Source names -> instances are wired in config (Phase 1).
# Yahoo MCP is stdio-only => dev/local workhorse (Alpha Vantage free tier ~25 req/day).
# AWS chain: Alpha Vantage (remote HTTP MCP) primary, TASE authoritative for IL (Phase 6).
FALLBACK_CHAINS: dict[str, dict[str, list[str]]] = {
    "local": {"market_data": ["yahoo", "alpha_vantage"], "filings": ["sec_edgar"]},
    "aws": {"market_data": ["alpha_vantage", "tase"], "filings": ["sec_edgar"]},
}


def is_israeli(symbol: str) -> bool:
    s = symbol.upper()
    return s.endswith(TA_SUFFIX) or s.startswith("^TA")
