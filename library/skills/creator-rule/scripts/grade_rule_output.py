#!/usr/bin/env python3
"""Heuristic grader for creator-rule output-quality evals.

This script is intentionally deterministic. It does not replace human review or
model grading; it catches common failures cheaply: vague rules, missing scoped
paths, missing commands copied from the prompt, unsafe handling of conflicts or
secrets, and wrong runtime format.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


GENERIC_FILLER = [
    "write clean code",
    "be careful",
    "ensure quality",
    "use best practices",
    "make the code good",
]

IMPERATIVE_RE = re.compile(
    r"\b(use|run|never|do not|don't|ask|include|update|avoid|prefer|keep|"
    r"write|add|check|verify|redact|report|call out|do)\b",
    re.IGNORECASE,
)


def load_eval(evals_path: Path, eval_id: int) -> dict:
    data = json.loads(evals_path.read_text())
    for item in data.get("evals", []):
        if item.get("id") == eval_id:
            return item
    raise ValueError(f"eval id {eval_id} not found in {evals_path}")


def code_terms(text: str) -> list[str]:
    return sorted(set(re.findall(r"`([^`]+)`", text)))


def contains_any(text: str, terms: list[str]) -> bool:
    lower = text.lower()
    return any(term.lower() in lower for term in terms)


def add_check(checks: list[dict], name: str, passed: bool, evidence: str) -> None:
    checks.append({"name": name, "passed": bool(passed), "evidence": evidence})


def grade(eval_item: dict, output: str) -> dict:
    checks: list[dict] = []
    prompt = eval_item["prompt"]
    expected = eval_item["expected_output"]
    lower_output = output.lower()
    lower_prompt = prompt.lower()
    lower_expected = expected.lower()

    add_check(
        checks,
        "non_empty_substantial_output",
        len(output.strip()) >= 250,
        f"Output length is {len(output.strip())} characters",
    )
    add_check(
        checks,
        "uses_direct_imperatives",
        len(IMPERATIVE_RE.findall(output)) >= 3,
        "Found at least three imperative verbs" if len(IMPERATIVE_RE.findall(output)) >= 3 else "Too few imperative verbs",
    )
    add_check(
        checks,
        "avoids_generic_filler",
        not contains_any(output, GENERIC_FILLER),
        "No banned generic filler found" if not contains_any(output, GENERIC_FILLER) else "Generic filler phrase found",
    )

    prompt_terms = code_terms(prompt)
    if prompt_terms:
        missing_terms = [term for term in prompt_terms if term not in output]
        add_check(
            checks,
            "preserves_prompt_commands_and_paths",
            not missing_terms,
            "All backticked prompt terms appear in output" if not missing_terms else f"Missing: {missing_terms}",
        )

    wants_modular = any(term in lower_prompt + lower_expected for term in [".agents/rules", "modular", "playbook-compatible"])
    if wants_modular:
        add_check(
            checks,
            "has_rule_frontmatter",
            output.lstrip().startswith("---") and all(key in output for key in ("name:", "description:", "priority:")),
            "Front matter includes name, description, and priority",
        )

    wants_claude = "claude" in lower_prompt or "claude" in lower_expected
    if wants_claude:
        add_check(
            checks,
            "claude_rule_mentions_paths_or_claude_rules",
            "paths:" in lower_output or ".claude/rules" in lower_output,
            "Claude output includes path scoping or .claude/rules location",
        )

    wants_cursor = "cursor" in lower_prompt or "cursor" in lower_expected
    if wants_cursor:
        add_check(
            checks,
            "cursor_rule_mentions_cursor_or_path_scope",
            "cursor" in lower_output or "globs:" in lower_output or "applies_to:" in lower_output,
            "Cursor output includes Cursor or path-scope metadata",
        )

    wants_copilot = "copilot" in lower_prompt or "copilot" in lower_expected
    if wants_copilot:
        add_check(
            checks,
            "copilot_rule_mentions_expected_file",
            "copilot-instructions.md" in lower_output or ".github/instructions" in lower_output,
            "Copilot output mentions a supported instruction location",
        )

    if "secret" in lower_prompt or ".env" in lower_prompt:
        add_check(
            checks,
            "handles_secrets_safely",
            contains_any(output, ["never", "do not", "redact"]) and contains_any(output, [".env", "secret", "token"]),
            "Output contains secret-handling prohibitions and redaction language",
        )

    if "conflict" in lower_expected or "existing instruction says" in lower_prompt:
        add_check(
            checks,
            "detects_rule_conflict",
            contains_any(output, ["conflict", "contradict", "existing instruction", "clarify", "which rule"]),
            "Output flags conflict or asks for clarification",
        )

    if "local-only" in lower_prompt or "never commit" in lower_prompt:
        add_check(
            checks,
            "keeps_personal_context_local",
            contains_any(output, ["local", "gitignore", "do not commit", "never commit"]) and contains_any(output, ["shared", "project instructions", "version control"]),
            "Output keeps local details out of shared instructions",
        )

    passed = sum(1 for check in checks if check["passed"])
    total = len(checks)
    return {
        "eval_id": eval_item["id"],
        "summary": {
            "passed": passed,
            "failed": total - passed,
            "total": total,
            "pass_rate": round(passed / total, 3) if total else 0,
        },
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Grade one creator-rule eval output")
    parser.add_argument("--eval-id", type=int, required=True, help="Eval id from evals/evals.json")
    parser.add_argument("--output", required=True, help="Path to the generated rule output")
    parser.add_argument(
        "--evals",
        default=None,
        help="Path to evals.json. Defaults to ../evals/evals.json relative to this script.",
    )
    parser.add_argument("--min-pass-rate", type=float, default=0.8)
    args = parser.parse_args()

    script_root = Path(__file__).resolve().parent
    evals_path = Path(args.evals) if args.evals else script_root.parent / "evals" / "evals.json"

    try:
        eval_item = load_eval(evals_path, args.eval_id)
        output = Path(args.output).read_text()
        result = grade(eval_item, output)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2))
    return 0 if result["summary"]["pass_rate"] >= args.min_pass_rate else 1


if __name__ == "__main__":
    sys.exit(main())

