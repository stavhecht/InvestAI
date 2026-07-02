"""Hybrid retrieval: dense (pgvector) + lexical (Postgres FTS) -> RRF fusion
-> rerank -> top-k with citations.

Why hybrid + rerank (design justification, see CLAUDE.md): finance filings are
jargon-dense — BM25/FTS nails exact terms ("expense ratio", tickers, "Item 1A")
that cosine similarity blurs; dense catches paraphrase; the cross-encoder
reranker buys back precision@k. Phase 2.
"""

from investai.rag.embed import Embedder
from investai.rag.rerank import Reranker
from investai.rag.store import ScoredChunk, VectorStore


async def retrieve(
    query: str,
    *,
    store: VectorStore,
    embedder: Embedder,
    reranker: Reranker,
    k: int = 8,
    fanout: int = 25,
) -> list[ScoredChunk]:
    # Phase 2:
    #   1. embed(query, input_type="query")
    #   2. dense_search(fanout) + lexical_search(fanout) concurrently
    #   3. reciprocal-rank fusion of the two lists
    #   4. reranker.rerank(query, fused, k)
    raise NotImplementedError("Phase 2: hybrid retrieval pipeline")
