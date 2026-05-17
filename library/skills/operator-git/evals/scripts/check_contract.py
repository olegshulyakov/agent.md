#!/usr/bin/env python3
"""Static contract checks for the operator-git skill."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT.parent / "SKILL.md"
BRANCH = ROOT.parent / "references" / "branch-naming.md"
COMMIT = ROOT.parent / "references" / "commit-message.md"
TRIGGER_EVALS = ROOT / "trigger-evals.json"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check(condition: bool, message: str, evidence: str) -> dict:
    return {
        "text": message,
        "passed": bool(condition),
        "evidence": evidence,
    }


def main() -> int:
    skill = read(SKILL)
    branch = read(BRANCH)
    commit = read(COMMIT)
    trigger_evals = json.loads(TRIGGER_EVALS.read_text(encoding="utf-8"))

    expectations = [
        check(
            "### Output workflow" in skill and "### Action workflow" in skill,
            "SKILL.md defines both output and action workflow types",
            "Found both workflow headings in SKILL.md",
        ),
        check(
            "return only the requested artifact" in skill and "Do not wrap generated artifacts" in skill,
            "Output workflows require artifact-only responses",
            "Found artifact-only and no-wrapper instructions in SKILL.md",
        ),
        check(
            "do not add extra explanatory output" in skill,
            "Action workflows suppress extra narrative on success",
            "Found successful-action quiet-output instruction in SKILL.md",
        ),
        check(
            "`references/branch-naming.md`" in skill and "`references/commit-message.md`" in skill,
            "Router points to both convention references",
            "Found both reference paths in the routing table",
        ),
        check(
            "Output vs Action Behavior" not in branch and "Output vs Action Behavior" not in commit,
            "Shared output/action behavior is not duplicated in references",
            "The duplicate heading is absent from branch and commit references",
        ),
        check(
            bool(re.search(r"`git switch -c <branch>`", branch)),
            "Branch action guidance prefers git switch -c for creation",
            "Found git switch -c guidance in branch-naming.md",
        ),
        check(
            len(trigger_evals) >= 16
            and any(item["should_trigger"] for item in trigger_evals)
            and any(not item["should_trigger"] for item in trigger_evals),
            "Trigger evals cover both positive and negative routing cases",
            f"Found {len(trigger_evals)} trigger evals",
        ),
    ]

    passed = sum(1 for item in expectations if item["passed"])
    result = {
        "expectations": expectations,
        "summary": {
            "passed": passed,
            "failed": len(expectations) - passed,
            "total": len(expectations),
            "pass_rate": passed / len(expectations),
        },
    }
    print(json.dumps(result, indent=2))
    return 0 if passed == len(expectations) else 1


if __name__ == "__main__":
    raise SystemExit(main())
