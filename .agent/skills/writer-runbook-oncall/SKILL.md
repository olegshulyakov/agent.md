---
name: writer-runbook-oncall
description: >
  Produces on-call runbooks for specific alerts with symptoms, diagnosis steps, escalation paths,
  and rollback procedures. Use this skill whenever the user wants to create a runbook for an on-call
  alert, document how to respond to a specific alert, write a troubleshooting guide for on-call
  engineers, or asks to "write an on-call runbook", "document what to do when this alert fires",
  "create a response playbook for this alert", "write a runbook for PagerDuty alert X", "how should
  on-call respond to high latency alerts", "create an escalation path for this service", or "document
  the troubleshooting steps for this incident type". Also trigger for "alert response playbook",
  "incident response runbook", "SRE runbook", and "on-call handbook for service X". Distinct from
  writer-runbook (which documents general operational procedures, not specific alert responses) and
  writer-postmortem (which documents what happened after an incident).
---

# writer-runbook-oncall

Produce an **on-call alert runbook** with symptoms, diagnosis steps, escalation paths, and resolution procedures.

## What makes a great on-call runbook

An on-call runbook is read at 3 AM by someone who just got paged. It must be fast to scan, immediately actionable, and complete enough that even someone unfamiliar with the service can mitigate the issue. Prioritize getting to diagnosis and mitigation quickly — context and explanation can come later in postmortems.

## Information gathering

From context, identify:
- **Alert name**: What alert fires? What does the alert condition measure?
- **Service**: What service or component does this cover?
- **Symptoms**: What does a user or system experience when this fires?
- **Common causes**: Known root causes?
- **Mitigation**: Known fixes, rollbacks, restarts?
- **Escalation**: Who else needs to be involved?

## Output format

```markdown
# On-Call Runbook: [Alert Name / Service Name]

**Alert:** `[AlertName]` in [Prometheus / Datadog / PagerDuty]
**Service:** [service-name]
**Severity:** [Critical / High / Medium]
**SLO impact:** [e.g., "This alert indicates SLO breach — error budget is being consumed"]
**Owner:** [team-name] | [Slack: #channel] | [PagerDuty: escalation-policy-name]

---

## Quick Reference

*For experienced responders — skip to details if needed.*

| Symptom | Most likely cause | Quick fix |
|---------|-------------------|-----------|
| Error rate > 1% | Bad deploy | Roll back: `kubectl rollout undo deploy/[service]` |
| High latency, not errors | DB slow queries | Check: `[query]` |
| Service down | Pod crashloop | Check: `kubectl logs [pod]` |
| Queue backed up | Consumer lag | Restart: `kubectl rollout restart deploy/[consumer]` |

---

## 1. Assess the Situation (2 minutes)

**Confirm the alert is real:**

```bash
# Check current error rate
kubectl exec -n prod deploy/[service] -- curl -s localhost:8080/metrics | grep http_requests_errors

# Or: check the dashboard
# https://grafana.internal/d/[dashboard-id]
```

**Determine scope:**
- [ ] Is this affecting ALL users or a subset? (geography, plan tier, feature?)
- [ ] Is this isolated to one instance or all instances?
  ```bash
  kubectl get pods -n prod -l app=[service] -o wide
  # Are all pods showing errors, or just one node?
  ```
- [ ] Is this correlated with a recent deploy?
  ```bash
  kubectl rollout history deploy/[service] -n prod
  ```

**Initial severity assessment:**

| Condition | Action |
|-----------|--------|
| > 50% error rate, all users affected | Escalate immediately; consider rollback |
| > 10% error rate, partial impact | Investigate + prepare rollback |
| < 5% error rate, no SLO breach | Investigate; monitor |

---

## 2. Communicate (within 5 minutes of acknowledgment)

- [ ] Update PagerDuty: acknowledge + add note "Investigating"
- [ ] Post in [#incidents] Slack: "[service] experiencing [symptom]. On-call [name] investigating."
- [ ] Update status page if user-visible: https://status.example.com (or: ping [#status-page])

---

## 3. Diagnose

### Check 1: Recent deployments (most common cause)

```bash
# Was there a deploy in the last hour?
kubectl rollout history deploy/[service] -n prod

# When was the most recent pod restart?
kubectl describe pod -l app=[service] -n prod | grep "Started:"
```

→ **If deploy was recent:** Jump to [Rollback Procedure](#rollback)

### Check 2: Application logs

```bash
# Last 200 error logs
kubectl logs -l app=[service] -n prod --tail=200 | grep -E "ERROR|WARN|Exception"

# Or: Datadog / Splunk / Loki query
# logs from:[service] level:error last:30m
```

**What to look for:**
- Database connection errors → [Check 3: Database]
- `OutOfMemoryError` or `KILLED` → [Check 4: Memory]
- Network timeout errors → [Check 5: Upstream Dependencies]
- NullPointerException → likely a code bug; rollback

### Check 3: Database health

```bash
# Connection pool status
kubectl exec -n prod deploy/[service] -- curl -s localhost:8080/actuator/health | python3 -m json.tool | grep -A5 db

