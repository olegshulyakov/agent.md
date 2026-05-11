---
name: writer-slo
description: >
  Produces SLO definitions with SLI metrics, targets, error budgets, alerting policy, and review
  cadence. Use this skill whenever the user wants to define service level objectives, create SLOs for
  a service, define error budgets, document reliability targets, or asks to "write an SLO", "define
  our service level objectives", "create an error budget policy", "what SLO should we set for this
  service", "define our SLIs and SLOs", "write a reliability target document", "set up error budget
  alerts", or "define our uptime goals". Also trigger for "SLI definition", "availability target",
  "reliability engineering", "error budget burn rate", and "SLO review". Distinct from writer-alert-rules
  (which writes the alert rule syntax) and writer-runbook-oncall (which documents alert responses).
---

# writer-slo

Produce **SLO definitions** with SLI metrics, targets, error budgets, and alerting policy.

## SLO concepts

- **SLI** (Service Level Indicator): A metric that measures the quality of a service (e.g., request success rate)
- **SLO** (Service Level Objective): A target value or range for an SLI (e.g., 99.9% success rate)
- **SLA** (Service Level Agreement): A contractual commitment, usually a subset of SLOs
- **Error budget**: The allowed amount of unreliability = 1 - SLO (e.g., 99.9% SLO → 0.1% error budget = 43.8 min/month)

## SLI categories

| Category | Measures | Common SLIs |
|----------|----------|-------------|
| **Availability** | Is the service up? | `success_rate = successful_requests / total_requests` |
| **Latency** | Is it fast? | `p95_latency`, `p99_latency`, `% requests < threshold` |
| **Throughput** | Can it handle load? | `requests_per_second`, `events_processed_per_minute` |
| **Quality** | Is the output correct? | `% orders processed correctly`, `% results relevant` |
| **Freshness** | Is data up-to-date? | `% data updated within threshold`, `max data lag` |

## Information gathering

From context, identify:
- **Service**: What service is this SLO for?
- **User journey**: What are users trying to do? (The SLO should measure their experience)
- **Current performance**: What does today's data look like?
- **Reliability goal**: How critical is this service? (Criticality → aspirational availability)
- **Dependencies**: What uptime can the service realistically achieve given its dependencies?

## Availability target guide

| Service type | Suggested SLO | Error budget/month | Notes |
|-------------|--------------|-------------------|-------|
| Internal tool | 99% | 7.2 hours | Lower cost of downtime |
| Customer-facing, non-critical | 99.5% | 3.6 hours | |
| Core customer experience | 99.9% | 43.2 minutes | |
| Revenue-critical path | 99.95% | 21.6 minutes | |
| Infrastructure foundation | 99.99% | 4.3 minutes | Very expensive to maintain |

**Don't set SLOs higher than you can measure or achieve with your current infrastructure.**

## Output format

