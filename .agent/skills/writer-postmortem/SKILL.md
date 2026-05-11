---
name: writer-postmortem
description: >
  Produces a blameless incident postmortem with timeline, root cause analysis, impact assessment, and
  action items. Use this skill whenever the user wants to write a postmortem, document an incident,
  analyze what went wrong in a production outage, create an incident report, or asks to "write a
  postmortem", "document this incident", "create an incident report", "blameless postmortem",
  "root cause analysis for the outage", "write up what happened during the incident", "5 Whys
  analysis", or "action items from the incident". Also trigger for "post-incident review",
  "incident retrospective", "outage report", and "service disruption analysis". Distinct from
  template-retro (which is for sprint retrospectives) and writer-runbook (which documents
  operational procedures).
---

# writer-postmortem

Produce a **blameless incident postmortem** with timeline, root cause analysis, impact, and action items.

## What makes a great postmortem

A great postmortem focuses on systemic failures, not individual mistakes. The goal is to understand how the system — processes, tooling, team structure, monitoring — allowed an incident to happen, and what changes will prevent recurrence. "The engineer made a mistake" is never an acceptable root cause. "The system allowed a single engineer's mistake to cascade into a production outage without alerting or circuit-breaking" is.

## Information gathering

From context, identify:
- **Incident**: Service affected, what happened, when?
- **Impact**: Users affected, revenue impact, SLO breach?
- **Timeline**: Key events with timestamps?
- **Root cause**: Known or still being investigated?
- **Responders**: Who detected, responded, resolved?

Work with what's provided. Mark unknown items `[TBD]`.

## Output format

