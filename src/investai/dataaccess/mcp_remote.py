"""Streamable-HTTP MCP client — used for the official Alpha Vantage server
(https://mcp.alphavantage.co/mcp). Remote transport = directly Lambda-callable
on AWS, no sidecar. Phase 1."""

from typing import Any

from investai.dataaccess.interface import ToolSpec


class RemoteMcpSource:
    def __init__(self, name: str, url: str, headers: dict[str, str] | None = None) -> None:
        self.name = name
        self._url = url
        self._headers = headers or {}

    async def list_tools(self) -> list[ToolSpec]:
        # Phase 1: mcp.client.streamable_http session -> list_tools()
        raise NotImplementedError("Phase 1: remote MCP client")

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        raise NotImplementedError("Phase 1: remote MCP client")
