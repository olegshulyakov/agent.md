---
name: writer-changelog
description: >
  Produces a developer changelog grouped by type (Added, Changed, Fixed, Deprecated, Removed, Security),
  linked to PRs and issues, following Keep a Changelog format. Use this skill whenever the user wants
  to write a changelog entry, generate release notes for developers, document changes between versions,
  or asks to "write a CHANGELOG entry", "generate a changelog", "document what changed in v2.0",
  "write the changelog for this release", "create a CHANGELOG.md", "what changed in this sprint",
  "summarize these commits into a changelog", or "follow Keep a Changelog format". Also trigger when
  the user provides a list of commits or PRs and wants them organized into a changelog. Distinct from
  writer-release-notes (which is user-facing, not developer-facing) and writer-postmortem
  (which documents incidents).
---

# writer-changelog

Produce a **developer changelog** in Keep a Changelog format, grouped by change type.

## Keep a Changelog format

Always follow [keepachangelog.com](https://keepachangelog.com) conventions:

**Change types:**
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Deprecated features (to be removed in a future version)
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes (always call these out prominently)

## Information gathering

From context, identify:
- **Version**: What version number is this entry for?
- **Date**: Release date
- **Changes**: Commit messages, PR titles, Jira tickets, or a description of what changed
- **Links**: PR numbers, issue tracker URLs (if available)

If given raw commit messages, organize them into appropriate types. If given PR titles, do the same. Fill in what you can; mark unclear items with `[?]`.

## Output format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- [Brief description] ([#XXX](https://github.com/org/repo/pull/XXX))

### Fixed
- [Brief description] ([#XXX](https://github.com/org/repo/issues/XXX))

---

## [2.1.0] — 2024-03-15

### Added
- Support for OAuth2 PKCE flow in the authentication module ([#421](https://github.com/org/repo/pull/421))
- New `--dry-run` flag for the CLI migration command ([#418](https://github.com/org/repo/pull/418))
- REST endpoint `GET /api/v2/users/{id}/sessions` to list active sessions ([#415](https://github.com/org/repo/pull/415))

### Changed
- `createOrder()` now returns the full order object instead of just the ID. Callers may need to update ([#422](https://github.com/org/repo/pull/422))
- Upgraded React from 17 to 18; `ReactDOM.render()` replaced with `createRoot()` ([#409](https://github.com/org/repo/pull/409))
- Default request timeout increased from 5s to 10s ([#407](https://github.com/org/repo/pull/407))

### Deprecated
- `UserAPI.getById(id)` is deprecated; use `UserAPI.findById(id)` instead. Will be removed in v3.0.0 ([#420](https://github.com/org/repo/pull/420))

### Removed
- Removed legacy `v1/auth` endpoints (deprecated since v1.8.0) ([#416](https://github.com/org/repo/pull/416))

### Fixed
- Fixed race condition in session cleanup that caused intermittent 401 errors on logout ([#423](https://github.com/org/repo/pull/423))
- Corrected timezone handling in `formatDate()` — was always using UTC instead of user's timezone ([#419](https://github.com/org/repo/pull/419))
- Fixed memory leak in WebSocket handler when client disconnects unexpectedly ([#414](https://github.com/org/repo/pull/414))

### Security
- **[HIGH]** Fixed SQL injection vulnerability in the search endpoint. Upgrade immediately. CVE-2024-XXXX ([#424](https://github.com/org/repo/pull/424))
- Updated `jsonwebtoken` from 8.5.1 to 9.0.0 to address CVE-2022-23529 ([#412](https://github.com/org/repo/pull/412))

---

## [2.0.0] — 2024-01-20

### ⚠️ Breaking Changes

This is a major release. See the [migration guide](./docs/migration/v1-to-v2.md) for upgrade instructions.

- **[BREAKING]** Renamed `createUser()` to `registerUser()`; old name removed
- **[BREAKING]** Authentication tokens are now JWTs; existing session tokens are invalid
- **[BREAKING]** Minimum Node.js version increased from 14 to 18

### Added
[...]

---

## [1.9.2] — 2023-11-05

### Fixed
- Fixed pagination cursor overflow on very large datasets ([#388](https://github.com/org/repo/pull/388))

### Security
- Bumped `express` to 4.18.2 to resolve prototype pollution vulnerability ([#390](https://github.com/org/repo/pull/390))

---

[Unreleased]: https://github.com/org/repo/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/org/repo/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/org/repo/compare/v1.9.2...v2.0.0
[1.9.2]: https://github.com/org/repo/compare/v1.9.1...v1.9.2
```

## Writing style guidelines

- **Be specific**: "Fixed bug" is useless. "Fixed race condition in session cleanup that caused 401 errors" is actionable.
- **Write for the developer reading it**: Will they know whether to change their code?
- **Note breaking changes prominently**: Use `[BREAKING]` prefix in Changed/Removed sections
- **Note security fixes separately**: Even if a CVE is just a dependency bump, put it in Security
- **Link everything**: Every entry should have a PR or issue link if available
- **Omit non-user-visible internals**: CI config changes, test-only changes, style fixes don't need individual entries (can be batched)

## Commit → changelog mapping

When converting commits to changelog entries:

```
fix: resolve null pointer in payment flow (#432)     → Fixed
feat: add bulk user import via CSV (#429)            → Added
chore: upgrade dependency X to 2.0.0                → Security (if security fix), else omit or batch
refactor: extract service layer from controllers     → omit (internal; no user-visible change)
docs: update API documentation                       → Changed (only if docs are the product)
BREAKING CHANGE: remove deprecated v1 endpoints      → Removed + [BREAKING] prefix
perf: reduce database query count on /users          → Changed (if perf is meaningful to users)
```

## Calibration

- **Single release entry**: Just the section for that version
- **Full CHANGELOG.md**: Multiple versions going back as far as the user provides history
- **From commit log**: Parse and categorize; create the entry
- **Unreleased section**: Add items to the `[Unreleased]` section without a version number
- **Breaking changes release**: Lead with a prominent breaking changes section + migration guide link
