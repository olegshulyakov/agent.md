---
name: writer-backlog
description: >
  Produces a groomed product backlog with prioritized, sized, and dependency-flagged user stories.
  Use this skill whenever the user wants to create or groom a product backlog, organize stories by
  priority, size backlog items, map story dependencies, or asks to "groom our backlog", "create a
  product backlog", "prioritize these stories", "write a groomed backlog", "help me organize our
  backlog", "size these user stories", "create a backlog from these requirements", or "which stories
  should we do first?". Also trigger for "RICE scoring", "story mapping", "backlog refinement",
  "MoSCoW prioritization", and "backlog ordering". Distinct from planner-sprint (which allocates
  stories to a specific sprint) and writer-story-task (which decomposes a single story into tasks).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# writer-backlog

Produce a **groomed product backlog** with prioritized, sized, and dependency-mapped user stories.

## What makes a great backlog

A backlog is a prioritized bet sheet, not a wishlist. The best backlogs are ruthlessly ordered — the team should always know exactly what the highest-value thing to do next is. Items near the top are detailed and ready to develop; items further down can be sketchy. Stories should be independent where possible; dependencies should be surfaced and managed, not hidden.

## Information gathering

From context, identify:
- **Product context**: What's being built? Who are the users?
- **Raw requirements**: Features, requests, bugs, or ideas to organize
- **Prioritization inputs**: Business goals, OKRs, user research, effort estimates?
- **Team velocity**: How many points per sprint? (helps right-size the backlog view)
- **Constraints**: Technical dependencies, third-party dependencies, regulatory requirements?

## Prioritization framework

Default: **Value vs Effort** (simple, effective). Offer alternatives:

| Framework | Best for | How it works |
|-----------|----------|-------------|
| **Value / Effort** | General backlog ordering | High value + low effort = do first |
| **RICE** | Data-driven teams | Reach × Impact × Confidence / Effort |
| **MoSCoW** | Scope management | Must have / Should have / Could have / Won't have |
| **Kano** | User satisfaction | Classify: basic, performance, delighter |
| **Story mapping** | User journey visualization | Map stories across user activities |

## Output format

```markdown
# Product Backlog: [Product / Feature Area]

**Last groomed:** [date]
**Product Owner:** [name]
**Team:** [name]
**Sprint length:** [2 weeks]
**Team velocity:** ~[N] points/sprint

---

## Backlog Summary

| Priority tier | Stories | Total points | Sprints needed |
|--------------|---------|-------------|----------------|
| 🔴 Must Have (P1) | [N] | [N] | [N] |
| 🟠 Should Have (P2) | [N] | [N] | [N] |
| 🟡 Could Have (P3) | [N] | [N] | [N] |
| ⚪ Won't Have (this cycle) | [N] | — | — |

---

## Prioritized Backlog

### 🔴 P1 — Must Have (Next 1–2 Sprints)

*These are the highest-value, ready-to-develop stories. Team should start here.*

---

#### [1] [Story title]

**As a** [user type]
**I want to** [action]
**So that** [benefit]

| Field | Value |
|-------|-------|
| **Ticket** | [PROJ-XXX] |
| **Points** | [N] |
| **Value** | 🔴 High — [brief rationale, e.g., "blocks checkout flow"] |
| **Effort** | 🟡 Medium |
| **Risk** | Low |
| **Dependencies** | [None / Blocks: #XX / Blocked by: #XX] |
| **Status** | Ready for development |

**Acceptance criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Notes:** [Design link, technical notes, clarifications needed]

---

#### [2] [Story title]

[Repeat pattern for each P1 story]

---

### 🟠 P2 — Should Have (Next 3–4 Sprints)

*Important but not blocking. Will be refined before they reach the top.*

| # | Story | Points | Dependencies | Notes |
|---|-------|--------|-------------|-------|
| 3 | As a [user], I want to [action] | [N] | — | [Brief note] |
| 4 | As a [user], I want to [action] | [N] | After #2 | |
| 5 | As a [user], I want to [action] | [N] | — | Needs UX design |

---

### 🟡 P3 — Could Have (Backlog)

*Nice to have. Needs more refinement before committing. May be deferred.*

| # | Story | Rough Size | Notes |
|---|-------|-----------|-------|
| 6 | [Idea / rough story] | L | [Why it's P3] |
| 7 | [Idea] | XL | Requires research spike first |

---

### ⚪ Won't Have (This Cycle)

*Explicitly de-prioritized. Documented so we don't forget why.*

| Story | Why deferred |
|-------|-------------|
| [Feature idea] | [Reason — e.g., "Not validated by user research", "Deferred to Q3"] |

---

## Dependency Map

```
[Story 1] (P1)
    └── blocks → [Story 3] (P2)
    
[Story 2] (P1)
    └── blocks → [Story 4] (P2)
                    └── blocks → [Story 6] (P3)

[Story 5] (P2) — independent
```

---

## Technical Debt & Enablers

| Item | Priority | Points | Business impact | Notes |
|------|----------|--------|----------------|-------|
| [Tech debt item] | P2 | [N] | Enables faster feature dev in area X | |
| [Infrastructure story] | P1 | [N] | Unblocks [feature] | |

---

## Backlog Health Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Stories ready for development (top 10) | [N] | ≥ 10 (2 sprints ahead) |
| Average story age (not yet started) | [N weeks] | < 3 months |
| % stories with acceptance criteria | [%] | ≥ 100% for P1 |
| % stories with estimates | [%] | ≥ 100% for P1/P2 |

---

## Refinement Notes

*From the last grooming session:*
- [Decision: moved story X from P1 to P2 because Y]
- [Open question: story N needs UX design before we can size it]
- [New discovery: story M is larger than estimated; split into M1 + M2]

---

## Next Grooming Session

**Date:** [next session date]
**Focus areas:** [What to review next time]
- [ ] Size stories [N–N]
- [ ] Resolve dependency question on story [N]
- [ ] Review user research for [P3 area]
```

## RICE scoring (alternative)

When the user wants data-driven prioritization:

```markdown
## RICE Scoring

| Story | Reach (users/qtr) | Impact (1–3) | Confidence (%) | Effort (wks) | RICE Score |
|-------|------------------|-------------|----------------|--------------|------------|
| [Story] | 5000 | 3 | 80% | 2 | 6000 |
| [Story] | 200 | 3 | 90% | 0.5 | 1080 |

RICE = (Reach × Impact × Confidence) / Effort
Higher score = higher priority
```

## Calibration

- **Terse input (list of features)**: Organize into user stories; size roughly; MoSCoW prioritize based on reasonable business assumptions
- **Detailed input with goals/OKRs**: Apply RICE or explicit value scoring
- **Re-grooming existing backlog**: Focus on ordering changes, new dependencies, and size updates
- **Sprint planning prep**: Output just the top 10 stories in sprint-ready detail
