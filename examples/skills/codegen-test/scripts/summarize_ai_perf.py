#!/usr/bin/env python3
"""Summarize AI performance benchmark results from JSONL."""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


NUMERIC_FIELDS = (
    "latency_ms",
    "first_token_ms",
    "model_calls",
    "tool_calls",
    "retries",
    "input_tokens",
    "output_tokens",
    "estimated_cost_usd",
)


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return math.nan
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (len(ordered) - 1) * pct
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return ordered[int(rank)]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (rank - lower)


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    try:
        lines = path.read_text().splitlines()
    except FileNotFoundError:
        raise ValueError(f"{path} does not exist")

    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number} is not valid JSON: {exc}")
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{line_number} must contain a JSON object")
        rows.append(row)
    if not rows:
        raise ValueError(f"{path} contains no result rows")
    return rows


def numeric_values(rows: Iterable[dict], field: str) -> list[float]:
    values: list[float] = []
    for row in rows:
        value = row.get(field)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            values.append(float(value))
    return values


def summarize(rows: list[dict]) -> str:
    total = len(rows)
    passed = sum(1 for row in rows if row.get("quality_passed") is True)
    failed = sum(1 for row in rows if row.get("quality_passed") is False)
    unknown = total - passed - failed
    pass_rate = passed / total if total else 0.0
    cost_values = numeric_values(rows, "estimated_cost_usd")
    total_cost = sum(cost_values)
    cost_per_passing = total_cost / passed if passed else math.nan

    lines = [
        "# AI Performance Summary",
        "",
        f"- Runs: {total}",
        f"- Quality pass rate: {pass_rate:.1%} ({passed}/{total}, unknown: {unknown})",
        f"- Total estimated cost: ${total_cost:.4f}",
        f"- Cost per passing run: {'n/a' if math.isnan(cost_per_passing) else f'${cost_per_passing:.4f}'}",
        "",
        "## Metrics",
        "",
        "| Metric | p50 | p95 | max | total |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]

    for field in NUMERIC_FIELDS:
        values = numeric_values(rows, field)
        if not values:
            continue
        suffix = " ms" if field.endswith("_ms") else ""
        prefix = "$" if field == "estimated_cost_usd" else ""
        decimals = 4 if field == "estimated_cost_usd" else 1
        fmt = f"{{:.{decimals}f}}"
        lines.append(
            "| {field} | {p50} | {p95} | {max_value} | {total_value} |".format(
                field=field,
                p50=f"{prefix}{fmt.format(percentile(values, 0.50))}{suffix}",
                p95=f"{prefix}{fmt.format(percentile(values, 0.95))}{suffix}",
                max_value=f"{prefix}{fmt.format(max(values))}{suffix}",
                total_value=f"{prefix}{fmt.format(sum(values))}{suffix}",
            )
        )

    model_counts = Counter(str(row.get("model", "unknown")) for row in rows)
    if model_counts:
        lines.extend(["", "## Models", ""])
        for model, count in model_counts.most_common():
            lines.append(f"- `{model}`: {count} runs")

    by_case: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_case[str(row.get("case_id", "unknown"))].append(row)
    lines.extend(["", "## Cases", "", "| Case | Runs | Pass rate | p95 latency | Total cost |", "| --- | ---: | ---: | ---: | ---: |"])
    for case_id in sorted(by_case):
        case_rows = by_case[case_id]
        case_passed = sum(1 for row in case_rows if row.get("quality_passed") is True)
        latencies = numeric_values(case_rows, "latency_ms")
        costs = numeric_values(case_rows, "estimated_cost_usd")
        p95_latency = percentile(latencies, 0.95) if latencies else math.nan
        latency_text = "n/a" if math.isnan(p95_latency) else f"{p95_latency:.1f} ms"
        lines.append(
            f"| `{case_id}` | {len(case_rows)} | {case_passed / len(case_rows):.1%} | {latency_text} | ${sum(costs):.4f} |"
        )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path, help="Path to results.jsonl")
    parser.add_argument("--output", type=Path, help="Write summary markdown to this path")
    args = parser.parse_args()

    try:
        summary = summarize(load_jsonl(args.results))
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.output:
        args.output.write_text(summary)
    else:
        print(summary, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
