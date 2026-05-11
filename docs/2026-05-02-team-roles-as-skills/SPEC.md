# SPEC: Software Team Roles as Skills — Technical Specification

## Concept

Each skill encodes a specific capability of a software team role. A role (e.g. System Analyst) produces multiple artifact types (functional specs, use cases, data flow diagrams, gap analyses), so it maps to multiple skills. Conversely, one skill type (e.g. `codegen-backend`) serves multiple roles (Backend Dev, Team Lead). The library works both ways:

- **Role → Skills:** install all skills for a role to give the agent a complete role capability
- **Skill → Roles:** install individual skills across roles to solve a specific artifact need

## Naming Convention

All skills use prefix-first naming: `<type>-<subject>`

This groups related skills together on the filesystem automatically. The type is the kind of artifact produced; the subject is the domain or topic.

```text
<type>-<subject>[-<variant>]
```

**Valid types:**
`audit` · `checklist` · `codegen` · `design` · `diagram` · `model` · `patterns` · `planner` · `report` · `setup` · `strategy` · `template` · `tracker` · `writer`

**Multi-variant skills** append a variant suffix only when domains are significantly distinct (e.g., `writer-sql-analytics`). For most domains, variants are handled dynamically by the router skill.

---

## Filesystem Layout

```text
skills/
├── audit-a11y/
├── audit-gap/
├── audit-secrets/
├── audit-security/
├── audit-test-flaky/
├── checklist-code-review/
├── checklist-release/
├── codegen-backend/
├── codegen-frontend/
├── codegen-mobile/
├── codegen-test/
├── design-api/
├── design-arch/
├── design-css/
├── design-schema/
├── diagram-c4/
├── diagram-dfd/
├── diagram-integration/
├── diagram-ux-flow/
├── model-dbt/
├── model-threat/
├── patterns-auth/
├── patterns-graphql/
├── patterns-realtime/
├── planner-capacity/
├── planner-sprint/
├── report-cve/
├── report-db-health/
├── report-team-health/
├── setup-developer-portal/
├── setup-eval-harness/
├── setup-infra/
├── setup-monorepo/
├── setup-observability/
├── setup-pipeline/
├── setup-rag/
├── setup-test-framework/
├── strategy-api-versioning/
├── strategy-backup/
├── strategy-dependency-upgrade/
├── strategy-feature-flag/
├── strategy-test/
├── template-pr/
├── template-retro/
├── tracker-velocity/
├── writer-adr/
├── writer-alert-rules/
├── writer-api-docs/
├── writer-backlog/
├── writer-changelog/
├── writer-compliance/
├── writer-epic/
├── writer-lineage/
├── writer-mentorship/
├── writer-migration/
├── writer-ml-experiment/
├── writer-postmortem/
├── writer-prd/
├── writer-prompt/
├── writer-readme/
├── writer-release-notes/
├── writer-runbook/
├── writer-slo/
├── writer-spec/
├── writer-sql/
├── writer-sql-analytics/
├── writer-stakeholder/
├── writer-story-task/
├── writer-team-agreement/
├── writer-tech-radar/
└── writer-use-case/
```

---

## Skill Structure (per skill)

```text
<skill-name>/
├── SKILL.md              # Required. YAML frontmatter + instructions. Max 500 lines.
├── evals/
│   └── evals.json        # Min 10 test cases
└── references/           # Optional. Large reference files, loaded on demand.
    ├── <variant-a>.md
    └── <variant-b>.md
```

### SKILL.md Frontmatter (required fields)

```yaml
---
name: <skill-name>
description: >
  <When to trigger + what it produces. Be specific about output artifact.
   Lean toward over-triggering — mention related keywords and contexts.>
---
```

---

## Full Skill Catalog (71 skills)

### 📋 Requirements (6)

| Skill                 | Roles             | Output Artifact                                                           |
| --------------------- | ----------------- | ------------------------------------------------------------------------- |
| `writer-prd`          | PM, PO            | Product Requirements Document with goals, personas, scope, metrics        |
| `writer-spec`         | SA, Architect, UX | Specification doc (functional, technical, NFR, design, data-contract)     |
| `writer-use-case`     | System Analyst    | Use case document with actors, preconditions, main/alt flows              |
| `diagram-dfd`         | System Analyst    | Data flow diagram (Mermaid or structured text)                            |
| `audit-gap`           | System Analyst    | Gap analysis report: current state vs target state, with remediation list |
| `diagram-integration` | System Analyst    | Integration map: systems, APIs, data flows, ownership                     |

