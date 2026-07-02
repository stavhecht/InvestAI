"""Output schemas. The disclaimer is a REQUIRED field of every brief — grounding
and not-investment-advice are non-negotiables (see CLAUDE.md)."""

from datetime import datetime

from pydantic import BaseModel, Field

from investai.rag.citations import Citation

DISCLAIMER = (
    "This document is automated research synthesis for personal use only. "
    "It is NOT investment advice, may contain errors or delayed data, and must "
    "not be relied upon for investment decisions."
)


class ResearchRequest(BaseModel):
    question: str = Field(..., min_length=3)


class Finding(BaseModel):
    """One claim in the brief. Numeric claims MUST carry at least one citation."""

    text: str
    citations: list[Citation] = Field(default_factory=list)


class ResearchBrief(BaseModel):
    question: str
    findings: list[Finding] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)  # doc_ids / URLs referenced
    generated_at: datetime
    disclaimer: str = DISCLAIMER  # mandated default; serializes into every brief
