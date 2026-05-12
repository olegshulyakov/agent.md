---
description: Generate a Conventional Commits message from staged changes
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

Write a commit message in the Conventional Commits format for the currently staged changes.

Use the structure:

```text
<type>(<optional scope>): <short description>
<optional body>
<optional footer>
```

Example types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert.
Optionally, include a body for more details in bullet points.
Optionally, in the footer, use `BREAKING CHANGE:` followed by a detailed explanation of the breaking change.

Just return the commit message, do not include any other text.
