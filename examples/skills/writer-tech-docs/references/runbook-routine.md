# writer-tech-docs — runbook-routine variant

Produce a **general operational runbook** with clear steps, prerequisites, verification, and rollback procedures.

## What makes a great runbook

A runbook should be executable by someone unfamiliar with the system. Assume nothing — list prerequisites, provide exact commands, specify expected output, and tell the reader what to do when something doesn't look right. If a step can fail in an interesting way, the runbook should address it.

## Information gathering

- **Procedure**: What operation is being documented?
- **Audience**: On-call engineer unfamiliar with the system? Experienced SRE? Junior developer?
- **Frequency**: One-time? Daily? Monthly?
- **Risk level**: Read-only or does it make changes? Can it cause an outage?
- **Systems involved**: What services, databases, cloud resources?

## Output format

````markdown
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
- [Trigger condition 2 — e.g., "Monthly: rotate API keys per security policy"]

---

## Prerequisites

**Access:**

- [ ] SSH access to [server/bastion] or VPN connected
- [ ] [Role] permissions in AWS / GCP / Azure
- [ ] [Service] CLI installed and configured

**Status checks:**

- [ ] Confirm the right time (not during peak traffic / deployment window)
- [ ] Notify [#channel] before starting

**Tools:**

```bash
[tool] --version  # Expected: [version range]
```
````

---

## Procedure

### Step 1: [Step name]

**What this does:** [Brief explanation]

```bash
[exact command here]
```

**Expected output:**

```
[what you should see if it's working]
```

**If this fails:** [What to do]

---

### Step N: [Step name]

[Continue pattern]

---

## Verification

- [ ] **[Check 1]**: Run `[command]`; expected output: `[expected]`
- [ ] **[Check 2]**: Navigate to `[URL or location]`; confirm `[what to see]`

**If verification fails:** [What to do]

---

## Rollback

**When to rollback:**

- [Condition 1 — e.g., "Error rate increases after step X"]
- [Condition 2 — e.g., "Step N fails and cannot be retried"]

**Rollback steps:**

1. [Rollback step 1]
   ```bash
   [rollback command]
   ```
2. [Rollback step 2]

**After rollback:** Notify [#channel]. Create a ticket to investigate.

---

## Troubleshooting

| Symptom           | Likely cause | Resolution |
| ----------------- | ------------ | ---------- |
| `[Error message]` | [Cause]      | [Fix]      |

---

## Additional Context

**Related runbooks:**

- [Related runbook name and link]

**Who to escalate to:**

- **[Team/person]**: [When to escalate]

---

## Completion

- [ ] Notify [#channel]: "[Your name] completed [operation]. Status: [OK / issues]"
- [ ] Update this runbook if any steps were incorrect or missing

```

## Calibration

- **Read-only diagnostic procedure**: Skip rollback section; lower risk rating
- **Dangerous/irreversible operation**: Emphasize prerequisites heavily; add explicit confirmation prompts
- **Automated procedure**: Document both the manual version and the automation trigger/command
- **Audience is experienced**: More concise; fewer explanations per step
```
