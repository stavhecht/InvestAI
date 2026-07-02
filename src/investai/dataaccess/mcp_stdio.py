"""stdio MCP client — used for the Yahoo Finance and (locally) SEC EDGAR
servers. stdio is dev/local-only: the AWS profile drops Yahoo and runs EDGAR's
streamable-HTTP mode on Fargate instead (see CLAUDE.md data-source table).
Phase 1."""

from typing import Any

from investai.dataaccess.interface import ToolSpec


class StdioMcpSource:
    def __init__(
        self,
        name: str,
        command: str,
        args: list[str] | None = None,
        env: dict[str, str] | None = None,
    ) -> None:
        self.name = name
        self._command = command
        self._args = args or []
        self._env = env or {}

    async def list_tools(self) -> list[ToolSpec]:
        # Phase 1: mcp.client.stdio session -> list_tools()
        raise NotImplementedError("Phase 1: stdio MCP client")

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        raise NotImplementedError("Phase 1: stdio MCP client")
