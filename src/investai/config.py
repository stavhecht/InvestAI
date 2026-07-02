"""Profile-driven settings. PROFILE=local|aws selects seam implementations.

Secrets come from .env locally (see .env.example) and from Secrets Manager on AWS
(Phase 5). Nothing here is ever hardcoded.
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    profile: Literal["local", "aws"] = "local"

    # --- API keys / secrets ---
    anthropic_api_key: str = ""
    voyage_api_key: str = ""
    alphavantage_api_key: str = ""
    tase_client_id: str = ""  # Phase 6 — TASE Data Hub OAuth2
    tase_client_secret: str = ""
    sec_edgar_user_agent: str = "InvestAI (you@example.com)"  # SEC requires identification

    # --- LLM model per role (Haiku planner, Sonnet specialists — see CLAUDE.md) ---
    planner_model: str = "claude-haiku-4-5"
    agent_model: str = "claude-sonnet-4-6"

    # --- Embeddings / rerank (multilingual — Hebrew-ready from day one) ---
    embed_model: str = "voyage-3.5"
    rerank_model: str = "rerank-2.5"

    # --- Storage (local profile defaults; AWS values land in Phase 5) ---
    database_url: str = "postgresql://investai:investai@localhost:5432/investai"
    state_db_path: str = "data/state.sqlite3"  # SqliteStateStore
    blob_dir: str = "data/blobs"  # LocalBlobStore


@lru_cache
def get_settings() -> Settings:
    return Settings()
