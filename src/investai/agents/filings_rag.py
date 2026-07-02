"""Filings-RAG agent — retrieves grounded facts + citations from our own
RAG pipeline (Sonnet). Facts without a Citation are not facts."""

from investai.orchestration.state import RunState


class FilingsRagAgent:
    async def __call__(self, state: RunState) -> RunState:
        # Phase 3: rag.retrieve() per subtask; evidence (chunks + citations) -> BlobStore
        raise NotImplementedError("Phase 3: filings retrieval")
