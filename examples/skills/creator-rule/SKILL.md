---
name: creator-rule
description: >
  Write or improve CLI-agent rules, custom instruction files, Cursor rules,
  or modular `.agents/rules/*.md` files.
author: Oleg Shulyakov
license: MIT
version: 1.1.0
---

# creator-rule

Write agent rules like project config: concise, scoped, and specific enough to act on without guessing.

## Output Locations

| Runtime | Location |
|---|---|
| Agent Playbook *(default)* | `.agents/rules/<name>.md` |
| Codex / multi-agent | `AGENTS.md` (shared); rule files for scoped concerns |
| Claude Code | `CLAUDE.md` or `.claude/rules/*.md` |
| GitHub Copilot / VS Code | `.github/copilot-instructions.md` (repo-wide); `.github/instructions/*.instructions.md` (scoped) |

Default to Agent Playbook format when runtime is unspecified.

## Workflow

1. **Identify** target runtime and output path.
2. **Inspect** existing files before writing: `AGENTS.md`, `CLAUDE.md`, `.agents/rules/`, `.claude/rules/`, `.github/copilot-instructions.md`, `.cursorrules`, `.cursor/rules/`.
3. **Extract only durable behavior:** build/test commands, coding standards, repo layout, review expectations, security constraints, workflow rules, domain conventions. No temporary task notes.
4. **Scope narrowly.** Project-wide file for global rules; path-scoped rule for language, framework, or directory-specific guidance.
5. **Write direct imperatives.** Replace vague preferences with verifiable actions. Add a short reason only when it helps edge-case decisions.
6. **Avoid duplication.** Reference existing docs as source of truth; summarize only what an agent must follow.
7. **Check for conflicts.** If a new rule contradicts existing instructions, call out the conflict and either update the older rule or ask one question before proceeding.
8. **Add safety boundaries** for shell commands, secrets, destructive actions, generated files, migrations, deployment, and external services when relevant.
9. **One concern per file.** Split large or mixed drafts and update the index.
10. **Report** created/changed files and assumptions after writing.

## Rule Template

```markdown
---
name: [Human-Readable Rule Name]
description: [One sentence describing the behavior this rule governs]
applies_to: ["glob/or/path/**"]
priority: low | medium | high | critical
---

# [Human-Readable Rule Name] Rules

- [Direct, testable instruction]
- [Instruction with `command` or `path` where useful]
- [Instruction referencing authoritative source instead of duplicating it]
```

Use `applies_to: ["**/*"]` or omit for global scope. Reserve `critical` for security, data-loss, compliance, or production-safety rules.

## Good vs. Bad

**Write this:**
- `pnpm test -- --runInBand` for integration tests (shared DB fixture).
- Never edit `src/generated/**`; update the schema and run `pnpm generate`.
- When changing `db/migrations/**`, include a rollback note in the response.

**Not this:**
- "Write clean code" or "be careful."
- Long README sections or style guides copied verbatim.
- Tone/personality mixed with build, test, or security rules (unless writing a top-level instruction file).
- Rules requiring unlisted tools, hidden knowledge, or credentials.

## Quality Checklist

Before finishing, verify the rule:
- One concern; descriptive `lowercase-hyphenated` filename
- Front matter present when runtime supports filtering or priority
- Concrete commands, paths, globs, or examples where they reduce ambiguity
- Non-obvious rationale explained briefly
- No secrets, personal preferences, stale context, or unrelated docs
- No conflict with existing instructions
- Indexed from `AGENTS.md` or runtime entry point when the project expects an index