---
name: writer-tech-docs
description: >
  Write technical docs. Use for READMEs, API docs, endpoint references, routine or on-call
  runbooks, operational procedures, changelogs, and release notes.
author: Oleg Shulyakov
license: MIT
version: 1.0.0
---

# writer-tech-docs

Router skill that dispatches to the correct technical documentation variant.

## Variant Detection

**Classify the documentation task before loading any variant reference.**

Check in this order:

1. **Explicit user mention**: "write a README", "API docs for this endpoint", "on-call runbook for alert X", "changelog entry", "release notes for version Y"
2. **File references in context**: `README.md`, `CHANGELOG.md`, `docs/api/`, `runbooks/`
3. **Keywords in the request**:
   - `readme` — README variant
   - `api doc` / `endpoint` / `route` / `reference doc` — api-docs variant
   - `runbook` / `operational` / `procedure` / `how-to` (ops) — runbook-routine variant
   - `on-call` / `alert` / `pagerduty` / `incident response` — runbook-oncall variant
   - `changelog` / `keep a changelog` / `CHANGELOG` — changelog variant
   - `release notes` / `what's new` / `version announcement` — release-notes variant
4. **If still ambiguous**: ask the user once with the list of variants

## Variants

**Each variant has one audience and one expected documentation shape.**

| Variant           | Output                                                | When to use                                 |
| ----------------- | ----------------------------------------------------- | ------------------------------------------- |
| `readme`          | Full README.md: install, usage, API, contributing     | Project/repo documentation, library docs    |
| `api-docs`        | Endpoint reference: params, schemas, errors, examples | Documenting existing endpoints              |
| `runbook-routine` | Step-by-step operational procedures                   | Routine maintenance, deploy, rotate secrets |
| `runbook-oncall`  | Alert response runbook with diagnosis/mitigation      | On-call alerts, incident response           |
| `changelog`       | Developer changelog (Keep a Changelog format)         | Changes between versions, developer-facing  |
| `release-notes`   | User-facing release notes                             | Product updates, version announcements      |

## Loading References

**Load only the reference for the detected variant.**

After detecting the variant, load the corresponding reference:

- `references/readme.md`
- `references/api-docs.md`
- `references/runbook-routine.md`
- `references/runbook-oncall.md`
- `references/changelog.md`
- `references/release-notes.md`

Never load multiple reference files simultaneously. If the user switches context to a different variant, unload and reload.

## Common Principles Across All Variants

**Write durable docs that point to source-of-truth material instead of copying it.**

- **Know your audience**: internal devs, external partners, end users, or on-call engineers
- **Link rather than repeat**: reference existing docs rather than duplicating them
- **Default to Markdown** unless the context specifies another format
- **Flag assumptions**: mark anything you inferred with `[assumed]` if you're not certain
- **Remove placeholder text before outputting**: no `[YOUR_VALUE]` or `[TODO]` left behind
