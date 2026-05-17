# User Story Output Format

Use this reference when drafting user stories and developer tasks.

## Template

Use this exact structure. Repeat for each story.

```md
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
