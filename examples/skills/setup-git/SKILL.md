---
name: setup-git
description: >
  Use this skill whenever the user asks to name a branch, create a branch, suggests a branch name for review,
  mentions Git workflow tasks (starting a feature, fixing a bug, making a hotfix, preparing a release),
  or asks to write, generate, or improve a commit message, or pastes a diff needing a commit.
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# setup-git

A **router** skill for Git conventions. Identify user intent and produce the appropriate output using its reference format.

## Routing Table

| Request Type                                          | Reference                      |
| :---------------------------------------------------- | :----------------------------- |
| Branch naming, branch name review, Git workflow tasks | `references/branch-naming.md`  |
| Commit message generation, improvement, diff commit   | `references/commit-message.md` |
