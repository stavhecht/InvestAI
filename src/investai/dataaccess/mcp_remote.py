"""Streamable-HTTP MCP client — used for the official Alpha Vantage server
(https://mcp.alphavantage.co/mcp). Remote transport = directly Lambda-callable
on AWS, no sidecar."""

from mcp.client.streamable_http import streamablehttp_client

from investai.dataaccess.mcp_base import BaseMcpSource


class RemoteMcpSource(BaseMcpSource):
    def __init__(self, name: str, url: str, headers: dict[str, str] | None = None) -> None:
        super().__init__(name)
        self._url = url
        self._headers = headers or {}

    def _transport(self):
        return streamablehttp_client(self._url, headers=self._headers or None)
