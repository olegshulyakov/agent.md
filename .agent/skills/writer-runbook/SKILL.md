---
name: writer-runbook
description: >
  Produces a general operational runbook with step-by-step procedures, prerequisites, verification
  steps, and rollback instructions for routine operations. Use this skill whenever the user wants
  to document an operational procedure, write a how-to guide for operations, create a runbook for
  a maintenance task, or asks to "write a runbook", "document this procedure", "create an operational
  guide", "how do we do X in production", "write a how-to for rotating secrets", "document the
  deploy procedure", "create a runbook for scaling up the database", or "write an operational
  runbook for this process". Also trigger for "operational playbook", "procedure documentation",
  "maintenance guide", and "operations how-to". Distinct from writer-runbook-oncall (which is
  specific to on-call alert responses) and checklist-release (which is a deployment checklist).
---

# writer-runbook

Produce a **general operational runbook** with clear steps, prerequisites, verification, and rollback procedures.

## What makes a great runbook

A runbook should be executable by someone unfamiliar with the system. The best runbooks assume nothing — they list prerequisites, provide exact commands, specify expected output, and tell you what to do when something doesn't look right. If a step can fail in an interesting way, the runbook should address it.

## Information gathering

From context, identify:
- **Procedure**: What operation is being documented?
- **Audience**: On-call engineer unfamiliar with the system? Experienced SRE? Junior developer?
- **Frequency**: One-time? Daily? Monthly?
- **Risk level**: Is this read-only or does it make changes? Can it cause an outage?
- **Systems involved**: What services, databases, cloud resources?

## Output format

```markdown
# Runbook: [Operation Name]

**Version:** 1.0
**Last updated:** [date]
**Owner:** [team or person]
**Estimated duration:** [X minutes]
**Risk level:** 🔴 High (makes production changes) / 🟠 Medium / 🟢 Low (read-only)

---

## Purpose

[1–3 sentences: What does this runbook help you do? Why would you need to do it?]

---

## When to Use This Runbook

- [Trigger condition 1 — e.g., "On-call alert fires: 'Database disk usage > 85%'"]
- [Trigger condition 2 — e.g., "After a new engineer joins who needs database access"]
- [Trigger condition 3 — e.g., "Monthly: rotate API keys per security policy"]

---

## Prerequisites

Before starting, confirm you have:

**Access:**
- [ ] SSH access to [server/bastion] or VPN connected
- [ ] [Role] permissions in AWS / GCP / Azure
- [ ] [Service] CLI installed and configured

**Knowledge:**
- [ ] Basic familiarity with [technology]
- [ ] Read the [linked document] if this is your first time

**Status checks:**
- [ ] Confirm this is the right time to perform this operation (not during peak traffic / deployment window)
- [ ] Notify [#channel] before starting: "[Your name] starting [operation] on [target]"

**Tools:**
```bash
# Verify required tools are installed
[tool] --version  # Expected: [version range]
```

---

## Procedure

### Step 1: [Step name]

**What this does:** [Brief explanation of why this step exists]

```bash
# Command to run
[exact command here]
```

**Expected output:**
```
[What you should see if it's working]
```

**If this fails:** [What to do if you see an error or unexpected output]

---

### Step 2: [Step name]

[Brief explanation]

```bash
[command]
```

**Expected output:**
```
[expected output]
```

**Verification:** [How to confirm the step succeeded]

---

### Step 3: [Step name — add as many as needed]

[Continue pattern]

---

## Verification

After completing all steps, verify the operation succeeded:

- [ ] **[Check 1]**: Run `[command]`; expected output: `[expected]`
- [ ] **[Check 2]**: Navigate to `[URL or location]`; confirm `[what to see]`
- [ ] **[Check 3]**: Monitor [dashboard/logs] for [X minutes] — no errors expected

**If verification fails:** [What to do — check logs? Escalate? Roll back?]

---

## Rollback

*Follow these steps if the operation needs to be undone or something went wrong.*

**When to rollback:**
- [Condition 1 — e.g., "Error rate increases after step X"]
- [Condition 2 — e.g., "Step N fails and cannot be retried"]

**Rollback steps:**

1. [Rollback step 1]
   ```bash
   [rollback command]
   ```

2. [Rollback step 2]

**After rollback:** Notify [#channel] that the rollback was performed. Create a ticket to investigate.

---

## Troubleshooting

| Symptom | Likely cause | Resolution |
|---------|-------------|------------|
| `[Error message]` | [Cause] | [Fix] |
| `[Other error]` | [Cause] | [Fix] |
| Nothing happens after running step N | [Cause] | [Check: `[diagnostic command]`] |

---

## Additional Context

**Useful commands:**
```bash
# [Description]
[command]

# [Description]
[command]
```

**Related runbooks:**
- [Related runbook name and link]
- [Related runbook name and link]

**Who to escalate to:**
- **[Team/person]**: [When to escalate — e.g., "If database cannot be reached"]
- **[Team/person]**: [When to escalate — e.g., "For any changes to infrastructure beyond this scope"]

---

## Completion

- [ ] Notify [#channel]: "[Your name] completed [operation]. Status: [OK / issues encountered]"
- [ ] Update this runbook if any steps were incorrect or missing
- [ ] Log the operation in [log/ticket/spreadsheet if required]
```

## Example runbooks (common patterns)

### Rotating a secret / API key

```markdown
# Runbook: Rotate [Service] API Key

**Estimated duration:** 15 minutes
**Risk:** 🟠 Medium — brief service disruption if not done in correct order

## Steps

1. **Generate new key** in [Service Admin UI] → Settings → API Keys → New Key
2. **Update secret in Vault / Secret Manager** (NOT in code or ENV files):
   ```bash
   aws secretsmanager update-secret \
     --secret-id "/prod/[service]/api-key" \
     --secret-string "NEW_KEY_HERE"
   ```
3. **Trigger rolling restart** (picks up new secret without downtime):
   ```bash
   kubectl rollout restart deployment/[service] -n production
   ```
4. **Verify** new key is working:
   ```bash
   kubectl logs -l app=[service] --tail=50 | grep "API key"
   # Expected: no auth errors
   ```
5. **Revoke old key** in [Service Admin UI] only after step 4 confirms success
```

## Calibration

- **Read-only diagnostic procedure**: Skip rollback section; lower risk rating
- **Dangerous/irreversible operation**: Emphasize prerequisites heavily; add explicit confirmation prompts in commands
- **Automated procedure**: Document both the manual version and the automation trigger/command
- **Audience is experienced**: More concise; fewer explanations per step; trusted to know prerequisites
