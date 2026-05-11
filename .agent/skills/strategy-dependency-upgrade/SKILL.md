---
name: strategy-dependency-upgrade
description: >
  Produces a dependency upgrade strategy with audit, upgrade path planning, risk assessment, PR
  checklist, and testing recommendations. Use this skill whenever the user wants to plan dependency
  upgrades, manage third-party package updates, handle major version bumps, create a dependency
  management strategy, or asks to "plan our dependency upgrades", "how do I upgrade to React 19",
  "create a major version upgrade plan", "dependency audit strategy", "how should we handle npm
  updates", "upgrade all our packages safely", "Dependabot upgrade strategy", or "create a framework
  upgrade plan". Also trigger for "dependency health check", "outdated packages strategy",
  "major version migration", "breaking change management in dependencies", and "package update
  policy". Distinct from checklist-release (which focuses on deployment) and setup-pipeline-cicd
  (which sets up automation).
---

# strategy-dependency-upgrade

Produce a **dependency upgrade strategy** with audit, prioritized upgrade plan, risk assessment, and testing guidance.

## What makes a great dependency upgrade strategy

The worst dependency strategies are either "never update anything" (accumulates risk) or "update everything at once" (breaks everything simultaneously). A good strategy is incremental, risk-aware, and automated where possible. The goal is to make upgrades a routine activity, not a scary quarterly event.

## Information gathering

From context, identify:
- **Tech stack**: Language, package manager (npm, pip, Maven, Gradle, Go modules)?
- **Current state**: How outdated are dependencies? Any known CVEs?
- **Scale**: How many dependencies? Monorepo or single repo?
- **Constraints**: Automated testing available? CI/CD? Deployment frequency?
- **Driver**: Security patch? Framework major upgrade? Compliance requirement?

## Output format

```markdown
# Dependency Upgrade Strategy: [Project / Repo Name]

**Date:** [date]
**Owner:** [team]
**Review cycle:** [quarterly]

---

## Current Dependency Health

Run this first to understand the current state:

```bash
# npm
npx npm-check-updates --format group   # Group by minor/major/patch
npm audit                               # Security vulnerabilities

# pip
pip list --outdated
safety check                            # pip-audit for CVEs

# Maven
mvn versions:display-dependency-updates
mvn dependency-check:check              # OWASP dependency check

# Go
go list -m -u all                       # Show available updates
govulncheck ./...                       # Security scan
```

## Dependency Audit Summary

| Category | Count | Risk |
|----------|-------|------|
| Patch updates (backward compatible bug fixes) | [N] | 🟢 Low |
| Minor updates (backward compatible new features) | [N] | 🟡 Medium |
| Major updates (breaking changes) | [N] | 🔴 High |
| Security vulnerabilities (any severity) | [N] | 🔴 Critical |
| Abandoned / deprecated packages | [N] | 🟠 High |

---

## Upgrade Prioritization

### Priority 1: Security vulnerabilities (this week)

| Package | Current | Fixed | CVE | CVSS | Action |
|---------|---------|-------|-----|------|--------|
| `[package]` | [version] | [fixed-version] | CVE-XXXX-XXXX | [score] | Upgrade immediately |

**Action:** Create a dedicated PR per vulnerable package. No bundling with feature work.

### Priority 2: Patch updates (this sprint)

These are always safe to apply — bug fixes with no API changes.

**Approach:** Update all patch versions in one PR.

```bash
# npm: update all patch versions
npx npm-check-updates --target patch -u && npm install

# pip
pip install --upgrade [package1] [package2]  # one by one
```

**Review checklist:**
- [ ] All tests pass
- [ ] `git diff package-lock.json` reviewed for unexpected transitive changes

### Priority 3: Minor updates (this month)

Minor updates add features but are nominally backward compatible. Still require testing.

**Approach:** Group by ecosystem/theme into batches of 3–5 packages max.

**Batch example:**
- Batch A: Testing libraries (jest, @testing-library/*)
- Batch B: Build tools (webpack, babel, typescript)
- Batch C: Runtime dependencies (axios, lodash)

**Review checklist per batch:**
- [ ] Read CHANGELOG for each package — look for deprecation warnings
- [ ] All automated tests pass
- [ ] Smoke test the application manually (10 minutes)

### Priority 4: Major updates (quarterly planning)

Major updates may have breaking changes that require code modifications.

| Package | Current | Target | Breaking? | Effort | Timeline |
|---------|---------|--------|-----------|--------|----------|
| React | 17 | 18 | Yes — strict mode changes | Medium | Q2 |
| TypeScript | 4.x | 5.x | Yes — strictness improvements | Small | This month |
| [Framework] | [N] | [N+1] | [details] | [XL] | [Q] |

**For each major upgrade, create a dedicated plan with:**
1. Read the official migration guide
2. Run codemods if available (e.g., `react-codemod`, `angular-update`)
3. Fix compilation errors and type errors
4. Run full test suite; fix test failures
5. Manual smoke test of affected functionality
6. Create dedicated PR with [migration notes in description]

---

## Automation Strategy

### Dependabot / Renovate configuration

Automate dependency discovery and PR creation — but don't auto-merge without review.

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: "/"
    schedule:
      interval: weekly
      day: monday
      time: "09:00"
    open-pull-requests-limit: 5        # Don't overwhelm with PRs
    groups:                            # Group minor/patch updates
      testing-deps:
        patterns: ["jest*", "@testing-library/*", "vitest"]
      lint-deps:
        patterns: ["eslint*", "prettier*"]
    ignore:
      - dependency-name: "react"       # Manage major updates manually
        update-types: ["version-update:semver-major"]
    labels:
      - "dependencies"
      - "automated"
```

