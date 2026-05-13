---
name: writer-tech-docs
description: >
  Produces technical documentation: README, API docs, runbooks (standard + on-call), changelogs,
  and release notes. Detects the variant from keywords, file references, or user mention.
  Trigger on any request about "README", "API documentation", "document these endpoints",
  "runbook", "operational procedure", "on-call runbook", "alert response", "changelog",
  "Keep a Changelog", "release notes", "what's new", "version announcement", "endpoint docs",
  "API reference", "deploy procedure", "rotate secrets procedure", "how-to guide for operations",
  "incident response playbook", "SRE runbook". Distinct from design-api (contract-first spec)
  and writer-postmortem (incident postmortem).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# writer-tech-docs

Router skill that dispatches to the correct technical documentation variant.

## Variant Detection

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

| Variant           | Output                                                | When to use                                 |
| ----------------- | ----------------------------------------------------- | ------------------------------------------- |
| `readme`          | Full README.md: install, usage, API, contributing     | Project/repo documentation, library docs    |
| `api-docs`        | Endpoint reference: params, schemas, errors, examples | Documenting existing endpoints              |
| `runbook-routine` | Step-by-step operational procedures                   | Routine maintenance, deploy, rotate secrets |
| `runbook-oncall`  | Alert response runbook with diagnosis/mitigation      | On-call alerts, incident response           |
| `changelog`       | Developer changelog (Keep a Changelog format)         | Changes between versions, developer-facing  |
| `release-notes`   | User-facing release notes                             | Product updates, version announcements      |

## Loading References

After detecting the variant, load the corresponding reference:

- `references/readme.md`
- `references/api-docs.md`
- `references/runbook-routine.md`
- `references/runbook-oncall.md`
- `references/changelog.md`
- `references/release-notes.md`

Never load multiple reference files simultaneously. If the user switches context to a different variant, unload and reload.

## Common Principles Across All Variants

- **Know your audience**: internal devs, external partners, end users, or on-call engineers
- **Link rather than repeat**: reference existing docs rather than duplicating them
- **Default to Markdown** unless the context specifies another format
- **Flag assumptions**: mark anything you inferred with `[assumed]` if you're not certain
- **Remove placeholder text before outputting**: no `[YOUR_VALUE]` or `[TODO]` left behind
