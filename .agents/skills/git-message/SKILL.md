---
name: git-message
description: Use when the user asks to write, generate, or improve a commit message, or pastes a diff needing a commit.
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# Commit Message Guidelines

This skill produces well-formed commit messages following the **Conventional Commits** specification.

---

## Format

```
<type>(<optional scope>): <short description>

<optional body>

<optional footer>
```

### Rules

- **First line** (header): max 72 characters; imperative mood; no trailing period.
- **Blank line** separates header from body and body from footer.
- **Body**: explain _what_ and _why_, not _how_. Use bullet points (`-`) for multiple points.
- **Footer**: reserved for metadata such as breaking changes or issue references.

---

## Types

| Type       | When to use                               |
| ---------- | ----------------------------------------- |
| `feat`     | A new feature                             |
| `fix`      | A bug fix                                 |
| `docs`     | Documentation changes only                |
| `style`    | Formatting, whitespace — no logic change  |
| `refactor` | Code restructure with no feature/fix      |
| `perf`     | Performance improvement                   |
| `test`     | Adding or updating tests                  |
| `build`    | Build system or dependency changes        |
| `ci`       | CI/CD configuration changes               |
| `chore`    | Maintenance tasks (e.g. updating scripts) |
| `revert`   | Reverts a previous commit                 |

---

## Scope (optional)

A short noun in parentheses that clarifies which part of the codebase the change affects.

Examples: `auth`, `api`, `ui`, `payments`, `parser`, `cli`

---

## Short Description

- Imperative mood: "add feature" not "adds feature" or "added feature"
- Lowercase first letter
- No trailing period
- Max ~72 characters total for the header line

---

## Body (optional)

Include when the change is non-obvious or complex. Use bullet points:

```
- Describe motivation or background
- Explain key decisions made
- Note anything reviewers should pay attention to
```

---

## Footer (optional)

### Breaking Changes

```
BREAKING CHANGE: <description of what broke and migration path>
```

### Issue References

```
Closes #123
Fixes #456
Refs #789
```
