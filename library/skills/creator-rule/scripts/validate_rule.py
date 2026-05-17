#!/usr/bin/env python3
"""Validate creator-rule skill packaging."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - depends on local Python environment
    yaml = None


ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "author",
    "license",
    "version",
    "allowed-tools",
    "metadata",
    "compatibility",
}


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def parse_frontmatter(content: str) -> dict:
    if not content.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML front matter")

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md front matter is not closed with ---")

    text = match.group(1)
    if yaml is not None:
        data = yaml.safe_load(text)
    else:
        data = {}
        for line in text.splitlines():
            if not line.strip() or line.startswith("  "):
                continue
            if ":" not in line:
                raise ValueError("Install PyYAML or use simple key: value front matter")
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()

    if not isinstance(data, dict):
        raise ValueError("SKILL.md front matter must be a YAML mapping")
    return data


def validate(skill_root: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_root / "SKILL.md"

    if not skill_md.exists():
        return ["SKILL.md not found"]

    try:
        frontmatter = parse_frontmatter(skill_md.read_text())
    except Exception as exc:
        return [str(exc)]

    unexpected = set(frontmatter) - ALLOWED_FRONTMATTER_KEYS
    if unexpected:
        errors.append(f"Unexpected front matter keys: {', '.join(sorted(unexpected))}")

    name = frontmatter.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("Missing non-empty name")
    elif not re.match(r"^[a-z0-9-]+$", name):
        errors.append("name must be kebab-case")

    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("Missing non-empty description")
    elif len(description.strip()) > 1024:
        errors.append("description must be 1024 characters or fewer")

    if not (skill_root / "evals" / "evals.json").exists():
        errors.append("evals/evals.json not found")
    if not (skill_root / "evals" / "trigger-evals.json").exists():
        errors.append("evals/trigger-evals.json not found")

    return errors


def main() -> int:
    skill_root = Path(__file__).resolve().parents[1]
    errors = validate(skill_root)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("creator-rule skill is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())

