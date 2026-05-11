---
name: audit-secrets
description: >
  Produces a secrets exposure report identifying hardcoded credentials, API keys, tokens, and sensitive values
  in source code or configuration files, with remediation steps and vault migration guidance.
  Use this skill whenever the user wants to find secrets in code, audit for hardcoded credentials,
  check for exposed API keys, review environment variable usage, scan for sensitive data in repos,
  or asks to "find secrets", "check for hardcoded passwords", "audit credentials in code", "help rotate
  leaked keys", or "migrate secrets to a vault". Also trigger when the user mentions .env files,
  secret scanning, credential rotation, or vault setup (HashiCorp, AWS Secrets Manager, etc.).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# audit-secrets

Produce a **secrets exposure report** identifying hardcoded credentials, tokens, and sensitive values with prioritized remediation steps.

## What makes a great secrets audit

The best secrets audits are thorough but precise — they distinguish actual secrets from placeholders, rank findings by blast radius (production credentials > dev keys), and give the team a clear action plan: what to rotate immediately, what to remove from history, and how to prevent recurrence.

## Information gathering

From context, identify:

- **Scope**: What files, directories, or repo to audit (code provided directly, or description of project type)
- **Stack**: Language, framework, CI/CD system (affects where secrets commonly appear)
- **Rotation urgency**: Is this a pre-commit review, post-incident audit, or routine scan?

If code is provided, analyze it directly. If only a project description is given, enumerate the likely exposure surfaces for that stack.

## Output format

```
# Secrets Exposure Report: [Project / Scope]

## Executive Summary
**Date:** [date]
**Scope:** [what was audited]
**Critical findings:** [N] (rotate immediately)
**High findings:** [N] (rotate within 24h)
**Medium findings:** [N] (remediate this sprint)
**Low findings:** [N] (improve practices)

## Critical Findings (Rotate Immediately)

### [SEC-001] [Secret type] in [file/location]
- **Type:** API key / Database password / Private key / OAuth token / etc.
- **Severity:** Critical / High / Medium / Low
- **File:** `path/to/file.ext` (line N)
- **Snippet:** [partial, masked after first 4 chars]
  ```
  DB_PASSWORD = "mypassw***"
  ```
- **Blast radius:** [What systems/data could be accessed with this credential]
- **Rotation steps:**
  1. [Specific step to invalidate the exposed credential]
  2. [How to set a new value securely]
  3. [How to remove from git history if committed]
- **Long-term fix:** [Environment variable, secret manager reference]

[Repeat for each finding]

## Exposure Surfaces Checked

| Surface | Status | Notes |
|---------|--------|-------|
| Source files (.py, .js, .ts, etc.) | ✅ Checked / ⚠️ Partial | |
| Config files (.env, .yaml, .json) | ✅ Checked / ⚠️ Partial | |
| CI/CD pipeline files | ✅ Checked / ⚠️ Not provided | |
| Dockerfile / docker-compose | ✅ Checked / ⚠️ Not provided | |
| Infrastructure-as-code | ✅ Checked / ⚠️ Not provided | |
| Test files | ✅ Checked / ⚠️ Partial | |
| Git history | ⚠️ Cannot check without repo access | |

## False Positive Notes
[Any patterns flagged that are likely safe — e.g., placeholder values, test fixtures with fake creds]

## Prevention Recommendations

### Immediate
- Add `.env` and `*.pem` to `.gitignore`
- Enable secret scanning in your repository (GitHub Advanced Security / GitLab Secret Detection / gitleaks)

### Short-term
- Migrate all secrets to a secret manager (see recommendations below)
- Add pre-commit hooks to block secret commits

### Long-term
- [Vault migration guidance — specific to stack/platform]
- [Secret rotation policy recommendation]

## Recommended Secret Management Tools

| Option | Best for | Notes |
|--------|----------|-------|
| HashiCorp Vault | Self-hosted, complex needs | Open source, full-featured |
| AWS Secrets Manager | AWS workloads | Native IAM integration |
| GCP Secret Manager | GCP workloads | Native, simple pricing |
| Azure Key Vault | Azure workloads | Native, RBAC integration |
| Doppler | Multi-cloud, teams | Developer-friendly DX |
| 1Password Secrets Automation | Small teams | Simple setup |
```

## Secret pattern recognition

Common secret patterns to look for:

**Credentials:**
- Passwords in connection strings: `postgresql://user:PASSWORD@host`
- Hardcoded basic auth: `Authorization: Basic BASE64`
- Private keys: `-----BEGIN RSA PRIVATE KEY-----`

**API keys (common formats):**
- AWS: `AKIA[A-Z0-9]{16}` / `aws_secret_access_key`
- GitHub: `ghp_[a-zA-Z0-9]{36}` or `github_token`
- Stripe: `sk_live_` / `rk_live_`
- Twilio: `SK[a-z0-9]{32}`
- Generic: `api_key`, `apikey`, `secret`, `token`, `password`, `passwd`, `pwd`, `auth`

**High-risk file patterns:**
- `.env`, `.env.local`, `.env.production`
- `config/secrets.yml`, `application.properties`
- `*.pem`, `*.key`, `*.p12`, `*.pfx`
- `terraform.tfvars`, `*.tfstate`

## Severity criteria

| Severity | Criteria |
|----------|----------|
| **Critical** | Production credentials, high-privilege keys, private keys, payment processor keys |
| **High** | Staging/dev credentials that share secrets with prod, third-party service keys |
| **Medium** | Low-privilege dev-only keys, internal service tokens |
| **Low** | Patterns that suggest poor practice but no confirmed secret (e.g., commented-out placeholder) |

## Removing from git history

If a secret was committed, the credential must be rotated AND removed from history:

```bash
# Using git-filter-repo (preferred over BFG)
pip install git-filter-repo
git filter-repo --path-glob '**/*.env' --invert-paths

# Or replace specific strings
git filter-repo --replace-text <(echo 'EXPOSED_SECRET==>REDACTED')
```

> ⚠️ History rewriting requires force-push and all collaborators must re-clone.