```yaml
# renovate.json (Renovate bot — more powerful than Dependabot)
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:base"],
  "schedule": ["before 9am on Monday"],
  "prConcurrentLimit": 5,
  "packageRules": [
    {
      "matchUpdateTypes": ["patch"],
      "automerge": true,               # Auto-merge patches (safe)
      "automergeType": "pr",
      "requiredStatusChecks": ["ci"]   # Only if CI passes
    },
    {
      "matchUpdateTypes": ["minor"],
      "groupName": "minor-updates",    # Group all minor updates into one PR
      "automerge": false               # Require human review
    },
    {
      "matchUpdateTypes": ["major"],
      "labels": ["major-upgrade"],
      "assignees": ["[tech-lead]"]     # Notify tech lead
    }
  ]
}
```

---

## PR Checklist for Dependency Upgrades

For every dependency upgrade PR:

### Before merging
- [ ] **CHANGELOG reviewed**: Read release notes for each updated package
- [ ] **Breaking changes identified**: If any, documented in PR description
- [ ] **Tests pass**: All CI checks green
- [ ] **No unexpected transitive changes**: Review lock file diff
- [ ] **Bundle size check**: No significant size regression (if applicable)
- [ ] **Dependency purpose understood**: New indirect dependencies explained

### PR description template
```markdown
## Dependency Upgrade: [package name] [old] → [new]

**Type:** Patch / Minor / Major
**Security fix:** Yes (CVE-XXXX) / No

### Changes in this version
[Relevant CHANGELOG entries]

### Breaking changes
[None / Description of what changed]

### Testing
- [ ] All unit tests pass
- [ ] Manual smoke test: [what was tested]

### Rollback plan
`git revert [commit-sha]` + re-deploy
```

---

## Major Version Migration Playbook

When upgrading a major framework or library:

### 1. Preparation (1–2 weeks before)
- [ ] Read official migration guide end to end
- [ ] Identify all breaking changes that affect your code (search for deprecated APIs)
- [ ] Run any available codemods in a draft branch
- [ ] Check that all your transitive dependencies support the new major version

### 2. Execution (dedicated sprint or dedicated branch)
- [ ] Create a long-lived feature branch
- [ ] Upgrade the package in package.json / requirements.txt
- [ ] Fix compilation errors (type errors first, then runtime errors)
- [ ] Fix test failures (broken assertions, new behavior, new test APIs)
- [ ] Fix runtime issues found in manual testing

### 3. Validation
- [ ] All existing tests pass
- [ ] Performance benchmarks within ±5% of baseline
- [ ] No new warnings in browser console or server logs
- [ ] Tested in staging by at least one team member

### 4. Rollout
- [ ] Merge to main; deploy to staging
- [ ] Observe for [24 hours] before production deploy
- [ ] Feature flag if possible (for gradual rollout)
- [ ] Monitor error rates for [48 hours] post-deploy

---

## Upgrade Policy

| Principle | Policy |
|-----------|--------|
| Patch updates | Apply within 1 sprint; auto-merge if CI passes |
| Minor updates | Apply monthly; group into batches; human review required |
| Major updates | Plan quarterly; dedicated effort; one at a time |
| Security CVEs | Critical/High: within 24–72 hours; Medium: within 2 weeks |
| EOL packages | Replace before end-of-life date; track in dependency audit |
| Abandoned packages | Evaluate alternatives if not updated in 2+ years |

---

## Metrics to Track

| Metric | Target | Measurement |
|--------|--------|-------------|
| Mean dependency age | < 6 months behind latest | Monthly `npm-check-updates` report |
| % dependencies on latest | > 80% | Dependency dashboard |
| Security CVEs open | 0 Critical/High; < 5 Medium | Dependabot dashboard |
| Time to patch critical CVE | < 72 hours | Incident tracking |
```

## Calibration

- **Security-driven**: Focus on CVE triage and fast patching; use report-cve skill for individual CVEs
- **Framework major upgrade**: Expand the major version migration playbook; link to official guides
- **Automated-first request**: Focus on Renovate/Dependabot config; auto-merge policy
- **Audit-only request**: Generate the audit commands and summary table only
