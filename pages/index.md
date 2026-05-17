# Agent Playbook

**A portable, tool-agnostic file structure playbook for LLM agents in software projects.**

Agent behavior is code. It should be versioned, reviewed, modular, and readable by both humans and machines. The `.agents/` folder is the single source of truth for everything an LLM agent needs to operate within a project — permissions, instructions, skills, memory, commands, and documentation artifacts.

---

## Why This Exists

Every team using LLM agents invents their own folder structure. Instructions live in random `.md` files, prompts are buried in config, and memory is nowhere. When the runtime changes or someone new joins the project, nothing is discoverable.

This playbook gives agents — and the humans working alongside them — a consistent, predictable home.

---

## Folder Structure

```text
project-root/
├── .agents/
│   ├── rules/                 # Modular instruction files
│   │   └── <rule-name>.md
│   ├── skills/                # Context-invoked workflows
│   │   └── <skill-name>/
│   │       └── SKILL.md
│   ├── commands/              # Custom slash commands
│   │   └── <command-name>.md
│   ├── agents/                # Subagent personas
│   │   └── <agent-persona>.md
│   └── memory/                # Persistent agent memory
│       ├── MEMORY.md          # Long-term memory. Durable facts, preferences, and decisions
│       └── YYYY-MM-DD.md      # Daily notes (UTC timezone). Running context and observations
└── AGENTS.md                  # Primary instruction file + table of contents
```

---

## Core Principles

**Co-location** — Agent files live alongside the code they govern. No external dashboards or separate repos.

**Modularity** — Each concern has its own folder. Adopt only what you need; leave the rest out.

**Composability** — Rules, skills, and subagents can be shared and reused across projects like packages.

**Portability** — Tool-agnostic. Works with Claude, Cursor, GitHub Copilot, or any custom runtime.

**Progressive disclosure** — Start with a single `AGENTS.md`. Add folders only when you have a reason.

---

## Agent PDLC

The Agent PDLC is the working loop for humans and agents building software together: intake, framing, context loading, planning, building, verification, refinement, capture, and learning.

Use it when you want the agent to help with product development work without turning the process into prompt roulette with a meeting invite. It makes intent, context, verification, and learning explicit before the next request arrives.

See the [Agent PDLC diagram](./AGENT_PDLC.md).

---

## Quick Reference

### `AGENTS.md` — Entry Point

The agent's system prompt and manifest. Every runtime loads this first. Contains a `## Loaded Context` table that tells the runtime what else to load and when.

### `.agents/rules/` — Instructions

Composable, single-concern instruction files. Each rule file targets a specific area: code style, testing conventions, security policy, git workflow.

- `rules/code-style.md`
- `rules/security.md`
- `rules/testing.md`

Front matter controls when a rule is injected:

```markdown
---
applies_to: ["**/*.ts"]
priority: high
---
```

### `.agents/skills/` — Context-Invoked Workflows

Skills are reusable procedures the agent can load when the current task matches their metadata, or when the user invokes them directly.

- `skills/on-new-file/SKILL.md` → use when creating source files that need matching tests
- `skills/on-test-fail/SKILL.md` → use when diagnosing failing tests or CI
- `skills/on-commit/SKILL.md` → use when preparing a commit

Use `description` and `when_to_use` to explain when a skill applies. Use `paths` to scope a skill to matching files, and `disable-model-invocation: true` for workflows that should only run when explicitly invoked.

### `.agents/commands/` — Slash Commands

Explicit, user-invoked operations. Registered by the runtime and exposed via its invocation interface.

- `commands/review.md` → /review — structured code review
- `commands/scaffold.md` → /scaffold — generate boilerplate
- `commands/deploy-check.md` → /deploy-check — pre-deployment checklist

### `.agents/agents/` — Subagent Personas

Specialized agents for specific roles. Invoked by `@mention`. Each carries its own identity, constraints, and optional permission overrides.

- `agents/architect.md` → @architect — system design and ADRs
- `agents/reviewer.md` → @reviewer — code review and quality
- `agents/security-auditor.md` → @security — OWASP-focused audit

### `.agents/memory/` — Persistent Memory

Structured, append-only files that persist facts across sessions. Treated as low-confidence context — informative, not authoritative.

- `memory/MEMORY.md` → Long-term memory. Durable facts, preferences, and decisions
- `memory/YYYY-MM-DD.md` → Daily notes (UTC timezone). Running context and observations

---

## Adoption

### Start here (< 5 minutes)

```text
AGENTS.md
```

Write your agent instructions. That's it.

### Playbook setup

```text
AGENTS.md
.agents/
├── rules/
│   └── general.md
└── memory/
    └── MEMORY.md
```

### Full setup

```text
project-root/
├── .agents/
│   ├── rules/
│   ├── skills/
│   ├── commands/
│   ├── agents/
│   └── memory/
└── AGENTS.md
```

---

## Runtime Compliance

A compliant runtime **MUST**:

1. Always load `AGENTS.md` at session start.
2. Enforce permissions defined in `AGENTS.md` before any file operation.
3. Auto-inject all files marked `Auto-load: yes` in `AGENTS.md`.
4. Load skills whose `description`, `when_to_use`, or `paths` match the current context.
5. Register commands from `commands/` and expose them via the invocation interface.
6. Respect subagent boundaries — a subagent must not exceed the parent agent's permissions.

A compliant runtime **SHOULD**:

- Warn when a referenced file in `AGENTS.md` does not exist.
- Surface memory from `memory/` as low-confidence context.
- Prompt the user before executing any shell command.
- Validate permissions configuration and report errors.

---

## Security

- `.agents/` should be committed to version control — it is project configuration, not secrets.
- **Never** store API keys, tokens, or credentials in any `.agents/` file.
- Permissions configuration should always deny access to `**/.env` and `**/secrets/**`.
- Memory files must be reviewed periodically to ensure no sensitive data has been inadvertently captured.
- Subagent personas should have the minimum permissions necessary for their role.

---

## References

- **[PLAYBOOK.md](./PLAYBOOK.md)**
- **[Agent PDLC](./AGENT_PDLC.md)**
- **[library](https://github.com/olegshulyakov/agent.md/tree/main/library)**

---

**Version 0.0.2 — Draft**

_This playbook is intentionally tool-agnostic. Runtimes may extend it provided they do not break compatibility with the core specification._
