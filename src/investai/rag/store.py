"""VectorStore seam — ONE implementation, pgvector, everywhere.

Locally it's the docker-compose Postgres; on AWS it's RDS. The seam collapses
to the DSN. Dense search = pgvector; lexical (BM25-ish) = Postgres full-text
search in the same database; fusion happens in retrieve.py. Phase 2.
"""

from typing import Protocol

from pydantic import BaseModel

from investai.rag.citations import Citation


class Chunk(BaseModel):
    doc_id: str
    section: str | None
    text: str
    lang: str = "en"  # language tag on EVERY chunk from day one (bilingual design)
    start_char: int
    end_char: int
    source_url: str

    def to_citation(self, quote: str | None = None) -> Citation:
        return Citation(
            doc_id=self.doc_id,
            source_url=self.source_url,
            section=self.section,
            start_char=self.start_char,
            end_char=self.end_char,
            quote=quote,
            language=self.lang,
        )


class ScoredChunk(BaseModel):
    chunk: Chunk
    score: float


class VectorStore(Protocol):
    async def upsert(self, chunks: list[Chunk], vectors: list[list[float]]) -> None: ...

    async def dense_search(self, query_vector: list[float], k: int) -> list[ScoredChunk]: ...

    async def lexical_search(self, query: str, k: int) -> list[ScoredChunk]: ...


class PgVectorStore:
    def __init__(self, dsn: str) -> None:
        self._dsn = dsn

    async def upsert(self, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        raise NotImplementedError("Phase 2: pgvector upsert + FTS index")

    async def dense_search(self, query_vector: list[float], k: int) -> list[ScoredChunk]:
        raise NotImplementedError("Phase 2: pgvector cosine search")

    async def lexical_search(self, query: str, k: int) -> list[ScoredChunk]:
        raise NotImplementedError("Phase 2: Postgres FTS search")
