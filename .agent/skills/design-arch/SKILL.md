---
name: design-arch
description: >
  Produces a system design document with components, interactions, data flows, and architectural trade-offs.
  Use this skill whenever the user wants to design a system, document an architecture, evaluate architectural
  options, or asks to "design this system", "what's the architecture for X", "document the architecture",
  "help me design the backend", "choose between microservices and monolith", or "how should this system be
  structured". Also trigger for system decomposition, service boundary design, and architecture discussions.
  Distinct from diagram-c4 (visual C4 diagram) and writer-adr (records a single specific decision).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# design-arch

Produce a **system design document** describing components, their interactions, data flows, and the trade-offs behind key architectural decisions.

## What makes a great architecture document

The best architecture docs communicate *why* not just *what*. They explain the forces that shaped the design, present options considered, and articulate trade-offs. They give a new engineer enough context to understand and maintain the system.

## Information gathering

From context, identify:
- **System purpose**: What problem does this system solve?
- **Scale**: Expected load, data volume, user count (now and projected)
- **Constraints**: Team size, existing codebase, technology lock-in
- **Quality attributes**: Latency, availability, consistency, security priorities
- **Integration**: External systems, third-party APIs, existing services

Make reasonable assumptions for unspecified attributes; mark them `[assumed]`.

## Output format

```markdown
# Architecture: [System Name]

## Status
[Draft | Reviewed | Approved] — [Date]

## Context
[2–4 paragraphs: What is this system? What problem? Who uses it? Key constraints?]

## Quality Attributes

| Attribute | Requirement | Priority |
|-----------|-------------|----------|
| Availability | 99.9% uptime | High |
| Latency | p99 < 200ms | High |
| Scalability | 10x current load | Medium |

## System Overview
[High-level narrative. Mermaid or ASCII diagram of major components.]

## Components

### [Component Name]
- **Responsibility:** [Single sentence]
- **Technology:** [Language, framework, DB]
- **Interfaces:** [APIs exposed, events published]
- **Dependencies:** [Other components / external services]

[Repeat for each component]

## Data Architecture
[Key entities, data flows, storage choices with rationale]

| Store | Technology | Data | Rationale |
|-------|------------|------|-----------|

## Key Decisions

### Decision: [Title]
- **Options:** [A vs B vs C]
- **Chosen:** [What]
- **Rationale:** [Why]
- **Trade-offs:** [What was sacrificed]

[2–4 decisions]

## Integration Points

| System | Direction | Protocol | Data |
|--------|-----------|----------|------|

## Security, Observability, Resilience
[Auth/authz, metrics/logging/tracing, failure modes and mitigations]

## Deployment
[Cloud, containers, regions, environments]

## Open Questions
- [ ] [Unresolved issue]
```

## Architecture pattern reference

| Pattern | Use when |
|---------|----------|
| Monolith | Small team, early stage, simple deployment |
| Modular monolith | Growing team, needs boundaries without distributed complexity |
| Microservices | Large teams, independent scaling, separate deployment cycles |
| Event-driven | Loose coupling, async processing, audit trail |
| CQRS | Read/write patterns differ, complex queries |
| BFF | Multiple clients with different data needs |
| API Gateway | Cross-cutting auth/rate-limiting across services |

## Calibration

- **Greenfield**: Cover all sections; make opinionated recommendations
- **Existing system**: Current state + problems + target state
- **Decision help**: Emphasize trade-offs; recommend with rationale
- **Overview only**: Skip detailed data model; focus on components and decisions
