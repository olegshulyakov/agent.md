---
name: writer-prd
description: Use this skill whenever the user mentions writing a PRD, product requirements, product brief, feature requirements, go-to-market requirements, OKRs tied to a feature, product scope definition, or asks for help capturing what a product should do and for whom.
author: Oleg Shulyakov
license: MIT
version: 1.0.0
---

# writer-prd

Produce a complete, structured **Product Requirements Document (PRD)** for the described product, feature, or initiative.

## What makes a great PRD

**A PRD defines product intent without prescribing implementation.**

A PRD bridges business intent and engineering execution. It must be specific enough to guide decisions but not prescribe implementation.
The goal is to answer: _Why are we building this? For whom? What does success look like? What is and isn't in scope?_

## Information gathering

**Extract known context first and ask only when a missing answer changes the document.**

Before writing, extract from the user's prompt (or ask once if genuinely missing):

- **What** is being built (feature, product, initiative)?
- **Why** — the business problem or opportunity it solves
- **Who** — the target users / personas
- **Success** — how will we know it worked? (metrics, KPIs, OKRs)
- **Constraints** — timeline, platform, budget, regulatory

If the user provides a rough description, work with what's there. Make educated inferences and mark them clearly with `[assumed]` so the user can verify.

## Output format

**Load the detailed Markdown structure only when writing the PRD.**

Always produce a Markdown file. Before drafting, read `references/output-format.md` for the required structure.

## Writing guidance

**Keep requirements outcome-focused, testable, and scoped.**

- **Goals first, solutions second.** Resist the urge to specify UI or technical implementation in the requirements.
- **Keep scope simple.** Prefer the smallest coherent product slice that can prove the goal before expanding into adjacent workflows.
- **Use STAR for evidence and examples.** Frame user problems with situation, task, action, and result when describing journeys, research notes, or success examples.
- **Make requirements testable.** "The page loads in under 2 seconds" is better than "the page should be fast."
- **Scope the out-of-scope.** Explicitly naming non-goals is as valuable as naming goals — it prevents future debate.
- **Mark inferences.** If you infer a persona, metric, or assumption, add `[assumed]` inline so the user can verify.
- **Keep it scannable.** Use tables for metrics and assumptions. Avoid walls of prose.

## Multi-section depth calibration

**Scale the document to the amount of source context.**

Scale depth to what the user provides:

- **Terse prompt** (one sentence): Write a lean PRD with 2–3 goals, 1–2 personas, and 5–10 requirements. Mark most things `[assumed]`.
- **Detailed prompt**: Fill out all sections thoroughly, infer less.
- **Existing draft**: Improve, restructure, and fill gaps rather than rewriting from scratch.

When examples would help calibrate tone, specificity, or section depth, read `references/examples.md`.
