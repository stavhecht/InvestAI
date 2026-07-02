"""RunState — the JSON-serializable object passed between orchestration states.

Mirrors a Step Functions payload: everything must survive JSON round-trips and
stay well under SFN's 256KB cap. Large artifacts (filings, chunk sets) go to
BlobStore; state carries references only.
"""

from typing import Literal

from pydantic import BaseModel, Field

from investai.api.schemas import ResearchBrief


class Subtask(BaseModel):
    id: str
    agent: Literal["market_data", "filings_rag"]
    instruction: str
    status: Literal["pending", "done", "failed"] = "pending"
    result_ref: str | None = None  # BlobStore key — never an inline payload


class RunState(BaseModel):
    run_id: str
    question: str
    current_state: str = "plan"
    plan: list[Subtask] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)  # BlobStore keys
    brief: ResearchBrief | None = None
    errors: list[str] = Field(default_factory=list)
