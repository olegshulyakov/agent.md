---
description: Create a properly named Git branch for staged changes after confirmation
author: Oleg Shulyakov
license: MIT
version: 1.2.0
---

Create a Git branch for the currently staged changes.

Workflow:

1. Inspect the current branch and staged changes.
2. Generate a branch name from the staged changes.
3. Ask the user to confirm the branch name before running any Git command that changes repository state.
4. After confirmation, create and switch to the branch.

Branch format: `<type>/<ticket-id>-<short-description>` (kebab-case, lowercase)

Example types: feature, bugfix, hotfix, release, chore, docs, test, experiment.

Use `git switch -c <branch-name>` after confirmation.

If there are no staged changes, stop and ask whether to create a branch from the working tree context instead. Do not stage files.
