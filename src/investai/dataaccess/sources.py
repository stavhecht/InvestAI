"""Builds the named DataSource instances the registry's fallback chains refer to.

Local profile: Yahoo (stdio, no key — dev workhorse), SEC EDGAR (stdio),
Alpha Vantage (remote streamable-HTTP; only wired when a key is configured,
since its free tier is ~25 req/day). TASE joins in Phase 6.
"""

from investai.config import Settings, get_settings
from investai.dataaccess.interface import DataSource
from investai.dataaccess.mcp_remote import RemoteMcpSource
from investai.dataaccess.mcp_stdio import StdioMcpSource

ALPHAVANTAGE_MCP_URL = "https://mcp.alphavantage.co/mcp"


def build_sources(settings: Settings | None = None) -> dict[str, DataSource]:
    settings = settings or get_settings()
    sources: dict[str, DataSource] = {
        "yahoo": StdioMcpSource(
            "yahoo",
            command="uvx",
            args=["mcp-yahoo-finance"],
        ),
        "sec_edgar": StdioMcpSource(
            "sec_edgar",
            command="uvx",
            args=["sec-edgar-mcp"],
            env={"SEC_EDGAR_USER_AGENT": settings.sec_edgar_user_agent},
        ),
    }
    if settings.alphavantage_api_key:
        # Key-in-URL is Alpha Vantage's documented non-interactive connection
        # (the OAuth flow is for interactive clients like Claude Desktop).
        sources["alpha_vantage"] = RemoteMcpSource(
            "alpha_vantage",
            url=f"{ALPHAVANTAGE_MCP_URL}?apikey={settings.alphavantage_api_key}",
        )
    return sources


async def close_sources(sources: dict[str, DataSource]) -> None:
    for source in sources.values():
        aclose = getattr(source, "aclose", None)
        if aclose is not None:
            await aclose()
