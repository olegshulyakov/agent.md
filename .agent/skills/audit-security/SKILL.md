---
name: audit-security
description: >
  Produces an OWASP-aligned security review of code, architecture, or a system description, with findings
  categorized by severity and actionable remediation steps. Use this skill whenever the user wants a security
  audit, code security review, OWASP checklist, vulnerability assessment, or asks to "review this for security
  issues", "check for SQL injection", "find XSS vulnerabilities", "audit authentication logic", "assess the
  attack surface", or "do a security review". Also trigger for threat analysis, security hardening reviews,
  penetration test prep, and security sign-off before release. Distinct from model-threat (which produces
  a STRIDE threat model) and audit-secrets (which focuses specifically on credential exposure).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# audit-security

Produce a **security review report** aligned to OWASP Top 10 and relevant standards, with findings rated by severity and concrete remediation guidance.

## What makes a great security review

A great security audit is more than a checklist — it reasons about the actual attack surface, identifies the most likely exploitation paths, and gives developers fixes they can implement immediately. Prioritize findings by exploitability and impact, not just theoretical risk.

## Information gathering

From context, identify:

- **Scope**: Code snippet, API design, architecture description, or full codebase
- **Stack**: Language, framework, database, auth mechanism
- **Context**: Internet-facing, internal tool, handles PII/payments, authentication required?
- **Priority concerns**: User mentioned specific areas (auth, input validation, etc.)?

Analyze what's provided. If only architecture is described (no code), audit at the design level and note which findings are theoretical vs. confirmed.

## Output format

```
# Security Audit: [Scope / Component]

## Executive Summary
**Date:** [date]
**Scope:** [what was reviewed]
**Standard:** OWASP Top 10 [year] + relevant additions
**Critical:** [N] | **High:** [N] | **Medium:** [N] | **Low:** [N] | **Info:** [N]

## Findings

### [VULN-001] [Vulnerability Title]
- **Category:** [OWASP category — e.g., A01:2021 Broken Access Control]
- **Severity:** Critical / High / Medium / Low / Informational
- **CVSS estimate:** [e.g., 8.1 (High)] (if quantifiable)
- **Location:** [File, function, endpoint, or component]
- **Description:** [What the vulnerability is and how it could be exploited]
- **Vulnerable code:**
  ```[language]
  // problematic snippet
  ```
- **Remediation:**
  ```[language]
  // fixed snippet
  ```
- **References:** [OWASP link, CWE number]

[Repeat for each finding]

## OWASP Top 10 Coverage

| # | Category | Status | Findings |
|---|----------|--------|----------|
| A01:2021 | Broken Access Control | ✅ Reviewed / ⚠️ Partial | [finding IDs] |
| A02:2021 | Cryptographic Failures | ✅ Reviewed | — |
| A03:2021 | Injection | ✅ Reviewed | VULN-001 |
| A04:2021 | Insecure Design | ✅ Reviewed | — |
| A05:2021 | Security Misconfiguration | ✅ Reviewed | — |
| A06:2021 | Vulnerable and Outdated Components | ⚠️ Partial | — |
| A07:2021 | Identification and Authentication Failures | ✅ Reviewed | — |
| A08:2021 | Software and Data Integrity Failures | ⚠️ Not applicable | — |
| A09:2021 | Security Logging and Monitoring Failures | ✅ Reviewed | — |
| A10:2021 | Server-Side Request Forgery | ✅ Reviewed | — |

## Positive Findings
[Security controls that are correctly implemented — credit the good stuff]

## Recommendations (Prioritized)
1. [Highest-impact fix]
2. [Next priority]
...

## Out of Scope / Needs Further Testing
[Items that require dynamic testing, pentest, or data not provided]
```

## Key vulnerability patterns by category

### A01 — Broken Access Control
- Missing authorization checks on endpoints (IDOR, privilege escalation)
- Insecure direct object references in URL parameters
- CORS misconfiguration allowing unauthorized origins
- JWT validation bypasses

### A02 — Cryptographic Failures
- Sensitive data transmitted over HTTP
- Weak hashing (MD5, SHA1) for passwords — must use bcrypt/Argon2/scrypt
- Hardcoded encryption keys
- Missing TLS certificate validation

### A03 — Injection
- SQL injection (string concatenation instead of parameterized queries)
- NoSQL injection (unsanitized MongoDB/Redis queries)
- OS command injection (shell exec with user input)
- LDAP injection, XPath injection
- Template injection (SSTI)

### A04 — Insecure Design
- Missing rate limiting on auth endpoints
- No account lockout policy
- Predictable resource IDs (sequential integers instead of UUIDs)

### A05 — Security Misconfiguration
- Debug mode enabled in production
- Default credentials not changed
- Overly permissive CORS (`Access-Control-Allow-Origin: *`)
- Stack traces exposed to users
- Unnecessary HTTP methods enabled

### A07 — Authentication Failures
- Session tokens not invalidated on logout
- Missing MFA for privileged operations
- Weak session ID entropy
- Password reset tokens that don't expire
- Missing `HttpOnly` and `Secure` cookie flags

### A09 — Logging Failures
- Sensitive data (passwords, tokens) logged
- Authentication failures not logged
- No audit trail for privileged actions

## Severity criteria

| Severity | Criteria |
|----------|----------|
| **Critical** | Directly exploitable with high impact (RCE, auth bypass, full data breach) |
| **High** | Significant data exposure or privilege escalation with moderate effort |
| **Medium** | Requires specific conditions or chaining to exploit |
| **Low** | Defense-in-depth improvement, minimal direct exploitability |
| **Info** | Best-practice deviation without direct security impact |

## Calibration

- **Code audit**: Analyze the exact code provided; give precise line references and working fixes
- **Architecture review**: Focus on design-level risks; note which need code-level verification
- **API review**: Focus on auth/authz, input validation, rate limiting, data exposure in responses
- **Infrastructure**: Focus on network exposure, IAM permissions, secrets handling, logging
