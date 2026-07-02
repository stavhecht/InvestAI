"""SEC 10-K / 10-Q section detection (English). Phase 2."""

import re

from investai.rag.ingest.sections.base import Section

# Canonical 10-K item headings — matched case-insensitively at line starts.
ITEM_PATTERN = re.compile(
    r"^\s*item\s+(\d{1,2}[ab]?)\s*[.:—-]", re.IGNORECASE | re.MULTILINE
)


class Sec10KChunker:
    lang = "en"

    def split(self, doc_text: str) -> list[Section]:
        # Phase 2: split on ITEM_PATTERN boundaries, keep char offsets for citations,
        # sub-chunk oversized sections on paragraph boundaries.
        raise NotImplementedError("Phase 2: 10-K section chunker")