# Or directly:
psql $DB_URL -c "SELECT state, count(*) FROM pg_stat_activity WHERE datname='[dbname]' GROUP BY state;"
# Expected: <MAX_CONNECTIONS connections, no "idle in transaction" accumulation
```

**Slow query alert:**
```sql
-- Running queries > 5 seconds
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE state <> 'idle' AND now() - pg_stat_activity.query_start > interval '5 seconds'
ORDER BY duration DESC;
```

→ **If DB is slow:** Check [DB Health Runbook](./db-health.md) | Escalate to DBA: [name] [contact]

### Check 4: Memory / Resources

```bash
# Pod resource usage
kubectl top pods -n prod -l app=[service]
# Alert if memory > 90% of limit

# Pod restarts (OOMKilled?)
kubectl describe pods -l app=[service] -n prod | grep -E "Restart|OOMKilled|Reason"
```

→ **If OOMKilled:** Increase memory limit temporarily or rollback if this is a regression

### Check 5: Upstream dependencies

```bash
# Check health of services this depends on
curl -s https://[upstream-service]/health | python3 -m json.tool

# Or: check the service map dashboard
# https://grafana.internal/d/[service-map-dashboard]
```

→ **If upstream is down:** Escalate to [upstream team]; implement circuit breaker temporarily

---

## 4. Mitigate

### Option A: Rollback (fastest, if deploy was recent)

**Time to mitigate: ~3 minutes**

```bash
# Rollback to previous deployment
kubectl rollout undo deploy/[service] -n prod

# Monitor rollout
kubectl rollout status deploy/[service] -n prod

# Verify error rate dropping (watch dashboard or run)
watch -n 5 'kubectl exec -n prod deploy/[service] -- curl -s localhost:8080/metrics | grep error_rate'
```

### Option B: Restart service

**Use when:** Logs show memory leak, connection leak, or transient resource exhaustion.

```bash
# Rolling restart (zero downtime)
kubectl rollout restart deploy/[service] -n prod
kubectl rollout status deploy/[service] -n prod
```

### Option C: Scale up

**Use when:** Load is higher than capacity; no obvious bug.

```bash
kubectl scale deploy/[service] -n prod --replicas=[N+2]
```

### Option D: Enable circuit breaker / feature flag

**Use when:** Specific feature is causing errors; can be disabled safely.

```bash
# Disable feature flag
curl -X POST https://launchdarkly.internal/flag/[flag-name]/disable \
  -H "Authorization: $LD_API_KEY"
```

### Option E: Failover to backup / secondary

*[Document only if applicable to this service]*

---

## 5. Verify Resolution

After applying a fix:

- [ ] Error rate back to baseline (< [threshold]) for [5 minutes]
  ```bash
  kubectl exec -n prod deploy/[service] -- curl -s localhost:8080/metrics | grep error_rate
  ```
- [ ] No new error patterns in logs for 5 minutes
- [ ] Database connections back to normal
- [ ] Status page updated if it was changed

---

## 6. Escalation

**Escalate if:** You've been on the incident for 30 minutes without mitigation, or the scope is larger than expected.

| Who | When | How |
|-----|------|-----|
| [Service team engineer] | Can't diagnose in 15 min | Slack DM + PagerDuty escalate |
| [DB team] | Database issues | Slack [#db-oncall] |
| [Platform/Infra team] | Network or Kubernetes issues | PagerDuty: platform-oncall |
| [Leadership/product] | Customer-visible outage > 30 min | Slack [#leadership-incidents] |

---

## 7. Post-Incident

Once mitigated:

- [ ] Close the incident in PagerDuty
- [ ] Post all-clear in [#incidents]: "[service] back to normal as of [time]. Root cause: [brief]. Postmortem: [Yes/No]"
- [ ] Create postmortem ticket if: SEV1 or SEV2, or data loss, or same root cause as previous incident
- [ ] Update this runbook if any steps were wrong or missing

---

## Reference

**Key dashboards:**
- Main service dashboard: https://grafana.internal/d/[dashboard-id]
- Error breakdown: https://grafana.internal/d/[dashboard-id]

**Log queries:**
```
# Datadog: All errors in last 15m
service:[service-name] status:error @timestamp:>now-15m

# Splunk
index=prod source=[service] level=ERROR earliest=-15m
```

**Related runbooks:**
- [DB Health Runbook](./db-health.md)
- [Deployment Rollback](./deployment-rollback.md)
- [Upstream Service X Runbook](./service-x.md)
```

## Calibration

- **New service onboarding**: Generate a template runbook to fill in as the team learns the failure modes
- **Specific alert**: Generate detailed diagnosis steps for that specific alert condition
- **Multiple alerts for one service**: Generate one runbook per alert, with a master index
- **Experienced team**: Shorter; emphasize quick reference table over detailed steps
