# Skill Authoring

Use this reference when creating a new skill or revising an existing `SKILL.md`.

## Capture Intent

Extract what the user already provided before asking questions. Identify what the skill enables the calling agent to do, when it should trigger, what output it should produce, and whether test cases should be created.

Ask at most one focused question when a missing answer would materially change the skill.

## Research and Interview

Ask about edge cases, input formats, output formats, success criteria, dependencies, and example files. For existing skills, inspect the current folder before editing. Check bundled scripts, references, assets, and evals so you preserve local conventions.

## Write `SKILL.md`

Required frontmatter fields are `name` and `description`. Keep the complete frontmatter under 100 tokens. The description is the primary trigger signal, so include the core task and strongest trigger contexts, but avoid long keyword inventories.

Keep the Markdown body under 500 lines. The body should explain workflow, routing decisions, critical rules, and output format. Move deep detail into `references/` and point to it clearly.

## Length Budgets

Follow these budgets for every `SKILL.md`:

- Metadata/frontmatter: no more than 100 tokens.
- Main instruction body: no more than 500 lines.

If a skill exceeds either budget, shorten trigger metadata first, then move detailed procedures, examples, platform notes, and variant-specific guidance into `references/`. Router skills are the preferred shape for broad domains: keep the main file focused on routing and shared rules, then load only the relevant reference.

Use this shape when helpful:

```text
skill-name/
├── SKILL.md
├── references/
├── scripts/
├── assets/
└── evals/
```

Do not create placeholder directories. Add a folder only when it contains useful files.

## Progressive Disclosure

Use three levels: metadata loaded by the runtime, main body loaded when the skill triggers, and bundled resources loaded only when needed.

Router skills should classify the request, choose the relevant reference, read only that reference, and act.

## Compatibility

Write core instructions so they work in any agent runtime. Put runtime-specific notes under a short compatibility section or in `references/agent-compatibility.md`.

Avoid relying on one agent's tool names, slash commands, event stream, or UI unless the skill is explicitly for that agent.

## Writing Style

Use imperative instructions. Explain why constraints matter instead of stacking brittle all-caps rules. Include examples when they prevent ambiguity, but keep examples short and move large examples into references.

Skills must not contain malware, hidden exfiltration behavior, credential capture, or instructions that would surprise the user relative to the skill description.
