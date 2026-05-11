# Agent Playbook

**A portable, tool-agnostic file structure playbook for LLM agents in software projects.**

Agent behavior is code. It should be versioned, reviewed, modular, and readable by both humans and machines. The `.agent/` folder is the single source of truth for everything an LLM agent needs to operate within a project — permissions, instructions, skills, memory, commands, and documentation artifacts.

---

## Why This Exists

Every team using LLM agents invents their own folder structure. Instructions live in random `.md` files, prompts are buried in config, and memory is nowhere. When the runtime changes or someone new joins the project, nothing is discoverable.

This playbook gives agents — and the humans working alongside them — a consistent, predictable home.

---

## Folder Structure

```text
project-root/
└── .agent/
    ├── README.md              # Primary instruction file + table of contents
    ├── rules/                 # Modular instruction files
    │   └── <rule-name>/
    │       └── RULE.md
    ├── skills/                # Auto-invoking workflows (trigger → action)
    │   └── <skill-name>/
    │       └── SKILL.md
    ├── commands/              # Custom slash commands
    │   └── <command-name>/
    │       └── COMMAND.md
    ├── agents/                # Subagent personas
    │   └── <agent-persona>/
    │       └── AGENT.md
    └── memory/                # Persistent agent memory
        ├── MEMORY.md          # Long-term memory. Durable facts, preferences, and decisions
        └── YYYY-MM-DD.md      # Daily notes (UTC timezone). Running context and observations
```

---

## Core Principles

**Co-location** — Agent files live alongside the code they govern. No external dashboards or separate repos.

**Modularity** — Each concern has its own folder. Adopt only what you need; leave the rest out.

**Composability** — Rules, skills, and subagents can be shared and reused across projects like packages.

**Portability** — Tool-agnostic. Works with Claude, Cursor, GitHub Copilot, or any custom runtime.

**Progressive disclosure** — Start with a single `README.md`. Add folders only when you have a reason.

---

## Quick Reference

### `.agent/README.md` — Entry Point

The agent's system prompt and manifest. Every runtime loads this first. Contains a `## Loaded Context` table that tells the runtime what else to load and when.

### `.agent/rules/` — Instructions

Composable, single-concern instruction files. Each rule file targets a specific area: code style, testing conventions, security policy, git workflow.

```text
rules/code-style/RULE.md
rules/security/RULE.md
rules/testing/RULE.md
```

Front matter controls when a rule is injected:

```markdown
---
applies_to: ["**/*.ts"]
priority: high
---
```

### `.agent/skills/` — Auto-Invoking Workflows

Skills are the agent's reflexes — they trigger automatically based on events or file patterns, without the user asking.

```text
skills/on-new-file/SKILL.md      → triggers when a file is created
skills/on-test-fail/SKILL.md     → triggers when CI fails
skills/on-commit/SKILL.md        → triggers before/after a commit
```

### `.agent/commands/` — Slash Commands

Explicit, user-invoked operations. Registered by the runtime and exposed via its invocation interface.

```text
commands/review/COMMAND.md       → /review — structured code review
commands/scaffold/COMMAND.md     → /scaffold — generate boilerplate
commands/deploy-check/COMMAND.md → /deploy-check — pre-deployment checklist
```

### `.agent/agents/` — Subagent Personas

Specialized agents for specific roles. Invoked by `@mention`. Each carries its own identity, constraints, and optional permission overrides.

```text
agents/architect/AGENT.md        → @architect — system design and ADRs
agents/reviewer/AGENT.md         → @reviewer — code review and quality
agents/security-auditor/AGENT.md → @security — OWASP-focused audit
```

### `.agent/memory/` — Persistent Memory

Structured, append-only files that persist facts across sessions. Treated as low-confidence context — informative, not authoritative.

```text
memory/MEMORY.md       → Long-term memory. Durable facts, preferences, and decisions
memory/YYYY-MM-DD.md   → Daily notes (UTC timezone). Running context and observations
```

---

## Adoption

### Start here (< 5 minutes)

```text
.agent/
└── README.md
```

Write your agent instructions. That's it.

### Playbook setup

```text
.agent/
├── README.md
├── rules/
│   └── general/
│       └── RULE.md
└── memory/
    └── MEMORY.md
```

### Full setup

```text
project-root/
└── .agent/
    ├── README.md
    ├── rules/
    ├── skills/
    ├── commands/
    ├── agents/
    └── memory/
```

---

## Runtime Compliance

A compliant runtime **MUST**:

1. Always load `.agent/README.md` at session start.
2. Enforce permissions defined in `README.md` before any file operation.
3. Auto-inject all files marked `Auto-load: yes` in `README.md`.
4. Trigger skills whose `trigger.event` or `trigger.pattern` matches the current context.
5. Register commands from `commands/` and expose them via the invocation interface.
6. Respect subagent boundaries — a subagent must not exceed the parent agent's permissions.

A compliant runtime **SHOULD**:

- Warn when a referenced file in `README.md` does not exist.
- Surface memory from `memory/` as low-confidence context.
- Prompt the user before executing any shell command.
- Validate permissions configuration and report errors.

---

## Security

- `.agent/` should be committed to version control — it is project configuration, not secrets.
- **Never** store API keys, tokens, or credentials in any `.agent/` file.
- Permissions configuration should always deny access to `**/.env` and `**/secrets/**`.
- Memory files must be reviewed periodically to ensure no sensitive data has been inadvertently captured.
- Subagent personas should have the minimum permissions necessary for their role.

---

## Full Playbook

→ **[PLAYBOOK.md](./PLAYBOOK.md)**

---

**Version 0.0.2 — Draft**
_This playbook is intentionally tool-agnostic. Runtimes may extend it provided they do not break compatibility with the core specification._
