# Agent Context Standard

**A portable, tool-agnostic file structure standard for LLM agents in software projects.**

Agent behavior is code. It should be versioned, reviewed, modular, and readable by both humans and machines. The `.agent/` folder is the single source of truth for everything an LLM agent needs to operate within a project — permissions, instructions, skills, memory, commands, and documentation artifacts.

---

## Why This Exists

Every team using LLM agents invents their own folder structure. Instructions live in random `.md` files, prompts are buried in config, and memory is nowhere. When the runtime changes or someone new joins the project, nothing is discoverable.

This standard gives agents — and the humans working alongside them — a consistent, predictable home.

---

## Folder Structure

```
project-root/
│
├── docs/                          # Task-scoped documentation
│   ├── <task-name>/
│   │   ├── PRD.md
│   │   ├── SPEC.md
│   │   ├── ARCHITECTURE.md
│   │   ├── DESIGN.md
│   │   └── TASKS.md
│   └── <another-task>/
│       └── ...
│
└── .agent/
    ├── README.md              # Agent entry point + file manifest
    ├── settings.json          # Permissions, preferences, runtime config
    │
    ├── rules/                 # Modular instruction files
    │   ├── general.md
    │   ├── code-style.md
    │   └── security.md
    │
    ├── skills/                # Auto-invoking workflows (trigger → action)
    │   ├── on-new-file.md
    │   └── on-commit.md
    │
    ├── commands/              # Custom slash commands
    │   ├── review.md
    │   └── scaffold.md
    │
    ├── agents/                # Subagent personas
    │   ├── architect.md
    │   └── reviewer.md
    │
    └── memory/                # Persistent agent memory
        ├── index.md
        ├── decisions.md
        └── entities.md
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

### `.agent/settings.json` — Permissions & Config

Declares what the agent can read, write, and execute. `permissions.deny` always wins.

```json
{
  "permissions": {
    "read": ["src/**", "docs/**", ".agent/**"],
    "write": ["src/**", "docs/**", ".agent/memory/**"],
    "deny": ["**/.env", "**/secrets/**"]
  }
}
```

### `.agent/rules/` — Instructions

Composable, single-concern instruction files. Each rule file targets a specific area: code style, testing conventions, security policy, git workflow.

```
rules/code-style.md
rules/security.md
rules/testing.md
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

```
skills/on-new-file.md      → triggers when a file is created
skills/on-test-fail.md     → triggers when CI fails
skills/on-commit.md        → triggers before/after a commit
```

### `.agent/commands/` — Slash Commands

Explicit, user-invoked operations. Registered by the runtime and exposed via its invocation interface.

```
/review [target]     → structured code review
/scaffold [name]     → generate boilerplate
/deploy-check        → pre-deployment checklist
```

### `.agent/agents/` — Subagent Personas

Specialized agents for specific roles. Invoked by `@mention`. Each carries its own identity, constraints, and optional permission overrides.

```
@architect    → system design and ADRs
@reviewer     → code review and quality
@security     → OWASP-focused audit
```

### `.agent/memory/` — Persistent Memory

Structured, append-only files that persist facts across sessions. Treated as low-confidence context — informative, not authoritative.

```
memory/decisions.md   → architectural and technical decisions log
memory/entities.md    → key people, services, and systems
memory/index.md       → table of contents for all memory
```

### `docs/<task>/` — Task Documentation

Documentation lives at the project root, organized by task, feature, or epic. All files are optional — create only what's needed.

```
docs/user-authentication/
├── PRD.md
├── SPEC.md
└── ARCHITECTURE.md

docs/payment-integration/
├── PRD.md
└── TASKS.md
```

---

## Examples

This repo practices what it preaches. The [`.agent/`](./.agent) folder is the reference implementation — every file is a working example of the standard applied to a real project. Use it as a starting point: copy any file, drop it into your project, and adapt it.

---

## Adoption

### Start here (< 5 minutes)

```
.agent/
└── README.md
```

Write your agent instructions. That's it.

### Standard setup

```
.agent/
├── README.md
├── settings.json
├── rules/
│   └── general.md
└── memory/
    └── decisions.md
```

### Full setup

```
project-root/
├── docs/
│   └── <task>/
│       └── *.md
└── .agent/
    ├── README.md
    ├── settings.json
    ├── rules/
    ├── skills/
    ├── commands/
    ├── agents/
    └── memory/
```

---

## Runtime Compliance

A compliant runtime **MUST**:

1. Load `.agent/README.md` at session start.
2. Enforce `permissions.deny` before any file operation.
3. Auto-inject files marked `Auto-load: yes` in the manifest.
4. Trigger skills matching the current event or file pattern.
5. Register and expose commands from `.agent/commands/`.
6. Prevent subagents from exceeding parent agent permissions.

A compliant runtime **SHOULD**:

- Warn when a manifest-referenced file does not exist.
- Treat memory as low-confidence context.
- Prompt before executing shell commands.
- Validate `settings.json` on load.

---

## Security

- Commit `.agent/` to version control — it's configuration, not secrets.
- **Never** store API keys, tokens, or credentials in `.agent/`.
- Always include `**/.env` and `**/secrets/**` in `permissions.deny`.
- Review memory files periodically for inadvertent sensitive data.

---

## Full Specification

→ **[STANDARD.md](./STANDARD.md)**

---

**Version 0.0.1 — Draft**
_This standard is intentionally tool-agnostic. Runtimes may extend it provided they do not break compatibility with the core specification._
