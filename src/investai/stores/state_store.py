"""StateStore seam — run state + thesis/ledger history.

Local: SQLite. AWS: DynamoDB (reuses Smart Scheduler single-table patterns).
"""

from typing import Protocol

from investai.orchestration.state import RunState


class StateStore(Protocol):
    async def save_run(self, state: RunState) -> None: ...

    async def load_run(self, run_id: str) -> RunState | None: ...

    async def list_runs(self, limit: int = 50) -> list[RunState]: ...


class SqliteStateStore:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    async def save_run(self, state: RunState) -> None:
        raise NotImplementedError("Phase 1: sqlite state store")

    async def load_run(self, run_id: str) -> RunState | None:
        raise NotImplementedError("Phase 1: sqlite state store")

    async def list_runs(self, limit: int = 50) -> list[RunState]:
        raise NotImplementedError("Phase 1: sqlite state store")


class DynamoStateStore:
    def __init__(self, table_name: str) -> None:
        self._table_name = table_name

    async def save_run(self, state: RunState) -> None:
        raise NotImplementedError("Phase 5: DynamoDB state store")

    async def load_run(self, run_id: str) -> RunState | None:
        raise NotImplementedError("Phase 5: DynamoDB state store")

    async def list_runs(self, limit: int = 50) -> list[RunState]:
        raise NotImplementedError("Phase 5: DynamoDB state store")
