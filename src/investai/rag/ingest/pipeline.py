"""Ingest pipeline: fetch -> section-split -> chunk -> embed -> upsert.

Language-agnostic by construction: the chunker is selected per doc type/language,
every chunk carries a lang tag, and the embedder is multilingual — so the Hebrew
corpus (Phase 8) is a new chunker + new documents, not a pipeline rewrite. Phase 2.
"""

from investai.dataaccess.models import FilingRef
from investai.rag.embed import Embedder
from investai.rag.ingest.sections.base import SectionChunker
from investai.rag.store import VectorStore
from investai.stores.blob_store import BlobStore


async def ingest_filing(
    filing: FilingRef,
    *,
    blobs: BlobStore,
    chunker: SectionChunker,
    embedder: Embedder,
    store: VectorStore,
) -> int:
    """Returns the number of chunks upserted."""
    raise NotImplementedError("Phase 2: ingest pipeline")