**Trigger disambiguation:**

- `writer-prd` → triggered by business goals, personas, success metrics language
- `writer-spec` → triggered by "write a spec", "tech spec", "TDD", "functional requirements", "non-functional requirements", "NFR", "data contract", "UI spec", "handoff doc"

#### Multi-variant: `writer-spec`

```text
writer-spec/
├── SKILL.md
└── references/
    ├── functional.md     # Business rules, actors, main/alt flows
    ├── technical.md      # System architecture, integrations, data flow
    ├── non-functional.md # Performance, security, scalability targets
    ├── design-ui.md      # UI tokens, spacing, component states
    └── data-contract.md  # Schema, ownership, versioning, SLA
```

---

### 🔄 Planning & Agile (8)

| Skill                   | Roles         | Output Artifact                                                             |
| ----------------------- | ------------- | --------------------------------------------------------------------------- |
| `writer-prd`            | PM, PO        | (see Requirements)                                                          |
| `writer-epic`           | PO            | Epic: goal, value, child story list, definition of done                     |
| `writer-story-task`     | PO, Team Lead | Hierarchical: story with AC → developer tasks with file hints and estimates |
| `writer-backlog`        | PO            | Groomed backlog: prioritized, sized, dependency-flagged                     |
| `writer-stakeholder`    | PM, PO        | Stakeholder update: progress, risks, decisions needed                       |
| `planner-sprint`        | Scrum Master  | Sprint plan: goal, stories, capacity, impediment section                    |
| `template-retro`        | Scrum Master  | Retrospective template: went well / improve / actions                       |
| `tracker-velocity`      | Scrum Master  | Sprint metrics report: velocity, completion rate, trend                     |
| `writer-team-agreement` | Scrum Master  | Working agreements: DoD, DoR, communication norms                           |

**Trigger disambiguation:**

- `writer-story-task` → triggered by breaking down a story into tasks, implementation steps
- `writer-epic` → triggered by creating or defining an epic, feature grouping
- `planner-sprint` → triggered by sprint planning, capacity, sprint goal

---

### 🏛️ Architecture (4)

| Skill               | Roles                | Output Artifact                                                        |
| ------------------- | -------------------- | ---------------------------------------------------------------------- |
| `design-arch`       | Architect            | System design document: components, interactions, trade-offs           |
| `writer-adr`        | Architect, Team Lead | Architecture Decision Record: context, options, decision, consequences |
| `diagram-c4`        | Architect            | C4 diagram: Context / Container / Component / Code levels              |
| `writer-tech-radar` | Architect            | Tech radar: adopt / trial / assess / hold, with rationale              |

**Trigger disambiguation:**

- `design-arch` → high-level design document with prose and trade-offs
- `diagram-c4` → user explicitly wants a diagram, C4 levels, visual output
- `writer-adr` → recording a specific decision already made or being made

---

### 🗄️ Database (6)

| Skill                  | Roles         | Output Artifact                                                           |
| ---------------------- | ------------- | ------------------------------------------------------------------------- |
| `design-schema`        | DBA           | Normalized schema: tables, columns, types, PKs, FKs, indexes              |
| `writer-sql`           | DBA, Backend  | SQL queries/DDL for OLTP dialects: Postgres, MySQL, MSSQL, SQLite, Oracle |
| `writer-sql-analytics` | DBA, Data Eng | SQL for analytics dialects: Snowflake, BigQuery, ClickHouse, CockroachDB  |
| `writer-migration`     | DBA           | Migration scripts: up/down, safe for production, idempotent               |
| `report-db-health`     | DBA           | DB health report: slow queries, bloat, index usage, replication lag       |
| `strategy-backup`      | DBA           | Backup strategy: schedule, retention, restore SLAs, tooling               |

**Trigger disambiguation:**

- `writer-sql` → OLTP: transactional queries, stored procedures, standard DDL
- `writer-sql-analytics` → analytical: window functions, partitioning, warehouse-specific syntax
- `design-schema` → designing the structure, not writing queries

#### Multi-variant: `writer-sql`

```text
writer-sql/
├── SKILL.md          # Detects dialect from context or asks once
└── references/
    ├── postgres.md   # JSONB, CTEs, EXPLAIN ANALYZE, pg-specific types
    ├── mysql.md      # Engine differences, EXPLAIN, charset considerations
    ├── mssql.md      # T-SQL, execution plans, TempDB patterns
    ├── sqlite.md     # Type affinity, limitations, WITHOUT ROWID
    └── oracle.md     # PL/SQL, hints, dual table, sequences
```

