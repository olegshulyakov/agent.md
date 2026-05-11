---
name: writer-spec
description: >
  Use this skill whenever the user wants to write a spec, document system behavior, define requirements, or design a contract.
  Triggers include:
    - "write a spec",
    - "write a tech spec",
    - "write a design doc",
    - "write a TDD",
    - "functional requirements",
    - "non-functional requirements",
    - "NFR document",
    - "data contract",
    - "UI spec",
    - "handoff doc",
  "system requirements", "design specification", "what should the system do", "document this feature".
author: Oleg Shulyakov
licence: MIT
version: 1.1.0
---

# writer-spec

This skill is a **router**. Identify the user's intent, pick the matching spec type below, and produce
that document using its format. When the request is ambiguous or spans multiple types, combine the
relevant sections and note which spec types were merged.

---

## Routing table

| If the user asks for…                                                                      | Reference          |
| ------------------------------------------------------------------------------------------ | ------------------ |
| Full tech spec, design doc, TDD, "spec out end-to-end"                                     | **Tech**           |
| Functional requirements, system behavior, use cases, actors, business rules                | **Functional**     |
| Non-functional requirements, performance targets, SLA, availability, security constraints  | **Non-Functional** |
| Data contract, data product interface, event schema, producer/consumer agreement, data SLA | **Data Contract**  |
| UI spec, component states, design handoff, interaction patterns, design tokens             | **Design**         |

When multiple types are needed (e.g., "I need a functional spec and NFRs"), produce each as a
clearly headed section within one document rather than switching between formats mid-flow.

---

## Spec type: Tech (Full Technical Specification)

Use when: "write a tech spec", "design doc", "TDD", "full spec before we build", end-to-end coverage.
Reference: `references/technical.md`

A tech spec is a contract between the person who understands what to build and the team who builds
it. Resolve all major ambiguities before implementation starts.

**Information to extract from context:**

- Feature or system being built
- Problem being solved and why now
- Actors (users, admins, external systems)
- Tech stack, scale, integration points
- Constraints (timeline, compliance, team size)

**Depth calibration:**

- Simple feature (< 1 week): Focus on sections 2, 5, 6, 10.
- Major feature (1–4 weeks): Full document.
- New system: Emphasize sections 4, 6, 7, 8.
- Existing system change: Emphasize what's changing, migration plan, backward compatibility.

---

## Spec type: Functional

Use when: "functional requirements", "what should the system do", "use case spec", "system behavior", "business rules".
Reference: `references/functional.md`

A functional spec is the contract between the business analyst / product owner and engineering.
It must be unambiguous enough that two developers reading it independently would build compatible systems.

**Information to extract:** system or module, actors, scope, key data entities, business rules.

**Writing rules:**

- Requirements are behavioral, not implementational.
- Use consistent actor names throughout.
- Every requirement gets an ID (FR-5-2 = area 5, requirement 2).
- Error conditions are mandatory — requirements without error paths are incomplete.
- Business rules live in section 6; reference them by BR-N from within FRs.

---

## Spec type: Non-Functional

Use when: "non-functional requirements", "performance targets", "NFR document", "availability SLA", "system constraints".
Reference: `references/non-functional.md`

---

## Spec type: Data Contract

Use when: "data contract", "data product spec", "event schema", "producer/consumer agreement", "data SLA", "data mesh contract".
Reference: `references/data-contract.md`

---

## Spec type: Design (UI/UX Handoff)

Use when: "UI spec", "design spec", "design handoff", "component states", "interaction patterns", "UX spec".
Reference: `references/design-ui.md`

---

## General writing rules (apply to all spec types)

- **Be specific**: "Token expires after 15 minutes" not "tokens expire quickly."
- **Make it testable**: Every requirement should translate directly to a test case.
- **Requirements are behavioral, not implementational**: "The system shall validate email uniqueness" — not "use a UNIQUE constraint."
- **Document the omissions**: If auth is out of scope, say why.
- **Mark inferences**: Flag every assumed detail with `[assumed]` so reviewers can verify.
- **Error conditions are mandatory**: Requirements without error paths are incomplete.
