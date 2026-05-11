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
- Not every file is required — small tasks may only need `TASKS.md`

## Working on a task

- Create a task folder before writing code: `mkdir docs/$(date +%Y-%m-%d)-my-feature`
- Use `TASKS.md` as the checklist; check off items as you go
- If the task changes anything described in a project-scoped document, update it in the same commit
- Do not deviate from `SPEC.md` silently — update the file if the spec changes
