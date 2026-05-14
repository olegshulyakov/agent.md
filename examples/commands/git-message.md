---
description: Commit staged changes with a Conventional Commits message after confirmation
author: Oleg Shulyakov
license: MIT
version: 1.1.0
---

Commit the currently staged changes using a Conventional Commits message.

Workflow:

1. Inspect the current branch and staged changes.
2. Generate a commit message from the staged changes.
3. Ask the user to confirm the exact commit message before running `git commit`.
4. After confirmation, commit only the staged changes.

Do not stage files. If there are no staged changes, stop and ask what the user wants to stage.

Use the structure:

```text
<type>(<optional scope>): <short description>
<optional body>
<optional footer>
```

Example types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert.
Optionally, include a body for more details in bullet points.
Optionally, in the footer, use `BREAKING CHANGE:` followed by a detailed explanation of the breaking change.

Preserve the confirmed message exactly, including literal backticks or other shell-sensitive characters. Prefer a safe commit path such as `git commit -F <message-file>` for multi-line or shell-sensitive messages.