#### Multi-variant: `writer-sql-analytics`

```text
writer-sql-analytics/
├── SKILL.md
└── references/
    ├── bigquery.md       # ARRAY/STRUCT, partitioning, INFORMATION_SCHEMA
    ├── snowflake.md      # Variant type, clustering, time travel
    ├── clickhouse.md     # MergeTree, materialized views, sparse indexes
    └── cockroachdb.md    # Distributed SQL, geo-partitioning, follower reads
```

---

### 💻 Code Generation (9)

| Skill                     | Roles                  | Output Artifact                                                  |
| ------------------------- | ---------------------- | ---------------------------------------------------------------- |
| `codegen-frontend`        | Frontend Dev           | Frontend code: components, pages, state management               |
| `codegen-backend`         | Backend Dev            | Backend code: routes, services, middleware, tests                |
| `codegen-mobile`          | Mobile Dev             | Mobile code: screens, navigation, platform-specific patterns     |
| `design-api`              | Backend Dev            | API contract: OpenAPI/AsyncAPI spec, endpoints, schemas          |
| `strategy-api-versioning` | Backend Dev, Architect | API versioning strategy + deprecation guide + migration notes    |
| `patterns-auth`           | Backend Dev            | Auth implementation: JWT, OAuth2, session, RBAC patterns         |
| `patterns-graphql`        | Backend Dev            | GraphQL: schema, resolvers, N+1 prevention, pagination           |
| `patterns-realtime`       | Backend Dev            | Real-time: WebSocket, SSE, polling strategy selection            |
| `strategy-feature-flag`   | Team Lead, Backend     | Feature flag strategy: rollout plan, flag lifecycle, kill switch |

**Trigger disambiguation:**

- `design-api` → contract-first, produces OpenAPI spec before any code is written
- `writer-api-docs` → reference documentation for an existing API

#### Multi-variant: `codegen-frontend`

```text
codegen-frontend/
├── SKILL.md          # Detects framework from imports, package.json, or file extensions
└── references/
    ├── react.md      # Hooks, RSC, Tailwind, React Query
    ├── vue.md        # Composition API, Pinia, Vue Router
    ├── angular.md    # Services, RxJS, NgModules, signals
    ├── svelte.md     # Stores, reactive declarations, SvelteKit
    ├── nextjs.md     # App router, server actions, metadata API
    ├── nuxt.md       # Auto-imports, composables, Nitro
    ├── remix.md      # Loaders, actions, nested routes
    ├── astro.md      # Islands, content collections, SSG/SSR
    └── solidjs.md    # Signals, createStore, SolidStart
```

#### Multi-variant: `codegen-backend`

```text
codegen-backend/
├── SKILL.md          # Detects language from file extension, imports, or asks once
└── references/
    ├── python.md     # FastAPI/Django, type hints, Poetry, async patterns
    ├── nodejs.md     # Express/Fastify, ESM, async/await, Zod
    ├── go.md         # stdlib patterns, goroutines, modules, error wrapping
    ├── java.md       # Spring Boot, Maven/Gradle, records, streams
    ├── ruby.md       # Rails conventions, ActiveRecord, gems, RSpec
    ├── rust.md       # Cargo, ownership, Axum, error handling with anyhow
    ├── csharp.md     # .NET minimal APIs, EF Core, LINQ, async/await
    ├── php.md        # Laravel, Eloquent, Artisan, Pest
    ├── kotlin.md     # Spring Boot / Ktor, coroutines, data classes
    └── elixir.md     # Phoenix, Ecto, OTP, pattern matching
```

#### Multi-variant: `codegen-mobile`

```text
codegen-mobile/
├── SKILL.md          # Detects platform from file extension or project structure
└── references/
    ├── swift.md          # SwiftUI, Combine, Swift concurrency, SPM
    ├── kotlin-android.md # Jetpack Compose, Coroutines, Hilt, Room
    ├── react-native.md   # Expo, navigation, NativeWind, MMKV
    └── flutter.md        # Widgets, Riverpod, go_router, freezed
```

---

### 🎨 UI/UX (3)

| Skill             | Roles            | Output Artifact                                                     |
| ----------------- | ---------------- | ------------------------------------------------------------------- |
| `diagram-ux-flow` | UX Designer      | User flow / journey map in structured Mermaid or text format        |
| `audit-a11y`      | Frontend Dev, UX | Accessibility audit: WCAG violations, severity, fix recommendations |
| `design-css`      | Frontend Dev     | Design system: tokens, component styles, spacing scale, typography  |

