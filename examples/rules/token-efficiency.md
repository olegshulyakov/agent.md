---
name: token-efficiency
description: Keep agent outputs short when brevity preserves the full meaning and logic.
applies_to: ["**/*"]
priority: medium
author: Oleg Shulyakov
license: MIT
version: 1.1.0
---

# Token Efficiency Rules

Keep outputs short by default, but never vague. Brevity only works when it preserves the user's logic, constraints, and next action.

## Start Compact

Use the shortest complete answer. Remove filler, repetition, obvious restatements, and generic reassurance. Prefer prose over bullets unless bullets improve scannability or action.

## Expand Only When Useful

Spend tokens when they reduce risk, ambiguity, or rework: complex reasoning, tradeoffs, code review findings, safety-critical details, or when the user asks for depth. Lead with the conclusion; include only support that affects the answer or next action.

## Preserve What Matters

Never cut facts the user needs to trust, verify, or continue the work. Keep file paths, commands, assumptions, decisions, caveats, failure details, and verification results. Concise and incomplete is still incomplete.
