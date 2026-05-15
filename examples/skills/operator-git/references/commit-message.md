# Commit Message Guidelines

Generate commit messages in the Conventional Commits format. Use the target repository's recent Git history to refine scope, capitalization, body usage, and footer conventions without abandoning the Conventional Commits structure.

Before generating a message, inspect the relevant diff and recent commit subjects.

## Format

```text
<type>(<optional scope>): <short description>

<optional body>

<optional footer>
```

### Rules

- **First line** (header): match recent repository subjects; keep it concise; no trailing period.
- **Blank line** separates header from body and body from footer.
- **Body**: omit for simple changes. Include only when the change has several meaningful parts or the motivation would otherwise be unclear.
- **Body bullets**: when needed, use `-` bullets and describe what changed and why.
- **Footer**: reserved for metadata such as breaking changes or issue references.

## Repository Style

Infer local preferences from recent commit subjects in the target repository:

- Use `type(scope): summary` when the repository commonly uses scopes and there is a clear package, folder, domain, component, or feature area.
- Use `type: summary` when the change is broad or no scope is clearer.
- Prefer scopes already present in history when they fit. If no local scope pattern exists, derive a short noun from the changed area, such as the package, module, app, command, or documentation section.
- Match the repository's capitalization style after the colon. If history is mixed or unclear, default to lowercase imperative text and preserve proper nouns, acronyms, tool names, and file names.
- Include PR, issue, or ticket suffixes only when they are already known from the user's context, branch name, staged diff, or command output. Do not invent identifiers.
- Preserve quoting style around literal file names, directories, commands, API names, config keys, or package names when that matches the repository or improves clarity.
- For simple commits, return a single-line message unless the repository consistently uses bodies.
- For squash-style or multi-part commits, use a concise header followed by bullets. Do not copy GitHub merge bullet prefixes such as `* feat(...)` into newly generated messages.

Do not imitate obvious historical mistakes such as misspelled types, malformed headers, duplicate prefixes, or accidental copied bullet text. Treat those as evidence that the generator needs guardrails, not as precedent. A little mercy for past commits; none for new ones.

### Types

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

Use only these type names. Convert `feature` to `feat`, and fix obvious type typos.

## Action Words

Treat these user words as commit action intent:

| User wording                         | Git behavior                                      |
| ------------------------------------ | ------------------------------------------------- |
| `commit this`                        | Commit staged changes only                        |
| `commit the staged changes`          | Commit staged changes only                        |
| `create a commit`                    | Commit staged changes only                        |
| `create a commit message and commit` | Generate the message, then commit staged changes  |
| `write a commit message`             | Output a message only, unless commit is requested |

Before committing, inspect staged changes. If nothing is staged, ask whether to stage files or only provide a message. Do not stage files by default.

### Scope (optional)

A short noun in parentheses that clarifies which part of the codebase the change affects.

Prefer scopes from recent history when applicable. If the repository has no clear scope convention, use a short noun from the changed path or omit the scope.

### Short Description

- Imperative mood: "add feature" not "adds feature" or "added feature"
- Lowercase first letter unless the first word is a proper noun or acronym
- No trailing period
- Keep the header compact; if it becomes hard to read, use a body instead of cramming

### Body (optional)

Include when the change is non-obvious, complex, or has multiple independently useful points. Use bullets:

```
- Describe motivation or background
- Explain key decisions made
- Note anything reviewers should pay attention to
```

Avoid a body that merely restates the header.

### Footer (optional)

#### Breaking Changes

Use a `BREAKING CHANGE:` footer when the staged change introduces an incompatible API, behavior, config, data, CLI, or migration change. Keep the prefix exactly uppercase:

```
BREAKING CHANGE: <description of what broke and migration path>
```

#### Issue References

```
Closes #123
Fixes #456
Refs #789
```
