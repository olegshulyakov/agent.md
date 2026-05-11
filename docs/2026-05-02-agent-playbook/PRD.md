# PRD: Agent Playbook

## Status

Draft — 2026-05-11
**Author:** Oleg Shulyakov
**Stakeholders:** Developers, AI/LLM tool builders, AI agents

## Problem Statement

Currently, LLM agents lack a standardized, tool-agnostic way to maintain context, memory, rules, and documentation within a software project. Each runtime or IDE handles this differently or relies on external dashboards. This creates fragmentation, loss of context when switching tools, and makes it difficult to version-control or review an agent's behavior alongside the code it governs. The cost of inaction is continued siloing of agent logic and inability to build robust, reproducible AI-assisted development workflows.

## Goals

- Standardize agent configuration
- Enable tool portability
- Improve context retention

## Target Users / Personas

- **Software Engineers / Developers:** Need a predictable way to direct agent behavior and ensure coding standards are followed within their projects without constantly repeating context.
- **AI Agent Runtimes / IDEs:** Need a standard specification to load project-specific rules, skills, and memory into their LLM context window efficiently.

## Scope

### In Scope

- Definition of the `.agents/` folder structure and its core components (`rules/`, `skills/`, `commands/`, `agents/`, `memory/`).
- Specification of the `README.md` entry point for agents.
- Schemas for modular instructions, skills, custom slash commands, and subagent personas.
- Runtime expectations for compliant tools.

### Out of Scope

- Implementation of a specific LLM agent runtime.
- Vendor-specific integrations or proprietary configuration formats.

## Functional Requirements

1. **Playbook Structure Definition**
   1.1 The system shall define a standard `.agents/` folder schema.
   1.2 The system shall specify the structure and purpose of the `.agents/README.md` file.
   1.3 The system shall provide schemas for rules, skills, commands, subagents, and memory.
2. **Runtime Expectations**
   2.1 The system shall list requirements for runtimes to be considered compliant (e.g., auto-loading context, enforcing permissions, triggering skills).

## Non-Functional Requirements (summary)

- **Portability:** Must be tool-agnostic and work with any LLM runtime (Claude, Cursor, GPT, etc.).
- **Security:** Must prohibit storing sensitive credentials in the `.agents/` folder.
- **Maintainability:** Agent behavior should be version-controlled, modular, and human-readable.

## User Journeys / Key Flows

1. **Bootstrapping a new project:** A developer creates a `.agents/README.md` file to initialize the agent context.
2. **Defining a rule:** A developer creates `.agents/rules/code-style/RULE.md` to enforce 2-space indentation. The agent runtime reads this file and automatically applies the rule in future code generation.
3. **Running a skill:** A developer creates a new TypeScript file, triggering a skill defined in `.agents/skills/on-new-file/SKILL.md` which automatically generates a scaffolded test file.

## Assumptions & Dependencies

| Item | Type | Detail |
|------|------|--------|
| LLM tool support | Dependency | LLM IDEs and runtimes will adopt or allow custom configuration reading to support this specification. |
| Markdown adoption | Assumption | Markdown remains the standard format for LLM instructions. |

## Open Questions

- [x] How will runtimes handle conflicting rules defined in different `.agents/rules/` files?

  Advanced agents use Large Language Models (LLMs) to understand the **underlying intent** of conflicting instructions.

  - **Semantic Merging**: If two rules or code changes overlap, the agent analyzes both to synthesize a version that fulfills the logic of both sides.
  - **First-Principles Reasoning**: Agents may ignore rigid rules in favor of a "judgment call" based on the full context of the project.

## Centralized Registry

A centralized registry of common skills and rules to share across projects will be placed in the user's home folder at `~/.agents/`.

## Appendix

- [Agent Playbook v0.0.1](../../PLAYBOOK.md)
