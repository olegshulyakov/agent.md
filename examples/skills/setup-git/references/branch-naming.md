# Branch Naming Guidelines

Produce clear, consistent, and informative Git branch names that follow team best practices.

---

## Branch Name Structure

```text
<type>/<ticket-id>-<short-description>
```

| Part                | Required     | Notes                                         |
| ------------------- | ------------ | --------------------------------------------- |
| `type`              | Yes          | Category prefix (see below)                   |
| `ticket-id`         | If available | Issue/ticket number, e.g. `PROJ-123` or `#42` |
| `short-description` | Yes          | kebab-case summary of the work                |

**Examples:**

- `feature/PROJ-42-user-authentication`
- `bugfix/PROJ-101-fix-login-redirect`
- `hotfix/payment-null-pointer-crash`
- `chore/upgrade-node-18`
- `release/v2.4.0`

---

## Type Prefixes

| Prefix        | When to Use                                                |
| ------------- | ---------------------------------------------------------- |
| `feature/`    | New functionality or user-facing capability                |
| `bugfix/`     | Non-urgent bug fixes going through normal workflow         |
| `hotfix/`     | Urgent fixes that go directly to production/main           |
| `release/`    | Release preparation branches (`release/v1.2.0`)            |
| `chore/`      | Maintenance, dependency updates, config changes, refactors |
| `docs/`       | Documentation-only changes                                 |
| `test/`       | Adding or fixing tests with no production code change      |
| `experiment/` | Exploratory work, spikes, or proof-of-concepts             |

---

## Formatting Rules

1. **kebab-case only** — Use hyphens, never underscores or spaces.
   - ✅ `feature/user-profile-settings`
   - ❌ `feature/user_profile_settings`
   - ❌ `feature/User Profile Settings`

2. **Lowercase** — All characters should be lowercase.
   - ✅ `bugfix/proj-99-fix-api-timeout`
   - ❌ `BugFix/Proj-99-Fix-API-Timeout`

3. **Keep it short but descriptive** — Aim for 3–6 words in the description segment. Max ~60 characters total.
   - ✅ `feature/add-dark-mode-toggle`
   - ❌ `feature/add-a-new-dark-mode-toggle-setting-to-the-user-preferences-page`

4. **No special characters** — Avoid `/`, `\`, `@`, `#`, `~`, `^`, `:`, `?`, `*`, spaces. Hyphens and slashes (for the prefix separator) are the only allowed non-alphanumeric characters.

5. **Include ticket ID when available** — Makes branches traceable to issues.
   - ✅ `bugfix/GH-204-session-expiry-error`
   - ✅ `feature/123-export-to-csv` _(if project uses numeric IDs only)_

6. **No trailing slashes or dots.**
   - ❌ `feature/add-search.`
   - ❌ `feature/`

---

## When the User Provides a Branch Name for Review

Check it against:

- [ ] Correct type prefix used?
- [ ] Ticket ID included (if relevant)?
- [ ] kebab-case, all lowercase?
- [ ] Under ~60 characters?
- [ ] No special characters or spaces?
- [ ] Description is meaningful (not vague like `fix` or `stuff`)?

Give specific, actionable feedback. If the name is mostly fine, say so and suggest a small tweak. If it's unclear what the branch is for, ask what the task is before suggesting a name.
