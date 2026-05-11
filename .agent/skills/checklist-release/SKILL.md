---
name: checklist-release
description: >
  Produces a release checklist with pre-deployment, deployment, and post-deployment steps, sign-off sections,
  rollback criteria, and go/no-go gates. Use this skill whenever the user wants to create a release checklist,
  plan a deployment, prepare for a production release, coordinate a release across teams, or asks to "create
  a release checklist", "what do we need to do before we release", "make a deployment plan", "go/no-go
  checklist", "release sign-off checklist", or "what's the rollback plan". Also trigger for "release
  readiness review", "deployment runbook", "cut a release", and "production deployment plan". Distinct
  from writer-runbook (general operational runbook) and strategy-dependency-upgrade (focused on dependency
  management during releases).
---

# checklist-release

Produce a **release checklist** with go/no-go gates, pre/during/post deployment steps, and rollback criteria.

## What makes a great release checklist

A release checklist is a safety net, not a formality. The best ones are specific enough that any team member can execute them without tribal knowledge, and conservative enough that they catch real problems before users do. Include explicit sign-off owners and clear rollback triggers.

## Information gathering

From context, identify:
- **Release type**: Hotfix, minor feature, major version, database migration?
- **Deployment target**: Cloud (AWS/GCP/Azure), on-prem, mobile app store, npm package?
- **Stack**: What services, databases, caches, queues are involved?
- **Team**: Who needs to sign off? On-call engineer identified?
- **Risk level**: Breaking changes, DB migrations, external API changes, traffic-impacting?
- **Rollback capability**: Can we roll back? How fast? Any data migration to reverse?

## Output format

