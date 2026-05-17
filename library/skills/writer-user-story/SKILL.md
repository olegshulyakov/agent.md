---
name: writer-user-story
description: >
  Write user stories with acceptance criteria and developer tasks. Use for story writing,
  Jira/Linear/GitHub tickets, task breakdowns, story points, and story-level sprint planning.
author: Oleg Shulyakov
license: MIT
version: 1.0.0
---

# writer-user-story

Produce one or more **user stories** with acceptance criteria, then decompose each into **developer tasks** with file/module hints and effort estimates.

## Why this structure matters

**Stories connect user value to verifiable delivery work.**

Stories capture user intent and define done. Tasks translate that intent into work a developer can pick up without a meeting. Linking them hierarchically prevents the classic gap where stories are approved but engineers still don't know what to build.

Follow the **3 C's** framework: **Card** (the written story), **Conversation** (the ongoing dialogue that refines scope and details — stories are conversation starters, not specs), **Confirmation** (acceptance criteria that define done).

Use **STAR** as a lightweight quality check when context is available: the situation explains the user's current problem, the task defines the goal, the action appears in the behavior or developer work, and the result is captured in the "so that" clause and acceptance criteria.

## Information gathering

**Extract the story ingredients before estimating or decomposing work.**

Extract from the user's input:

- **Feature or capability** being described
- **User type(s)** / persona(s)
- **Technical context**: codebase language, framework, relevant modules (if mentioned or inferable)
- **Scope**: single story, or multiple stories for a feature/epic?

If context is sparse, write one exemplary story with a clear note that more context would yield better task breakdowns.

## Output format

**Load the detailed story template only when writing stories.**

Before drafting, read `references/output-format.md` for the required story structure.

## Writing guidance

**Make each story independently valuable, estimable, and testable.**

**Stories:**

- One user value per story — resist the urge to bundle two different user goals
- The "so that" is the most important part — it defines the WHY and prevents gold-plating
- Keep stories simple. Split whenever the card needs multiple personas, unrelated outcomes, or more than one sprint-sized goal.
- Validate each story against **INVEST**:
  - **I**ndependent (self-contained, orderable),
  - **N**egotiable (details emerge through conversation),
  - **V**aluable (delivers user value),
  - **E**stimable (team can size it),
  - **S**mall (fits one sprint),
  - **T**estable (clear pass/fail via AC)
- Write AC in Given/When/Then; each criterion should be independently testable
- Include at least one error/edge-case AC
- Points reflect uncertainty + effort. Anything >5 should be split.
- **Keep the story statement implementation-free** — describe the user goal, not the UI or technology. "I want to invite my friends" not "I want to click an invite button in the settings menu".

**Tasks:**

- Each task is a single coherent unit of developer work (ideally <1 day)
- Use imperative phrasing: "Add", "Create", "Update", "Wire", "Write"
- File hints should be concrete if context allows: `src/api/users.ts`, `UserService.java`
- If you don't know the codebase, use logical module names and note them as `[assumed path]`
- Effort: XS (<1h), S (1–2h), M (half-day), L (full day)

**Estimation:**

- Be honest about uncertainty. If the task involves unknown third-party APIs, say so.
- Flag high-risk tasks with ⚠️

## Splitting stories

**Split whenever one card contains more than one user goal.**

If the feature described maps to multiple user goals, split into separate stories. Common split patterns:

- **Happy path + error handling** (different complexity, can ship incrementally)
- **Core feature + admin/configuration** (different user types)
- **Read + write operations** (can be developed in parallel)

When examples would help calibrate story granularity, acceptance criteria, or developer-task detail, read `references/examples.md`.
