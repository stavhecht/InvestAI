"""FastAPI layer. Async so the orchestrator's parallel fan-out isn't blocked.
Full /research implementation lands in Phase 4 (reuses Smart Scheduler layout)."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from investai.api.schemas import ResearchRequest
from investai.config import get_settings

app = FastAPI(title="InvestAI Research Desk", version="0.1.0")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "profile": get_settings().profile}


@app.post("/research")
async def research(req: ResearchRequest) -> JSONResponse:
    # Phase 4: build RunState, LocalRunner().run(), persist via StateStore,
    # return the ResearchBrief (disclaimer included by schema).
    return JSONResponse(
        status_code=501,
        content={"detail": "Phase 4: orchestrated research runs", "question": req.question},
    )
