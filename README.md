# Agent Playbook

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

> A portable, tool-agnostic file structure playbook for LLM agents in software projects.

Agent behavior is code. It should be versioned, reviewed, and readable by both humans and machines. This playbook defines where agent instructions, rules, skills, memory, commands, and documentation live — consistently, across any project and any runtime.

---

## At a Glance

```text
project-root/
└── .agents/
    ├── README.md             # Agent entry point + file manifest
    ├── settings.json         # Permissions & runtime config
    ├── rules/                # Instruction files
    │   └── <rule-name>.md
    ├── skills/               # Auto-invoking workflows
    │   └── <skill-name>/
    │       └── SKILL.md
    ├── commands/             # Custom slash commands
    │   └── <command-name>.md
    ├── agents/               # Subagent personas
    │   └── <agent-persona>.md
    └── memory/               # Persistent agent memory
        ├── MEMORY.md         # Long-term memory. Durable facts, preferences, and decisions
        └── YYYY-MM-DD.md     # Daily notes. Running context and observations
```

## Examples

This repo practices what it preaches — the [`examples/`](./examples) folder contains working examples. Every folder inside is a working example of the playbook applied to a real project. Browse it directly to see how rules, skills, commands, and memory files look in practice.

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

→ **[Read the full playbook](./PLAYBOOK.md)**
→ **[Browse the docs site](https://olegshulyakov.github.io/agent.md)**

---

## Folder Reference

| Path                    | Purpose                                             | File pattern             |
| ----------------------- | --------------------------------------------------- | ------------------------ |
| `.agents/README.md`     | Entry point — system prompt + file manifest         | `README.md`              |
| `.agents/settings.json` | Permissions, tool access, runtime config            | `settings.json`          |
| `.agents/rules/`        | Granular, composable instruction files              | `rules/<name>.md`        |
| `.agents/skills/`       | Trigger-based auto-invoking workflows               | `skills/<name>/SKILL.md` |
| `.agents/commands/`     | Explicit slash commands (`/review`, `/scaffold`).   | `commands/<name>.md`     |
| `.agents/agents/`       | Subagent personas (`@architect`, `@reviewer`)       | `agents/<name>.md`       |
| `.agents/memory/`       | Persistent facts, decisions, and daily observations | `memory/*.md`            |

---

## Status

**Version:** 0.0.1 — Draft · [MIT License](./LICENSE)
Feedback, issues, and PRs welcome.

---

_This playbook is intentionally tool-agnostic. Runtimes may extend it provided they do not break compatibility with the core specification._
