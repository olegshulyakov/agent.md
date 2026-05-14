#!/usr/bin/env python3
"""Validate creator-rule eval files."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        raise ValueError(f"{path} does not exist")
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is not valid JSON: {exc}")


def validate_task_evals(path: Path) -> list[str]:
    errors: list[str] = []
    data = load_json(path)

    if data.get("skill_name") != "creator-rule":
        errors.append("evals.json skill_name must be creator-rule")

    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        errors.append("evals.json must contain a non-empty evals list")
        return errors

    seen_ids: set[int] = set()
    for index, item in enumerate(evals, start=1):
        prefix = f"evals[{index}]"
        eval_id = item.get("id")
        if not isinstance(eval_id, int):
            errors.append(f"{prefix}.id must be an integer")
        elif eval_id in seen_ids:
            errors.append(f"{prefix}.id duplicates {eval_id}")
        else:
            seen_ids.add(eval_id)

        for field in ("prompt", "expected_output"):
            value = item.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}.{field} must be a non-empty string")

        files = item.get("files", [])
        if not isinstance(files, list):
            errors.append(f"{prefix}.files must be a list")

    return errors


def validate_trigger_evals(path: Path) -> list[str]:
    errors: list[str] = []
    data = load_json(path)

    if not isinstance(data, list) or not data:
        return ["trigger-evals.json must contain a non-empty list"]

    positives = 0
    negatives = 0
    seen_queries: set[str] = set()

    for index, item in enumerate(data, start=1):
        prefix = f"trigger[{index}]"
        query = item.get("query")
        if not isinstance(query, str) or not query.strip():
            errors.append(f"{prefix}.query must be a non-empty string")
        elif query in seen_queries:
            errors.append(f"{prefix}.query is duplicated")
        else:
            seen_queries.add(query)

        should_trigger = item.get("should_trigger")
        if not isinstance(should_trigger, bool):
            errors.append(f"{prefix}.should_trigger must be a boolean")
        elif should_trigger:
            positives += 1
        else:
            negatives += 1

    if positives == 0 or negatives == 0:
        errors.append("trigger-evals.json must include both positive and negative cases")

    return errors


def main() -> int:
    skill_root = Path(__file__).resolve().parents[1]
    evals_dir = skill_root / "evals"

    try:
        errors = validate_task_evals(evals_dir / "evals.json")
        errors.extend(validate_trigger_evals(evals_dir / "trigger-evals.json"))
    except ValueError as exc:
        return fail(str(exc))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("creator-rule eval files are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())

