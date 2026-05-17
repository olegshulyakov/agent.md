#!/usr/bin/env python3
"""Scaffold AI eval fixtures for codegen-test users."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


VALID_TYPES = ("output", "tool-use", "ai-perf")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    if not slug:
        raise ValueError("name must contain at least one letter or number")
    return slug


def write_new(path: Path, content: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} already exists; pass --force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def output_cases(name: str) -> str:
    rows = [
        {
            "id": f"{name}-001",
            "input": "User asks a representative question for this AI feature.",
            "expected": "Answer is correct, complete, grounded in supplied context, and follows the requested format.",
            "assertions": [
                {"type": "schema", "description": "Output parses as the expected structure."},
                {"type": "rubric", "description": "Score >= 2 on task success and grounding rubric."},
            ],
            "metadata": {"category": "normal", "owner": "unset"},
        }
    ]
    return "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n"


def tool_use_cases(name: str) -> str:
    rows = [
        {
            "id": f"{name}-001",
            "input": "Agent should inspect context, call the right tool, recover from an empty result, and stop.",
            "fixtures": ["fixtures/workspace"],
            "expected_trace": {
                "required_tools": ["search"],
                "forbidden_tools": [],
                "max_tool_calls": 6,
            },
            "assertions": [
                {"type": "trace", "description": "Search happens before final answer."},
                {"type": "trace", "description": "Empty tool result triggers a revised query or blocker report."},
            ],
        }
    ]
    return "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n"


def ai_perf_cases(name: str) -> str:
    rows = [
        {
            "id": f"{name}-001",
            "input": "Representative AI task for benchmark measurement.",
            "quality_assertion": "Task passes the output/tool-use quality gate for this feature.",
            "thresholds": {
                "p95_latency_ms": 15000,
                "max_estimated_cost_usd": 0.25,
                "min_quality_pass_rate": 0.9,
            },
            "metadata": {"category": "normal", "runs": 5},
        }
    ]
    return "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n"


def runner_stub(eval_type: str) -> str:
    if eval_type == "ai-perf":
        return """#!/usr/bin/env python3
\"\"\"Benchmark runner stub.

Wire run_case() to your application entry point, then write one JSON object per run
to results.jsonl using the metrics schema from references/ai-perf.md.
\"\"\"

from __future__ import annotations

import json
from pathlib import Path


def run_case(case: dict) -> dict:
    raise NotImplementedError(\"connect this to the AI feature under test\")


def main() -> int:
    root = Path(__file__).resolve().parent
    cases = [json.loads(line) for line in (root / \"cases.jsonl\").read_text().splitlines() if line.strip()]
    with (root / \"results.jsonl\").open(\"w\") as output:
        for case in cases:
            result = run_case(case)
            output.write(json.dumps(result) + \"\\n\")
    return 0


if __name__ == \"__main__\":
    raise SystemExit(main())
"""

    return """#!/usr/bin/env python3
\"\"\"Eval runner stub.

Wire run_case() to your model, app endpoint, or agent harness. Keep raw outputs
so failures can be reviewed without rerunning the model.
\"\"\"

from __future__ import annotations

import json
from pathlib import Path


def run_case(case: dict) -> dict:
    raise NotImplementedError(\"connect this to the AI feature under test\")


def main() -> int:
    root = Path(__file__).resolve().parent
    cases = [json.loads(line) for line in (root / \"cases.jsonl\").read_text().splitlines() if line.strip()]
    results = []
    for case in cases:
        results.append(run_case(case))
    (root / \"results.json\").write_text(json.dumps(results, indent=2) + \"\\n\")
    return 0


if __name__ == \"__main__\":
    raise SystemExit(main())
"""


def rubric(eval_type: str) -> str:
    if eval_type == "tool-use":
        return """# Tool-Use Eval Rubric

Pass when the agent chooses appropriate tools, supplies valid arguments, handles tool errors, completes the task, and stops without unnecessary calls.

Fail when it fabricates tool results, calls forbidden tools, exceeds the call budget, edits unrelated state, or reports success without verification.
"""
    if eval_type == "ai-perf":
        return """# AI Performance Benchmark Gates

Evaluate quality and operational metrics together. A run only counts as successful when the quality gate passes and latency/cost thresholds stay within budget.
"""
    return """# AI Output Eval Rubric

Score 0: Fails the task or contradicts supplied context.
Score 1: Partially correct but misses important constraints or includes unsupported claims.
Score 2: Correct, grounded, complete, and follows the requested format.

Pass threshold: score >= 2.
"""


def scaffold(eval_type: str, name: str, root: Path, force: bool) -> list[Path]:
    slug = slugify(name)
    target = root / "evals" / ("ai-perf" if eval_type == "ai-perf" else eval_type) / slug
    created = [
        target / "cases.jsonl",
        target / "run.py",
        target / "rubric.md",
        target / "README.md",
    ]

    if eval_type == "output":
        cases = output_cases(slug)
    elif eval_type == "tool-use":
        cases = tool_use_cases(slug)
        created.append(target / "fixtures" / "workspace" / ".gitkeep")
    else:
        cases = ai_perf_cases(slug)
        created.extend([target / "pricing.json", target / "baseline.json"])

    write_new(target / "cases.jsonl", cases, force)
    write_new(target / "run.py", runner_stub(eval_type), force)
    write_new(target / "rubric.md", rubric(eval_type), force)
    write_new(target / "README.md", f"# {slug}\n\nType: `{eval_type}`\n", force)

    if eval_type == "tool-use":
        write_new(target / "fixtures" / "workspace" / ".gitkeep", "", force)
    elif eval_type == "ai-perf":
        write_new(target / "pricing.json", "{}\n", force)
        write_new(target / "baseline.json", "{}\n", force)

    return created


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--type", choices=VALID_TYPES, required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    try:
        created = scaffold(args.type, args.name, args.root, args.force)
    except (ValueError, FileExistsError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    for path in created:
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
