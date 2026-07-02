"""Section-aware chunking seam — language-agnostic by design.

Why section-aware (not fixed windows): 10-K structure (Item 1/1A/7/8) carries
meaning; fixed windows split tables mid-thought and destroy citation
granularity. Per-doc-type detection lives in subclasses; Hebrew MAYA support
(Phase 8) plugs in here without touching the rest of the pipeline.
"""

from typing import Protocol

from pydantic import BaseModel


class Section(BaseModel):
    title: str
    text: str
    start_char: int
    end_char: int


class SectionChunker(Protocol):
    lang: str

    def split(self, doc_text: str) -> list[Section]: ...
