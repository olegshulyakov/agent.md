---
name: audit-gap
description: >
  Produces a gap analysis report comparing current state vs target state with a prioritized remediation list.
  Use this skill whenever the user wants to perform a gap analysis, assess the distance between where they are
  and where they want to be, identify missing capabilities, analyze what needs to change to reach a goal state,
  or asks to "do a gap analysis", "what's the gap between current and target state", "compare our current system
  to requirements", "identify missing features", "assess readiness for X", or "what do we need to get from A to B".
  Also trigger for capability assessments, maturity model evaluations, compliance readiness reviews, and any
  structured current-state vs future-state comparison. Distinct from audit-security (security focus) and
  writer-spec-functional (defines requirements, doesn't compare states).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# audit-gap

Produce a **gap analysis report** that clearly maps current state to target state and gives a prioritized remediation list.

## What makes a great gap analysis

A gap analysis is most useful when it's honest and specific. Vague descriptions like "the process is inefficient" are less valuable than "step 3 of the onboarding flow has no error handling — 40% of failed signups happen here." Quantify gaps where possible and make the remediation actionable.

## Information gathering

From context, identify:
- **Scope**: What system, process, or domain is being analyzed?
- **Current state**: What exists today? (from code, docs, user description)
- **Target state**: What should exist? (from requirements, standards, goals, or user intent)
- **Constraints**: Time, budget, team size, technical debt?
- **Audience**: Executive summary vs. engineering action plan?

Work with what's provided. Mark assumptions `[assumed]`. If target state is implicit (e.g., "be GDPR compliant"), derive it from the relevant standard.

## Output format

```markdown
# Gap Analysis: [Domain / System Name]

**Date:** [date]
**Analyst:** [name if known, else omit]
**Scope:** [What was assessed]
**Target State:** [Standard, goal, or reference architecture being compared against]

---

## Executive Summary

[3–5 sentences: What was assessed, the overall gap severity, and the top 2–3 priorities. Written for a non-technical stakeholder.]

**Overall Readiness:** [Red / Amber / Green]

---

## Current State

[Describe what exists today. Be specific. Use bullet lists or a brief paragraph per area. Cite evidence (files, docs, interviews) where available.]

## Target State

[Describe the goal. Reference the standard, spec, or aspirational architecture. Be specific enough that gaps are measurable.]

---

## Gap Summary Table

| Area | Current State | Target State | Gap Severity | Effort | Priority |
|------|--------------|-------------|-------------|--------|----------|
| [Area] | [What exists] | [What's needed] | 🔴 Critical / 🟠 High / 🟡 Medium / ⚪ Low | S/M/L/XL | P1/P2/P3 |

---

## Detailed Gap Analysis

### [Area 1]

**Current:** [Specific description of what exists]
**Target:** [Specific description of what's required]
**Gap:** [What's missing or misaligned]
**Root Cause:** [Why the gap exists — design decision, technical debt, resource constraint, etc.]
**Impact:** [What happens if not addressed — user impact, risk, compliance exposure]

### [Area 2]
[Repeat pattern]

---

## Remediation Roadmap

### Immediate (P1 — must fix, high impact / low effort or risk)

- [ ] **[Action]** — [Specific step, who does it, success criterion]
- [ ] **[Action]** — [...]

### Short-Term (P2 — fix this quarter)

- [ ] **[Action]** — [...]

### Medium-Term (P3 — next 6 months)

- [ ] **[Action]** — [...]

### Long-Term / Accepted Risk (P4 — won't fix now, rationale documented)

- [ ] **[Action]** — [Rationale for deferral]

---

## Effort vs Impact Matrix

| Gap | Effort | Impact | Recommendation |
|-----|--------|--------|----------------|
| [Gap name] | Low/Med/High | Low/Med/High | Quick win / Plan / Defer / Accept |

---

## Risks of Not Acting

[List the top risks if the identified gaps are not addressed — regulatory, security, operational, competitive.]

## Assumptions & Limitations

- [What was assumed because data was unavailable]
- [What was out of scope and why]

## Next Steps

1. [Immediate next action with owner]
2. [Follow-up review date]
```

## Calibration

- **Compliance gap analysis** (e.g., GDPR, SOC2): Derive target state from the relevant standard's controls; map each control to a pass/fail with evidence
- **Architecture gap analysis**: Focus on system components, data flows, non-functional attributes
- **Process gap analysis**: Map workflow steps; identify missing steps, bottlenecks, or ownership gaps
- **Feature gap analysis** (against competitor or spec): Use the spec as target state; identify missing/partial/wrong behavior
- **Terse input**: Generate a lean report covering the top 3–5 gaps with clear remediation steps
- **Detailed input**: Full report with all sections including effort/impact matrix