```markdown
# Postmortem: [Brief Incident Title]

**Incident ID:** [INC-XXXX or ticket reference]
**Date:** [incident date]
**Written by:** [author(s)]
**Reviewed by:** [reviewers]
**Status:** [Draft / Review / Approved]
**Severity:** [SEV1 / SEV2 / SEV3]

---

## Summary

[3–5 sentences for a non-technical reader: What happened? What was the impact? What's the team doing to prevent recurrence?]

**Duration:** [X hours Y minutes] ([HH:MM UTC] → [HH:MM UTC])
**Services affected:** [List of services / endpoints / features]
**Users affected:** [N users / [X%] of traffic / all users in [region]]
**SLO breach:** [Yes — error budget consumed: X% / No]

---

## Impact

| Dimension | Details |
|-----------|---------|
| **User impact** | [e.g., "Users could not complete checkout for 2 hours 15 minutes"] |
| **Error rate** | [e.g., "100% 5xx on /api/orders for 45 minutes; partial degradation for remainder"] |
| **Revenue impact** | [e.g., "~$35,000 in lost GMV based on average order value × orders lost"] |
| **Data impact** | [e.g., "No data loss; 47 duplicate events generated (cleaned up)"] |
| **Regulatory** | [e.g., "None" or "SLA breach with enterprise customer — notification required"] |

---

## Timeline

*All times in UTC. [Timezone] local time shown in parentheses where helpful.*

| Time | Event |
|------|-------|
| **[HH:MM]** | [Causal event — e.g., "Deploy of v2.4.1 completed to production"] |
| **[HH:MM]** | [First symptom — e.g., "Error rate began rising; not yet above alert threshold"] |
| **[HH:MM]** | [Detection — e.g., "PagerDuty fired: 'High error rate on order-service' — [Name] acknowledged"] |
| **[HH:MM]** | [Response begins — e.g., "Incident bridge opened; [Name] and [Name] joined"] |
| **[HH:MM]** | [Investigation finding — e.g., "Identified new database connection pool exhaustion in order-service logs"] |
| **[HH:MM]** | [Hypothesis — e.g., "Suspected connection pool sizing regression in new deploy"] |
| **[HH:MM]** | [Mitigation attempt — e.g., "Rolled back v2.4.1 to v2.4.0"] |
| **[HH:MM]** | [Mitigation outcome — e.g., "Error rate returned to baseline; incident mitigated"] |
| **[HH:MM]** | [All-clear — e.g., "Monitoring confirmed stable for 30 min; incident closed"] |
| **[HH:MM]** | [Post-incident — e.g., "Postmortem drafted; stakeholders notified"] |

**Total time to detect (TTD):** [X minutes]
**Total time to mitigate (TTM):** [X hours Y minutes]
**Total time to resolve (TTR):** [X hours Y minutes]

---

## Root Cause Analysis

### What happened

[Technical description of the failure chain. Be specific: which service, which code path, which dependency. Enough detail that an engineer not on the incident can understand exactly what broke and how.]

### 5 Whys

Starting from the user-visible symptom:

1. **Why did users see errors?** → [order-service returned 500s when creating orders]
2. **Why did order-service return 500s?** → [Database connections were exhausted; new connections were refused]
3. **Why were database connections exhausted?** → [Connection pool was configured at 10 max connections; v2.4.1 introduced a N+1 query that used 5× more connections per request under load]
4. **Why was this N+1 not caught in testing?** → [Integration tests use a stub; no load test in CI; staging environment has 5% of production traffic]
5. **Why was there no alert for connection pool exhaustion?** → [No metric for DB connection pool usage; only error rate was monitored]

### Contributing factors

[List things that made the incident worse or delayed resolution]

- 🔴 **No connection pool metric / alert** — connection pool exhaustion was not detectable until service errors appeared
- 🟠 **N+1 query not caught by code review** — the query pattern change was subtle; no automated lint rule
- 🟠 **Staging traffic too low** — the issue only manifests at >100 RPS; staging runs at ~5 RPS
- 🟡 **Runbook not up to date** — responders had to rediscover rollback procedure; added 8 minutes

---

## What Went Well

[Be specific about what the team did right — this is as important as what went wrong. It reinforces good practices.]

- ✅ Alert fired within 3 minutes of user-visible impact (alert threshold working)
- ✅ Rollback decision was made quickly (12 minutes after incident opened)
- ✅ Communication was clear and calm throughout the incident bridge
- ✅ Status page updated promptly; reduced inbound support volume

---

## What Went Poorly

[Specific, factual observations — no blame]

- ❌ No connection pool saturation metric; we couldn't detect the root cause without log diving
- ❌ TTD was 22 minutes — should be < 5 minutes for a 100% error rate
- ❌ Rollback procedure was not in the runbook; responders had to find it in Slack history
- ❌ Stakeholders not notified until 1 hour in

---

## Where We Got Lucky

[What could have made this worse? What safeguards almost failed?]

- The N+1 regression only affected the orders endpoint; if it had been in auth, impact would have been total
- The deploy was made at 10 AM, not at peak traffic (18:00); impact was 3× lower than it could have been
- On-call engineer happened to be at their desk when the page fired; response would have taken longer otherwise

---

## Action Items

*Each action item must have: a specific owner, a target date, and a success criterion.*

| Priority | Action | Owner | Target | Status |
|----------|--------|-------|--------|--------|
| 🔴 P1 | Add DB connection pool utilization metric and alert (threshold: 80%) | [DevOps name] | [Date] | Open |
| 🔴 P1 | Add load test to CI for critical paths (>100 RPS against a staging clone) | [Engineering name] | [Date] | Open |
| 🟠 P2 | Update rollback runbook with step-by-step procedure; verify quarterly | [SRE name] | [Date] | Open |
| 🟠 P2 | Add N+1 query detection to code review checklist | [Engineering lead] | [Date] | Open |
| 🟡 P3 | Define stakeholder communication template and SLA (notify within 30 min for SEV1) | [Engineering lead] | [Date] | Open |

---

## Lessons Learned

[3–5 principles that this incident teaches — written as transferable lessons, not just this-specific fixes]

1. **Measure what can kill you**: If a resource (connection pool, thread pool, memory) can cause an outage, it needs a metric and an alert before the outage happens.
2. **Staging must experience production-like load**: A staging environment that runs at 5% traffic will miss 95% of load-related bugs. Use production traffic replay or traffic shadowing for critical deploys.
3. **Runbooks must be verified, not just written**: A runbook not executed in 6 months is likely stale. Schedule runbook verification as part of quarterly DR drills.

---

## Related Incidents

| Incident | Date | Relationship |
|----------|------|-------------|
| [INC-XXXX] | [date] | Similar root cause (DB pool exhaustion in different service) |
| [INC-XXXX] | [date] | Same alert fired; same rollback needed |
```

## Calibration

- **Immediate post-incident (while events are fresh)**: Fill timeline first; leave analysis sections for later
- **Draft for review**: Emphasize "What Went Well" as much as "What Went Poorly" — this is read by the whole team
- **Sensitive incident**: Focus on systemic factors; use "the system" not "the engineer"
- **No root cause yet**: Mark root cause as `[Investigation ongoing]`; still write timeline and impact
