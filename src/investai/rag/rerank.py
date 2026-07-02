"""Reranker seam — cross-encoder rerank recovers precision@k that hybrid
retrieval alone misses on jargon-dense filings. Voyage rerank-2.5 is
multilingual. Phase 2."""

from typing import Protocol

from investai.rag.store import ScoredChunk


class Reranker(Protocol):
    async def rerank(self, query: str, chunks: list[ScoredChunk], k: int) -> list[ScoredChunk]: ...


class VoyageReranker:
    def __init__(self, api_key: str, model: str = "rerank-2.5") -> None:
        self._api_key = api_key
        self.model = model

    async def rerank(self, query: str, chunks: list[ScoredChunk], k: int) -> list[ScoredChunk]:
        raise NotImplementedError("Phase 2: Voyage reranking")
