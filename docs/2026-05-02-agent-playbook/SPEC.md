# Technical Specification: Agent Playbook

## Document Info

**Status:** Draft
**Version:** 1.0
**Date:** 2026-05-11
**Author(s):** Oleg Shulyakov
**Target release:** Initial

---

## 1. Overview

### 1.1 Purpose

This specification defines the standard structure, schemas, and runtime expectations for the Agent Playbook. It provides a standardized, tool-agnostic way to maintain context, memory, rules, and documentation for LLM agents within software projects.

### 1.2 Background

Currently, LLM agents lack a standardized way to maintain context, rules, and memory within a project. Each runtime or IDE handles this differently, creating fragmentation and context loss. The Agent Playbook solves this by providing a unified `.agents/` folder structure and schema that any compliant agent runtime can ingest, ensuring consistent behavior across tools. Link to [PRD](./PRD.md).

### 1.3 Goals

| Goal                            | Success Metric                        | Target                                               |
| ------------------------------- | ------------------------------------- | ---------------------------------------------------- |
| Standardize agent configuration | Adoption of `.agents/` structure      | 100% of defined schemas supported                    |
| Enable tool portability         | Compliant tools can read rules/skills | Support for multiple runtimes (Claude, Cursor, etc.) |
| Improve context retention       | Automated loading of context          | 0 manual context setups per project                  |

### 1.4 Non-Goals

- Implementation of a specific LLM agent runtime.
- Vendor-specific integrations or proprietary configuration formats.
- Updating or modifying existing Agent Runtimes to support this specification.

---

## 2. Functional Requirements

### 2.1 Actors

| Actor         | Description                                                                          |
| ------------- | ------------------------------------------------------------------------------------ |
| Developer     | Creates and manages playbook structures, rules, and skills within the repository.    |
| Agent Runtime | Reads the playbook structure and applies rules/skills to prompt context dynamically. |

### 2.2 Functional Requirements

#### FR-001: Playbook Structure Definition

**Priority:** Must-have
**Actor:** Developer
**Description:** The system shall define a standard `.agents/` folder schema including subdirectories with the following concrete layout:

```text
.agents/
├── rules/
│   ├── code-style.md
│   ├── testing.md
│   └── security.md
├── skills/
│   ├── on-new-file/SKILL.md
│   └── on-test-fail/SKILL.md
├── commands/
│   ├── review.md
│   └── scaffold.md
├── agents/
│   ├── architect.md
│   └── security-auditor.md
└── memory/
    └── MEMORY.md
```

**Acceptance criteria:**

- [ ] The folder structure is clearly documented and reproducible.

#### FR-002: Entry Point Definition

**Priority:** Must-have
**Actor:** Developer
**Description:** The system shall define the structure and purpose of the `AGENTS.md` file at the project root as the primary entry point for agents.
**Acceptance criteria:**

- [ ] Schema and required sections for `AGENTS.md` are documented.

#### FR-003: Schema Provisioning

**Priority:** Must-have
**Actor:** Developer
**Description:** The system shall provide schemas for rules, skills, commands, subagents, and memory files.
**Acceptance criteria:**

- [ ] Markdown schemas are provided for each component type.

#### FR-004: Context Auto-loading

**Priority:** Must-have
**Actor:** Agent Runtime
**Description:** The agent runtime shall automatically load context from `AGENTS.md` and relevant rules based on the user's current directory or task.
**Acceptance criteria:**

- [ ] Compliant runtimes automatically inject rules into the context window.

#### FR-005: Skill Triggering

**Priority:** Should-have
**Actor:** Agent Runtime
**Description:** The agent runtime shall trigger relevant skills based on file context or explicit commands defined in `.agents/skills/`.
**Acceptance criteria:**

- [ ] Skills execute defined actions (e.g., scaffolding test files).
- [ ] Skill schemas document a metadata budget of no more than 100 tokens and an instruction-body budget of no more than 5000 tokens.

---

## 3. Non-Functional Requirements

| Category        | Requirement             | Target                                          | Priority |
| --------------- | ----------------------- | ----------------------------------------------- | -------- |
| Portability     | Tool-agnostic execution | Compatible with major LLM runtimes              | High     |
| Security        | Credential protection   | No sensitive data stored in `.agents/`          | High     |
| Maintainability | Version control         | Playbook files are human-readable and versioned | High     |

---

## 4. System Architecture

### 4.1 Folder Structure Architecture

The Agent Playbook is implemented as a standard directory structure within a repository.

```mermaid
flowchart TD
    RepoRoot[Repository Root] --> AgentsFile[AGENTS.md (Entry Point)]
    RepoRoot --> AgentsFolder[.agents/]
    AgentsFolder --> Rules[rules/]
    AgentsFolder --> Skills[skills/]
    AgentsFolder --> Commands[commands/]
    AgentsFolder --> Agents[agents/]
    AgentsFolder --> Memory[memory/]
```

### 4.2 Component Responsibilities

| Component   | Responsibility                                                                            |
| ----------- | ----------------------------------------------------------------------------------------- |
| `AGENTS.md` | Central registry and bootstrapping instructions for the project's agents.                 |
| `rules/`    | Project-specific constraints and style guidelines (e.g., indentation, language features). |
| `skills/`   | Actionable capabilities the agent can invoke (e.g., scaffolding, linting).                |
| `commands/` | Custom slash commands or macros for developers to use with the agent.                     |
| `agents/`   | Specialized subagent personas or roles (e.g., code reviewer, architect).                  |
| `memory/`   | Ephemeral or long-term state/context for the agent.                                       |

### 4.3 Centralized Registry

- A centralized registry of common skills and rules to share across projects will be placed in the user's home folder at `~/.agents/`.
- **Rationale**: Enables sharing common behavior across multiple projects without duplicating `.agents/` configurations.

---

## 5. Security Considerations

- **Credential Management:** Explicitly prohibit the storage of API keys, tokens, or other sensitive information within the `.agents/` directory.
- **Execution Sandboxing:** Agent runtimes executing skills from `.agents/skills/` must enforce permissions to prevent malicious script execution or unauthorized system access.

---

## 6. Implementation Plan

### Phase 1: Structure and Schema Definition

- [ ] Define the exact markdown structure for `AGENTS.md`.
- [ ] Create schemas for `RULE.md`, `SKILL.md`, and subagent definitions.
- [ ] Document the centralized registry structure (`~/.agents/`).

### Phase 2: Runtime Compliance Guidelines

- [ ] Document expectations for compliant Agent Runtimes.
- [ ] Define conflict resolution strategies (Semantic Merging, First-Principles Reasoning).

---

## 7. Open Questions

| #   | Question | Owner | Due | Status |
| --- | -------- | ----- | --- | ------ |
|     |          |       |     |        |

---

## 8. Appendix

- [PRD: Agent Playbook](./PRD.md)
- [Agent Playbook v0.0.1](../../pages/PLAYBOOK.md)
