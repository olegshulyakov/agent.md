---
name: writer-spec-functional
description: >
  Produces a Functional Requirements Specification (FRS) documenting system behavior, actors, business rules,
  and functional flows. Use this skill whenever the user wants to write functional requirements, a functional spec,
  system requirements specification (SRS), document system behavior, define business rules, describe actors
  and their interactions, write use case narratives in spec form, or asks "what should the system do?"
  Distinct from writer-prd (which captures business goals and personas, not system behavior) and
  writer-spec-tech (which orchestrates functional + NFR + integration into a full technical specification).
---

# writer-spec-functional

Produce a **Functional Requirements Specification (FRS)** that precisely documents what a system must do: its actors, business rules, data entities, and functional flows.

## Why this is different from a PRD

A PRD answers "Why are we building this and for whom?" A functional spec answers "What exactly must the system do?" The FRS is the contract between the business analyst / product owner and the engineering team. It must be unambiguous enough that two developers reading it independently would build compatible systems.

## Information gathering

Extract from the user's input:

- **System or module** being specified
- **Actors** (who/what interacts with the system: users, external systems, scheduled jobs)
- **Scope** (which features or workflows are in this spec)
- **Key data entities** (what information does the system store and process)
- **Business rules** (constraints, conditions, calculations)

If you're working from a PRD or user stories, reference them and add behavioral precision. If working from scratch, make explicit inferences and mark them `[assumed]`.

## Output format

```
# Functional Requirements Specification: [System / Module Name]

**Version:** [e.g., 1.0 Draft]
**Date:** [YYYY-MM-DD]
**Status:** [Draft | In Review | Approved]

## 1. Overview

[2–4 sentences: what system this specifies, its purpose, and the business context.]

## 2. Actors

| Actor | Type | Description |
|-------|------|-------------|
| [Name] | [Human / System / Scheduled] | [Role and key interactions] |

## 3. System Boundary

[What is inside this spec vs. what interacts with it from outside. A simple diagram or bulleted list of external systems suffices.]

## 4. Data Entities (Conceptual)

[Key entities with attributes relevant to functional behavior — not a full schema, just enough to reason about the requirements.]

| Entity | Key Attributes | Notes |
|--------|---------------|-------|
| [Name] | [attr1, attr2] | [constraints, relationships] |

## 5. Functional Requirements

Group by capability area or actor workflow. Number requirements for traceability.

### 5.1 [Capability Area / Actor Workflow]

**FR-[N]-[M]: [Requirement name]**
- **Description:** [What the system must do. Start with "The system shall..." or "The system must..."]
- **Trigger:** [What initiates this behavior]
- **Preconditions:** [What must be true before]
- **Postconditions:** [What is true after successful completion]
- **Business Rules:** [Constraints, calculations, validation logic]
- **Error Conditions:** [What happens when preconditions aren't met or processing fails]

[Repeat for each requirement]

## 6. Business Rules

[Collect cross-cutting business rules that apply to multiple requirements.]

| Rule ID | Rule | Applies To |
|---------|------|-----------|
| BR-1 | [e.g., "Email addresses must be unique across all accounts"] | FR-1-1, FR-2-3 |

## 7. Data Validation Rules

| Field | Validation | Error Message |
|-------|-----------|---------------|
| [field] | [rule, e.g., "Required, max 255 chars, valid email format"] | [user-facing message] |

## 8. State Transitions (if applicable)

[For entities with lifecycle states, document the valid transitions.]

```

[State A] --[trigger]--> [State B]

```

Or as a table:

| From State | Event | To State | Guards |
|-----------|-------|---------|--------|

## 9. Non-Functional Requirements (brief)

[Note only the most critical NFRs here — performance thresholds, availability needs, security classifications. For a full NFR spec, recommend writer-spec-nfr.]

## 10. Assumptions & Constraints

| # | Type | Detail |
|---|------|--------|
| A-1 | Assumption | [assumed] |
| C-1 | Constraint | |

## 11. Open Issues

- [ ] [Question or decision needed before this spec can be finalized]

## Appendix: Glossary

| Term | Definition |
|------|-----------|
```

## Writing guidance

- **Requirements are behavioral, not implementational.** "The system shall validate that the email is unique" — not "use a database UNIQUE constraint on the email column."
- **Use consistent actor names.** Pick one name per actor and use it throughout.
- **Every requirement gets an ID.** FR-5-2 means requirement 2 in capability area 5. This enables traceability.
- **Error conditions are mandatory.** Requirements without error paths are incomplete.
- **Business rules live in section 6.** Don't embed complex rules inline in FR descriptions; reference them by BR-N.
- **Mark inferences.** If you infer a business rule or precondition, flag it `[assumed]`.

## Depth calibration

- **Small feature**: Sections 1, 2, 5, 6, 7 are sufficient.
- **Full module**: All sections.
- **Brownfield (existing system)**: Focus on changes; reference existing behavior by section/ID rather than restating it.