---

### 🧪 Testing (4)

| Skill                  | Roles   | Output Artifact                                                  |
| ---------------------- | ------- | ---------------------------------------------------------------- |
| `codegen-test`         | AQA     | Test suite (E2E, API, Performance) with page objects and scripts |
| `strategy-test`        | AQA, QA | Test strategy: scope, types, coverage targets, tooling decisions |
| `setup-test-framework` | AQA     | Test framework setup: config, folder structure, CI integration   |
| `audit-test-flaky`     | AQA     | Flaky test report: root cause analysis, fix recommendations      |

#### Multi-variant: `codegen-test`

```text
codegen-test/
├── SKILL.md
└── references/
    ├── e2e.md    # Playwright, Cypress, Selenium patterns
    ├── api.md    # Supertest, Jest-extended, Postman/Newman
    └── perf.md   # k6, JMeter, Locust scripts
```

---

### 🚀 DevOps / SRE (6)

| Skill                 | Roles       | Output Artifact                                              |
| --------------------- | ----------- | ------------------------------------------------------------ |
| `setup-pipeline`      | DevOps      | Pipeline config (CI/CD, ETL) with logging and error handling |
| `setup-infra`         | DevOps      | IaC: Terraform/Pulumi modules for target cloud               |
| `planner-capacity`    | DevOps, SRE | Capacity plan: traffic and storage projections, sizing       |
| `setup-observability` | DevOps, SRE | Observability setup: metrics, logs, traces, dashboards       |
| `writer-slo`          | SRE         | SLO definition: SLI, target, error budget, alerting policy   |
| `writer-alert-rules`  | SRE         | Alert rules: conditions, severity, routing, runbook links    |

#### Multi-variant: `setup-pipeline`

```text
setup-pipeline/
├── SKILL.md
└── references/
    ├── cicd.md    # GitHub Actions, GitLab CI, Jenkins
    └── etl.md     # dbt, Airflow, Glue patterns
```

#### Multi-variant: `planner-capacity`

```text
planner-capacity/
├── SKILL.md
└── references/
    ├── db.md      # Storage, IOPS, connection pool sizing
    └── infra.md   # Compute, memory, scaling thresholds
```

---

### 🏗️ Platform (2)

| Skill                    | Roles        | Output Artifact                                                        |
| ------------------------ | ------------ | ---------------------------------------------------------------------- |
| `setup-monorepo`         | Platform Eng | Monorepo setup: tooling config (Nx/Turborepo), workspace structure     |
| `setup-developer-portal` | Platform Eng | Developer portal: service catalog, internal docs structure, onboarding |

---

### 🔐 Security (5)

| Skill               | Roles           | Output Artifact                                                          |
| ------------------- | --------------- | ------------------------------------------------------------------------ |
| `model-threat`      | Security Eng    | Threat model: STRIDE analysis, attack surface, mitigations               |
| `audit-security`    | Security Eng    | Security audit: OWASP checklist, findings, severity, remediation         |
| `audit-secrets`     | Security Eng    | Secrets audit: exposed credentials, rotation plan, vault migration       |
| `writer-compliance` | Security, Legal | Compliance doc: GDPR/SOC2/HIPAA controls, evidence checklist             |
| `report-cve`        | Security Eng    | CVE triage report: affected versions, severity (CVSS), remediation steps |

---

### 📊 Data & ML (6)

| Skill                  | Roles      | Output Artifact                                                        |
| ---------------------- | ---------- | ---------------------------------------------------------------------- |
| `model-dbt`            | Data Eng   | dbt model: SQL + schema.yml + tests + documentation                    |
| `writer-lineage`       | Data Eng   | Data lineage doc: source → transformation → consumer map               |
| `writer-ml-experiment` | ML Eng     | ML experiment: hypothesis, setup, metrics, results, model card section |
| `writer-prompt`        | ML, AI Eng | Prompt engineering: system prompt, few-shot examples, eval criteria    |
| `setup-rag`            | AI Eng     | RAG pipeline: chunking strategy, embedding, retrieval, reranking       |
| `setup-eval-harness`   | ML Eng     | Eval harness: metrics, dataset, scoring rubric, benchmark runner       |

---

### 📝 Documentation (5)

