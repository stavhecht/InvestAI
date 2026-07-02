# Infrastructure (Phase 5)

Terraform lands here in Phase 5. Planned modules (personal AWS account,
least-privilege IAM per component — reusing Smart Scheduler patterns):

- `network` — VPC + private subnets (EDGAR MCP Fargate service is private-only)
- `rds_pgvector` — Postgres + pgvector, **stoppable** (idle cost ≈ 0)
- `lambda_agent` — one per state-machine state
- `step_functions` — ASL compiled from `orchestration/machine.py`
- `api_gateway` — → FastAPI (Lambda)
- `fargate_mcp` — SEC EDGAR MCP, streamable-HTTP, private subnet
- `secrets` — Secrets Manager entries for the keys in `.env.example`
- `dynamodb` / `s3` — StateStore / BlobStore backing

Secrets are provided via `envs/dev/terraform.tfvars` (gitignored);
a `terraform.tfvars.example` with placeholders will accompany the modules.
