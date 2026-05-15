# Description Optimization

Use this reference when optimizing a skill's frontmatter description for trigger accuracy.

The `description` field is the main signal native skill runtimes use to decide whether to invoke a skill. Optimize it after the skill behavior is stable.

## Choose the Agent Adapter

Infer the calling agent from the current session or CLI. Use native trigger detection when the agent exposes it. Otherwise, use routing-judgment evals.

Examples:

```bash
python -m scripts.run_eval \
  --eval-set <skill-path>/evals/trigger-evals.json \
  --skill-path <skill-path> \
  --agent codex-cli

python -m scripts.run_loop \
  --eval-set <skill-path>/evals/trigger-evals.json \
  --skill-path <skill-path> \
  --agent my-agent
```

For CLIs with unusual invocation shapes, pass `--agent-command` with `{prompt}` or `{prompt_file}` placeholders. Do not override the model unless the user explicitly asks; the eval should match the agent's normal behavior.

## Create Trigger Evals

Create about 20 realistic queries, split between should-trigger and should-not-trigger cases. Use concrete prompts that resemble real user requests, including file paths, domain details, typos, abbreviations, and ambiguous phrasing.

Positive cases should cover varied ways users ask for the skill's core capability. Negative cases should be near misses, not obviously irrelevant prompts.

Save them as:

```json
[
  { "query": "the user prompt", "should_trigger": true },
  { "query": "a near miss", "should_trigger": false }
]
```

## Review the Eval Set

When possible, present the eval set to the user before running optimization. Use `assets/eval_review.html` by replacing:

- `__EVAL_DATA_PLACEHOLDER__` with the JSON array
- `__SKILL_NAME_PLACEHOLDER__` with the skill name
- `__SKILL_DESCRIPTION_PLACEHOLDER__` with the current description

The user can edit queries and export the final eval set.

## Run the Optimization Loop

Run:

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --agent <calling-agent-label> \
  --results-dir <skill-path>/evals/description-optimization \
  --max-iterations 5 \
  --verbose
```

The loop splits train and held-out test data, evaluates the current description, proposes revisions, and selects `best_description` by held-out test score.

Apply the best description to `SKILL.md`, then report the before/after and scores. Keep the updated metadata under 100 tokens.

## Triggering Notes

Agents may skip a skill for simple tasks they can handle directly. Trigger eval prompts should be substantive enough that a specialized skill would help. Tiny prompts like "read this file" are poor trigger tests even if the skill technically could help.
