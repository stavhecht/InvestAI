"""Embedder seam. Voyage voyage-3.5 is multilingual (Hebrew-capable) from day
one, so the Phase 8 Hebrew corpus lands with NO re-embedding. Phase 2."""

from typing import Literal, Protocol


class Embedder(Protocol):
    async def embed(
        self, texts: list[str], *, input_type: Literal["document", "query"]
    ) -> list[list[float]]: ...


class VoyageEmbedder:
    def __init__(self, api_key: str, model: str = "voyage-3.5") -> None:
        self._api_key = api_key
        self.model = model

    async def embed(
        self, texts: list[str], *, input_type: Literal["document", "query"]
    ) -> list[list[float]]:
        # Phase 2: voyageai.AsyncClient().embed(texts, model=..., input_type=...)
        raise NotImplementedError("Phase 2: Voyage embeddings")
