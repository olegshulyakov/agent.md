---
name: writer-spec
description: >
  Use this skill whenever the user wants to write functional requirements, a functional spec,
  system requirements specification (SRS), document system behavior, define business rules, describe actors
  and their interactions, write use case narratives in spec form, or asks "what should the system do?".
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# writer-spec

Produce a **Functional Requirements Specification (FRS)** that precisely documents what a system must do: its actors, business rules, data entities, and functional flows.

## What makes a great SPEC

A functional spec answers "What exactly must the system do?". The FRS is the contract between the business analyst / product owner and the engineering team. It must be unambiguous enough that two developers reading it independently would build compatible systems.

## Information gathering

Extract from the user's input:

- **System or module** being specified
- **Actors** (who/what interacts with the system: users, external systems, scheduled jobs)
- **Scope** (which features or workflows are in this spec)
- **Key data entities** (what information does the system store and process)
- **Business rules** (constraints, conditions, calculations)

If you're working from a PRD or user stories, reference them and add behavioral precision. If working from scratch, make explicit inferences and mark them `[assumed]`.

## Output format

````md
# Functional Requirements Specification: [System / Module Name]

**Version:** [e.g., 1.0 Draft]
**Date:** [YYYY-MM-DD]
**Status:** [Draft | In Review | Approved]

## 1. Overview

[2–4 sentences: what system this specifies, its purpose, and the business context.]

## 2. Actors

| Actor  | Type                         | Description                 |
| ------ | ---------------------------- | --------------------------- |
| [Name] | [Human / System / Scheduled] | [Role and key interactions] |

## 3. System Boundary

[What is inside this spec vs. what interacts with it from outside. A simple diagram or bulleted list of external systems suffices.]

## 4. Data Entities (Conceptual)

[Key entities with attributes relevant to functional behavior — not a full schema, just enough to reason about the requirements.]

| Entity | Key Attributes | Notes                        |
| ------ | -------------- | ---------------------------- |
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

| Rule ID | Rule                                                         | Applies To     |
| ------- | ------------------------------------------------------------ | -------------- |
| BR-1    | [e.g., "Email addresses must be unique across all accounts"] | FR-1-1, FR-2-3 |

## 7. Data Validation Rules

| Field   | Validation                                                  | Error Message         |
| ------- | ----------------------------------------------------------- | --------------------- |
| [field] | [rule, e.g., "Required, max 255 chars, valid email format"] | [user-facing message] |

## 8. State Transitions (if applicable)

[For entities with lifecycle states, document the valid transitions.]

```
[State A] --[trigger]--> [State B]
```

Or as a table:

| From State | Event | To State | Guards |
| ---------- | ----- | -------- | ------ |

## 9. Non-Functional Requirements [System / Feature Name]

[For non-functional requirements, for example performance thresholds, availability needs, security classifications.]

### 1. Performance & Responsiveness

| Requirement ID | Description          | Target      | Measure                                       |
| -------------- | -------------------- | ----------- | --------------------------------------------- |
| NFR-PERF-01    | API Response Time    | p95 < 200ms | Measured at the API gateway under normal load |
| NFR-PERF-02    | Page Load Time (TTI) | < 2.0s      | Measured on 3G network / Mobile device        |
| NFR-PERF-03    | Batch Processing     | < 1 hour    | Time to process 1M daily records              |

### 2. Scalability & Throughput

| Requirement ID | Description        | Target     | Measure                                      |
| -------------- | ------------------ | ---------- | -------------------------------------------- |
| NFR-SCAL-01    | Concurrent Users   | 5,000      | Number of active websocket connections       |
| NFR-SCAL-02    | Request Throughput | 500 RPS    | Peak requests per second                     |
| NFR-SCAL-03    | Data Growth        | 50GB/month | Expected database storage growth             |
| NFR-SCAL-04    | Elasticity         | < 5 mins   | Time to scale up new instances automatically |

### 3. Availability & Reliability

| Requirement ID | Description         | Target    | Measure                                     |
| -------------- | ------------------- | --------- | ------------------------------------------- |
| NFR-AVAIL-01   | Uptime (SLO)        | 99.9%     | 43.8 minutes downtime allowed per month     |
| NFR-AVAIL-02   | RPO (Data Loss)     | < 1 hour  | Maximum acceptable data loss in disaster    |
| NFR-AVAIL-03   | RTO (Recovery Time) | < 4 hours | Maximum time to restore service from backup |
| NFR-AVAIL-04   | Fault Tolerance     | Yes       | System remains operational if one AZ fails  |

### 5. Usability & Accessibility

| Requirement ID | Description    | Target                                                    |
| -------------- | -------------- | --------------------------------------------------------- |
| NFR-UX-01      | Accessibility  | WCAG 2.1 Level AA compliance                              |
| NFR-UX-02      | Device Support | iOS 15+, Android 12+, latest 2 versions of major browsers |
| NFR-UX-03      | Localization   | UI must support English, Spanish, and French              |

### 6. Maintainability & Operability

| Requirement ID | Description   | Target                                                         |
| -------------- | ------------- | -------------------------------------------------------------- |
| NFR-OPS-01     | Observability | All services must export metrics to Prometheus and logs to ELK |
| NFR-OPS-02     | Deployability | Zero-downtime deployments via CI/CD pipeline                   |
| NFR-OPS-03     | Test Coverage | > 80% line coverage for new backend code                       |

## 10. Assumptions & Constraints

| #   | Type       | Detail    |
| --- | ---------- | --------- |
| A-1 | Assumption | [assumed] |
| C-1 | Constraint |           |

## 11. Open Issues

- [ ] [Question or decision needed before this spec can be finalized]

## Appendix: Glossary

| Term | Definition |
| ---- | ---------- |
````

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
