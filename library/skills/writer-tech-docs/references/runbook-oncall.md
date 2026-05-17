# writer-tech-docs — runbook-oncall variant

Produce an **on-call alert runbook** with symptoms, diagnosis steps, escalation paths, and resolution procedures.

## What makes a great on-call runbook

An on-call runbook is read at 3 AM by someone who just got paged. It must be fast to scan, immediately actionable, and complete enough that even someone unfamiliar with the service can mitigate the issue. Prioritize getting to diagnosis and mitigation quickly.

## Information gathering

- **Alert name**: What alert fires? What does the alert condition measure?
- **Service**: What service or component does this cover?
- **Symptoms**: What does a user or system experience when this fires?
- **Common causes**: Known root causes?
- **Mitigation**: Known fixes, rollbacks, restarts?
- **Escalation**: Who else needs to be involved?

## Output format

````markdown
# On-Call Runbook: [Alert Name / Service Name]

**Alert:** `[AlertName]` in [Prometheus / Datadog / PagerDuty]
**Service:** [service-name]
**Severity:** [Critical / High / Medium]
**SLO impact:** [e.g., "This alert indicates SLO breach — error budget is being consumed"]
**Owner:** [team-name] | [Slack: #channel] | [PagerDuty: escalation-policy-name]

---

## Quick Reference

| Symptom                  | Most likely cause | Quick fix                                            |
| ------------------------ | ----------------- | ---------------------------------------------------- |
| Error rate > 1%          | Bad deploy        | Roll back: `kubectl rollout undo deploy/[service]`   |
| High latency, not errors | DB slow queries   | Check: `[query]`                                     |
| Service down             | Pod crashloop     | Check: `kubectl logs [pod]`                          |
| Queue backed up          | Consumer lag      | Restart: `kubectl rollout restart deploy/[consumer]` |

---

## 1. Assess the Situation (2 minutes)

**Confirm the alert is real:**

```bash
# Check current error rate
kubectl exec -n prod deploy/[service] -- curl -s localhost:8080/metrics | grep http_requests_errors
```
````

**Determine scope:**

- Is this affecting ALL users or a subset?
- Is this isolated to one instance or all instances?
- Is this correlated with a recent deploy?

| Condition                            | Action                                  |
| ------------------------------------ | --------------------------------------- |
| > 50% error rate, all users affected | Escalate immediately; consider rollback |
| > 10% error rate, partial impact     | Investigate + prepare rollback          |
| < 5% error rate, no SLO breach       | Investigate; monitor                    |

---

## 2. Communicate (within 5 minutes)

- [ ] Update PagerDuty: acknowledge + add note "Investigating"
- [ ] Post in [#incidents] Slack: "[service] experiencing [symptom]. On-call [name] investigating."
- [ ] Update status page if user-visible

---

## 3. Diagnose

### Check 1: Recent deployments

```bash
kubectl rollout history deploy/[service] -n prod
```

→ **If deploy was recent:** Jump to Rollback

### Check 2: Application logs

```bash
kubectl logs -l app=[service] -n prod --tail=200 | grep -E "ERROR|WARN|Exception"
```

- Database connection errors → Check DB health
- `OutOfMemoryError` or `KILLED` → Check memory
- Network timeout errors → Check upstream dependencies

### Check 3: Database health

```bash
kubectl exec -n prod deploy/[service] -- curl -s localhost:8080/actuator/health | python3 -m json.tool | grep -A5 db
```

**Slow query check:**

```sql
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE state <> 'idle' AND now() - pg_stat_activity.query_start > interval '5 seconds'
ORDER BY duration DESC;
```

### Check 4: Memory / Resources

```bash
kubectl top pods -n prod -l app=[service]
kubectl describe pods -l app=[service] -n prod | grep -E "Restart|OOMKilled|Reason"
```

### Check 5: Upstream dependencies

```bash
curl -s https://[upstream-service]/health | python3 -m json.tool
```

---

## 4. Mitigate

### Option A: Rollback (fastest, if deploy was recent)

```bash
kubectl rollout undo deploy/[service] -n prod
kubectl rollout status deploy/[service] -n prod
```

### Option B: Restart service

```bash
kubectl rollout restart deploy/[service] -n prod
```

### Option C: Scale up

```bash
kubectl scale deploy/[service] -n prod --replicas=[N+2]
```

### Option D: Enable circuit breaker / feature flag

```bash
curl -X POST https://launchdarkly.internal/flag/[flag-name]/disable -H "Authorization: $LD_API_KEY"
```

---

## 5. Verify Resolution

- [ ] Error rate back to baseline (< [threshold]) for [5 minutes]
- [ ] No new error patterns in logs for 5 minutes
- [ ] Database connections back to normal
- [ ] Status page updated if it was changed

---

## 6. Escalation

| Who                     | When                             | How                           |
| ----------------------- | -------------------------------- | ----------------------------- |
| [Service team engineer] | Can't diagnose in 15 min         | Slack DM + PagerDuty escalate |
| [DB team]               | Database issues                  | Slack [#db-oncall]            |
| [Platform/Infra team]   | Network or Kubernetes issues     | PagerDuty: platform-oncall    |
| [Leadership/product]    | Customer-visible outage > 30 min | Slack [#leadership-incidents] |

---

## 7. Post-Incident

- [ ] Close the incident in PagerDuty
- [ ] Post all-clear in [#incidents]
- [ ] Create postmortem ticket if SEV1, SEV2, data loss, or repeat root cause
- [ ] Update this runbook if any steps were wrong or missing

---

## Reference

**Key dashboards:**

- Main service dashboard: <https://grafana.internal/d/[dashboard-id>]
- Error breakdown: <https://grafana.internal/d/[dashboard-id>]

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

```

## Calibration

- **New service onboarding**: Generate a template runbook to fill in as the team learns the failure modes
- **Specific alert**: Generate detailed diagnosis steps for that specific alert condition
- **Multiple alerts for one service**: Generate one runbook per alert, with a master index
- **Experienced team**: Shorter; emphasize quick reference table over detailed steps
```
