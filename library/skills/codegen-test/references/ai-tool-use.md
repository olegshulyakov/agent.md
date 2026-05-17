# AI Tool-Use Eval Generation

Use this reference for testing agents that call tools, functions, APIs, shell commands, browser actions, database queries, or local code-modification utilities.

Do not use this reference for malicious tool-use, data exfiltration, prompt-injection, or policy bypass testing. Route those to `audit-security`.

## What To Test

- Tool selection: the agent chooses the right tool for the task and avoids tools when no tool is needed.
- Argument correctness: tool arguments match schema, paths, IDs, filters, and user constraints.
- Sequencing: tool calls happen in a valid order, especially for search-read-edit-verify workflows.
- Error recovery: the agent handles failed, empty, or partial tool results without looping or inventing success.
- Stop condition: the agent stops after completion instead of continuing to make unnecessary calls.
- State discipline: the agent does not overwrite unrelated files, reuse stale observations, or ignore newer user instructions.

## Eval Case Shape

Each case should define:

- User task and starting state.
- Available tools and schemas.
- Mocked tool responses or fixture workspace.
- Expected tool-call trace, allowing harmless equivalent calls when appropriate.
- Expected final output or changed files.
- Failure budget such as max calls, max retries, or forbidden calls.

## Trace Assertions

Use trace-level assertions:

- Required tool was called at least once.
- Forbidden tool was not called.
- Tool arguments match schema and include required constraints.
- Calls happen in order: inspect before edit, execute before summarize, verify after change.
- On simulated failure, the agent retries with a changed input or reports the blocker.
- Total tool calls stay under a reasonable limit for the scenario.

Avoid overfitting exact traces unless the workflow is deterministic. Two different valid search queries are not a failure; deleting the wrong directory very much is.

## Fixture Design

Make fixtures small but realistic:

- Include one relevant file and one tempting irrelevant file.
- Include stale or ambiguous data when testing recency handling.
- Mock both success and failure responses for external tools.
- Include edge cases such as spaces in paths, empty search results, pagination, or malformed API responses.

## Runner Pattern

Generate or extend a runner that:

- Runs the agent against fixture tasks with a controlled tool registry.
- Captures every tool call, argument payload, result, final answer, and file diff.
- Applies deterministic assertions to the trace and final state.
- Writes artifacts per case so failures can be inspected without rerunning.

## Output Files

Common outputs:

- `evals/tool-use/cases.jsonl` for tasks and expected traces.
- `evals/tool-use/fixtures/` for local files and mocked tool responses.
- `evals/tool-use/run.*` for the harness.
- `evals/tool-use/assertions.*` for reusable trace checks.
