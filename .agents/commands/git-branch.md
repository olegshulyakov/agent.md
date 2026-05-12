---
description: Create a properly named Git branch from a task description
---

Create a Git branch based on the provided description.

## Current state

!`git branch --show-current`

!`git status --short`

## Task

$ARGUMENTS

## Branch naming rules

Format: `<type>/<ticket-id>-<short-description>` (kebab-case, lowercase, max ~60 chars)

**Examples:**

- `feature/PROJ-42-user-authentication`
- `bugfix/PROJ-101-fix-login-redirect`
- `hotfix/payment-null-pointer-crash`
- `chore/upgrade-node-18`
- `release/v2.4.0`

Type prefixes:

| Prefix        | When to Use                                                |
| ------------- | ---------------------------------------------------------- |
| `feature/`    | New functionality or user-facing capability                |
| `bugfix/`     | Non-urgent bug fixes going through normal workflow         |
| `hotfix/`     | Urgent fixes that go directly to production/main           |
| `release/`    | Release preparation branches (e.g. `release/v1.2.0`)       |
| `chore/`      | Maintenance, dependency updates, config changes, refactors |
| `docs/`       | Documentation-only changes                                 |
| `test/`       | Adding or fixing tests with no production code change      |
| `experiment/` | Exploratory work, spikes, or proof-of-concepts             |

Formatting rules:

1. **kebab-case only** — Use hyphens, never underscores or spaces
2. **All lowercase**
3. **Keep it short but descriptive** — Aim for 3–6 words, max ~60 chars total
4. **No special characters** — Avoid `\`, `@`, `#`, `~`, `^`, `:`, `?`, `*`, spaces. Only hyphens and the type separator slash are allowed
5. **Include ticket ID when available** — e.g. `bugfix/GH-204-session-expiry-error`, `feature/123-export-to-csv`
6. **No trailing slashes or dots**

## Steps

1. Infer the branch type from the description if not explicitly provided
2. Extract any ticket/issue ID from the description
3. Generate a valid branch name following the formatting rules above
4. Validate the name against all rules before creating — check type prefix, ticket ID inclusion, kebab-case, length, special characters, and meaningful description
5. Create the branch with `git checkout -b <name>`

## Output

Print the generated branch name and confirm it was created.
