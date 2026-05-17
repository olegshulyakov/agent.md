---
name: operator-git
description: >
  Handle Git branch naming, branch actions, commit-message drafting, and committing staged changes.
  Use for Git workflow tasks, branch review, commit requests, and diffs needing commit messages.
author: Oleg Shulyakov
license: MIT
version: 1.1.0
---

# operator-git

A **router** skill for Git workflow conventions. First classify the request as either an output workflow or an action workflow, then load the relevant convention reference.

## Workflow Types

### Output workflow

Use when the user asks for text to use elsewhere.

Typical verbs: `give`, `suggest`, `name`, `write`, `generate`, `draft`, `improve`, `review`, `format`.

For pure generation requests, return only the requested artifact unless the user asks for explanation. A branch-name request returns only the branch name. A commit-message request returns only the commit message.

Review requests may include concise feedback because the requested artifact is evaluation, not just generation.

Do not wrap generated artifacts in a sentence, markdown, quotes, or extra explanation unless the user asks for options or rationale.

### Action workflow

Use when the user asks Codex to perform a Git operation in the repository.

Typical verbs: `create`, `checkout`, `switch`, `start`, `commit`, `apply`, `rename`.

For successful actions, run the Git command and do not add extra explanatory output unless the user asks for it or the command output is necessary to understand the result. If an action cannot be completed safely, state the blocker briefly and ask at most one focused question.

For branch actions, create or switch to the branch using the selected branch convention. For commit actions, create the commit using the selected message convention.

## Routing Table

| Request Type                            | Workflow Type      | Reference                      |
| :-------------------------------------- | :----------------- | :----------------------------- |
| Branch name generation                  | Output             | `references/branch-naming.md`  |
| Branch name review                      | Output             | `references/branch-naming.md`  |
| Branch creation, checkout, switch/start | Action             | `references/branch-naming.md`  |
| Commit message generation/improvement   | Output             | `references/commit-message.md` |
| Commit staged changes                   | Action             | `references/commit-message.md` |

## Repository Safety

- Inspect the current branch and worktree before action workflows.
- Do not overwrite, reset, or discard user changes unless the user explicitly asks.
- If a requested branch already exists, switch to it only if that clearly matches the request; otherwise report the conflict briefly.
- For commits, use staged changes as the commit input. Do not stage unrelated files unless the user explicitly asks.
