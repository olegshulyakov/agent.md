---
description: Create a properly named Git branch from a task description
author: Oleg Shulyakov
licence: MIT
version: 1.1.0
---

Create a Git branch based on the provided description.

Format: `<type>/<ticket-id>-<short-description>` (kebab-case, lowercase)

Example types: feature, bugfix, hotfix, release, chore, docs, test, experiment.

Just return the generated branch name, do not include any other text.
