"""TASE Data Hub adapter (Phase 6) — REST wrapped in the DataSource interface.

There is no MCP server for TASE; this thin internal client (NOT a published
MCP server) makes openapi.tase.co.il look identical to the MCP sources.
Constraints to honor when implemented: OAuth2 client-credentials, burst limit
~10 req / 2 s (token-bucket throttle), prices in agorot -> Currency.ILA.
"""

from typing import Any

from investai.dataaccess.interface import ToolSpec


class TaseAdapter:
    name = "tase"

    def __init__(self, client_id: str, client_secret: str) -> None:
        self._client_id = client_id
        self._client_secret = client_secret

    async def list_tools(self) -> list[ToolSpec]:
        raise NotImplementedError("Phase 6: TASE Data Hub integration")

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        raise NotImplementedError("Phase 6: TASE Data Hub integration")
