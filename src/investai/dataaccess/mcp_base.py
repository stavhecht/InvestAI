"""Shared MCP client machinery for both transports.

Sessions are lazy and persistent: first call opens the transport + initializes
the session; `aclose()` tears it down. Payload extraction prefers the server's
structuredContent, falling back to JSON-parsing text blocks.
"""

import json
from contextlib import AsyncExitStack
from typing import Any

from mcp import ClientSession

from investai.dataaccess.interface import DataSourceError, ToolSpec


class BaseMcpSource:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name
        self._stack: AsyncExitStack | None = None
        self._sess: ClientSession | None = None

    def _transport(self):
        """Async context manager yielding (read, write, ...) streams."""
        raise NotImplementedError

    async def _session(self) -> ClientSession:
        if self._sess is None:
            self._stack = AsyncExitStack()
            try:
                streams = await self._stack.enter_async_context(self._transport())
                read, write = streams[0], streams[1]
                self._sess = await self._stack.enter_async_context(ClientSession(read, write))
                await self._sess.initialize()
            except BaseException:
                await self.aclose()
                raise
        return self._sess

    async def aclose(self) -> None:
        if self._stack is not None:
            stack, self._stack, self._sess = self._stack, None, None
            await stack.aclose()

    async def list_tools(self) -> list[ToolSpec]:
        session = await self._session()
        result = await session.list_tools()
        return [
            ToolSpec(name=t.name, description=t.description or "", input_schema=t.inputSchema)
            for t in result.tools
        ]

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        session = await self._session()
        result = await session.call_tool(name, arguments)
        payload = _extract_payload(result)
        if result.isError:
            raise DataSourceError(f"{self.name}.{name} failed: {payload}")
        return payload


def _extract_payload(result) -> Any:
    if result.structuredContent is not None:
        return result.structuredContent
    texts = [block.text for block in result.content if getattr(block, "text", None) is not None]
    text = "\n".join(texts)
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return text
