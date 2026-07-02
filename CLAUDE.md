# InvestAI — AI Personal Finance Research Desk

Multi-agent investment research system covering **US and Israeli markets**. Answers
questions like "compare SOXX vs SMH — holdings overlap and expense ratios" or
"research brief on LUMI.TA vs the TA-35" by orchestrating specialized agents.

**Portfolio/CV project** demonstrating three skills:
1. Multi-agent orchestration (supervisor + specialists, hand-rolled)
2. MCP **consumption** (client of existing third-party servers — we do NOT publish MCP servers)
3. Self-built bilingual RAG with citations

## Non-negotiables

- **Grounding:** every factual number in output must trace to a real source document
  via a citation. Never model-guessed. Numeric computation (overlap %, fee diffs) is
  done by deterministic Python tools in `analysis/`, never LLM arithmetic.
- **Disclaimer:** output is research synthesis, NOT investment advice. The
  `ResearchBrief` schema has a required `disclaimer` field.
- **No LangChain / LangGraph / CrewAI.** Orchestrator is a hand-rolled state machine
  (Anthropic SDK + shared `RunState`).
- **No OpenSearch Serverless** (~$700/mo floor). Vector store is pgvector.
- **Local-first, AWS-deployable.** Both paths behind the same seams; switching is
  config (`PROFILE=local|aws`), not a rewrite. AWS resources must be stoppable
  (`scripts/aws_stop.sh`) so idle cost ≈ $0.
- Docker must run on ARM / Apple Silicon.

## Architecture

Four agents, each a pure step `(RunState) -> RunState`:
- **Planner** (Haiku): decomposes the question into subtasks.
- **Market-Data** (Sonnet): quotes/holdings/expense-ratios/fundamentals via the
  data-access layer, US + Israeli (`.TA` suffix).
- **Filings-RAG** (Sonnet): retrieves grounded facts + citations from our own RAG
  pipeline.
- **Analyst** (Sonnet): calls deterministic `analysis/` tools, weighs evidence,
  writes the brief with inline citations.

The state machine is defined as data in `orchestration/machine.py`; `LocalRunner`
executes it in-process, and (Phase 5) `asl_compiler.py` translates the SAME
definition to Step Functions ASL. Two rules keep that mirror honest:
1. `RunState` is JSON-serializable and stays under SFN's 256KB payload limit —
   big artifacts go to `BlobStore`, state carries references.
2. Retry/catch semantics are declared per-state in the machine definition.

## Abstraction seams (local ↔ AWS)

| Seam | Local | AWS |
|---|---|---|
| `VectorStore` | pgvector in Docker | pgvector on RDS (same class, different DSN) |
| `StateStore` | SQLite | DynamoDB |
| `BlobStore` | local FS | S3 |
| `Orchestrator` | `LocalRunner` | Step Functions (compiled ASL) |
| `DataSource` | MCP clients + adapters | same; stdio sources demoted (see below) |
| `Embedder`/`Reranker` | Voyage API | Voyage API |

## Data-access layer

Uniform `DataSource` protocol (`list_tools()` / `call_tool()`). We are MCP
**clients** only. Registry (`dataaccess/registry.py`) routes symbols and defines
primary→fallback chains.

| Source | Kind | Transport | Notes |
|---|---|---|---|
| Alpha Vantage (official MCP) | US+IL market data | remote streamable HTTP (`mcp.alphavantage.co/mcp`, OAuth) | Lambda-friendly. Free tier ~25 req/day → dev uses Yahoo. |
| Yahoo Finance MCP | free fallback / dev workhorse | stdio (npx/uvx) | `.TA` symbols work. **Dev/local-only in AWS profile** (stdio). |
| SEC EDGAR MCP (stefanoamorelli/sec-edgar-mcp) | US filings | stdio locally; supports `--transport streamable-http` | On AWS: Fargate service in private VPC (its HTTP mode is unauthenticated). Needs `SEC_EDGAR_USER_AGENT` only. |
| TASE Data Hub (openapi.tase.co.il) | authoritative Israeli data + MAYA filings feed | REST, wrapped in `tase_adapter.py` (Phase 6) | OAuth2, ~10 req/2s burst limit. Registration submitted in Phase 0. |

**Israeli-market gotchas (verified 2026-07-02 by `scripts/spike_symbols.py`):**
TASE **equities** quote in **agorot** (currency code `ILA`, 1/100 ILS — LUMI.TA
returns 6704 ILA = 67.04 ILS) while TA **indices** quote in ILS; `Quote` carries
`currency` + `price_normalized()`. Quotes are delayed — carry `as_of` + `is_delayed`.
Verified index symbols (inconsistent caret!): TA-35 → `TA35.TA`, TA-90 → `TA90.TA`,
TA-125 → `^TA125.TA` (see `dataaccess/registry.py:TA_INDEX_SYMBOLS`).

## RAG pipeline (self-built — the core skill)

fetch → section-aware chunk → embed → pgvector upsert; query → hybrid (dense +
Postgres FTS) → RRF fusion → Voyage rerank → top-k with `Citation` objects
(doc_id, section, char span, source URL).

- **Section-aware chunking** (not fixed windows): 10-K structure (Item 1/1A/7/8)
  carries meaning; fixed windows split tables mid-thought and ruin citation granularity.
