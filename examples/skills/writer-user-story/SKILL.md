---
name: writer-user-story
description: >
  Write user stories with acceptance criteria and developer tasks. Use for story writing,
  Jira/Linear/GitHub tickets, task breakdowns, story points, and story-level sprint planning.
author: Oleg Shulyakov
license: MIT
version: 1.0.0
---

# writer-user-story

Produce one or more **user stories** with acceptance criteria, then decompose each into **developer tasks** with file/module hints and effort estimates.

## Why this structure matters

Stories capture user intent and define done. Tasks translate that intent into work a developer can pick up without a meeting. Linking them hierarchically prevents the classic gap where stories are approved but engineers still don't know what to build.

Follow the **3 C's** framework: **Card** (the written story), **Conversation** (the ongoing dialogue that refines scope and details — stories are conversation starters, not specs), **Confirmation** (acceptance criteria that define done).

Use **STAR** as a lightweight quality check when context is available: the situation explains the user's current problem, the task defines the goal, the action appears in the behavior or developer work, and the result is captured in the "so that" clause and acceptance criteria.

## Information gathering

Extract from the user's input:

- **Feature or capability** being described
- **User type(s)** / persona(s)
- **Technical context**: codebase language, framework, relevant modules (if mentioned or inferable)
- **Scope**: single story, or multiple stories for a feature/epic?

If context is sparse, write one exemplary story with a clear note that more context would yield better task breakdowns.

## Output format

Use this exact structure. Repeat for each story.

```
## User-Story [N]: [Short title]

**As a** [user type],
**I want** [action or capability],
**so that** [benefit or outcome].

**Story points:** [estimate: 1 / 2 / 3 / 5 / 8 — Fibonacci]
**Priority:** [High / Medium / Low]

### Acceptance Criteria
- [ ] **Given** [context], **When** [action], **Then** [outcome]
- [ ] **Given** [context], **When** [action], **Then** [outcome]
- [ ] [Edge case or error scenario]
- [ ] [Performance or NFR criterion if relevant]

### Developer Tasks

| # | Task | Effort | Files / Modules |
|---|------|--------|-----------------|
| 1 | [Concrete imperative: "Create X endpoint in Y service"] | [XS/S/M/L] | `path/to/file.ts` |
| 2 | ... | ... | ... |

### Definition of Done
- [ ] All AC pass
- [ ] Unit tests written for business logic
- [ ] Code reviewed and merged
- [ ] [Any environment-specific items if mentioned]
```

## Writing guidance

**Stories:**

- One user value per story — resist the urge to bundle two different user goals
- The "so that" is the most important part — it defines the WHY and prevents gold-plating
- Keep stories simple. Split whenever the card needs multiple personas, unrelated outcomes, or more than one sprint-sized goal.
- Validate each story against **INVEST**:
  - **I**ndependent (self-contained, orderable),
  - **N**egotiable (details emerge through conversation),
  - **V**aluable (delivers user value),
  - **E**stimable (team can size it),
  - **S**mall (fits one sprint),
  - **T**estable (clear pass/fail via AC)
- Write AC in Given/When/Then; each criterion should be independently testable
- Include at least one error/edge-case AC
- Points reflect uncertainty + effort. Anything >5 should be split.
- **Keep the story statement implementation-free** — describe the user goal, not the UI or technology. "I want to invite my friends" not "I want to click an invite button in the settings menu".

**Tasks:**

- Each task is a single coherent unit of developer work (ideally <1 day)
- Use imperative phrasing: "Add", "Create", "Update", "Wire", "Write"
- File hints should be concrete if context allows: `src/api/users.ts`, `UserService.java`
- If you don't know the codebase, use logical module names and note them as `[assumed path]`
- Effort: XS (<1h), S (1–2h), M (half-day), L (full day)

**Estimation:**

- Be honest about uncertainty. If the task involves unknown third-party APIs, say so.
- Flag high-risk tasks with ⚠️

## Splitting stories

If the feature described maps to multiple user goals, split into separate stories. Common split patterns:

- **Happy path + error handling** (different complexity, can ship incrementally)
- **Core feature + admin/configuration** (different user types)
- **Read + write operations** (can be developed in parallel)

## Example

**Input:** "Users should be able to reset their password via email."

```markdown
## User-Story 1: Request password reset

**As a** registered user who has forgotten my password,
**I want** to request a password reset link via my email,
**so that** I can regain access to my account without contacting support.

**Story points:** 3
**Priority:** High

### Acceptance Criteria

- [ ] **Given** I'm on the login page, **When** I click "Forgot password", **Then** I see a form asking for my email
- [ ] **Given** I enter a valid registered email, **When** I submit, **Then** I receive a reset email within 60 seconds
- [ ] **Given** I enter an unregistered email, **When** I submit, **Then** I see a generic "If this email exists, a link was sent" message (no enumeration)
- [ ] Reset link expires after 1 hour

### Developer Tasks

| #   | Task                                             | Effort | Files / Modules                           |
| --- | ------------------------------------------------ | ------ | ----------------------------------------- |
| 1   | Add `POST /auth/forgot-password` endpoint        | S      | `src/auth/auth.controller.ts`             |
| 2   | Implement token generation and storage (TTL: 1h) | S      | `src/auth/reset-token.service.ts`         |
| 3   | Create reset email template                      | XS     | `src/email/templates/reset-password.mjml` |
| 4   | Wire email dispatch via existing mailer service  | XS     | `src/email/email.service.ts`              |
| 5   | Write unit tests for token expiry logic          | S      | `src/auth/reset-token.service.spec.ts`    |
```
