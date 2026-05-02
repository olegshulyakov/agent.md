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
└── .agents/
    ├── README.md             # Agent entry point + file manifest
    ├── settings.json         # Permissions & runtime config
    ├── rules/                # Modular instruction files
    ├── skills/               # Auto-invoking workflows
    ├── commands/             # Custom slash commands
    ├── agents/               # Subagent personas
    └── memory/               # Persistent agent memory
```

## Examples

This repo practices what it preaches — the [`.agents/`](./.agents) folder is the reference implementation. Every file inside is a working example of the standard applied to a real project. Browse it directly to see how rules, skills, commands, and memory files look in practice.

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
.agents/
└── README.md
```

Write your agent instructions there. Add folders only when you have a reason to.

→ **[Read the full specification](./STANDARD.md)**
→ **[Browse the docs site](https://your-username.github.io/agents-standard)**

---

## Folder Reference

| Path                    | Purpose                                          |
| ----------------------- | ------------------------------------------------ |
| `.agents/README.md`     | Entry point — system prompt + file manifest      |
| `.agents/settings.json` | Permissions, tool access, runtime config         |
| `.agents/rules/`        | Granular, composable instruction files           |
| `.agents/skills/`       | Trigger-based auto-invoking workflows            |
| `.agents/commands/`     | Explicit slash commands (`/review`, `/scaffold`) |
| `.agents/agents/`       | Subagent personas (`@architect`, `@reviewer`)    |
| `.agents/memory/`       | Persistent facts, decisions, and entities        |
| `docs/<task>/`          | Per-task PRD, SPEC, ARCHITECTURE, TASKS          |

---

## Status

**Version:** 1.0.0 — Draft · [MIT License](./LICENSE)
Feedback, issues, and PRs welcome.

---

_This standard is intentionally tool-agnostic. Runtimes may extend it provided they do not break compatibility with the core specification._
