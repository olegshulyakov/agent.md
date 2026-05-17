---
name: karpathy-guidelines
description: >
  Behavioral guidelines to avoid common LLM coding mistakes. Use when writing, reviewing, or refactoring code — especially when scope is ambiguous or the request could be solved multiple ways.
author: Multica AI
license: MIT
version: 1.1.0
---

# Karpathy Guidelines

Behavioral guidelines to reduce common LLM coding mistakes, derived from Andrej Karpathy's observations on LLM coding pitfalls.

Tradeoff: These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Silent guesses are expensive. Before implementing: state your assumptions explicitly, name competing interpretations rather than picking one silently, and ask one focused question if something is unclear. If a simpler approach exists than what was asked, say so.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

Write the least code that fully solves the stated problem — no speculative features, single-use abstractions, or error handling for impossible scenarios. If the solution is 200 lines and 50 would do, write 50.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

Touch only what the task requires. Don't reformat, refactor, or rename things outside your change. Match existing style. Clean up only what _your_ edits orphaned (unused imports, dead variables). If you notice something broken nearby, mention it — don't silently fix it.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → write tests for invalid inputs, then make them pass
- "Fix the bug" → write a test that reproduces it, then make it pass
- "Refactor X" → ensure tests pass before and after

For multi-step tasks, state a brief plan: `[step] → verify: [check]` per line. Weak criteria require constant clarification; strong criteria let you loop to done independently.
