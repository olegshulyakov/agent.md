---
name: strategy-test
description: >
  Produces a test strategy document defining scope, test levels, coverage targets, tooling decisions,
  and quality gates for a project or system. Use this skill whenever the user wants to define a testing
  strategy, plan their QA approach, decide what types of tests to write, determine test coverage targets,
  choose testing tools, or asks to "create a test strategy", "what should our testing approach be",
  "how should we test this system", "define our QA strategy", "what's the right test pyramid for this
  project", or "how much test coverage do we need". Also trigger for "test planning", "testing standards
  document", "QA approach for this release", and "test coverage policy". Distinct from setup-test-framework
  (which sets up the tooling) and codegen-test-e2e (which generates test code).
---

# strategy-test

Produce a **test strategy document** defining what to test, how, with what tools, and to what coverage targets.

## What makes a great test strategy

A test strategy is a team decision document, not a rulebook. It should explain *why* certain trade-offs were made (e.g., why unit tests are prioritized over E2E, why a specific framework was chosen), so the team can evolve it as the system grows.

## Information gathering

From context, identify:
- **System type**: Web app, API, mobile, data pipeline, microservices?
- **Team**: Size, experience level, existing testing culture?
- **Quality attributes**: What matters most — correctness, performance, security, UX?
- **Constraints**: Timeline, team bandwidth, CI/CD capabilities?
- **Existing state**: Greenfield project or adding strategy to existing codebase?

## Output format

```markdown
# Test Strategy: [System / Project Name]

## Status
[Draft | Reviewed | Approved] — [Date]
**Owner:** [QA Lead / Tech Lead name if known]
**Applies to:** [Repository, system, or team scope]

## Context
[1–2 paragraphs: What is this system? What are the key quality risks? Why does testing matter here?]

## Testing Goals

| Goal | Metric | Target |
|------|--------|--------|
| Prevent regressions | New defects caught before merge | > 95% |
| Code coverage | Line coverage (unit + integration) | ≥ 80% |
| Fast feedback | CI pipeline duration | < 10 min |
| Production confidence | Critical path E2E tests | Pass on every deploy |

## Test Pyramid

[Choose the appropriate shape and explain why]

```
        /\
       /E2\       — few, high-value user journeys
      /----\
     / Int  \     — service boundaries, DB integration
    /--------\
   /   Unit   \   — most tests, fast, isolated
  /____________\
```

**Rationale:** [Why this balance — e.g., "We have a stable API contract but complex business logic, so unit tests at the service layer give the highest ROI. E2E covers only the critical checkout and auth flows."]

## Test Levels

### Unit Tests
- **What:** Individual functions, classes, components in isolation
- **Scope:** Business logic, data transformations, validators, utilities
- **Mock strategy:** Mock all external dependencies (DB, HTTP calls, file system)
- **Target coverage:** [e.g., 85% line coverage on `src/services/` and `src/domain/`]
- **Run on:** Every commit (pre-push hook + CI)
- **Tools:** [e.g., Vitest, Pytest, Go testing + testify]

### Integration Tests
- **What:** Multiple components together with real infrastructure (real DB, no HTTP mocks)
- **Scope:** Repository layer, service-to-DB interactions, API endpoint handlers
- **Setup:** [e.g., Docker Compose test environment, TestContainers]
- **Run on:** CI on every PR
- **Tools:** [e.g., Supertest, Pytest + httpx + real DB]

### End-to-End Tests
- **What:** User-facing workflows from browser to backend
- **Scope:** [List critical flows: login, checkout, user registration, payment, etc.]
- **Run on:** CI before staging deployment; blocking for prod
- **Tools:** [e.g., Playwright, Cypress]

### API Contract Tests *(if applicable)*
- **What:** Verify request/response contract between consumer and provider
- **Scope:** [List API boundaries]
- **Tools:** [e.g., Pact]

### Performance Tests *(if applicable)*
- **What:** Load and stress testing of critical paths
- **Scope:** [e.g., Login endpoint, product search API]
- **Thresholds:** [e.g., p95 < 500ms at 100 RPS]
- **Run on:** Weekly scheduled run, before major releases
- **Tools:** [e.g., k6, Gatling]

## Coverage Targets

| Layer | Metric | Threshold | Rationale |
|-------|--------|-----------|-----------|
| Business logic (services) | Line coverage | ≥ 90% | Highest change frequency, highest risk |
| API handlers | Line coverage | ≥ 80% | Auth and validation critical |
| Database layer | Integration tests | Key CRUD operations | No meaningful unit tests for repositories |
| Frontend components | Statement coverage | ≥ 70% | UI logic less critical than business rules |
| E2E flows | N critical paths | All must pass | Non-negotiable for deploy |

**What NOT to cover:** Generated code, third-party library wrappers, simple DTO/entity classes without logic.

## Test Data Strategy

- **Unit tests:** In-memory builders / factories. No external data.
- **Integration tests:** Seeded test database, reset between each test or test file.
- **E2E tests:** Dedicated test accounts and data sets; never use production data.
- **Sensitive data:** Never commit real user data. Use anonymized datasets or generators.

## Quality Gates

| Stage | Gate | On Failure |
|-------|------|-----------|
| Pre-commit | Linting, type check | Block commit |
| PR | Unit + integration tests, coverage threshold | Block merge |
| Staging deploy | E2E suite | Block deploy |
| Prod deploy | Smoke test (critical paths) | Rollback |

## Tooling Decisions

| Purpose | Tool | Rationale |
|---------|------|-----------|
| Unit / integration testing | [Tool] | [Why chosen] |
| E2E testing | [Tool] | [Why chosen] |
| Code coverage | [Tool] | [Why chosen] |
| API contract testing | [Tool] | [Why chosen] |
| Performance testing | [Tool] | [Why chosen] |

## Defect Classification

| Severity | Definition | Response |
|----------|------------|----------|
| P0 — Critical | System down, data loss, security breach | Fix and deploy same day |
| P1 — High | Core feature broken | Fix in current sprint |
| P2 — Medium | Feature degraded, workaround exists | Fix in next sprint |
| P3 — Low | Minor issue, cosmetic | Backlog |

## Responsibilities

| Role | Responsibility |
|------|---------------|
| Developers | Write unit + integration tests for code they author |
| AQA | Write E2E tests, maintain test framework, review coverage |
| Tech Lead | Set and enforce coverage thresholds, quality gates |
| Product | Define critical path for E2E; sign off on acceptance criteria |

## Anti-Patterns to Avoid

- **Testing implementation, not behavior** — tests should break when behavior changes, not when code is refactored
- **Flaky E2E tests** — delete or fix immediately; they erode trust in the suite
- **Coverage theater** — high coverage via trivial tests on getters/setters; measure meaningful coverage
- **Test debt accumulation** — no-coverage PRs merged "just this once" compound into a legacy untested codebase

## Open Questions
- [ ] [Unresolved decision about tooling, scope, or process]
```

## Calibration

- **Greenfield project**: Full strategy document; make opinionated tool recommendations
- **Existing project (no tests)**: Focus on where to start (highest-risk untested areas), incremental targets
- **Specific concern** (e.g., "how should we test this microservice?"): Scope the strategy to that service/domain
- **Team alignment**: Frame as decisions to make together rather than mandates
