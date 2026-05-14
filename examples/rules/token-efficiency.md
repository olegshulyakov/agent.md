---
name: token-efficiency
description: Keep agent outputs short when brevity preserves the full meaning and logic.
applies_to: ["**/*"]
priority: medium
---

# Token Efficiency Rules

- Prefer the shortest complete answer that preserves the request's logic, constraints, and next action.
- Remove filler, repetition, obvious restatements, and generic reassurance before sending a response.
- Use bullets only when they make the answer easier to scan; otherwise use compact prose.
- Expand only for complex reasoning, user-facing tradeoffs, code review findings, safety-critical details, or when the user asks for depth.
- When shortening content, preserve concrete file paths, commands, assumptions, decisions, and verification results.
- Do not omit necessary caveats or failure details just to reduce length.