```markdown
# Release Checklist: [Service/Product Name] v[Version]

**Release Date:** [date]
**Release Manager:** [name]
**On-Call Engineer:** [name]
**Deployment Window:** [e.g., Tuesday 14:00–16:00 UTC]
**Release Type:** [Hotfix / Minor / Major / DB Migration]
**Risk Level:** 🔴 High / 🟠 Medium / 🟡 Low

---

## Go/No-Go Gate

Complete this section BEFORE beginning deployment. All boxes must be checked for a green light.

### Code Readiness
- [ ] All planned features/fixes are merged to the release branch
- [ ] No open P0/P1 bugs targeting this release
- [ ] Code review completed on all changes
- [ ] CHANGELOG updated with this release's changes
- [ ] Version bumped in package manifest / deployment config

### Testing
- [ ] Unit and integration tests pass on release branch
- [ ] E2E / smoke test suite passes in staging
- [ ] Performance tests run (if applicable — no regression > 10%)
- [ ] Security scan run — no new critical/high vulnerabilities
- [ ] Manual exploratory testing completed for high-risk areas

### Infrastructure & Config
- [ ] Environment variables / secrets updated in target environment
- [ ] Database migrations reviewed — tested on a staging DB copy
- [ ] Feature flags configured correctly for rollout
- [ ] CDN / cache invalidation plan confirmed (if needed)
- [ ] Dependency versions pinned (no floating `latest`)

### Observability
- [ ] Dashboards are ready and being monitored
- [ ] Alerting thresholds verified — not too noisy, not too quiet
- [ ] On-call rotation confirmed with engineer briefed on this release

### Communication
- [ ] Stakeholders notified of release window
- [ ] Customer-facing teams briefed on changes (if user-visible)
- [ ] Status page / maintenance window announced (if needed)

### Rollback Readiness
- [ ] Rollback procedure documented (see section below)
- [ ] Previous stable artifact available and verified
- [ ] Rollback time estimated: [e.g., < 15 minutes]
- [ ] Data migration rollback script prepared (if applicable)

**🟢 GO / 🔴 NO-GO Decision:** _______________
**Signed off by:** _______________ @ _______________

---

## Pre-Deployment Steps

_Complete in order. Each step has an owner and verification criterion._

- [ ] 1. **Announce deployment start** — Post in #deployments channel: "Deploying [service] v[X] to prod. Monitor [dashboard link]."
  - Owner: [Release Manager]
- [ ] 2. **Take DB backup** (if DB migrations included)
  - Owner: [DBA / DevOps]
  - Verify: Backup timestamp confirmed in [backup tool]
- [ ] 3. **Enable maintenance mode** (if applicable)
  - Owner: [DevOps]
  - Verify: Maintenance page served at [URL]
- [ ] 4. **Scale up capacity** (if expecting traffic impact)
  - Owner: [DevOps]
  - Verify: Target instance count reached in [dashboard]
- [ ] 5. **[Custom step for this release]**
  - Owner: [Name]
  - Verify: [How to confirm success]

---

## Deployment Steps

- [ ] 1. **Deploy to [canary / first AZ / first region]**
  - Command/Action: [e.g., `kubectl apply -f deploy/prod.yaml` or CI pipeline link]
  - Owner: [Engineer]
  - Wait: [e.g., 5 minutes — watch error rate dashboard]
- [ ] 2. **Verify health checks pass**
  - Check: [Health endpoint URL or dashboard]
  - Pass criteria: HTTP 200, response time < [Xms], error rate < [1%]
- [ ] 3. **Run smoke tests against production**
  - Command: [e.g., `npm run test:smoke -- --env=prod`]
  - Pass criteria: All smoke tests green
- [ ] 4. **Run database migrations** (if applicable)
  - Command: [migration command]
  - Verify: Migration log shows success; spot-check [table name]
- [ ] 5. **Progressively roll out to 100%** (if using canary/blue-green)
  - Steps: 10% → 25% → 50% → 100%, with [X min] hold between steps
  - Monitor: [Error rate / latency dashboard]
- [ ] 6. **[Custom deployment step]**

---

## Post-Deployment Verification

Complete within [30 minutes] of full deployment.

- [ ] **Functional verification**: [Core user journey works — e.g., login, checkout, key API endpoint]
- [ ] **Error rate**: Within normal baseline (< [X%] 5xx rate)
- [ ] **Latency**: p95 response time within [X ms] (check: [dashboard link])
- [ ] **Database**: Query latency normal, no lock waits or connection pool exhaustion
- [ ] **Log scan**: No unexpected ERROR or WARN patterns in past 15 minutes
- [ ] **Business metrics**: [Conversion rate, order rate, etc.] showing normal values
- [ ] **Feature flag state**: Newly released features activated for correct % of users

**Post-deploy check completed by:** _______________ @ _______________

---

## Rollback Criteria

Initiate rollback immediately if ANY of the following are true:

- [ ] Error rate exceeds [3%] for more than [5 minutes]
- [ ] p95 latency exceeds [2x baseline] for more than [5 minutes]
- [ ] Core user flow [login/checkout/etc.] is broken for more than [2 minutes]
- [ ] Database errors or data corruption detected
- [ ] [Service-specific criterion]

**Rollback Decision Owner:** [On-call engineer / Release Manager]

### Rollback Procedure

1. [Step 1 — e.g., "Revert deployment: `kubectl rollout undo deploy/[service]`"]
2. [Step 2 — e.g., "If migrations ran: execute rollback script `db/rollback_v[X].sql`"]
3. [Step 3 — e.g., "Disable feature flags for new features"]
4. [Step 4 — e.g., "Notify #incidents channel"]

**Estimated rollback time:** [X minutes]

---

## Post-Release

- [ ] **Announce success** — Post in #deployments: "✅ [service] v[X] deployed successfully."
- [ ] **Disable maintenance mode** (if enabled)
- [ ] **Update release tracking** — Mark release as deployed in [Jira/Linear/GitHub]
- [ ] **Monitor for [24 hours]** — Keep on-call alert active with heightened sensitivity
- [ ] **Postmortem** (if anything went wrong) — Schedule within [48 hours]
- [ ] **Update runbook** — Capture any new learnings from this release

---

## Release Notes

[Link to CHANGELOG or brief summary of what was released]

## Contacts

| Role | Name | Contact |
|------|------|---------|
| Release Manager | [Name] | [Slack/email] |
| On-Call Engineer | [Name] | [PagerDuty/phone] |
| DBA | [Name] | [Contact] |
| Product Owner | [Name] | [Contact] |
```

## Calibration

- **Hotfix**: Streamline to only critical safety steps; rollback section is most important
- **Major release / DB migration**: Full checklist; extra emphasis on backup, migration verification, and rollback
- **Mobile app store**: Replace infrastructure steps with App Store Connect / Play Console steps; add review wait time
- **npm / library release**: Focus on versioning, changelog, registry publish, tag, and downstream notification
- **Simple feature deploy**: Shorter version emphasizing smoke tests and monitoring
