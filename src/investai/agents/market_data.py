"""Market-data agent — quotes/holdings/fees via the DataSource layer (Sonnet).

Routes symbols through dataaccess.registry (`.TA` handling, fallback chains);
raw payloads land in BlobStore, state carries refs.
"""

from investai.orchestration.state import RunState


class MarketDataAgent:
    async def __call__(self, state: RunState) -> RunState:
        # Phase 3: execute state.plan subtasks tagged agent="market_data"
        raise NotImplementedError("Phase 3: market-data gathering")
