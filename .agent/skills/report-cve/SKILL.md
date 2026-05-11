---
name: report-cve
description: >
  Produces a CVE triage report with affected versions, CVSS severity, impact analysis, and remediation
  steps. Use this skill whenever the user wants to investigate a CVE, triage a security vulnerability,
  assess the impact of a CVE on their system, create a vulnerability report, determine if a dependency
  is affected by a known vulnerability, or asks to "triage this CVE", "is our system affected by CVE-XXX",
  "write a CVE report", "assess the impact of this vulnerability", "what's the fix for CVE-XXX",
  "analyze this security advisory", or "create a vulnerability triage report". Also trigger for
  "dependency vulnerability", "npm audit findings", "OWASP dependency check", "Dependabot alerts",
  and "security advisory assessment". Distinct from audit-security (full OWASP code review) and
  audit-secrets (credential exposure).
---

# report-cve

Produce a **CVE triage report** with impact assessment, affected versions, and remediation steps.

## What makes a great CVE triage report

A CVE report is most useful when it answers three questions clearly: Are we affected? How bad is it? What do we do? The CVSS score is a starting point, not the final answer — a critical CVE in a library you use in a test-only context is lower priority than a high CVE in your authentication path.

## Information gathering

From context, identify:
- **CVE ID**: CVE-YYYY-NNNNN
- **Affected library**: Package name, ecosystem (npm, PyPI, Maven, etc.)
- **Your usage**: Where is this library used? Is the vulnerable code path exercised?
- **Current version**: What version are you running?
- **Fixed version**: What version fixes it?
- **System context**: Internet-facing? Internal only? Auth required to reach the affected code?

Look up CVE details from NVD, GitHub Security Advisories, or OSV.dev if not provided.

## Output format

```markdown
# CVE Triage Report: [CVE-YYYY-NNNNN]

**Date:** [date]
**Assessed by:** [name / team]
**Status:** 🔴 Critical Action Required / 🟠 Patch Soon / 🟡 Monitor / ⚪ Not Affected

---

## Summary

| Field | Value |
|-------|-------|
| **CVE ID** | [CVE-YYYY-NNNNN] |
| **Package** | `[package-name]` ([ecosystem: npm/PyPI/Maven/etc.]) |
| **Vulnerability Type** | [e.g., Remote Code Execution, SQL Injection, Path Traversal] |
| **CVSS Score** | [X.X] [Critical/High/Medium/Low] |
| **CVSS Vector** | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| **Affected Versions** | `< [fixed-version]` |
| **Fixed Version** | `[fixed-version]` |
| **Published** | [CVE publish date] |
| **References** | [NVD link], [GitHub Advisory link] |

---

## Vulnerability Description

[2–4 sentences explaining what the vulnerability is, what attack vector it uses, and what an attacker can achieve if they exploit it. No jargon — make this understandable to a product manager.]

**Attack vector:** [Network / Adjacent / Local / Physical]
**Prerequisites:** [What does an attacker need? Authentication required? User interaction?]
**Impact:** [Confidentiality / Integrity / Availability — what can an attacker do?]

### Technical Details

[More detailed description for engineers: the specific code path, function, or condition that is vulnerable. Include relevant CVE PoC or exploit information if publicly known and ethically appropriate to share.]

---

## Impact Assessment for [Your System / Product Name]

### Are We Affected?

**Verdict:** [Yes / No / Uncertain]

**Version in use:** `[your-current-version]` — [Affected / Not affected / Needs verification]

**Rationale:** [Why are you or are you not affected? E.g., "We use version X which is in the vulnerable range" or "We use version Y which was released after the fix"]

### Exposure Analysis

| Dimension | Assessment | Details |
|-----------|-----------|---------|
| **Code path reachable?** | [Yes/No/Conditional] | [Is the vulnerable function called in your code?] |
| **Internet-facing?** | [Yes/No] | [Does the vulnerable endpoint accept unauthenticated requests?] |
| **Authentication required?** | [Yes/No] | [Do users need to be logged in to reach this code?] |
| **Data at risk** | [None/Low/Medium/High] | [What data could be exposed or corrupted?] |
| **Services affected** | [List services/components using this package] | |

**Effective severity for our system:** [Critical/High/Medium/Low] *(may differ from CVSS if exposure is limited)*

**Exploitability in our context:** [High/Medium/Low] — [1–2 sentences explaining why]

---

## Remediation

### Recommended Action

**[PRIMARY RECOMMENDATION — be direct: upgrade to X, apply patch Y, implement workaround Z]**

### Remediation Options

| Option | Effort | Risk | Recommended? |
|--------|--------|------|-------------|
| **Upgrade to `[fixed-version]`** | [S/M/L] | [Low — backward compatible] | ✅ Recommended |
| **Apply vendor patch** | [S/M/L] | [Medium — manual patch] | If upgrade not feasible |
| **Workaround: [description]** | [S/M/L] | [High — incomplete mitigation] | Temporary only |
| **Accept risk** | None | High | ❌ Not recommended |

### Upgrade Steps

```bash
# npm
npm install [package]@[fixed-version]

# yarn
yarn upgrade [package]@[fixed-version]

# pip
pip install '[package]>=[fixed-version]'

# Maven: update pom.xml
# <version>[fixed-version]</version>
```

### Verification

After upgrading, verify:
- [ ] `[package-manager] audit` shows no remaining CVE
- [ ] Unit and integration tests pass
- [ ] [Specific functional test to confirm the vulnerable path is no longer exploitable]
- [ ] Deployed to staging and tested

---

## Timeline

| Date | Action | Owner |
|------|--------|-------|
| [today] | CVE identified and triaged | [Name] |
| [target] | Patch applied in development | [Engineer] |
| [target] | Patch deployed to staging | [DevOps] |
| [target] | Patch deployed to production | [DevOps] |
| [target] | Verification and closure | [Security] |

**SLA:** Based on [effective severity]:
- Critical: patch within 24 hours
- High: patch within 7 days
- Medium: patch within 30 days
- Low: patch in next planned maintenance

---

## Workarounds & Compensating Controls

If immediate upgrade isn't possible:

- [ ] [Specific workaround — e.g., "Disable endpoint X until patched"]
- [ ] [Compensating control — e.g., "Add WAF rule to block known exploit patterns"]
- [ ] [Monitoring — e.g., "Alert on X log pattern that indicates exploitation attempt"]

---

## References

- [NVD: https://nvd.nist.gov/vuln/detail/CVE-YYYY-NNNNN]
- [GitHub Advisory: https://github.com/advisories/GHSA-...]
- [Package release notes / changelog]
- [Vendor security bulletin]
```

## Calibration

- **CVE ID only, no context**: Focus on general description, CVSS, affected versions; leave impact sections with `[requires your system context]`
- **CVE + codebase context**: Full impact assessment with exposure analysis
- **Multiple CVEs**: Create a prioritized table of all CVEs, then detail top 2–3
- **Not affected**: Still document why; valuable for future reference and compliance
