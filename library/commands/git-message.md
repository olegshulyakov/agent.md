---
description: Commit staged changes with a Conventional Commits message after confirmation
author: Oleg Shulyakov
license: MIT
version: 1.1.0
---

Commit the currently staged changes using a Conventional Commits message, refined to match the repository's local commit-message style.

Workflow:

1. Inspect the current branch and staged changes.
2. Inspect recent commit subjects with `git log --pretty=format:%s -n 30`.
3. Generate a Conventional Commits message from the staged changes, using recent history to match the current repository style.
4. Ask the user to confirm the exact commit message before running `git commit`.
5. After confirmation, commit only the staged changes.

Do not stage files. If there are no staged changes, stop and ask what the user wants to stage.

Use the shared convention in the installed `operator-git` skill's `references/commit-message.md`. In short:

```text
<type>(<optional scope>): <short description>

<optional body>

<optional footer>
```

Example types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert.

Prefer scopes from recent history when applicable. If the repository has no clear scope convention, use a short noun from the changed path or omit the scope.

For simple changes, prefer a single-line message unless the repository consistently uses bodies. Include a body only when it adds useful context. Include PR, issue, or ticket identifiers only when they are already known; do not invent one. Do not copy obvious historical mistakes such as misspelled types or malformed headers.

Optionally, in the footer, use `BREAKING CHANGE:` followed by a detailed explanation of the breaking change. Keep the prefix exactly uppercase.

Preserve the confirmed message exactly, including literal backticks or other shell-sensitive characters. Prefer a safe commit path such as `git commit -F <message-file>` for multi-line or shell-sensitive messages.
