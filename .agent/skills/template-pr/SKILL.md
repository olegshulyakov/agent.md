---
name: template-pr
description: >
  Produces a pull request template with description, checklist, test plan, screenshots section, and
  risk notes. Use this skill whenever the user wants to create a PR template, improve their pull
  request process, write a PR description for a specific change, or asks to "create a PR template",
  "write a pull request template", "write a PR description for this change", "what should our PR
  template look like", "help me write a good PR description", "create a PULL_REQUEST_TEMPLATE.md",
  or "improve our PR review process". Also trigger for "PR checklist", "code review template",
  "pull request format", and "merge request template". Distinct from checklist-code-review (which
  is the reviewer's checklist, not the author's template).
---

# template-pr

Produce a **pull request template** or a filled-in PR description for a specific change.

## Two modes

1. **Template mode**: User wants a blank `.github/PULL_REQUEST_TEMPLATE.md` for their repo
2. **Description mode**: User wants help writing a specific PR description

Detect from context. If the user describes a specific change ("I'm adding auth, help me write the PR"), use description mode and fill in the template based on what they tell you.

## Template mode output

```markdown
<!-- Save to: .github/PULL_REQUEST_TEMPLATE.md -->
<!-- Or for multiple templates: .github/PULL_REQUEST_TEMPLATE/feature.md, bugfix.md, etc. -->

## Summary

<!-- 2–3 sentences: What does this PR do and why? What's the user-visible impact? -->

**Type:** 
- [ ] ✨ Feature
- [ ] 🐛 Bug fix
- [ ] 🔧 Refactor / tech debt
- [ ] 📦 Dependency update
- [ ] 📝 Documentation
- [ ] 🔐 Security fix

**Ticket:** [PROJ-XXX](https://jira.example.com/browse/PROJ-XXX)

---

## Changes

<!-- What changed? Be specific. If large, break into subsections by layer (API / UI / DB / infra) -->

- 
- 
- 

---

## Why this approach?

<!-- Optional but valuable for non-obvious decisions. Were there alternatives considered? Trade-offs made? -->

---

## Testing

### How to test

<!-- Step-by-step instructions for a reviewer to verify this PR works -->

1. 
2. 
3. 

### Test coverage

- [ ] Unit tests added / updated
- [ ] Integration tests added / updated
- [ ] E2E tests added / updated (if applicable)
- [ ] Manual testing completed (describe above)

---

## Screenshots / Demo

<!-- Required for UI changes. Optional for API/backend changes. -->

| Before | After |
|--------|-------|
| [screenshot] | [screenshot] |

<!-- Or: [video/gif demo] -->

---

## Risk Assessment

**Risk level:** 🔴 High / 🟠 Medium / 🟡 Low

<!-- For Medium/High risk, describe what could go wrong and how to detect it -->

| Risk | Mitigation |
|------|-----------|
| [e.g., DB migration on large table] | [e.g., Tested on staging with production-size data; migration takes <30s] |

**Rollback plan:** 
<!-- What to do if this breaks in production -->

---

## Checklist

### Author
- [ ] PR title follows convention: `type(scope): description`
- [ ] Linked to ticket
- [ ] Self-reviewed the diff (read your own code as a reviewer would)
- [ ] No debug code, console.logs, or TODO comments left in
- [ ] Documentation updated (if API or behavior changed)
- [ ] CHANGELOG updated (if user-facing change)

### Reviewer guidance
<!-- Optional: tell reviewers where to focus -->

- Reviewer focus: [e.g., "Please especially review the payment validation logic in `payment.service.ts`"]
- Can skip detailed review of: [e.g., "Generated migration file — just verify it runs"]

---

## Deployment notes

<!-- Anything special needed during or after deployment? -->

- [ ] Feature flag: `[flag_name]` needs to be enabled/configured
- [ ] Environment variable added: `[VAR_NAME]`
- [ ] DB migration runs automatically on deploy
- [ ] Cache invalidation needed for: [describe]
- [ ] No special deployment steps needed
```

## Description mode output

When the user describes a specific change, fill in the template:

```markdown
## Summary

[Write 2–3 specific sentences based on what the user told you. Include the "why."]

**Type:** ✨ Feature
**Ticket:** [PROJ-XXX]

---

## Changes

[Based on user's description, list specific files/components/behaviors changed]

- Added `[specific thing]` to `[file]`
- Modified `[component]` to `[what changed]`
- Updated `[config/docs]` to reflect `[what]`

---

## Why this approach?

[Capture any design decisions the user mentioned. If not provided, add placeholder.]

---

## Testing

### How to test

1. [Step 1 — derived from the feature description]
2. [Step 2]
3. [Expected result]

---
[Continue filling in other sections based on what the user provided]
```

## Multiple template support

For repos with distinct PR types, offer multiple templates:

```
.github/
└── PULL_REQUEST_TEMPLATE/
    ├── feature.md      (default — full template)
    ├── bugfix.md       (shorter — focus on root cause + regression test)
    ├── hotfix.md       (minimal — just what, what was tested, rollback plan)
    └── dependencies.md (minimal — package, changelog link, test result)
```

## Calibration

- **"Create a PR template"**: Generate the blank template for `.github/PULL_REQUEST_TEMPLATE.md`
- **"Help me write a PR description"**: Use description mode; fill in based on what the user tells you about the change
- **"Improve our PR template"**: Read their current template and suggest improvements
- **Multiple template types requested**: Generate the directory-based multi-template setup
