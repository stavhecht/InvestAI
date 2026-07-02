"""Phase 1 smoke: connect to each MCP source, list its tools, print schemas.

Yahoo + EDGAR need no API key; Alpha Vantage is probed only if a key is in .env.
First run doubles as tool-name DISCOVERY — the quotes facade maps whatever this
prints. Run: uv run python scripts/smoke_mcp.py [source ...]
"""

import asyncio
import sys

from investai.dataaccess.sources import build_sources, close_sources


async def probe(name: str, source) -> None:
    print(f"\n=== {name} ===")
    try:
        tools = await source.list_tools()
    except Exception as err:  # noqa: BLE001 — smoke script, report and continue
        print(f"  CONNECT FAILED: {type(err).__name__}: {err}")
        return
    print(f"  {len(tools)} tools:")
    for tool in tools:
        params = ", ".join((tool.input_schema.get("properties") or {}).keys())
        desc = (tool.description or "").split("\n")[0][:80]
        print(f"    - {tool.name}({params})")
        print(f"        {desc}")


async def main() -> None:
    only = set(sys.argv[1:])
    sources = build_sources()
    if only:
        sources = {k: v for k, v in sources.items() if k in only}
    if not sources:
        print(f"No matching sources. Available: {list(build_sources().keys())}")
        return
    try:
        for name, source in sources.items():
            await probe(name, source)
    finally:
        await close_sources(sources)


if __name__ == "__main__":
    asyncio.run(main())
