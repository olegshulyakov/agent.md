# Tasks

A collection of skills for AI coding agents, modeled after real software team roles.
Each skill is a `SKILL.md` that teaches the agent how to produce a specific artifact — document, code, diagram, report, or plan.

---

## Naming Convention

```text
<type>-<subject>
```

The **type prefix** comes first so skills sort naturally on the filesystem and visually cluster by what they _do_, not what they’re about.

| Prefix       | Produces                                         |
| ------------ | ------------------------------------------------ |
| `audit-`     | Review report with findings and recommendations  |
| `checklist-` | Step-by-step verification list                   |
| `codegen-`   | Source code files                                |
| `design-`    | Design document or spec (contract-first)         |
| `diagram-`   | Visual diagram (C4, DFD, flow, etc.)             |
| `model-`     | Structured model definition                      |
| `patterns-`  | Pattern catalogue with examples                  |
| `planner-`   | Planning document with estimates                 |
| `report-`    | Status or analysis report                        |
| `setup-`     | Configuration files and scaffolding              |
| `strategy-`  | Decision framework and approach                  |
| `template-`  | Reusable blank template                          |
| `tracker-`   | Metrics or progress tracking document            |
| `writer-`    | Authored prose artifact (spec, doc, story, etc.) |

---

## Priority Guide

| Priority | Meaning                                          |
| -------- | ------------------------------------------------ |
| 🔴 P1    | Build first — highest daily leverage, cross-role |
| 🟠 P2    | High value — foundational for a whole domain     |
| 🟡 P3    | Important — core to a specific role              |
| ⚪ P4    | Specialized — niche or lower frequency           |

---

## Skills

Ordered alphabetically by name (matches filesystem order).

### `audit-`

| Done  | Skill              | Priority | Domain       | Primary Role      | Produces                                                                |
| ----- | ------------------ | -------- | ------------ | ----------------- | ----------------------------------------------------------------------- |
| - [ ] | `audit-a11y`       | 🟠 P2    | UI/UX        | Frontend / UX     | Accessibility checklist with annotated findings and fix recommendations |
| - [ ] | `audit-gap`        | 🟡 P3    | Requirements | System Analyst    | Gap analysis report between current and target state                    |
| - [ ] | `audit-secrets`    | 🟠 P2    | Security     | Security Engineer | Secrets exposure report with remediation steps                          |
| - [ ] | `audit-security`   | 🟠 P2    | Security     | Security Engineer | OWASP-aligned security review with severity ratings                     |
| - [ ] | `audit-test-flaky` | 🟡 P3    | Testing      | AQA               | Root cause report for flaky tests with fix recommendations              |

### `checklist-`

| Done  | Skill                   | Priority | Domain     | Primary Role    | Produces                                          |
| ----- | ----------------------- | -------- | ---------- | --------------- | ------------------------------------------------- |
| - [ ] | `checklist-code-review` | 🟠 P2    | Leadership | Team Lead       | Structured PR review checklist by concern area    |
| - [ ] | `checklist-release`     | 🟡 P3    | Release    | Release Manager | Go/no-go release checklist with sign-off sections |

### `codegen-`

