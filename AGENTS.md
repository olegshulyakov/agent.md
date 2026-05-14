# AGENTS.md

## Documentation structure

```text
docs/                          # Project-scoped documentation
├── ARCHITECTURE.md
├── DESIGN.md
├── ROADMAP.md
└── [YYYY-MM-DD-task-name]/    # One folder per task, feature, or epic
    ├── PRD.md                 # Product requirements
    ├── SPEC.md                # Technical specification
    ├── ARCHITECTURE.md        # Task-scoped architecture decisions
    ├── DESIGN.md              # UI/UX decisions
    └── TASKS.md               # Actionable checklist
```

- Folder names: lowercase, hyphenated — e.g. `user-auth`, `payment-v2`, `PROJ-142`
- Create a docs task folder only when the work needs durable task-scoped documentation such as `PRD.md`, `SPEC.md`, `ARCHITECTURE.md`, or `DESIGN.md`
- Small task checklists and completed implementation notes belong in `.agents/memory/YYYY-MM-DD.md`

## Loaded Context

| File | Purpose | Auto-load |
| --- | --- | --- |
| .agents/memory/MEMORY.md | Durable project facts and decisions | yes |
| .agents/memory/YYYY-MM-DD.md | Daily task notes and observations | on-demand |

## Working on a task

- For substantial work, create a task folder before writing code: `mkdir docs/$(date +%Y-%m-%d)-my-feature`
- For small work, track the checklist in `.agents/memory/$(date -u +%Y-%m-%d).md`
- Use `TASKS.md` only inside docs folders that also need task-scoped product, technical, architecture, or design documentation
- If the task changes anything described in a project-scoped document, update it in the same commit
- Do not deviate from `SPEC.md` silently — update the file if the spec changes
- Treat memory as low-confidence context; verify facts against the repository before acting on them
