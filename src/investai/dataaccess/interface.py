"""DataSource — the uniform seam over every market/filings source.

Remote MCP (Alpha Vantage), stdio MCP (Yahoo, SEC EDGAR), and plain REST
(TASE Data Hub, Phase 6) all implement this, so agents and the registry never
know which transport is behind a symbol. We are MCP CLIENTS only — we never
publish a server.
"""

from typing import Any, Protocol

from pydantic import BaseModel


class DataSourceError(RuntimeError):
    """A source failed to answer — callers may try the next source in the chain."""


class ToolSpec(BaseModel):
    name: str
    description: str
    input_schema: dict[str, Any]


class DataSource(Protocol):
    name: str

    async def list_tools(self) -> list[ToolSpec]: ...

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any: ...