| Done  | Skill               | Priority | Domain  | Primary Role  | Produces                                                                                                      |
| ----- | ------------------- | -------- | ------- | ------------- | ------------------------------------------------------------------------------------------------------------- |
| - [ ] | `codegen-backend`   | 🔴 P1    | Code    | Backend Dev   | Production-ready backend code (Python, Node, Go, Java, Ruby, Rust, C#, PHP, Kotlin, Elixir)                   |
| - [ ] | `codegen-frontend`  | 🔴 P1    | Code    | Frontend Dev  | Production-ready frontend code (React, Vue, Angular, Svelte, Next.js, Nuxt, Remix, Astro, SolidJS, SvelteKit) |
| - [ ] | `codegen-mobile`    | 🟠 P2    | Code    | Mobile Dev    | Production-ready mobile code (Swift/iOS, Kotlin/Android, React Native, Flutter)                               |
| - [ ] | `codegen-test-api`  | 🟠 P2    | Testing | AQA / Backend | API test suite with assertions and fixtures                                                                   |
| - [ ] | `codegen-test-e2e`  | 🔴 P1    | Testing | AQA           | End-to-end test scenarios with page objects                                                                   |
| - [ ] | `codegen-test-perf` | 🟡 P3    | Testing | AQA / SRE     | Load and stress test scripts with thresholds                                                                  |

### `design-`

| Done  | Skill           | Priority | Domain       | Primary Role       | Produces                                                      |
| ----- | --------------- | -------- | ------------ | ------------------ | ------------------------------------------------------------- |
| - [ ] | `design-api`    | 🔴 P1    | Code         | Backend Dev        | Contract-first API spec (OpenAPI / AsyncAPI)                  |
| - [ ] | `design-arch`   | 🟠 P2    | Architecture | Solution Architect | System design document with components and tradeoffs          |
| - [ ] | `design-css`    | 🟡 P3    | UI/UX        | Frontend Dev       | Design system tokens, component style guide                   |
| - [ ] | `design-schema` | 🔴 P1    | Database     | DBA / Backend      | Normalized database schema with relationships and constraints |

### `diagram-`

| Done  | Skill                 | Priority | Domain       | Primary Role       | Produces                                                    |
| ----- | --------------------- | -------- | ------------ | ------------------ | ----------------------------------------------------------- |
| - [ ] | `diagram-c4`          | 🟠 P2    | Architecture | Solution Architect | C4 model diagrams (context, container, component, code)     |
| - [ ] | `diagram-dfd`         | 🟡 P3    | Requirements | System Analyst     | Data flow diagram (L0 context through L2 process detail)    |
| - [ ] | `diagram-integration` | 🟡 P3    | Requirements | System Analyst     | Integration map showing system boundaries and data exchange |
| - [ ] | `diagram-ux-flow`     | 🟡 P3    | UI/UX        | UX Designer        | User flows and journey maps                                 |

### `model-`

| Done  | Skill          | Priority | Domain   | Primary Role      | Produces                                           |
| ----- | -------------- | -------- | -------- | ----------------- | -------------------------------------------------- |
| - [ ] | `model-dbt`    | 🟡 P3    | Data     | Data Engineer     | dbt model definitions with tests and documentation |
| - [ ] | `model-threat` | 🟠 P2    | Security | Security Engineer | STRIDE threat model with mitigations               |

### `patterns-`

| Done  | Skill               | Priority | Domain | Primary Role | Produces                                                                              |
| ----- | ------------------- | -------- | ------ | ------------ | ------------------------------------------------------------------------------------- |
| - [ ] | `patterns-auth`     | 🟠 P2    | Code   | Backend Dev  | Auth pattern catalogue (JWT, OAuth2, sessions, API keys) with implementation examples |
| - [ ] | `patterns-graphql`  | 🟡 P3    | Code   | Backend Dev  | GraphQL schema, resolver, and N+1 pattern guide                                       |
| - [ ] | `patterns-realtime` | 🟡 P3    | Code   | Backend Dev  | WebSocket / SSE / polling pattern guide with tradeoffs                                |

### `planner-`

| Done  | Skill                    | Priority | Domain   | Primary Role | Produces                                           |
| ----- | ------------------------ | -------- | -------- | ------------ | -------------------------------------------------- |
| - [ ] | `planner-capacity-db`    | ⚪ P4    | Database | DBA          | Database capacity plan with growth projections     |
| - [ ] | `planner-capacity-infra` | ⚪ P4    | DevOps   | DevOps / SRE | Infrastructure capacity plan with scaling triggers |
| - [ ] | `planner-sprint`         | 🟡 P3    | Agile    | Scrum Master | Sprint plan with goals, capacity, impediment log   |

### `report-`

| Done  | Skill                | Priority | Domain     | Primary Role      | Produces                                                 |
| ----- | -------------------- | -------- | ---------- | ----------------- | -------------------------------------------------------- |
| - [ ] | `report-cve`         | 🟡 P3    | Security   | Security Engineer | CVE triage report with severity, impact, and remediation |
| - [ ] | `report-db-health`   | 🟡 P3    | Database   | DBA               | Database health report (indexes, bloat, slow queries)    |
| - [ ] | `report-team-health` | ⚪ P4    | Leadership | Team Lead         | Team health report (velocity, satisfaction, blockers)    |

### `setup-`

| Done  | Skill                    | Priority | Domain       | Primary Role      | Produces                                                 |
| ----- | ------------------------ | -------- | ------------ | ----------------- | -------------------------------------------------------- |
| - [ ] | `setup-developer-portal` | ⚪ P4    | Platform     | Platform Engineer | Internal developer portal structure with service catalog |
| - [ ] | `setup-eval-harness`     | 🟡 P3    | ML / AI      | ML Engineer       | Model evaluation harness with metrics and baselines      |
| - [ ] | `setup-infra`            | 🟠 P2    | DevOps       | DevOps            | Infrastructure-as-code scaffolding (Terraform / Pulumi)  |
| - [ ] | `setup-monorepo`         | 🟡 P3    | Platform     | Platform Engineer | Monorepo configuration (Nx, Turborepo, Bazel)            |
| - [ ] | `setup-observability`    | 🟠 P2    | DevOps / SRE | DevOps            | Observability stack config (metrics, logs, traces)       |
| - [ ] | `setup-pipeline-cicd`    | 🟠 P2    | DevOps       | DevOps            | CI/CD pipeline config (GitHub Actions, GitLab CI, etc.)  |
| - [ ] | `setup-pipeline-etl`     | 🟡 P3    | Data         | Data Engineer     | ETL pipeline scaffolding with error handling and logging |
| - [ ] | `setup-rag`              | 🟡 P3    | ML / AI      | AI Engineer       | RAG pipeline setup (chunking, embedding, retrieval)      |
| - [ ] | `setup-test-framework`   | 🟠 P2    | Testing      | AQA               | Test framework scaffolding with config and conventions   |

### `strategy-`

| Done  | Skill                         | Priority | Domain   | Primary Role        | Produces                                                        |
| ----- | ----------------------------- | -------- | -------- | ------------------- | --------------------------------------------------------------- |
| - [ ] | `strategy-api-versioning`     | 🟡 P3    | Code     | Backend Dev         | API versioning strategy with deprecation and migration guide    |
| - [ ] | `strategy-backup`             | 🟡 P3    | Database | DBA                 | Backup and recovery strategy with RPO/RTO targets               |
| - [ ] | `strategy-dependency-upgrade` | 🟡 P3    | Release  | DevOps / Team Lead  | Dependency upgrade strategy with risk assessment                |
| - [ ] | `strategy-feature-flag`       | 🟡 P3    | Code     | Team Lead / Backend | Feature flag strategy with rollout and rollback plan            |
| - [ ] | `strategy-test`               | 🟠 P2    | Testing  | AQA / QA            | Test strategy document (scope, levels, tools, coverage targets) |

### `template-`

| Done  | Skill            | Priority | Domain     | Primary Role | Produces                                                        |
| ----- | ---------------- | -------- | ---------- | ------------ | --------------------------------------------------------------- |
| - [ ] | `template-pr`    | 🟡 P3    | Leadership | Team Lead    | Pull request template with sections for context, testing, risks |
| - [ ] | `template-retro` | 🟡 P3    | Agile      | Scrum Master | Retrospective template (what went well, delta, actions)         |

### `tracker-`

| Done  | Skill              | Priority | Domain | Primary Role | Produces                                       |
| ----- | ------------------ | -------- | ------ | ------------ | ---------------------------------------------- |
| - [ ] | `tracker-velocity` | ⚪ P4    | Agile  | Scrum Master | Sprint velocity report with trend and forecast |

### `writer-`

| Done  | Skill                       | Priority | Domain       | Primary Role          | Produces                                                              |
| ----- | --------------------------- | -------- | ------------ | --------------------- | --------------------------------------------------------------------- |
| - [ ] | `writer-adr`                | 🟠 P2    | Architecture | Solution Architect    | Architecture Decision Record (context, decision, consequences)        |
| - [ ] | `writer-alert-rules`        | 🟡 P3    | DevOps / SRE | SRE                   | Alert rule definitions with severity and runbook links                |
| - [ ] | `writer-api-docs`           | 🟠 P2    | Docs         | Tech Writer / Backend | API reference documentation (endpoints, params, examples)             |
| - [ ] | `writer-backlog`            | 🟡 P3    | Agile        | Product Owner         | Groomed backlog with priorities, estimates, and dependencies          |
| - [ ] | `writer-changelog`          | 🟡 P3    | Docs         | Tech Writer           | Developer changelog (grouped by type: added, changed, fixed)          |
| - [ ] | `writer-compliance`         | ⚪ P4    | Security     | Security / Legal      | Compliance documentation (GDPR, SOC2, HIPAA)                          |
| - [ ] | `writer-epic`               | 🟠 P2    | Agile        | Product Owner         | Epic definition with goal, scope, child stories, DoD                  |
| - [ ] | `writer-lineage`            | ⚪ P4    | Data         | Data Engineer         | Data lineage documentation (sources, transforms, destinations)        |
| - [ ] | `writer-mentorship`         | ⚪ P4    | Leadership   | Team Lead             | Mentorship guide with goals, checkpoints, and resources               |
| - [ ] | `writer-migration`          | 🟠 P2    | Database     | DBA                   | Database migration scripts with up/down and validation                |
| - [ ] | `writer-ml-experiment`      | 🟡 P3    | ML / AI      | ML Engineer           | ML experiment report with setup, results, and model card              |
| - [ ] | `writer-postmortem`         | 🟡 P3    | Leadership   | Team Lead / SRE       | Incident postmortem (timeline, root cause, action items)              |
| - [x] | `writer-prd`                | 🔴 P1    | Requirements | PM / PO               | Product Requirements Document (goals, personas, scope, metrics)       |
| - [ ] | `writer-prompt`             | 🟡 P3    | ML / AI      | ML / AI Engineer      | Optimized prompt with system instructions, examples, and eval         |
| - [ ] | `writer-readme`             | 🔴 P1    | Docs         | Tech Writer           | Project README (overview, setup, usage, contributing)                 |
| - [ ] | `writer-release-notes`      | 🟡 P3    | Docs         | Release Manager       | User-facing release notes (features, fixes, upgrade guide)            |
| - [ ] | `writer-runbook`            | 🟡 P3    | Docs         | Tech Writer / SRE     | Operational runbook for routine procedures                            |
| - [ ] | `writer-runbook-oncall`     | 🟡 P3    | DevOps / SRE | SRE                   | On-call runbook with alert responses and escalation paths             |
| - [ ] | `writer-slo`                | 🟡 P3    | DevOps / SRE | SRE                   | SLO definition with indicators, targets, and error budget             |
| - [x] | `writer-spec-data-contract` | 🟡 P3    | Database     | DBA / Data Engineer   | Data contract spec (schema, ownership, SLA, versioning)               |
| - [x] | `writer-spec-design`        | 🟡 P3    | UI/UX        | UX Designer           | Design spec with component annotations and design tokens              |
| - [x] | `writer-spec-functional`    | 🔴 P1    | Requirements | System Analyst        | Functional requirements spec (actors, flows, business rules)          |
| - [x] | `writer-spec-nfr`           | 🟡 P3    | Requirements | SA / Architect        | Non-functional requirements (performance, scalability, security)      |
| - [x] | `writer-spec-tech`          | 🟠 P2    | Requirements | SA / Architect        | Technical specification (orchestrates functional + nfr + integration) |
| - [ ] | `writer-sql`                | 🔴 P1    | Database     | DBA / Backend         | Dialect-aware SQL (Postgres, MySQL, MSSQL, SQLite, Oracle)            |
| - [ ] | `writer-sql-analytics`      | 🟡 P3    | Database     | DBA / Data Engineer   | Analytics SQL (Snowflake, BigQuery, ClickHouse, CockroachDB)          |
| - [ ] | `writer-stakeholder`        | 🟡 P3    | Agile        | PM / PO               | Stakeholder update (status, risks, decisions needed)                  |
| - [ ] | `writer-story-task`         | 🔴 P1    | Agile        | PO / Team Lead        | User stories with acceptance criteria decomposed into dev tasks       |
| - [ ] | `writer-team-agreement`     | ⚪ P4    | Agile        | Scrum Master          | Team working agreement (definition of done, norms, ceremonies)        |
| - [ ] | `writer-tech-radar`         | ⚪ P4    | Architecture | Solution Architect    | Technology radar (adopt, trial, assess, hold)                         |
| - [ ] | `writer-use-case`           | 🟡 P3    | Requirements | System Analyst        | Use case document (actors, preconditions, main/alternate flows)       |

