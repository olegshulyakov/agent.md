# Example Skills

This directory contains example agent skills: portable instruction folders that teach an AI coding agent when and how to handle a specific kind of task.

A complete skill is a directory with a required `SKILL.md` file and optional bundled resources such as `references/`, `scripts/`, `assets/`, and `evals/`.

## What's Here

This directory contains complete example skills you can copy, adapt, or use as references. `creator-skill` is the best starting point when you want guided help creating, improving, packaging, or evaluating a skill.

## Setup

There is no global install step for this examples directory. Use a skill by copying or referencing its folder from the agent/runtime you are using.

For a local workflow, keep the full folder intact:

```bash
examples/skills/my-skill/
├── SKILL.md
├── references/
├── scripts/
├── assets/
└── evals/
```

The key rule is that `SKILL.md` and any referenced resources must stay together. If a skill says “read `references/postgres.md`,” that file needs to be available relative to the skill folder.

Useful local checks require Python 3:

```bash
python3 examples/skills/creator-skill/scripts/quick_validate.py examples/skills/writer-sql
```

Packaging and eval tooling should be run from the `creator-skill` directory so its Python module imports resolve cleanly:

```bash
cd examples/skills/creator-skill
python3 -m scripts.package_skill ../writer-sql /tmp/skills-dist
```

Packaged `.skill` files exclude root-level `evals/` because evals are development assets, not runtime instructions.

## Write A New Skill

You can write a skill manually or use `creator-skill` as a guided workflow. Either way, start with one narrow job. Good skills are specific enough to change the agent’s behavior, but not so narrow that they only work for one prompt.

## Quality Principles

Use common engineering frameworks as practical lenses, not required ceremony:

- **KISS**: keep each skill focused on one job, route to the smallest useful reference set, and remove instructions that do not change behavior.
- **STAR**: write examples and eval prompts with enough situation, task, action, and result context for another agent or reviewer to judge quality.
- **SOLID**: apply to code-generation skills and code examples where structure matters. Favor clear responsibilities, small interfaces, and existing project abstractions over new layers.

Do not name every principle in every skill. Use the plain instruction when it is clearer than the acronym.

### Option 1: Use `creator-skill`

Use `creator-skill` when you want help drafting the skill, tightening its trigger description, building evals, packaging it, or iterating based on benchmark results. It includes the helper scripts and references used throughout this README.

Open `creator-skill/SKILL.md` and follow its workflow, or ask an agent that has access to this directory to use `creator-skill` for your new skill.

### Option 2: Write It Manually

Create a folder and `SKILL.md`:

```bash
mkdir -p examples/skills/my-skill
touch examples/skills/my-skill/SKILL.md
```

Use this shape:

```markdown
---
name: my-skill
description: >
  Use this skill when the user asks for a specific workflow, output, or decision
  pattern that benefits from these instructions.
author: Your Name
license: MIT
version: 1.0.0
---

# my-skill

Explain what this skill helps the agent do.

## When To Use This Skill

Use this skill when...

## Workflow

1. Inspect the user's request and available files.
2. Choose the relevant reference or script.
3. Produce the expected output.

## Output

Describe the format the user should receive.
```

Write the `description` as trigger guidance. It should include the user intents and phrases that should activate the skill. Do not hide trigger logic only in the body; many agents decide whether to load the skill from the name and description first.

Use bundled resources when they reduce context:

| Folder        | Use it for                                                                |
| ------------- | ------------------------------------------------------------------------- |
| `references/` | Longer docs loaded only when needed, such as dialect guides or templates. |
| `scripts/`    | Deterministic helpers, validators, converters, or generators.             |
| `assets/`     | Templates, images, fonts, example files, or other reusable artifacts.     |
| `evals/`      | Development-time test prompts and fixtures.                               |

Prefer references over a huge `SKILL.md`. A skill body should be easy for an agent to scan; move long variants into focused files like `references/postgres.md` or `references/api-docs.md`.

## Test With Evals

Evals answer two questions: does the skill trigger for the right prompts, and does it produce better outputs when it is used?

### 1. Create `evals/evals.json`

Inside the skill folder, add realistic prompts:

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "Write a runbook for rotating the staging database password without downtime.",
      "expected_output": "A step-by-step operational runbook with validation and rollback steps.",
      "files": [],
      "expectations": [
        "Includes prerequisites",
        "Includes rollback steps",
        "Separates staging from production assumptions"
      ]
    }
  ]
}
```

Make prompts look like real user requests. Short labels such as “write docs” or “make SQL” are poor evals because they do not test routing or workflow quality.

The fuller schema lives in `creator-skill/references/schemas.md`.

### 2. Run Trigger Evals

Trigger evals test whether the skill description routes correctly. Create a trigger eval set:

```json
[
  { "query": "write a production-ready runbook for rotating our API token", "should_trigger": true },
  { "query": "summarize this incident timeline in three bullets", "should_trigger": false }
]
```

Then run:

```bash
cd examples/skills/creator-skill
python3 -m scripts.run_eval \
  --eval-set /path/to/trigger-evals.json \
  --skill-path ../my-skill \
  --agent claude-code