| Skill                  | Roles                | Output Artifact                                                    |
| ---------------------- | -------------------- | ------------------------------------------------------------------ |
| `writer-readme`        | Tech Writer          | README: overview, install, usage, contributing; scoped by audience |
| `writer-api-docs`      | Tech Writer, Backend | API reference documentation for existing APIs                      |
| `writer-runbook`       | Tech Writer, SRE     | Runbook guide: operational steps and on-call responses             |
| `writer-changelog`     | Tech Writer          | Changelog: grouped by type (feat/fix/breaking), linked to PRs      |
| `writer-release-notes` | Release Manager      | User-facing release notes: what's new, what's fixed, upgrade notes |

**Trigger disambiguation:**

- `writer-readme` → project intro, targeted at new users or contributors
- `writer-api-docs` → reference docs for existing API endpoints
- `design-api` → contract-first spec before implementation

#### Multi-variant: `writer-runbook`

```text
writer-runbook/
├── SKILL.md
└── references/
    ├── routine.md    # Standard operational procedures
    └── oncall.md     # Emergency response, alert triage
```

---

### 👥 Team & Leadership (5)

| Skill                   | Roles          | Output Artifact                                                         |
| ----------------------- | -------------- | ----------------------------------------------------------------------- |
| `checklist-code-review` | Team Lead      | Code review checklist: correctness, style, security, performance        |
| `writer-postmortem`     | Team Lead, SRE | Postmortem: timeline, root cause, impact, action items                  |
| `template-pr`           | Team Lead      | PR template: description, checklist, test plan, screenshots             |
| `report-team-health`    | Team Lead      | Team health report: delivery metrics, morale signals, risks             |
| `writer-mentorship`     | Team Lead      | Mentorship guide: growth areas, resources, milestones, feedback cadence |

---

### 📦 Release Management (2)

| Skill                         | Roles                   | Output Artifact                                                         |
| ----------------------------- | ----------------------- | ----------------------------------------------------------------------- |
| `checklist-release`           | Release Manager         | Release checklist: pre/during/post deployment steps, rollback criteria  |
| `strategy-dependency-upgrade` | Release Manager, DevOps | Dependency upgrade strategy: audit, upgrade path, PR checklist, testing |

---

## Build Process (per skill)

Each skill is built using the `skill-creator` skill in this sequence:

1. **Draft** `SKILL.md` with frontmatter, instructions, output template
2. **Write** `evals/evals.json` with ≥2 test cases
3. **Run** test cases via `skill-creator` eval loop
4. **Review** outputs qualitatively; grade assertions quantitatively
5. **Iterate** until >80% assertion pass rate and user satisfied
6. **Optimize** description for triggering accuracy
7. **Package** via `scripts/package_skill` → `.skill` file

## Multi-Variant Router Pattern

For `codegen-frontend`, `codegen-backend`, `codegen-mobile`, `codegen-test`, `writer-sql`, `writer-sql-analytics`, `writer-spec`, `setup-pipeline`, `writer-runbook`, `planner-capacity`:

The `SKILL.md` must:

1. Detect the target variant from context (file extensions, imports, `package.json`, explicit mention)
2. Load the correct `references/<variant>.md`
3. Only ask the user to specify if detection is genuinely ambiguous
4. Never load multiple reference files simultaneously

```markdown
## Variant Detection

Check in this order:

1. File extensions in context (.tsx → React, .vue → Vue, .py → Python)
2. Import statements or package names
3. Explicit user mention
4. If still ambiguous: ask once with short options list
```

## Trigger Collision Prevention

Skills with overlapping domains must have explicit disambiguation in their descriptions. High-risk pairs and their resolution:

| Pair                                 | Disambiguation Rule                                                |
| ------------------------------------ | ------------------------------------------------------------------ |
| `writer-prd` vs `writer-spec`        | PRD = business goals; spec = system behavior or technical detail   |
| `design-api` vs `writer-api-docs`    | design-api = contract first (no code yet); api-docs = existing API |
| `design-arch` vs `diagram-c4`        | design-arch = prose document; diagram-c4 = diagram output          |
| `design-schema` vs `writer-sql`      | design-schema = structure design; writer-sql = query/DDL writing   |
| `writer-story-task` vs `writer-epic` | story-task = single story → tasks; epic = feature grouping         |

## Totals

| Category                                    | Count |
| ------------------------------------------- | ----- |
| Total skills                                | 71    |
| Multi-variant router skills                 | 10    |
| Total framework/language/dialect references | 50+   |
| Prefix types                                | 14    |
