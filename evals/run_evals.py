"""Eval harness runner (fills out in Phases 2 and 4).

Metrics (targets in CLAUDE.md): fact accuracy (tolerance-aware), citation
coverage (100% of numeric claims), citation faithfulness (LLM judge, >=95%),
hallucination rate (0 tolerated).
"""

from pathlib import Path

import yaml

CASES_DIR = Path(__file__).parent / "cases"


def load_cases() -> list[dict]:
    return [yaml.safe_load(p.read_text()) for p in sorted(CASES_DIR.glob("*.yaml"))]


def main() -> None:
    cases = load_cases()
    print(f"Loaded {len(cases)} eval case(s):")
    for case in cases:
        print(f"  - {case['id']}: {case['question']}")
    print("\nEnd-to-end execution lands in Phase 4 (retrieval-only evals in Phase 2).")


if __name__ == "__main__":
    main()
