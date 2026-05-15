---
name: creator-skill
description: Create, edit, evaluate, package, and optimize skills. Use for skill authoring, iterative improvement, eval runs, benchmarks, trigger tuning, and skill packaging.
author: Anthropic
license: Apache-2.0
version: 1.1.0
---

# creator-skill

Create new skills, improve existing skills, evaluate outputs, optimize trigger descriptions, and package final skill folders.

## Route the Work

Choose the smallest reference needed for the user's current task:

| User intent | Read |
| --- | --- |
| Create a new skill or revise skill instructions | `references/authoring.md` |
| Build eval cases, run iterations, benchmark outputs, or collect human feedback | `references/evaluation.md` |
| Optimize a skill description for trigger accuracy | `references/description-optimization.md` |
| Adapt the workflow for agents without subagents, Claude Code, generic CLIs, or Cowork | `references/agent-compatibility.md` |
| Validate eval, grading, benchmark, or feedback JSON structures | `references/schemas.md` |

If the request spans multiple phases, read the references in workflow order: authoring, evaluation, description optimization, then agent compatibility only when platform details matter.

## Core Workflow

1. Clarify what the skill should do, when it should trigger, what output it should produce, and whether objective evals are useful.
2. Write or revise `SKILL.md` with concise metadata, focused instructions, and references for details that would bloat the main file.
3. For objectively testable skills, create realistic eval prompts and run skill-enabled outputs against a meaningful baseline.
4. Show outputs and benchmark results to the user before making another revision.
5. Iterate until feedback is resolved or further changes stop improving results.
6. Package the final skill only after the user is satisfied with behavior and trigger accuracy.

## Skill Authoring Rules

- Keep metadata under 100 tokens and the main instruction body under 5000 tokens.
- Put trigger cues in the frontmatter `description`; put routing, exclusions, examples, and detailed procedures in the body or references.
- Do not create placeholder directories. Add `scripts/`, `references/`, `assets/`, or `evals/` only when the skill actually uses them.
- Prefer deterministic scripts for repetitive validation, grading, packaging, and report generation.
- Keep skills portable across agents unless the user asks for one specific runtime. Isolate platform-specific behavior in a compatibility section or reference.

## Bundled Resources

- `scripts/run_eval.py`, `scripts/run_loop.py`, and `scripts/improve_description.py` support trigger-description optimization.
- `scripts/aggregate_benchmark.py` summarizes iteration results.
- `scripts/package_skill.py` packages a completed skill folder.
- `eval-viewer/generate_review.py` creates the human review UI for eval outputs and benchmark results.
- `agents/grader.md`, `agents/comparator.md`, and `agents/analyzer.md` support grading, blind comparison, and benchmark analysis.
