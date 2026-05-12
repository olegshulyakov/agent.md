---
name: writer-prd
description: Use this skill whenever the user mentions writing a PRD, product requirements, product brief, feature requirements, go-to-market requirements, OKRs tied to a feature, product scope definition, or asks for help capturing what a product should do and for whom.
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# writer-prd

Produce a complete, structured **Product Requirements Document (PRD)** for the described product, feature, or initiative.

## What makes a great PRD

A PRD bridges business intent and engineering execution. It must be specific enough to guide decisions but not prescribe implementation.
The goal is to answer: _Why are we building this? For whom? What does success look like? What is and isn't in scope?_

## Information gathering

Before writing, extract from the user's prompt (or ask once if genuinely missing):

- **What** is being built (feature, product, initiative)?
- **Why** — the business problem or opportunity it solves
- **Who** — the target users / personas
- **Success** — how will we know it worked? (metrics, KPIs, OKRs)
- **Constraints** — timeline, platform, budget, regulatory

If the user provides a rough description, work with what's there. Make educated inferences and mark them clearly with `[assumed]` so the user can verify.

## Output format

Always produce a Markdown file. Use this structure exactly:

```md
# PRD: [Product / Feature Name]

## Status

[Draft | In Review | Approved] — [Date]
**Author:** [if known, else omit]
**Stakeholders:** [list if mentioned, else omit]

## Problem Statement

[1–3 paragraphs. What pain exists? Who feels it? What's the cost of inaction?]

## Goals [optional]

- ...

## Target Users / Personas

[For each persona: role, context, key jobs-to-be-done, frustrations]

## Scope

### In Scope

- [Concrete capability or deliverable]

### Out of Scope [optional]

- [Explicit exclusions to prevent scope creep]

## Functional Requirements

[Numbered list of WHAT the system must do. Use "The system shall..." or "Users can..." phrasing. Group by user journey or capability area.]

1. **[Capability Area]**
   1.1 ...
   1.2 ...

## Non-Functional Requirements (summary)

[Performance, availability, security, compliance highlights. If deep NFRs are needed, recommend writer-spec-nfr.]

## User Journeys / Key Flows [optional]

[1–3 critical flows described as numbered steps. Diagrams optional but welcome.]

## Assumptions & Dependencies [optional]

| Item | Type                    | Detail |
| ---- | ----------------------- | ------ |
| ...  | Assumption / Dependency | ...    |

## Open Questions [optional]

- [ ] [Question that must be resolved before implementation]

## Appendix [optional]

[Glossary, related docs, links — only if needed]
```

## Writing guidance

- **Goals first, solutions second.** Resist the urge to specify UI or technical implementation in the requirements.
- **Make requirements testable.** "The page loads in under 2 seconds" is better than "the page should be fast."
- **Scope the out-of-scope.** Explicitly naming non-goals is as valuable as naming goals — it prevents future debate.
- **Mark inferences.** If you infer a persona, metric, or assumption, add `[assumed]` inline so the user can verify.
- **Keep it scannable.** Use tables for metrics and assumptions. Avoid walls of prose.

## Multi-section depth calibration

Scale depth to what the user provides:

- **Terse prompt** (one sentence): Write a lean PRD with 2–3 goals, 1–2 personas, and 5–10 requirements. Mark most things `[assumed]`.
- **Detailed prompt**: Fill out all sections thoroughly, infer less.
- **Existing draft**: Improve, restructure, and fill gaps rather than rewriting from scratch.

## Example

**Input:** "We want to add dark mode to our web app for enterprise users who use the tool all day."

**Output excerpt:**

```markdown
## Problem Statement

Enterprise users often work 8+ hours daily in the application. Prolonged exposure to bright interfaces causes eye strain, especially in low-light environments. Competitor tools already offer dark mode, which has become a baseline expectation for power users...

## Goals

- Reduce eye strain complaints
- Increase power-user retention
```
