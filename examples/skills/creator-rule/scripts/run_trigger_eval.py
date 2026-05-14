#!/usr/bin/env python3
"""Run creator-rule trigger evals.

By default this uses a transparent lexical router so the eval set can run
offline in CI. Pass --agent-command to test a real CLI/router. The command can
include {prompt_file}, {prompt}, {skill_name}, or {description}; otherwise the
judge prompt is sent on stdin.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


POSITIVE_PATTERNS = [
    r"\b(write|create|draft|make|improve|rewrite|turn).{0,60}\b(rule|rules|instruction|instructions)\b",
    r"\b(AGENTS\.md|CLAUDE\.md|copilot-instructions\.md|Cursor rule|\.agents/rules|\.claude/rules)\b",
    r"\bpath-scoped rule\b",
    r"\bCLI-agent rule\b",
]

NEGATIVE_PATTERNS = [
    r"\b(review this pull request|fix the failing|generate SQL|release notes|user story|technical spec)\b",
    r"\b(explain|summarize)\b.*\b(AGENTS\.md|README|coding standards)\b",
]


def parse_skill(skill_root: Path) -> tuple[str, str]:
    content = (skill_root / "SKILL.md").read_text()
    name_match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
    desc_match = re.search(r"^description:\s*>\n(?P<body>(?:  .+\n?)+)", content, re.MULTILINE)

    name = name_match.group(1).strip() if name_match else skill_root.name
    if desc_match:
        description = " ".join(line.strip() for line in desc_match.group("body").splitlines())
    else:
        description = ""
    return name, description


def lexical_router(query: str) -> bool:
    if any(re.search(pattern, query, re.IGNORECASE) for pattern in NEGATIVE_PATTERNS):
        return False
    return any(re.search(pattern, query, re.IGNORECASE) for pattern in POSITIVE_PATTERNS)


def parse_bool(text: str) -> bool | None:
    stripped = text.strip()
    try:
        data = json.loads(stripped)
        if isinstance(data, bool):
            return data
        if isinstance(data, dict):
            for key in ("should_trigger", "trigger", "use_skill", "would_use_skill"):
                if isinstance(data.get(key), bool):
                    return data[key]
    except json.JSONDecodeError:
        pass

    first = stripped.splitlines()[0].strip().lower() if stripped else ""
    if first in {"true", "yes", "trigger", "use", "use_skill"}:
        return True
    if first in {"false", "no", "skip", "do not trigger", "do_not_use"}:
        return False
    return None


def agent_router(command_template: str, query: str, skill_name: str, description: str, timeout: int) -> bool:
    judge_prompt = f"""Decide whether the skill should be used for the user query.

Skill name: {skill_name}
Skill description: {description}

User query: {query}

Respond with JSON only: {{"should_trigger": true}} or {{"should_trigger": false}}.
"""

    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as prompt_file:
        prompt_file.write(judge_prompt)
        prompt_path = prompt_file.name

    command = command_template.format(
        prompt=judge_prompt,
        prompt_file=prompt_path,
        skill_name=skill_name,
        description=description,
    )

    try:
        if "{prompt" in command_template:
            completed = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=timeout)
        else:
            completed = subprocess.run(command, shell=True, input=judge_prompt, text=True, capture_output=True, timeout=timeout)
    finally:
        Path(prompt_path).unlink(missing_ok=True)

    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or f"agent command exited {completed.returncode}")

    parsed = parse_bool(completed.stdout)
    if parsed is None:
        raise RuntimeError(f"could not parse agent response as boolean: {completed.stdout[:200]}")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description="Run creator-rule trigger evals")
    parser.add_argument("--eval-set", default=None, help="Path to trigger-evals.json")
    parser.add_argument("--skill-path", default=None, help="Path to creator-rule skill root")
    parser.add_argument("--agent-command", default=None, help="Optional CLI command template for real routing judgment")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    script_root = Path(__file__).resolve().parent
    skill_root = Path(args.skill_path) if args.skill_path else script_root.parent
    eval_set_path = Path(args.eval_set) if args.eval_set else skill_root / "evals" / "trigger-evals.json"
    skill_name, description = parse_skill(skill_root)
    evals = json.loads(eval_set_path.read_text())

    results = []
    for item in evals:
        query = item["query"]
        expected = item["should_trigger"]
        try:
            actual = (
                agent_router(args.agent_command, query, skill_name, description, args.timeout)
                if args.agent_command
                else lexical_router(query)
            )
            error = None
        except Exception as exc:
            actual = False
            error = str(exc)

        results.append(
            {
                "query": query,
                "should_trigger": expected,
                "triggered": actual,
                "pass": actual == expected,
                "error": error,
            }
        )

    passed = sum(1 for result in results if result["pass"])
    output = {
        "skill_name": skill_name,
        "method": "agent_command" if args.agent_command else "lexical_router",
        "summary": {"passed": passed, "failed": len(results) - passed, "total": len(results)},
        "results": results,
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(f"{passed}/{len(results)} trigger evals passed ({output['method']})")
        for result in results:
            if not result["pass"]:
                print(
                    f"FAIL expected={result['should_trigger']} actual={result['triggered']}: {result['query']}",
                    file=sys.stderr,
                )
                if result["error"]:
                    print(f"  {result['error']}", file=sys.stderr)

    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())

