# AI Cost, Latency, And Throughput Benchmark Generation

Use this reference for testing operational performance of AI features: latency, token usage, model-call count, retry rate, cache hit rate, throughput, and cost per successful task.

This is different from classic HTTP load testing. An AI endpoint can be fast while giving bad answers, or cheap because it skipped the hard work. Always pair operational metrics with at least one quality signal from `ai-output.md` or `ai-tool-use.md`.

## What To Measure

- End-to-end latency: user request to final answer.
- First-token latency: useful for streaming UX.
- Model latency by call: each model invocation, not only total request time.
- Tool latency: retrieval, browser, database, code execution, or API calls.
- Input/output tokens by call and total tokens by task.
- Estimated cost by provider/model pricing, recorded as a derived metric.
- Model-call count, tool-call count, retry count, and error rate.
- Cache hit rate for prompt, retrieval, embedding, or response caches.
- Throughput under concurrency: successful tasks per minute at target quality.
- Quality-per-dollar: pass rate divided by cost, or cost per passing case.

## How To Do It

1. Pick representative tasks, not only tiny prompts. Include easy, normal, and worst-case scenarios.
2. Add instrumentation around the application entry point and every model/tool call.
3. Run each case multiple times because model latency and output length vary.
4. Store raw per-run metrics, not only averages.
5. Compute percentiles: p50, p90, p95, and max for latency and cost.
6. Join metrics with quality results so the benchmark can report "passed in 8.2s for $0.04" instead of just "returned".
7. Compare against a baseline file when prompts, models, retrieval, or agent logic changes.

## Minimal Metrics Schema

```json
{
  "case_id": "support-refund-policy-001",
  "run_id": "2026-05-15T10:00:00Z-1",
  "model": "example-model",
  "prompt_version": "v3",
  "quality_passed": true,
  "latency_ms": 8240,
  "first_token_ms": 940,
  "model_calls": 2,
  "tool_calls": 1,
  "retries": 0,
  "input_tokens": 4180,
  "output_tokens": 612,
  "estimated_cost_usd": 0.041,
  "cache_hit": false
}
```

## Benchmark Thresholds

Use thresholds that match the product experience:

- Interactive chat: p95 end-to-end latency and first-token latency.
- Background agent: success rate, max wall-clock time, cost per passing task, and retry rate.
- RAG answer: retrieval latency, generation latency, grounded-answer pass rate, and cost per grounded answer.
- Tool-using agent: max model calls, max tool calls, task completion rate, and cost per completed task.

Avoid average-only gates. Averages hide the one slow path that users remember with surprising emotional clarity.

## Runner Pattern

Generate or extend a runner that:

- Reads benchmark cases from JSONL/YAML.
- Executes each case `N` times with fixed model settings.
- Captures provider usage metadata when available.
- Estimates cost from a checked-in pricing table or configurable environment values.
- Emits `results.jsonl` with one row per case run.
- Emits a summary report comparing current results to baseline.
- Fails only on agreed gates such as p95 latency, cost per passing case, or quality pass rate.

## Output Files

Common outputs:

- `evals/ai-perf/cases.jsonl` for representative tasks.
- `evals/ai-perf/run.*` for the benchmark harness.
- `evals/ai-perf/pricing.json` for provider/model prices when not supplied by telemetry.
- `evals/ai-perf/baseline.json` for comparison.
- `evals/ai-perf/results.jsonl` and `summary.md` for run artifacts.
