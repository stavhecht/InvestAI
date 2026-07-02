"""Hebrew MAYA announcement section detection — Phase 8 (stretch).

Stub exists now so the SectionChunker seam is demonstrably language-pluggable.
Embeddings are already multilingual (voyage-3.5), so landing this requires NO
re-embedding of the English corpus.
"""

from investai.rag.ingest.sections.base import Section


class MayaHebrewChunker:
    lang = "he"

    def split(self, doc_text: str) -> list[Section]:
        raise NotImplementedError("Phase 8: Hebrew MAYA section chunker")
