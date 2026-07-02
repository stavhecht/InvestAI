"""stdio MCP client — Yahoo Finance and (locally) SEC EDGAR servers.

stdio is dev/local-only: the AWS profile drops Yahoo and runs EDGAR's
streamable-HTTP mode on Fargate instead (see CLAUDE.md data-source table).
"""

from mcp import StdioServerParameters
from mcp.client.stdio import get_default_environment, stdio_client

from investai.dataaccess.mcp_base import BaseMcpSource


class StdioMcpSource(BaseMcpSource):
    def __init__(
        self,
        name: str,
        command: str,
        args: list[str] | None = None,
        env: dict[str, str] | None = None,
    ) -> None:
        super().__init__(name)
        self._params = StdioServerParameters(
            command=command,
            args=args or [],
            # SDK replaces the environment wholesale — merge over the safe
            # defaults or the child loses PATH/HOME and won't start.
            env={**get_default_environment(), **(env or {})},
        )

    def _transport(self):
        return stdio_client(self._params)
