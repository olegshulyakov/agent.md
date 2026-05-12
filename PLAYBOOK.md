# Agent Playbook

> **Version:** 0.0.5
> **Status:** Draft
> **Purpose:** A portable, tool-agnostic playbook for structuring LLM agent context, memory, rules, and documentation inside any software project.

---

## Philosophy

Agent behavior is code. It should be versioned, reviewed, modular, and readable by both humans and machines. The `.agents/` folder is the single source of truth for everything an LLM agent needs to operate within a project — permissions, instructions, skills, memory, commands, and documentation artifacts.

### Core Principles

- **Co-location** — Agent files live alongside the code they govern. No external dashboards required.
- **Modularity** — Each concern (rules, skills, memory, docs) lives in its own folder and can be adopted incrementally.
- **Composability** — Subagents, rules, and skills can be mixed and matched across projects.
- **Portability** — The playbook is tool-agnostic. It should work with any LLM agent runtime (Claude, Cursor, GPT, custom).
- **Progressive disclosure** — Start with just a `AGENTS.md`. Add folders only when needed.

---

## Folder Structure

```text
project-root/
├── AGENTS.md                  # Primary instruction file + table of contents
└── .agents/
    ├── rules/                 # Modular instruction files
    │   └── <rule-name>.md
    ├── skills/                # Auto-invoking workflows (trigger → action)
    │   └── <skill-name>/
    │       └── SKILL.md
    ├── commands/              # Custom slash commands
    │   └── <command-name>.md
    ├── agents/                # Subagent personas
    │   └── <agent-persona>.md
    └── memory/                # Persistent agent memory
        ├── MEMORY.md          # Long-term memory. Durable facts, preferences, and decisions
        └── YYYY-MM-DD.md      # Daily notes (UTC timezone). Running context and observations
```

---

## File & Folder Reference

---

### `AGENTS.md` — Primary Instruction File

Think of `AGENTS.md` as a **README for agents**: a dedicated, predictable place to provide the context and instructions an AI coding agent needs to work on your project.

The agent's entry point. Every runtime MUST load this file first. It serves two roles:

1. **System prompt** — High-level instructions, persona, tone, and behavioral defaults.
2. **Table of contents** — An index of all active agent files so the runtime knows what else to load.

#### Schema

```markdown
# Agent Instructions

## Setup commands

[Commands an agent may need to run, e.g. install, dev, test, lint, build]

## Code style

[Language and style conventions — TypeScript strict mode, single quotes, etc.]

## Loaded Context

<!-- The runtime uses this section to discover and load other files -->

| File                                  | Purpose              | Auto-load |
| ------------------------------------- | -------------------- | --------- |
| rules/code-style.md                   | Coding conventions   | yes       |
| rules/security.md                     | Security constraints | yes       |
| commands/review.md                    | /review command      | on-demand |
| memory/MEMORY.md                      | Long-term memory     | yes       |
| ../docs/auth-redesign/ARCHITECTURE.md | Task architecture    | on-demand |
```

#### Rules

- Must always be present at the project root.
- Must contain a `## Loaded Context` table listing all active files.
- `Auto-load: yes` files are injected into every session. `on-demand` files are loaded only when relevant or explicitly invoked.
- Keep it concise — this is a prompt, not a novel.
- Setup commands, code style, and other recurring instructions should already exist in `README.md`, `.editorconfig`, or committed IDE settings. Prefer referencing those over duplicating them.

---

### `rules/` — Modular Instruction Files

Granular, composable instruction files. Each file governs a single concern. Rules are injected into the context window based on relevance or the `Auto-load` setting in `AGENTS.md`.

#### Naming Convention

```text
rules/<name>.md
```

Examples: `rules/code-style.md`, `rules/security.md`, `rules/testing.md`, `rules/git-workflow.md`, `rules/api-conventions.md`

#### File Schema

```markdown
---
name: Code Style
description: Enforces project coding conventions
applies_to: ["**/*.ts", "**/*.tsx"]
priority: high
---

# Code Style Rules

- Use 2-space indentation
- Prefer `const` over `let`; never use `var`
- All exported functions must have JSDoc comments
  ...
```

#### Rules

- Front matter is optional but recommended for runtime filtering.
- `applies_to` globs tell the runtime when to auto-inject this rule (e.g., only when editing `.ts` files).
- `priority` helps runtimes resolve conflicts between rules. Values: `low | medium | high | critical`.
- Rules should be written as direct imperatives, not suggestions.

---

### `skills/` — Auto-Invoking Workflows

Skills are pre-defined workflows that trigger automatically based on context signals — a file being created, a test failing, a commit being made. They are the agent's "reflexes."

#### Naming Convention

```text
skills/<name>/SKILL.md
```