```

`claude-code` uses native trigger detection. Other agents use a routing-judgment eval. The runner has presets for common CLIs such as `codex-cli`, `gemini-cli`, `opencode`, `qwen-code`, `continue`, `crush`, `cursor-agent`, `copilot`, `goose`, and `aider`. Unknown agent labels are treated as executable names that receive the prompt on stdin.

Use `--agent-command` only when a CLI needs a different shape:

```bash
python3 -m scripts.run_eval \
  --eval-set /path/to/trigger-evals.json \
  --skill-path ../my-skill \
  --agent file-based-agent \
  --agent-command "my-agent run --prompt-file {prompt_file}"
```

Do not pass model overrides through these eval scripts. The point is to test the agent as configured by the user.

### 3. Run The Improve Loop

After the user approves a trigger eval set, run the optimization loop:

```bash
cd examples/skills/creator-skill
python3 -m scripts.run_loop \
  --eval-set /path/to/trigger-evals.json \
  --skill-path ../my-skill \
  --agent claude-code \
  --max-iterations 5 \
  --verbose
```

This tests descriptions against train and held-out queries, proposes better descriptions, and writes an HTML report.

### 4. Review Output Quality

For output-quality evals, compare runs with the skill against a baseline. The `creator-skill` workflow describes the full loop:

1. Run each eval with the skill and without the skill, or against an older skill snapshot.
2. Save outputs under an iteration workspace.
3. Grade expectations into `grading.json`.
4. Aggregate results:

```bash
cd examples/skills/creator-skill
python3 -m scripts.aggregate_benchmark /path/to/workspace/iteration-1 --skill-name my-skill
```

5. Generate the review UI:

```bash
python3 eval-viewer/generate_review.py \
  /path/to/workspace/iteration-1 \
  --skill-name my-skill \
  --benchmark /path/to/workspace/iteration-1/benchmark.json
```

Use the viewer before revising the skill. Human review catches issues that pass/fail metrics often miss.

## Improve An Existing Skill

When editing an existing skill:

1. Preserve the folder name and the `name` frontmatter unless you are intentionally creating a new skill.
2. Read the current `SKILL.md` and any referenced files before editing.
3. Add or update evals for the behavior you are changing.
4. Keep changes scoped. If you only need to improve routing, edit the description first.
5. Re-run validation and the relevant evals.

For larger revisions, snapshot the old skill and compare old-vs-new outputs. That is more useful than arguing with yourself in a mirror, though admittedly less theatrical.

## Package A Skill

From `creator-skill`:

```bash
cd examples/skills/creator-skill
python3 -m scripts.package_skill ../my-skill /tmp/skills-dist
```

This creates `/tmp/skills-dist/my-skill.skill`.

Packaging runs validation first. If validation fails, fix the frontmatter or folder structure before shipping the skill.

## Frontmatter Reference

Required:

| Field         | Notes                                                         |
| ------------- | ------------------------------------------------------------- |
| `name`        | Kebab-case identifier, matching the folder when possible.     |
| `description` | Trigger guidance. Keep it specific and under 1024 characters. |

Common optional fields:

| Field           | Notes                                                    |
| --------------- | -------------------------------------------------------- |
| `author`        | Person or organization maintaining the skill.            |
| `license`       | License for the skill content.                           |
| `version`       | Skill version. Use semantic versioning when practical.   |
| `compatibility` | Short note about required tools or runtime assumptions.  |
| `allowed-tools` | Tool restrictions, if your target runtime supports them. |
| `metadata`      | Extra structured data for runtimes that consume it.      |

## Troubleshooting

If a skill does not trigger, first improve the `description`. Include the user intents that should activate the skill and near-misses that should not.

If a skill triggers too often, narrow the description. Add negative trigger evals that share keywords but require a different workflow.

If packaging fails, run:

```bash
python3 examples/skills/creator-skill/scripts/quick_validate.py examples/skills/my-skill
```

If `python` is not found, use `python3`.

If module commands fail with `No module named scripts`, run them from `examples/skills/creator-skill` with `python3 -m ...`.

If an agent CLI hangs, provide an explicit `--agent-command` that uses its non-interactive mode. Avoid commands that open a TUI or wait for confirmation.

## Useful Starting Points

Use `creator-skill` when you want guided help creating or improving a skill. Use `writer-tech-docs`, `writer-spec`, `writer-sql`, and `operator-git` as examples of router-style skills that load only the relevant reference file.
