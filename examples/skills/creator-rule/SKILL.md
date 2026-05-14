---
name: creator-rule
description: >
  Use this skill to write or improve CLI-agent rules, custom instruction files, Cursor rules, or modular `.agents/rules/*.md` files.
author: Oleg Shulyakov
license: MIT
version: 1.0.0
---

# creator-rule

Create rule files for CLI and coding agents. Treat agent rules as project
configuration: concise, reviewable, scoped, and specific enough that another
agent can act on them without guessing.

## Compatibility

- Agent Playbook projects: write modular rules under `.agents/rules/<rule-name>.md`
  and list them from `AGENTS.md` when needed.
- Codex and multi-agent workspaces: prefer `AGENTS.md` for shared project
  instructions; use modular rule files for concerns that should load only when
  relevant.
- Claude Code: adapt rules to `CLAUDE.md` or `.claude/rules/*.md` when the user
  explicitly targets Claude Code.
- GitHub Copilot and VS Code: adapt repository-wide guidance to
  `.github/copilot-instructions.md`, file-scoped guidance to
  `.github/instructions/*.instructions.md`, or shared multi-agent guidance to
  `AGENTS.md`.

## Workflow

1. Identify the target runtime and output location from the user's request. If it
   is unclear, default to the portable Agent Playbook format:
   `.agents/rules/<lowercase-hyphenated-name>.md`.
2. Inspect existing instruction files before writing: `AGENTS.md`, `CLAUDE.md`,
   `.agents/rules/`, `.claude/rules/`, `.github/copilot-instructions.md`,
   `.github/instructions/`, `.cursorrules`, `.cursor/rules/`, and nearby docs.
3. Extract only durable project behavior: build/test commands, coding standards,
   repo layout, review expectations, security constraints, workflow rules, and
   domain conventions. Leave temporary task notes out of permanent rules.
4. Choose the narrowest useful scope. Use a project-wide instruction file for
   rules that apply to every session; use a path-scoped rule for language,
   framework, package, or directory-specific guidance.
5. Write direct imperatives. Replace vague preferences with verifiable actions:
   "Run `make test` before committing" beats "Ensure quality." Include a short
   reason when it helps the agent make edge-case decisions.
6. Avoid duplication. Reference existing docs or config files when they are the
   source of truth, and summarize only the behavior an agent must follow.
7. Check for conflicts with existing rules. If a requested rule contradicts
   current project instructions, call out the conflict and either update the
   older rule or ask one concise question before proceeding.
8. Include safety boundaries for shell commands, secrets, destructive actions,
   generated files, migrations, deployment, and external services when relevant.
9. Keep each rule file focused on one concern. If the draft grows large or mixes
   unrelated topics, split it into multiple rule files and update the index.
10. After writing, report the created or changed files and any assumptions.

## Agent Playbook Rule Template

Use this template for `.agents/rules/<rule-name>.md` unless the target runtime
requires a different front matter shape:

```markdown
---
name: [Human-Readable Rule Name]
description: [One sentence describing the behavior this rule governs]
applies_to: ["glob/or/path/**"]
priority: low | medium | high | critical
---

# [Human-Readable Rule Name] Rules

- [Direct, testable instruction]
- [Direct, testable instruction with `command` or `path` where useful]
- [Instruction that references the authoritative source instead of duplicating it]
```

For always-on project instructions, use `applies_to: ["**/*"]` or omit
`applies_to` if the runtime treats missing scope as global. Use `critical` only
for security, data-loss, compliance, permission, or production-safety rules.

## Writing Standards

Good rules are short, operational, and scoped. Prefer:

- "Use `pnpm test -- --runInBand` for integration tests because the database
  fixture is shared."
- "Never edit generated files in `src/generated/**`; update the schema and run
  `pnpm generate`."
- "When changing `db/migrations/**`, include a rollback note in the final
  response."

Avoid:

- Generic advice such as "write clean code" or "be careful."
- Duplicating long README sections, package scripts, or style guides.
- Mixing tone/personality guidance with build, test, security, and architecture
  rules unless the user explicitly asks for a top-level instruction file.
- Rules that require hidden knowledge, unlisted tools, or credentials.

## Quality Checklist

Before finishing, verify that the rule:

- Has one clear concern and a descriptive lowercase-hyphenated filename.
- Uses front matter when the target runtime supports filtering or priority.
- Contains concrete commands, paths, globs, or examples where they reduce
  ambiguity.
- Explains non-obvious rationale briefly.
- Avoids secrets, personal preferences, stale temporary context, and unrelated
  documentation.
- Does not conflict with existing project instructions.
- Is indexed from `AGENTS.md` or the runtime-specific instruction entry point
  when the project expects an index.
