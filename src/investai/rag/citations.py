"""Citation — maps every retrieved fact back to its source document + location."""

from pydantic import BaseModel


class Citation(BaseModel):
    doc_id: str
    source_url: str
    section: str | None = None  # e.g. "Item 1A"
    start_char: int | None = None
    end_char: int | None = None
    quote: str | None = None  # short verbatim supporting span
    language: str = "en"
