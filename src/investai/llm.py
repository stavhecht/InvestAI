"""Thin async Anthropic wrapper — one client, model selected per agent role.

Roles: "planner" -> Haiku (cheap decomposition), "agent" -> Sonnet (specialists).
Agents own their tool-use loops (Phase 3); this wrapper only issues single calls.
"""

from typing import Any, Literal

import anthropic

from investai.config import get_settings

Role = Literal["planner", "agent"]


class LlmClient:
    def __init__(self) -> None:
        settings = get_settings()
        self._client = anthropic.AsyncAnthropic(
            api_key=settings.anthropic_api_key or None  # None -> env/keychain resolution
        )
        self._models: dict[Role, str] = {
            "planner": settings.planner_model,
            "agent": settings.agent_model,
        }

    async def complete(
        self,
        *,
        role: Role,
        system: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        max_tokens: int = 16000,
    ) -> anthropic.types.Message:
        kwargs: dict[str, Any] = {
            "model": self._models[role],
            "max_tokens": max_tokens,
            "system": system,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools
        return await self._client.messages.create(**kwargs)