Examples: `skills/on-new-file/SKILL.md`, `skills/on-test-fail/SKILL.md`, `skills/on-pr-open/SKILL.md`, `skills/on-commit/SKILL.md`

#### File Schema

```markdown
---
name: On New File
trigger:
  event: file_created
  pattern: "src/**/*.ts"
description: Auto-generates a matching test file when a new TypeScript file is created
---

# Skill: On New File

## Trigger

Whenever a new `.ts` file is created in `src/`.

## Workflow

1. Inspect the new file and identify exported functions/classes.
2. Check if a corresponding `.test.ts` file exists in `src/__tests__/`.
3. If not, generate a scaffold test file using the project's test conventions (see `rules/testing.md`).
4. Notify the user: "Created test scaffold at `[path]`."

## Output

- Creates: `src/__tests__/<filename>.test.ts`
- Notifies: Yes
```

#### Rules

- Skills must define a `trigger` — either an `event` or a `pattern` (or both).
- Skills should be idempotent — running them twice should not cause harm.
- Skills may reference other files (rules, docs) in their workflow steps.
- A skill that has no clear trigger should be a `command` instead.

---

### `commands/` — Custom Slash Commands

Explicit, user-invoked operations exposed as slash commands (e.g., `/review`, `/scaffold`).

#### Naming Convention

```text
commands/<name>.md
```

Examples: `commands/review.md`, `commands/scaffold.md`, `commands/deploy-check.md`, `commands/summarize.md`

#### File Schema

````markdown
---
name: review
alias: ["/review", "/cr"]
description: Performs a structured code review on staged or specified files
args:
  - name: target
    type: string
    required: false
    default: "staged"
    description: File path, glob, or 'staged' for git-staged files
---

# Command: /review

## Usage

```text
/review [target]
/review src/auth/login.ts
/review staged
```

## Behavior

1. Load `rules/code-style.md` and `rules/security.md`.
2. Diff the target against `main` (or review the full file if untracked).
3. Produce a structured review in the following format:

### Review Format

**Summary:** [One-line verdict]

**Issues:**
| Severity | Line | Description |
|----------|------|-------------|
| 🔴 Critical | 42 | SQL injection risk — user input not sanitized |
| 🟡 Warning | 88 | Missing null check before `.data` access |
| 🔵 Info | 12 | Consider extracting magic number `3600` to a constant |

**Suggestion:** [Optional refactor idea]
````

#### Rules

- Command names must be lowercase and hyphenated.
- `alias` lists all valid invocation strings.
- `args` defines accepted parameters — the runtime uses this for autocomplete and validation.
- Commands should produce deterministic, structured output.

---

### `agents/` — Subagent Personas

Specialized agent personas that can be invoked for specific tasks. Each subagent has its own identity, capabilities, and behavioral constraints.

#### Naming Convention

```
agents/<name>.md
```

Examples: `agents/reviewer.md`, `agents/architect.md`, `agents/debugger.md`, `agents/writer.md`, `agents/security-auditor.md`

#### File Schema

```markdown
---
name: Architect
invoke: "@architect"
description: Senior software architect focused on system design and technical decisions
inherits: ["rules/general.md"]
overrides:
  temperature: 0.2
  tools: ["file_read", "web_search"]
---

# Subagent: @architect

## Identity

You are a senior software architect with 15 years of experience designing scalable distributed systems. You are opinionated, precise, and always consider long-term maintainability over short-term convenience.

## Responsibilities

- Evaluate architectural decisions and trade-offs
- Produce or review `docs/[YYYY-MM-DD-task-name]/ARCHITECTURE.md`
- Advise on technology choices with explicit rationale
- Flag designs that will not scale or will create debt

## Behavioral Constraints

- Never write implementation code — only design, diagrams, and guidance
- Always provide at least two alternatives before recommending one
- Cite `docs/[YYYY-MM-DD-task-name]/ARCHITECTURE.md` when context is available
- Use ADR (Architecture Decision Record) format for major decisions

## Output Format

Use structured Mermaid diagrams for system visualizations.
```

#### Rules

- `invoke` defines the `@mention` syntax to activate the subagent.
- `inherits` lists rule files that carry over from the parent agent.
- `overrides` allows subagents to override default runtime values (e.g., lower temperature for more deterministic output).
- Subagents should not have broader permissions than the parent agent.

---

### `memory/` — Agent Memory

Persistent storage of facts, decisions, entities, and context that should survive across sessions.

#### Recommended Files

| File            | Purpose                                                      |
| --------------- | ------------------------------------------------------------ |
| `MEMORY.md`     | Long-term memory. Durable facts, preferences, and decisions  |
| `YYYY-MM-DD.md` | Daily notes (UTC timezone). Running context and observations |

#### `MEMORY.md` Schema

