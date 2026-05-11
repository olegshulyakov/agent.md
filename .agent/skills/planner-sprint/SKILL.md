---
name: planner-sprint
description: >
  Produces a sprint plan with sprint goal, story allocation, capacity calculation, and impediment log.
  Use this skill whenever the user wants to plan a sprint, allocate stories to a sprint, calculate sprint
  capacity, set a sprint goal, prepare for sprint planning, or asks to "plan our sprint", "create a sprint
  plan", "help me with sprint planning", "allocate these stories to the sprint", "what's our sprint
  capacity", "create a sprint goal", or "write up the sprint plan". Also trigger for "sprint 1 planning",
  "two-week sprint", "capacity planning for the team", and "sprint backlog". Distinct from writer-epic
  (which defines feature groupings) and writer-story-task (which decomposes individual stories into tasks).
---

# planner-sprint

Produce a **sprint plan** with sprint goal, capacity, story allocation, and impediment tracking.

## What makes a great sprint plan

A sprint plan exists to align the team on what they're committing to and why. The sprint goal should be a single outcome statement that makes it obvious whether the sprint succeeded — not a laundry list of stories. Capacity should be honest (accounting for meetings, leave, and context switching), and the story allocation should reflect both the goal and the capacity.

## Information gathering

From context, identify:
- **Sprint number and dates**: Sprint N, start/end date
- **Team composition**: Names, roles, capacity (days or story points per person)
- **Velocity**: Historical story points per sprint (average, or recent trend)
- **Candidate stories**: Backlog items proposed for this sprint
- **Dependencies**: Stories that block or are blocked by others
- **Impediments**: Known blockers, risks, or concerns going into the sprint

Work with what's provided. Infer reasonable capacity if not given (e.g., 2-week sprint → 8 working days per person, minus 20% for overhead = ~6.5 effective days).

## Output format

```markdown
# Sprint [N] Plan

**Sprint dates:** [Start date] → [End date]
**Sprint duration:** [X weeks]
**Planning date:** [date]
**Team:** [Team name]

---

## Sprint Goal

> [One sentence outcome statement — what does the team deliver as a cohesive unit?]
>
> Success criteria: [How will we know this goal was met by end of sprint?]

*The sprint goal captures intent, not a story list. If we deliver the goal stories but the feature isn't working end-to-end, we haven't met the goal.*

---

## Team Capacity

| Team Member | Role | Available Days | Capacity Factor | Effective Capacity |
|-------------|------|---------------|----------------|-------------------|
| [Name] | Backend Dev | [X] | [e.g., 0.8 — 20% for meetings] | [Y] days / [Z] pts |
| [Name] | Frontend Dev | [X] | [0.8] | [Y] days / [Z] pts |
| [Name] | QA / AQA | [X] | [0.8] | [Y] days / [Z] pts |
| **Total** | | [X] | | **[Total] pts** |

**Notes:**
- [Name] is OOO [dates] — [X] days leave
- [Sprint ceremony overhead: planning, daily standups, retro, review = ~N hours]
- Target velocity: [N] points (based on [last N sprints] average: [X, Y, Z])

---

## Committed Stories

Stories the team is committing to deliver this sprint (sorted by priority):

| Priority | Story | Points | Owner | Goal? | Dependencies |
|----------|-------|--------|-------|-------|-------------|
| 1 | [Story title — link to ticket] | [N] | [Name] | ✅ | — |
| 2 | [Story title] | [N] | [Name] | ✅ | #123 |
| 3 | [Story title] | [N] | [Name] | — | — |
| 4 | [Story title — stretch] | [N] | [Name] | — | — |

**Total committed:** [N] points
**Stretch stories:** [N] points
**Total capacity:** [N] points

**Stories marked ✅ under Goal are sprint goal stories — these take priority if capacity is squeezed.**

---

## Story Details

### [Story 1 Title]
**Ticket:** [#123 or link]
**Points:** [N]
**Owner:** [Name]
**Goal story:** [Yes/No]

**Summary:** [1–2 sentences on what this story delivers]

**Key tasks:**
- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]

**Acceptance criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Dependencies / blockers:** [None / "Blocked by: #XXX — [Name] to resolve by [date]"]

---

### [Story 2 Title]
[Repeat pattern]

---

## Stretch Goals

If committed work is completed early:

| Story | Points | Notes |
|-------|--------|-------|
| [Story title] | [N] | [Why it's stretch — not goal-critical] |

---

## Impediments & Risks

| # | Impediment / Risk | Impact | Owner | Target Resolution |
|---|-------------------|--------|-------|-------------------|
| 1 | [Description of blocker] | [High/Med/Low] | [Name] | [Date] |
| 2 | [Tech debt that might slow story X] | Medium | [Name] | — |

**Escalations needed:**
- [Any impediment that requires management/stakeholder action]

---

## Definition of Done (Sprint Level)

A story is done when:
- [ ] All acceptance criteria met
- [ ] Code reviewed and approved
- [ ] Unit + integration tests written and passing
- [ ] QA sign-off obtained
- [ ] Documentation updated (if API or user-facing change)
- [ ] Deployed to staging

A sprint is done when:
- [ ] All sprint goal stories meet DoD
- [ ] Sprint review demo is ready
- [ ] Backlog updated with any new items discovered

---

## Sprint Events

| Event | Date | Duration | Owner |
|-------|------|----------|-------|
| Sprint Planning | [date] | [X] hours | Scrum Master |
| Daily Standup | Every day, [time] | 15 min | Team |
| Sprint Review | [date] | [X] hours | Product Owner |
| Sprint Retrospective | [date] | [X] hours | Scrum Master |

---

## Notes & Decisions

- [Any decisions made during planning — e.g., "Moved story #X to next sprint due to dependency on #Y"]
- [Technical approach decisions — e.g., "Agreed to use existing auth service rather than build new one"]
```

## Calibration

- **Minimal input (just stories)**: Generate capacity from typical defaults; create a sprint goal from the story themes
- **Detailed team info**: Full capacity table with individual breakdowns
- **Impediment-heavy sprint**: Expand impediment section; flag risk to sprint goal explicitly
- **No story points**: Use T-shirt sizes or count of stories; note velocity basis
- **Re-planning mid-sprint**: Omit capacity section; focus on what's in/out and revised goal
