---
name: writer-adr
description: >
  Produces an Architecture Decision Record (ADR) documenting the context, options considered, decision made,
  and consequences of a significant architectural or technical choice. Use this skill whenever the user wants
  to document a technical decision, write an ADR, record an architecture choice, capture why something was
  built a certain way, or asks to "write an ADR for this decision", "document why we chose X over Y",
  "create an architecture decision record", "record this tech choice", or "document the trade-offs we made".
  Also trigger when someone says "we decided to use X" and wants to capture the reasoning, or when reviewing
  past decisions that have no documentation. Distinct from design-arch (full system design) and writer-spec-tech
  (full technical specification).
---

# writer-adr

Produce an **Architecture Decision Record (ADR)** documenting the context, options considered, decision, and consequences.

## What makes a great ADR

ADRs capture *why* a decision was made at a specific point in time — the forces, constraints, and trade-offs that were present. They let future engineers understand decisions without re-litigating them, and know *when to revisit* them as those forces change.

A good ADR is a snapshot in time. It's OK for it to be "wrong" later — that's why you write a new ADR to supersede it.

## Information gathering

From context, identify:
- **What was decided**: The specific technical or architectural choice
- **Why it was needed**: The problem or requirement that forced a decision
- **Options considered**: What else was evaluated
- **Forces**: Constraints, requirements, or priorities that shaped the decision (timeline, team skill, cost, scale)
- **Status**: Is this a decision already made, or one being proposed?

If the user only describes the decision without the rationale, ask once: "What other options did you consider, and what made you choose this one?"

## ADR numbering

Check the project for existing ADR numbering convention:
- If `docs/adr/` or `docs/decisions/` exists: use the next sequential number
- Default format: `ADR-NNN` (e.g., `ADR-001`, `ADR-042`)
- File naming: `NNN-short-title-with-dashes.md`

## Output format

Always produce a Markdown document. Use this structure:

```markdown
# ADR-[NNN]: [Short, imperative title — e.g., "Use PostgreSQL as primary database"]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

**Date:** [YYYY-MM-DD]
**Deciders:** [Names or roles — e.g., "Backend team", "@alice, @bob"]
**Technical area:** [Database | Auth | Architecture | Frontend | DevOps | etc.]

---

## Context

[2–4 paragraphs describing the situation that made a decision necessary.
What problem needed solving? What requirements or constraints existed?
What forces were at play — team size, timeline, performance needs, budget?
Write in past tense if the decision has been made, present tense if proposed.]

## Decision Drivers

- [Key requirement or constraint that influenced the decision]
- [Another driver — e.g., "Must support horizontal scaling", "Team has no Go experience"]
- [Priority or quality attribute — e.g., "Operational simplicity prioritized over raw performance"]

## Options Considered

### Option 1: [Name]
[Brief description of the option]

**Pros:**
- [Advantage]
- [Advantage]

**Cons:**
- [Disadvantage]
- [Risk or concern]

### Option 2: [Name]
[Brief description]

**Pros:**
- [Advantage]

**Cons:**
- [Disadvantage]

[Repeat for each option considered. 2–4 options is typical.]

## Decision

**We will [chosen option].**

[1–3 paragraphs explaining the reasoning. Which decision drivers made this the winner?
What was sacrificed? What risks are accepted?]

## Consequences

### Positive
- [Benefit that will result]
- [Another benefit]

### Negative / Risks
- [Downside or risk accepted]
- [Technical debt introduced, if any]

### Neutral
- [Side effects that are neither good nor bad but worth noting]

## Implementation Notes
[Optional: specific steps, migration path, or considerations for implementation.
Omit if the decision is purely architectural with no immediate implementation impact.]

## Revisit Conditions
[Under what circumstances should this decision be revisited?
e.g., "If we need to support >1M concurrent users", "If the team grows beyond 20 engineers"]

## References
- [Link to relevant benchmark, article, or discussion]
- [Link to related ADR(s)]
```

## ADR writing guidance

**Context matters most.** Future readers will understand the decision if they understand the context. Spend more words on why the decision was needed than on what was decided.

**Make the trade-offs explicit.** Every architectural decision involves accepting downsides. Name them. "We chose X knowing it means Y" is more honest and more useful than pretending X was purely superior.

**Options don't have to be symmetric.** Sometimes one option was a serious contender and others were quickly eliminated. Reflect that reality rather than giving every option equal page time.

**Status lifecycle:**
- `Proposed` → being considered, not yet decided
- `Accepted` → decision made and active
- `Deprecated` → no longer relevant (system evolved)
- `Superseded by ADR-XXX` → a new decision replaced this one

## Example

**Input:** "We decided to use Redis for session storage instead of PostgreSQL because we needed sub-millisecond reads and didn't want session data taking up database connections."

**Output title:** `ADR-007: Store user sessions in Redis instead of PostgreSQL`

**Key points to cover:**
- Context: Growing user base causing connection pool saturation; session reads on every request
- Options: PostgreSQL sessions (current), Redis, cookie-based sessions
- Decision: Redis
- Consequences: Added infrastructure dependency, but freed DB connections, faster auth middleware