```markdown
# Memory

## Facts

- **Project uses Postgres** — Primary database since 2025-01
- **@alex is lead engineer** — Owns payment module

## Preferences

- **Code review** — Prefers concise PR reviews with clear action items
- **Testing** — Requires 80% coverage minimum

## Decisions

### [2025-05-01] Use Postgres over MongoDB

**Context:** Evaluating database for user profile storage.
**Decision:** Chose Postgres for its relational integrity.
**Revisit if:** Need to store unstructured event data at scale.
```

#### `YYYY-MM-DD.md` Schema

```markdown
# 2025-05-01 (UTC)

## Context

Working on user authentication feature.

## Observations

- Found that JWT refresh token rotation is not implemented
- AuthService currently lacks token blacklist

## Next Steps

- [ ] Implement JWT refresh token rotation
- [ ] Add rate limiting to login endpoint
```

#### Rules

- Memory files are append-only by convention. Old entries should not be deleted, only superseded.
- Use `MEMORY.md` for durable facts, preferences, and decisions that should persist long-term.
- Create `YYYY-MM-DD.md` files for daily notes using UTC dates.
- Memory should be treated as low-confidence context — the agent must not treat it as ground truth without verification.
- Sensitive data (tokens, passwords, PII) must never be written to memory files.

---

## Adoption Guide

### Minimal Setup (< 5 min)

```text
AGENTS.md
```

Start with just a `AGENTS.md`. Write your agent instructions. Add folders as needs emerge.

---

### Playbook Setup

```text
AGENTS.md
.agents/
├── rules/
│ ├── general.md
│ └── code-style.md
└── memory/
    └── MEMORY.md
```

---

### Full Setup

Add `skills/`, `commands/`, and `agents/` as the project matures.

---

## Runtime Expectations

A compliant runtime MUST:

1. **Always load** `AGENTS.md` at session start.
2. **Enforce permissions** defined in `AGENTS.md` before any file operation.
3. **Auto-inject** all files marked `Auto-load: yes` in `AGENTS.md`.
4. **Trigger skills** whose `trigger.event` or `trigger.pattern` matches the current context.
5. **Register commands** from `commands/` and expose them via the invocation interface.
6. **Respect subagent boundaries** — a subagent must not exceed the parent agent's permissions.

A compliant runtime SHOULD:

- Warn when a referenced file in `AGENTS.md` does not exist.
- Surface memory from `memory/` as low-confidence context.
- Prompt the user before executing any shell command.
- Validate permissions configuration and report errors.

---

## Versioning & Compatibility

- This playbook follows [Semantic Versioning](https://semver.org/).
- Breaking changes to the playbook require a major version bump.

---

## Security Considerations

- `.agents/` should be committed to version control — it is project configuration, not secrets.
- **Never** store API keys, tokens, or credentials in any `.agents/` file.
- Permissions configuration should always deny access to `**/.env` and `**/secrets/**`.
- Memory files must be reviewed periodically to ensure no sensitive data has been inadvertently captured.
- Subagent personas should have the minimum permissions necessary for their role.

---

## Reference Implementation

This repository uses itself as the reference implementation. The `examples/` folder at the root of this repo is a real, working example of the playbook applied to its own development — governing how agents should assist with writing, reviewing, and evolving the spec itself.

```text
agent.md/ ← this repo
├── examples/ ← reference implementation
│   ├── README.md
│   ├── rules/
│   │ ├── writing-style.md
│   │ └── contribution.md
│   ├── skills/
│   │ └── on-new-example/
│   │     └── SKILL.md
│   ├── commands/
│   │ └── validate.md
│   ├── agents/
│   │ └── spec-reviewer.md
│   └── memory/
│       └── MEMORY.md
├── README.md
├── index.md
└── PLAYBOOK.md
```

Browse the [`examples/`](./examples) folder directly to see real playbook-conformant files.

---

## Example: Real Project Layout

```text
my-saas-app/
├── .agents/
│   ├── rules/
│   │ ├── code-style.md       # TypeScript conventions
│   │ ├── testing.md          # Test coverage requirements
│   │ └── security.md         # OWASP top-10 awareness
│   ├── skills/
│   │ ├── on-new-file/        # Auto-scaffold test files
│   │ │ └── SKILL.md
│   │ └── on-test-fail/       # Diagnose CI failures
│   │     └── SKILL.md
│   ├── commands/
│   │ ├── review.md           # /review — structured code review
│   │ └── scaffold.md         # /scaffold — generate boilerplate
│   ├── agents/
│   │ ├── architect.md        # @architect — system design advisor
│   │ └── security-auditor.md # @security — OWASP-focused review
│   └── memory/
│       └── MEMORY.md
├── src/
├── tests/
├── package.json
└── README.md
```

---

_This playbook is intentionally tool-agnostic. Implementations may extend it with runtime-specific features provided they do not break compatibility with this core specification._
