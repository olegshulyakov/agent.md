---
name: writer-epic
description: >
  Produces an epic definition with goal, business value, scope, acceptance criteria, child user stories,
  and definition of done. Use this skill whenever the user wants to write an epic, define a feature grouping,
  create a large feature container, define the scope of a major initiative, or asks to "write an epic for X",
  "define this feature as an epic", "create an epic", "break this initiative into an epic and stories",
  or "write the epic definition for this feature". Also trigger for "epic breakdown", "what stories are in
  this epic", and "define the MVP scope for this epic". Distinct from writer-story-task (single story →
  tasks) and writer-prd (business-level requirements document).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# writer-epic

Produce a **complete epic definition** with goal, value, scope, child stories, acceptance criteria, and definition of done.

## What makes a great epic

An epic is a container for related user stories that together deliver meaningful business value. It should be small enough to complete within 1–3 sprints (not a quarter-long initiative) but large enough to be worth naming as a cohesive unit. The best epics have a clear "what success looks like" that the whole team can point to.

## Information gathering

From context, identify:
- **The feature or initiative**: What is being built?
- **Business value**: Why does this matter? Who benefits and how?
- **Scope**: What's included? What's explicitly excluded?
- **Audience/persona**: Who are the primary users?
- **Timeline or milestone**: Is there a deadline or release window?

Work with what's provided. Infer child stories from the feature description if not listed. Mark assumptions `[assumed]`.

## Output format

```markdown
# Epic: [Feature Name]

## Summary
[One sentence: What this epic delivers and for whom.]

## Status
[Draft | Defined | In Progress | Done]
**Created:** [date]
**Target release:** [version or date, if known]
**Priority:** [Critical | High | Medium | Low]

---

## Goal
[2–3 sentences: What outcome does this epic achieve? What does success look like from a user or business perspective?]

## Business Value
| Stakeholder | Value Delivered |
|-------------|----------------|
| [User type] | [Specific benefit — e.g., "Can complete checkout 40% faster"] |
| [Business] | [Metric impact — e.g., "Reduces abandonment at payment step"] |

## Hypothesis *(optional)*
**We believe that** [feature]  
**will result in** [outcome]  
**as measured by** [metric]

---

## Scope

### In Scope
- [Concrete capability]
- [Another capability]

### Out of Scope
- [Explicit exclusion — prevents scope creep]
- [Deferred to future epic]

---

## Child Stories

| # | Story | Priority | Points | Notes |
|---|-------|----------|--------|-------|
| 1 | As a [user], I want to [action] so that [benefit] | High | [?] | |
| 2 | As a [user], I want to [action] so that [benefit] | High | [?] | |
| 3 | As a [user], I want to [action] so that [benefit] | Medium | [?] | |

*For full story breakdown with acceptance criteria and tasks, use the `writer-story-task` skill on individual stories.*

---

## Acceptance Criteria (Epic-level)

These define when the epic as a whole is complete:

- [ ] [Functional criterion — e.g., "Users can complete checkout using a saved payment method"]
- [ ] [Quality criterion — e.g., "Checkout flow completes in < 3 seconds at p95"]
- [ ] [Coverage criterion — e.g., "E2E tests cover the happy path and the main error scenarios"]
- [ ] [Observability criterion — e.g., "Metrics dashboard shows conversion rate by step"]

---

## Definition of Done

- [ ] All child stories meet their individual DoD
- [ ] Feature flags removed (or documented if kept)
- [ ] Analytics / telemetry in place for success metrics
- [ ] Documentation updated (API docs, user-facing help, runbook)
- [ ] Security review completed for any new data handling
- [ ] Performance verified against thresholds
- [ ] Accessibility reviewed (WCAG AA for any new UI)

---

## Dependencies

| Dependency | Type | Owner | Risk |
|------------|------|-------|------|
| [Team/system] | Blocks / Informs | [Owner] | [High/Med/Low] |

## Risks & Open Questions

| Risk / Question | Impact | Status |
|-----------------|--------|--------|
| [Risk description] | [What happens if it materializes] | Open / Mitigated |
| [ ] [Open question to resolve before starting] | | |

---

## Mockups / Design Links
[Links to Figma, screenshots, or diagrams — omit section if none]

## References
[Related PRD, ADRs, previous epics, or background docs]
```

## Story breakdown guidance

When generating child stories, use these patterns:

**Happy path first:**
- Core CRUD for the primary entity
- The critical user journey end-to-end

**Then edge cases and non-primary users:**
- Error states and recovery
- Admin/power user workflows
- Mobile or alternative surface

**Then non-functional:**
- Performance / load handling
- Observability and monitoring
- Security controls

## Epic sizing calibration

- **Too large**: Epic can't be completed in 1–3 sprints → split into multiple epics
- **Too small**: Only 1–2 stories → probably just a story, not an epic
- **Right size**: 3–8 stories that cohesively deliver a named, demoable feature

## Calibration by input

- **Terse prompt**: Generate a lean epic with 3–5 stories; mark scope assumptions clearly
- **Detailed prompt**: Full epic with 6–10 stories, detailed scope, and risk section
- **Existing PRD**: Extract one epic from the PRD; align stories to functional requirements
