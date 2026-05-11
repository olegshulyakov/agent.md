---
name: writer-stakeholder
description: >
  Produces a stakeholder update report with status, key achievements, risks, and decisions needed.
  Use this skill whenever the user wants to write a project update, send a status report to
  leadership or stakeholders, communicate project risks, or asks to "write a stakeholder update",
  "create a weekly status report", "draft an update for the exec team", "summarize project status",
  or "write an email to stakeholders". Distinct from planner-sprint (which is for the engineering
  team) and writer-release-notes (which is for end users).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# writer-stakeholder

Produce a **Stakeholder Update** report summarizing status, achievements, risks, and blockers.

## Output format

```markdown
# Project Update: [Project Name]
**Date:** [date]
**Status:** 🟢 On Track / 🟡 At Risk / 🔴 Off Track
**Owner:** [name]

---

## 🚀 Executive Summary
[1-2 sentences summarizing the current state of the project. "We successfully completed X this week and are on track for the beta launch on [Date]."]

## ✅ Key Achievements (Since last update)
- **[Area 1]**: [What was accomplished — e.g., "Finished integrating the Stripe payment gateway in staging."]
- **[Area 2]**: [e.g., "Completed user testing sessions with 5 beta customers; feedback was highly positive regarding the new dashboard layout."]

## 🚧 Current Focus (Next 1-2 weeks)
- [What the team is working on right now — e.g., "Fixing critical bugs identified in user testing."]
- [e.g., "Finalizing the production database migration plan."]

## ⚠️ Risks & Blockers
- **[Risk 1]**: [Description — e.g., "Waiting on legal approval for the updated Terms of Service."]
  - *Mitigation/Ask*: [What are you doing about it, or what do you need? — e.g., "Need @[Name] to review by Friday to avoid launch delay."]
- **[Risk 2]**: [Description]

## 📅 Timeline Update
- [Milestone 1]: ✅ Completed on [Date]
- [Milestone 2]: 🔄 In Progress (Target: [Date])
- [Launch]: 🗓️ Scheduled for [Date]
```

## Guidelines for Stakeholder Updates

- **Keep it brief**: Executives skim. Use bullet points and bold text for scanning.
- **Be transparent about risks**: Don't hide bad news. Highlight risks early and present mitigation plans.
- **Clear asks**: If you need a stakeholder to make a decision or unblock the team, state it clearly in the "Risks & Blockers" section.
- **Audience awareness**: Avoid deep technical jargon unless the stakeholders are technical. Focus on business value and timeline impact.
