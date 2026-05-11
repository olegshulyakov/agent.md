---
name: audit-test-flaky
description: >
  Produces a flaky test report with root cause analysis and fix recommendations. Use this skill whenever
  the user wants to investigate flaky tests, identify tests that pass and fail non-deterministically,
  diagnose intermittent test failures, reduce CI noise from unreliable tests, or asks to "find flaky tests",
  "why does this test keep failing randomly", "audit our test suite for flakiness", "fix intermittent failures",
  "investigate non-deterministic tests", or "reduce flaky test noise in CI". Also trigger when the user
  mentions tests that "sometimes pass, sometimes fail", test quarantine lists, or CI pipelines with high
  retry rates. Distinct from strategy-test (which defines testing strategy) and setup-test-framework
  (which sets up tooling).
---

# audit-test-flaky

Produce a **flaky test audit report** with root cause categorization and prioritized fix recommendations.

## What makes a great flaky test audit

The most useful output isn't just a list of flaky tests — it's a root cause diagnosis. "This test is flaky because it uses `Date.now()` in assertions without mocking" is actionable. "This test is sometimes slow" is not. Group flaky tests by root cause so the team can fix the class of problem, not just individual tests.

## Information gathering

From context, identify:
- **Test suite**: Language, framework (Jest, Pytest, Playwright, Cypress, JUnit, etc.)
- **Evidence**: CI failure logs, retry counts, error messages, stack traces
- **History**: How long has this been a problem? Recent regressions or chronic?
- **Environment**: Is flakiness environment-specific (CI only, certain OS, certain DB)?
- **Volume**: How many tests are suspected flaky vs. total suite size?

Work with what's provided. If only test names are given without logs, analyze likely causes from the test code.

## Root Cause Taxonomy

Classify each flaky test into one or more categories:

| Category | Description | Common Fix |
|----------|-------------|------------|
| **Timing / Race Condition** | `setTimeout`, missing `await`, animation not complete | Use `waitFor`, increase timeout, mock timers |
| **Order Dependency** | Test assumes state from a previous test | Proper setup/teardown, isolated fixtures |
| **Shared State** | Global variable, singleton, shared DB | Reset state in `beforeEach`/`afterEach` |
| **External Dependency** | Real network, file system, clock, random | Mock or stub externals; use test containers |
| **Environment Drift** | Different behavior on CI vs local, timezone | Pin timezone, containerize environment |
| **Resource Contention** | Parallel tests sharing ports, files | Unique ports per test, temp directories |
| **Non-Deterministic Data** | Random IDs, current timestamps in assertions | Freeze time, use fixed seeds |
| **Async Leakage** | Previous test's async work bleeds into next | Proper cleanup, abort controllers |

## Output format

```markdown
# Flaky Test Audit Report

**Date:** [date]
**Suite:** [Test framework, language, project name]
**Tests Audited:** [N]
**Tests Identified as Flaky:** [N] ([%] of suite)

---

## Executive Summary

[2–3 sentences: How bad is the flakiness problem, what are the dominant root causes, and what's the recommended first action.]

**Flakiness Severity:** [🔴 Critical (>10% flaky) / 🟠 High (5–10%) / 🟡 Medium (1–5%) / ⚪ Low (<1%)]

---

## Flaky Tests by Root Cause

### ⏱️ Timing & Race Conditions ([N] tests)

| Test | File | Symptom | Evidence |
|------|------|---------|----------|
| `[test name]` | `[file:line]` | [What fails] | [Log snippet or behavior] |

**Fix pattern:** [Specific recommendation for this category]

### 🔗 Order Dependency ([N] tests)
[Same table pattern]

### 🌍 External Dependencies ([N] tests)
[Same table pattern]

[Continue for each category with tests]

---

## Individual Test Findings

### `[test name]`
**File:** `[path:line]`
**Category:** [Root cause category]
**Failure rate:** [e.g., ~30% of runs]
**Symptom:** [What the test outputs when it fails]
**Root Cause:** [Specific explanation of why it fails]
**Fix:** 
```[language]
// Current (flaky)
[code snippet]

// Fixed
[corrected code snippet]
```
**Effort:** [S/M/L]
**Priority:** [P1/P2/P3]

[Repeat for each flaky test]

---

## Remediation Plan

### Immediate Quarantine (remove from blocking CI now)

These tests should be quarantined immediately — they're causing more harm in CI than they're catching bugs:

- `[test name]` — quarantine + create ticket #XXX to fix
- `[test name]` — ...

### Quick Wins (fix in < 1 day, high impact)

- [ ] **[Action]**: [Which tests, specific fix]
- [ ] **[Action]**: [...]

### Systematic Fixes (fix by root cause class, this sprint)

- [ ] **Add `beforeEach` cleanup for shared DB state** — fixes [N] tests
- [ ] **Mock `Date.now()` globally in test setup** — fixes [N] tests
- [ ] **[Pattern fix]** — fixes [N] tests

### Prevention (add to developer guidelines)

- [Convention to adopt going forward]
- [Linting rule or CI check to add]

---

## Flakiness Metrics (if available)

| Test | Runs | Failures | Failure Rate | Mean Time to Detect |
|------|------|----------|-------------|---------------------|
| `[test]` | [N] | [N] | [%] | [ms] |

---

## CI Impact

- **Estimated retry overhead per week:** [N test-minutes wasted]
- **Developer trust impact:** [High/Medium/Low — are devs ignoring CI failures?]
- **Recommended CI policy:** [e.g., retry 2x max; quarantine after 3 consecutive failures]

---

## Recommendations

1. [Top recommendation]
2. [Second recommendation]
3. [Third recommendation]

## References

- [Links to relevant CI runs, issue trackers, or docs]
```

## Calibration

- **Given logs only**: Identify patterns, classify root causes, suggest fixes without specific line numbers
- **Given test code**: Provide specific code fixes with before/after snippets
- **Large suite (>100 flaky)**: Focus on root cause classes and patterns; don't enumerate all tests individually
- **Single flaky test**: Deep-dive diagnosis with specific fix
- **No evidence provided**: Ask for logs or list of flaky test names before proceeding
