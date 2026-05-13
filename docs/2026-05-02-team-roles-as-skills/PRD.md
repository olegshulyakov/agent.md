# PRD: Software Team Roles as Skills

## Overview

A comprehensive library of 67 skills for CLI Agent (and compatible CLI agents) that gives every software team role a dedicated, well-scoped AI capability. Instead of relying on generic prompting, each skill encodes the conventions, output formats, and domain knowledge specific to a role and artifact type.

## Problem

Any CLI agent is a general-purpose agent. When a DBA asks it to design a schema, or an AQA engineer asks it to generate E2E tests, it produces reasonable output — but without knowledge of team conventions, artifact formats, or role-specific best practices. Every user has to re-explain context every time. There is no shared, reusable, versioned encoding of "how our team does things."

## Goal

Build a skill library that:

- Covers every major software team role
- Produces concrete, named output artifacts (not vague help)
- Groups logically by prefix so the filesystem is self-documenting
- Is built with the `skill-creator` skill so each skill is tested and improvable

## Target Users

| User                  | How They Benefit                                                        |
| --------------------- | ----------------------------------------------------------------------- |
| Individual developers | Role-specific codegen, spec writing, SQL authoring without re-prompting |
| Team leads            | Consistent PR templates, postmortems, code review checklists            |
| Product owners / BAs  | Structured PRDs, epics, stories with acceptance criteria                |
| DBAs                  | Schema design, migrations, query optimization per dialect               |
| AQA engineers         | E2E, API, and performance test generation per framework                 |
| DevOps / SRE          | CI/CD pipeline YAML, IaC, SLOs, runbooks                                |
| Architects            | ADRs, C4 diagrams, system design docs                                   |
| Scrum Masters         | Sprint plans, retro templates, velocity reports                         |
| Security engineers    | Threat models, security audits, CVE triage reports                      |
| Data / ML engineers   | ETL pipelines, dbt models, eval harnesses                               |

## Roles Covered

System Analyst, Product Owner, Product Manager, DBA, AQA, Team Lead, Scrum Master, Solution Architect, Security Engineer, Data Engineer, ML/AI Engineer, Frontend Developer, Backend Developer, Mobile Developer, UI/UX Designer, Tech Writer, DevOps/SRE, Platform Engineer, Release Manager.

## Scope

### In Scope

- 67 skills across 14 prefix groups (see SPEC.md for full list)
- Multi-variant router skills for frontend frameworks, backend languages, mobile platforms, and SQL dialects
- Each skill built and tested via `skill-creator`
- Each skill packaged as a `.skill` file for distribution

### Out of Scope

- Live integrations (Jira, Confluence, GitHub) — future phase
- Team-specific convention overrides — handled via system prompts at install time
- Skills that require real-time data (dashboards, monitoring) — different tool category

## Success Metrics

- Every skill produces a named, concrete output artifact
- No two skills have ambiguous trigger overlap (verified by description optimization)
- Multi-variant router skills correctly identify and route to the right sub-reference without user specifying it
- Each skill passes its eval suite with >80% assertion pass rate

## Non-Goals

- This is not a plugin system — skills are installed locally, not fetched at runtime
- This is not a project management tool — skills produce documents, not workflow automations
- Skills do not store state between sessions

## Constraints

- Each `SKILL.md` must stay under 500 lines; overflow goes into `references/`
- Skills must follow the prefix-first naming convention (see SPEC.md)
- Every skill must have at least 2 test cases in its `evals/evals.json`
- Multi-variant router skills must detect the target variant from context, never ask unless ambiguous

## Build Priority

### Phase 1 — Foundation (highest cross-role leverage)

`writer-prd`, `writer-spec`, `writer-story-task`, `writer-adr`, `design-database`, `writer-sql`, `codegen-backend`, `codegen-frontend`, `codegen-test`

### Phase 2 — Delivery

`writer-epic`, `planner-sprint`, `design-arch`, `diagram-c4`, `setup-pipeline`, `writer-postmortem`, `audit-security`, `writer-tech-docs`

### Phase 3 — Specialist

All remaining skills across Data/ML, Mobile, UI/UX, Platform, Release Management, and Security domains.
