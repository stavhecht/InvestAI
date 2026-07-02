# InvestAI — AI Personal Finance Research Desk

Multi-agent investment research over **US and Israeli markets**: a Planner decomposes
questions like *"compare SOXX vs SMH — holdings overlap and expense ratios"* or
*"research brief on LUMI.TA vs the TA-35"*, specialist agents gather market data (via
MCP servers) and grounded facts (via a self-built bilingual RAG pipeline), and an
Analyst writes a cited research brief. Every number traces to a source document.

> Output is research synthesis for personal use — **not investment advice**.
> The disclaimer is a required field of the output schema.

## Skills on display (portfolio project)

1. **Multi-agent orchestration** — hand-rolled state machine (no LangChain), shaped to
   compile 1:1 to AWS Step Functions.
2. **MCP consumption** — client of existing servers (Alpha Vantage remote HTTP,
   Yahoo Finance stdio, SEC EDGAR) plus a TASE Data Hub REST adapter behind the
   same `DataSource` interface.
3. **Bilingual RAG with citations** — section-aware chunking, hybrid pgvector + Postgres
   FTS retrieval with RRF fusion and Voyage reranking; Hebrew-capable embeddings from
   day one.

## Quickstart

```bash
cp .env.example .env       # fill in API keys
docker compose up -d       # Postgres + pgvector
uv sync                    # install deps (Python 3.11+)
uv run pytest              # unit tests
uv run python scripts/spike_symbols.py   # verify .TA symbol resolution
```

## Architecture, phases & conventions

See [CLAUDE.md](CLAUDE.md) — it is the authoritative project document (seams table,
data-source matrix, phase plan, decisions log).