- **Hybrid + rerank justification:** filings are jargon-dense; BM25 nails exact
  terms ("expense ratio", tickers, "Item 1A") that cosine similarity blurs; dense
  catches paraphrase; cross-encoder rerank recovers precision@k.
- **Bilingual by design, English corpus first:** Voyage voyage-3.5 embeddings are
  multilingual (Hebrew-capable) from day 1; every chunk has a `lang` tag; section
  chunkers are pluggable per doc type (`sections/sec_10k.py` now, `maya_he.py` in
  Phase 8). Result: Hebrew corpus lands later with **no re-embedding**.
- v1 Israeli coverage = dual-listed companies' English SEC filings (CYBR, NICE, CHKP).

## Tech stack

Python 3.11+ (uv, ruff, pytest) · Anthropic API (Sonnet agents, Haiku planner) ·
Voyage AI (voyage-3.5 + rerank-2.5) · FastAPI + Pydantic (async fan-out) ·
Postgres + pgvector (Docker local / RDS AWS) · Terraform · React + Vite frontend
(Phase 7, dark mode, clickable citations).

**AWS account:** personal (NOT AWS Academy) — Terraform creates least-privilege
IAM roles per component, reusing Smart Scheduler patterns (FastAPI layout,
DynamoDB single-table, SFN ASL, Terraform modules, per-function IAM).

## Evals (`evals/`)

~18 YAML cases against a **frozen corpus snapshot**. Metrics: fact accuracy
(tolerance-aware), citation coverage (100% of numeric claims), citation
faithfulness (LLM judge, ≥95%), hallucination rate (0 tolerated). Mix: US ETF
comparisons (SOXX/SMH flagship, MAGS), 10-K facts, dual-listed IL briefs,
`.TA` quotes with agorot-scaling checks, multi-hop holdings questions, and
adversarial cases (absent ticker → must refuse; false premise → must correct;
Hebrew query on English corpus; intraday request → flag delayed/EOD).

## Phase plan & status

| Phase | Scope | Status |
|---|---|---|
| P0 | Scaffold, docker-compose, seam protocols, CLAUDE.md, TASE registration, symbol spike | ✅ (TASE registration = user action, pending) |
| P1 | Data-access layer: MCP clients (both transports), 3 sources, registry, models | ✅ (AV parser unverified — needs key) |
| P2 | RAG pipeline + retrieval evals (corpus: eval tickers' filings) | ☐ |
| P3 | Agents + state machine + deterministic analysis tools; CLI end-to-end | ☐ |
| P4 | FastAPI + full eval harness | ☐ |
| P5 | AWS deploy (Terraform, Lambda, SFN, RDS pgvector, Fargate EDGAR) | ☐ |
| P6 | TASE Data Hub adapter (authoritative IL data) | ☐ |
| P7 | React frontend | ☐ |
| P8 | Stretch: Hebrew/MAYA ingestion | ☐ |

## Decisions log

- **2026-07-02:** Hebrew corpus deferred to P8; pipeline language-agnostic from day 1.
- **2026-07-02:** TASE Data Hub — register immediately, integrate P6; Yahoo `.TA` is v1 Israeli data.
- **2026-07-02:** Personal AWS account (not AWS Academy/voclabs).
- **2026-07-02:** pgvector both local (Docker) and AWS (RDS) — one VectorStore impl.
- **2026-07-02:** Voyage AI for embeddings + rerank (multilingual, free tier, Lambda-friendly).
- **2026-07-02:** Yahoo MCP is dev/local-only in the AWS profile (stdio-only transport).
- **2026-07-02:** Spike verified — TASE equities quote in agorot (ILA), indices in ILS;
  index symbols: `TA35.TA`, `TA90.TA`, `^TA125.TA` (TA-125 alone takes the caret).
- **2026-07-02:** CYBR returns no data on Yahoo (likely delisted post-acquisition) —
  drop it from the eval ticker list; NICE/CHKP/TEVA confirmed working. CYBR's historical
  SEC filings may still serve the RAG corpus — decide at Phase 2 corpus freeze.
- **2026-07-02 (P1):** Yahoo MCP server = `uvx mcp-yahoo-finance` (10 tools). Its
  `get_current_stock_price` returns a BARE float with no currency — currency is inferred
  from the registry rule (TASE equity=ILA, TA index=ILS, else USD) in `quotes.py`.
- **2026-07-02 (P1):** SEC EDGAR MCP = `uvx sec-edgar-mcp` (21 tools). It has
  `get_filing_sections(identifier, accession_number, form_type)` — use it as the section
  source in Phase 2 instead of hand-parsing 10-K HTML.
- **2026-07-02 (P1):** Fallback happens at the CAPABILITY level (`quotes.get_quote`
  walks the chain with per-source parsers), not the raw tool level — tool names differ
  per server. Alpha Vantage parser written against documented GLOBAL_QUOTE shape;
  **verify live once ALPHAVANTAGE_API_KEY is set** (TODO in quotes.py).

## Developer context

Final-year CS student in Israel, bilingual Hebrew/English. Strong: Python, FastAPI,
React+Vite, AWS (Lambda, SFN, DynamoDB, S3, API GW, Terraform, IAM). Prior project
"Smart Scheduler" — reuse its FastAPI/DynamoDB/SFN/Terraform/IAM patterns where noted.
