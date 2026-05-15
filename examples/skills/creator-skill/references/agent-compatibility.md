# Agent Compatibility

Use this reference when adapting skill creation or evaluation to a specific runtime.

## Agents Without Subagents

Follow the same draft, test, review, and improve loop, but run test cases serially yourself. Skip baseline comparisons unless another local mechanism can produce them fairly.

Present outputs directly in the conversation or save files for the user to inspect. If a browser is unavailable, skip the live review server and use a static HTML review file or concise inline review prompts.

Quantitative benchmarking is less meaningful without isolated baseline runs. Prioritize qualitative feedback unless deterministic assertions can be checked locally.

## Claude Code

Claude Code can use native trigger detection through the optimization scripts:

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --agent claude-code \
  --verbose
```

Use the user's normal Claude Code configuration.

## Generic CLI Agents

Use the generic command adapter unless the agent exposes better trigger telemetry:

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --agent codex-cli \
  --verbose
```

For CLIs that need arguments or files instead of stdin, use:

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --agent custom \
  --agent-command "agent run --input {prompt_file}" \
  --verbose
```

## Cowork

Cowork has subagents, so parallel skill and baseline runs can work. If timeouts become a problem, run prompts in smaller batches.

Cowork may not have a display. Generate a static review file with `eval-viewer/generate_review.py --static <output_path>` and share that path. Use the generated review UI before revising from test outputs.

When feedback is downloaded as `feedback.json`, copy it into the current iteration directory before continuing.

## Updating Installed Skills

Preserve the original skill directory name and `name` frontmatter. If an installed skill path is read-only, copy it to a writable location, edit the copy, and package from there.

When packaging manually, stage temporary package contents in `/tmp/` first if direct writes fail.
