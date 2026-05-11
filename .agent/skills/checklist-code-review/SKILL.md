---
name: checklist-code-review
description: >
  Produces a structured pull request code review checklist organized by concern area (correctness, security,
  performance, style, testing, documentation). Use this skill whenever the user wants a code review checklist,
  PR review template, wants to review a pull request systematically, asks to "review this PR", "check this code",
  "generate a code review", "create a review checklist", or "review this diff". Also trigger when a user pastes
  code and asks for feedback on it holistically (not just a specific bug). Distinct from audit-security (security-only
  focus) and template-pr (the PR description template for the author, not the reviewer).
---

# checklist-code-review

Produce a **structured code review** with findings organized by concern area, ready to paste into a PR comment or review tool.

## What makes a great code review

A great review is specific, kind, and actionable. It distinguishes blockers from suggestions, explains the *why* behind each concern, and acknowledges what was done well. It's a conversation, not a judgment.

## Information gathering

From context, identify:

- **What's being reviewed**: Code diff, full file, description of a PR?
- **Context**: What does this code do? What's the feature or fix?
- **Reviewer role**: Should the review be from a security perspective, performance, general quality?
- **Style guide**: Is there a specific style guide or convention to enforce?

Work with what's provided. If only a description is given (no code), produce a review checklist template they can fill in.

## Checklist structure

Use this review structure. Omit sections that don't apply to the scope.

```
# Code Review: [PR Title / Feature Description]

## Overall Assessment
[1-2 sentences: Is this ready to merge, needs minor changes, or has blockers? What's the general quality?]

**Verdict:** ✅ Approve / 🔄 Request Changes / 💬 Comment

---

## ✅ What's Done Well
- [Specific positive observation with reference to code]
- [Another positive — always include at least one unless code is truly unacceptable]

---

## 🔴 Blockers (Must Fix)

### [B-01] [Issue Title]
**Location:** `path/to/file.ext:line`
**Issue:** [Specific description of the problem]
**Why it matters:** [Impact — bug, security risk, data loss, etc.]
**Suggestion:**
```[language]
// suggested fix
```

[Repeat for each blocker]

---

## 🟡 Suggestions (Should Fix)

### [S-01] [Issue Title]
**Location:** `path/to/file.ext:line`
**Issue:** [What could be improved]
**Suggestion:** [Concrete recommendation]

[Repeat for each suggestion]

---

## 💬 Nits (Optional / Style)
- `file.ext:line` — [minor style note, naming, comment, etc.]
- [Another nit]

---

## Concern Areas Reviewed

| Area | Status | Notes |
|------|--------|-------|
| Correctness | ✅ / ⚠️ / ❌ | [Finding summary] |
| Error handling | ✅ / ⚠️ / ❌ | |
| Security | ✅ / ⚠️ / ❌ | |
| Performance | ✅ / ⚠️ / ❌ | |
| Tests | ✅ / ⚠️ / ❌ | |
| Documentation | ✅ / ⚠️ / ❌ | |
| API/interface design | ✅ / ⚠️ / ❌ | |
| Logging & observability | ✅ / ⚠️ / ❌ | |
```

## Concern area checklists (internal reference)

Use these as your mental checklist while reviewing. Don't output the full checklist — synthesize findings into the format above.

**Correctness**
- Does the code do what the PR description says it does?
- Are edge cases handled (null, empty list, 0, negative numbers, very large input)?
- Are race conditions possible (concurrent access, async operations)?
- Are error paths handled and tested?
- Does it handle the "unhappy path" as carefully as the happy path?

**Security**
- Is user input validated and sanitized before use?
- Are SQL queries parameterized (no concatenation)?
- Are secrets/credentials hardcoded anywhere?
- Is sensitive data logged?
- Are authorization checks present on all endpoints/operations?
- Are output values properly escaped (XSS prevention)?

**Performance**
- Are there N+1 query patterns (loops that trigger database calls)?
- Is expensive computation cached where appropriate?
- Are there unnecessary re-renders or recalculations?
- Is pagination used for large result sets?
- Are database queries using indexes?

**Error handling**
- Are exceptions caught at the right level?
- Are errors propagated or swallowed silently?
- Are meaningful error messages returned to callers?
- Is cleanup (file handles, connections, locks) done in finally/defer blocks?

**Tests**
- Does the test coverage match the PR's risk level?
- Are edge cases tested (not just the happy path)?
- Are tests testing behavior, not implementation?
- Do tests have meaningful names and assertions?

**Documentation & readability**
- Are complex sections commented with *why*, not just *what*?
- Are public APIs/functions documented?
- Are variable and function names clear without needing comments?
- Is the code organized logically (single responsibility)?

**API / interface design**
- Is the API consistent with existing patterns in the codebase?
- Are breaking changes called out?
- Are parameters named and ordered logically?

## Tone guidance

- Start with what's good before blocking concerns
- Use "consider" / "suggest" / "what do you think about" for non-blockers
- Use "this will cause..." / "this is a blocker because..." for blockers — be specific
- Never make it personal ("you wrote..." vs. "this code...")
- For complex changes: acknowledge the complexity and effort

## Calibration

- **Small PR (< 100 lines)**: Detailed line-by-line review
- **Large PR (> 500 lines)**: Focus on architecture, interfaces, patterns; note that line-by-line review is limited
- **Hotfix**: Prioritize correctness and test coverage; skip style nits
- **Refactor**: Focus on behavior preservation, test coverage, and interface consistency
