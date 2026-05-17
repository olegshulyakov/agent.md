# Memory

## Facts

- **GitHub Pages source lives in `pages/`** — Repository Pages files were moved from the root into `pages/` on 2026-05-14.
- **Markdown PR checks use extracted helper scripts** — The pull request workflow for changed Markdown files delegates Bash and JavaScript logic to `.devops/markdown-format`.
- **Library skills have authoring documentation** — `library/skills/README.md` covers setup, authoring, evals, packaging, and troubleshooting.
- **Creator skills support multiple agent runtimes** — `library/skills/creator-skill` guidance and scripts were updated to avoid assumptions tied to a single tool.
- **Design API is a router skill** — `design-api` routes contract design work across OpenAPI, AsyncAPI, and GraphQL references.
- **Operator git has shared action/output behavior** — `operator-git` keeps branch naming and commit message conventions while centralizing action and output workflow behavior in router instructions.

## Preferences

- **Small completed task notes** — Prefer `.agents/memory/YYYY-MM-DD.md` over `docs/YYYY-MM-DD-task/TASKS.md` when a task does not need a PRD, SPEC, architecture, or design document.
- **Token-efficient agent output** — Keep agent responses concise while preserving logic and useful implementation detail.

## Decisions

### [2026-05-14] Use memory for small completed task notes

**Context:** Several `docs/2026-05-14-*` folders contained only completed `TASKS.md` files.
**Decision:** Preserve those notes in `.agents/memory/2026-05-14.md` and reserve docs task folders for work that needs task-scoped PRD, SPEC, architecture, or design documentation.
**Revisit if:** Small tasks start needing richer traceability than dated memory notes provide.
