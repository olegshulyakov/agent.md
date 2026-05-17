# User Story Examples

Use these examples to calibrate story granularity, acceptance criteria, and developer-task detail.

## Password Reset

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
