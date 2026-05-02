# Agent Context Standard

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

> A portable, tool-agnostic file structure standard for LLM agents in software projects.

Agent behavior is code. It should be versioned, reviewed, and readable by both humans and machines. This standard defines where agent instructions, rules, skills, memory, commands, and documentation live — consistently, across any project and any runtime.

---

## At a Glance

```
project-root/
├── docs/                     # Task-scoped documentation
│   └── <task-name>/
│       ├── PRD.md
│       ├── SPEC.md
│       ├── ARCHITECTURE.md
│       ├── DESIGN.md
│       └── TASKS.md
│
└── .agent/
    ├── README.md             # Agent entry point + file manifest
    ├── settings.json         # Permissions & runtime config
    ├── rules/                # Modular instruction files
    │   └── <rule-name>/
    │       └── RULE.md
    ├── skills/               # Auto-invoking workflows
    │   └── <skill-name>/
    │       └── SKILL.md
    ├── commands/             # Custom slash commands
    │   └── <command-name>/
    │       └── COMMAND.md
    ├── agents/               # Subagent personas
    │   └── <agent-persona>/
    │       └── AGENT.md
    └── memory/               # Persistent agent memory
        ├── decisions.md
        ├── entities.md
        └── index.md
```

## Examples

This repo practices what it preaches — the [`.agent/`](./.agent) folder is the reference implementation. Every folder inside is a working example of the standard applied to a real project. Browse it directly to see how rules, skills, commands, and memory files look in practice.

## Core Principles

- **Co-location** — Agent files live alongside the code they govern.
- **Modularity** — Each concern lives in its own folder, adopted incrementally.
- **Composability** — Rules, skills, and agents mix and match across projects.
- **Portability** — Works with any LLM runtime: Claude, Cursor, Copilot, custom.
- **Progressive disclosure** — Start with one `README.md`. Add folders as needed.

---

## Getting Started

The minimum viable setup is a single file:

```
.agent/
└── README.md
```

Write your agent instructions there. Add folders only when you have a reason to.

→ **[Read the full specification](./STANDARD.md)**
→ **[Browse the docs site](https://your-username.github.io/agents-standard)**

---

## Folder Reference

| Path                    | Purpose                                          | File pattern                 |
| ----------------------- | ------------------------------------------------ | ---------------------------- |
| `.agent/README.md`     | Entry point — system prompt + file manifest      | `README.md`                  |
| `.agent/settings.json` | Permissions, tool access, runtime config         | `settings.json`              |
| `.agent/rules/`        | Granular, composable instruction files           | `rules/<name>/RULE.md`       |
| `.agent/skills/`       | Trigger-based auto-invoking workflows            | `skills/<name>/SKILL.md`     |
| `.agent/commands/`     | Explicit slash commands (`/review`, `/scaffold`) | `commands/<name>/COMMAND.md` |
| `.agent/agents/`       | Subagent personas (`@architect`, `@reviewer`)    | `agents/<name>/AGENT.md`     |
| `.agent/memory/`       | Persistent facts, decisions, and entities        | `memory/*.md`                |
| `docs/<task>/`          | Per-task PRD, SPEC, ARCHITECTURE, TASKS          | `docs/<task>/*.md`           |

---

## Status

**Version:** 1.0.0 — Draft · [MIT License](./LICENSE)
Feedback, issues, and PRs welcome.

---

_This standard is intentionally tool-agnostic. Runtimes may extend it provided they do not break compatibility with the core specification._
