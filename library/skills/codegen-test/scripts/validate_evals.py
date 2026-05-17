#!/usr/bin/env python3
"""Validate codegen-test eval files."""

from __future__ import annotations

import json
import sys
from pathlib import Path


VALID_ROUTES = {
    "e2e",
    "api",
    "perf",
    "ai-output",
    "ai-tool-use",
    "ai-perf",
}


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        raise ValueError(f"{path} does not exist")
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is not valid JSON: {exc}")


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    data = load_json(path)

    if not isinstance(data, dict):
        return ["evals.json must contain a JSON object"]

    if data.get("skill_name") != "codegen-test":
        errors.append("skill_name must be codegen-test")

    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        errors.append("evals must be a non-empty list")
        return errors

    seen_ids: set[int] = set()
    seen_prompts: set[str] = set()
    routes_seen: set[str] = set()

    for index, item in enumerate(evals, start=1):
        prefix = f"evals[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue

        eval_id = item.get("id")
        if not isinstance(eval_id, int):
            errors.append(f"{prefix}.id must be an integer")
        elif eval_id in seen_ids:
            errors.append(f"{prefix}.id duplicates {eval_id}")
        else:
            seen_ids.add(eval_id)

        prompt = item.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"{prefix}.prompt must be a non-empty string")
        elif prompt in seen_prompts:
            errors.append(f"{prefix}.prompt is duplicated")
        else:
            seen_prompts.add(prompt)

        expected = item.get("expected_output")
        if not isinstance(expected, str) or not expected.strip():
            errors.append(f"{prefix}.expected_output must be a non-empty string")
        else:
            route_matches = {route for route in VALID_ROUTES if f"Routes to {route}" in expected}
            if not route_matches:
                errors.append(
                    f"{prefix}.expected_output must include one route marker: "
                    + ", ".join(f"'Routes to {route}'" for route in sorted(VALID_ROUTES))
                )
            elif len(route_matches) > 1:
                errors.append(f"{prefix}.expected_output mentions multiple routes: {sorted(route_matches)}")
            else:
                routes_seen.update(route_matches)

        files = item.get("files", [])
        if not isinstance(files, list):
            errors.append(f"{prefix}.files must be a list")
        elif not all(isinstance(file, str) for file in files):
            errors.append(f"{prefix}.files entries must be strings")

    missing_routes = VALID_ROUTES - routes_seen
    if missing_routes:
        errors.append(f"evals must cover every route; missing: {sorted(missing_routes)}")

    return errors


def main() -> int:
    skill_root = Path(__file__).resolve().parents[1]
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else skill_root / "evals" / "evals.json"

    try:
        errors = validate(path)
    except ValueError as exc:
        return fail(str(exc))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"{path} is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
