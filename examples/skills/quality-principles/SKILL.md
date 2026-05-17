---
name: quality-principles
description: >
  Use this skill when creating, reviewing, or substantially revising examples,
  rules, skills, technical docs, eval prompts, or generated code where quality,
  simplicity, maintainability, or implementation discipline matters. Do not use
  for trivial edits, formatting-only changes, simple factual answers, or quick
  command output.
author: Oleg Shulyakov
license: MIT
version: 1.0.0
---

# quality-principles

Use KISS, STAR, SOLID, and coding discipline as practical quality lenses. These rules bias toward clarity and restraint over speed. For trivial tasks, use judgment.

## 1. Use The Right Lens

**Apply the principle that improves the artifact at hand. Do not force every acronym into every answer.**

- Use KISS to keep examples narrow, direct, and complete. Remove workflow steps, abstractions, files, and sections that do not change the agent's behavior or the user's outcome.
- Use STAR for examples, eval prompts, case studies, incident summaries, and implementation notes. State the situation, the task, the action taken, and the result or expected result.
- Use SOLID when producing or reviewing code-oriented examples. Preserve clear responsibilities, isolate change-prone behavior, keep interfaces small, and depend on project-owned abstractions only when they already exist or clearly reduce coupling.
- Let KISS govern the other principles. STAR should make context easier to judge, and SOLID should prevent brittle code, not create ceremony.

## 2. Think Before Coding

**Do not assume. Do not hide confusion. Surface tradeoffs.**

Before substantial coding work:

- State assumptions and success criteria clearly enough that the change can be verified.
- If multiple plausible interpretations exist, ask or name the tradeoff instead of choosing silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop and name what is confusing.

## 3. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- Do not add features beyond what was asked.
- Do not add abstractions for single-use code.
- Do not add flexibility or configuration that was not requested.
- Do not add defensive branches unless they protect a realistic failure mode.
- If the implementation is much larger than the problem, simplify it.

## 4. Surgical Changes

**Touch only what you must. Clean up only your own changes.**

When editing existing code:

- Touch only files and lines that trace directly to the request.
- Match the surrounding style, even when a different style would be preferable in isolation.
- Leave unrelated cleanup, formatting, dead code removal, and refactors for a separate task.
- Remove imports, variables, functions, or files made unused by your own changes.

The test: every changed line should trace directly to the user's request.

## 5. Goal-Driven Execution

**Define success criteria. Verify with the narrowest meaningful check.**

Transform tasks into verifiable goals:

- "Add validation" means define invalid inputs, cover them, and make the check pass.
- "Fix the bug" means reproduce it, apply the fix, and verify the reproduction no longer fails.
- "Refactor X" means preserve behavior before and after the change.

Use a focused test, existing suite, typecheck, lint run, or explicit manual validation. Report any check that could not be run.