```markdown
# Service Level Objectives: [Service Name]

**Service:** [service-name]
**Owner:** [team]
**Created:** [date]
**Review cadence:** [Monthly / Quarterly]
**Next review:** [date]

---

## Context

[2–3 sentences: What does this service do? Who uses it? Why does reliability matter here?]

**User journey:** [The critical user action this SLO protects — e.g., "Users can complete checkout and receive an order confirmation"]

---

## SLO Definitions

### SLO 1: Availability

**SLI:** Proportion of valid requests that receive a successful response (non-5xx HTTP, or service-specific success criteria).

```promql
# SLI measurement (Prometheus)
sum(rate(http_requests_total{job="[service]", status!~"5.."}[5m]))
/
sum(rate(http_requests_total{job="[service]"}[5m]))
```

| Window | Target | Error Budget |
|--------|--------|-------------|
| Rolling 30 days | **99.9%** | 43.2 minutes per month |
| Rolling 7 days | 99.5% | 50.4 minutes per week (for fast alerting) |

**What counts as a valid request:** [All requests to /api/v2/*, excluding health check endpoints and requests with invalid auth tokens]

**What counts as a success:** [HTTP 2xx or 3xx response, with response body containing valid JSON]

---

### SLO 2: Latency

**SLI:** Proportion of requests that complete within the latency threshold.

```promql
# SLI measurement
sum(rate(http_request_duration_seconds_bucket{job="[service]", le="0.5"}[5m]))
/
sum(rate(http_request_duration_seconds_count{job="[service]"}[5m]))
```

| Metric | Target | Error Budget |
|--------|--------|-------------|
| p95 latency < 500ms | **99%** of requests | 1% can be slow |
| p99 latency < 2s | **99%** of requests | |

**Measurement window:** 30-day rolling
**Scope:** All GET requests to /api/v2/orders (read path); excludes report generation endpoints

---

### SLO 3: Data Freshness (if applicable)

**SLI:** Proportion of time that critical data is updated within the freshness threshold.

| Metric | Target | Threshold |
|--------|--------|-----------|
| Product catalog freshness | 99.9% | Updated within 5 minutes of source change |
| Inventory sync | 99.5% | Updated within 2 minutes |

---

## Error Budget Policy

**Total monthly error budget (availability SLO):** 43.2 minutes

### How we use the error budget

| Budget consumed | Action |
|----------------|--------|
| 0–25% | Normal operations; deployments proceed as usual |
| 25–50% | Increased caution; risky deployments need explicit approval |
| 50–75% | Freeze risky changes; focus on reliability improvements |
| 75–100% | Freeze all non-emergency changes; reliability work takes priority |
| 100%+ (budget exhausted) | Emergency mode; no new features; incident review required |

**Error budget review:** Reviewed monthly with [team] + [product owner]. If budget is consistently exhausted, we reassess the SLO target or allocate engineering time to reliability work.

---

## Alerting

### Burn rate alerts

Alert when the error budget is being consumed faster than expected.

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Fast burn | Consuming 5% of monthly budget in 1 hour (14.4x rate) | Critical | Page on-call immediately |
| Slow burn | Consuming 10% of monthly budget in 6 hours (6x rate) | Warning | Notify team; investigate |
| Budget warning | 75% consumed this month | Warning | Escalate to tech lead |
| Budget exhausted | 100% consumed | Critical | Emergency protocol |

```yaml
# Prometheus burn rate alerts (see writer-alert-rules skill for full syntax)
- alert: SLOBurnRateFast
  expr: |
    (rate(http_requests_total{job="[service]",status=~"5.."}[1h])
    / rate(http_requests_total{job="[service]"}[1h])) > (14.4 * 0.001)
  for: 2m
  labels:
    severity: critical
  annotations:
    summary: "Fast SLO burn: [service] error budget at risk"
```

---

## Measurement and Reporting

**Where to track:**
- Dashboard: https://grafana.internal/d/[slo-dashboard-id]
- SLO tracking tool: [Pyrra / Sloth / Grafana SLO / manual]
- Monthly report: [Link to template or tool]

**Reporting cadence:**
- Weekly: Automated SLO report to [#team-channel]
- Monthly: SLO review in [team meeting]; discuss error budget usage
- Quarterly: Reassess SLO targets based on business needs and achievability

---

## SLO Review Checklist

Use at each review cycle:

- [ ] Current error budget consumption: [X%]
- [ ] Any SLO breaches this period? [Yes/No] — if yes, link to postmortem
- [ ] Are we meeting the SLO consistently? (Consistently < 10% budget consumed → consider raising the target)
- [ ] Is the SLO still meaningful? (Does it measure what users care about?)
- [ ] Are there new user journeys that need SLO coverage?

---

## Non-goals

These are explicitly NOT covered by this SLO:

- [e.g., "Third-party payment provider availability — we measure our API success rate, not Stripe's"]
- [e.g., "Batch export jobs — these have a separate SLO documented in [link]"]
- [e.g., "Dev and staging environments"]
```

## Calibration

- **New service / greenfield**: Focus on defining 1–2 SLOs; don't over-engineer
- **Existing service with incidents**: Derive SLO from historical data; set target just above current baseline
- **Multiple SLOs**: Prioritize — choose 2–3 that matter most; avoid SLO sprawl
- **Contractual SLA**: SLO should be ≥ 0.5pp higher than the SLA to give a buffer
