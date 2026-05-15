---
name: codegen-test
description: >
  Generate production-ready automated test suites for applications and services. Use this
  skill whenever the user asks to create, add, scaffold, or improve E2E tests, API tests,
  integration tests, smoke tests, regression tests, performance tests, load tests, AI evals,
  LLM output evals, tool-use evals, RAG evals, prompt regression tests, agent benchmarks,
  cost/latency benchmarks, k6, Playwright, Cypress, Selenium, Supertest, Postman/Newman,
  Locust, JMeter, test fixtures, page objects, test data, or CI-ready test scripts. Produces
  source test files plus focused setup notes. For security testing, prompt-injection audits,
  jailbreak tests, data exfiltration checks, or policy review use audit-security. For test
  strategy documents use strategy-test; for framework installation from scratch use
  setup-test-framework; for flaky-test diagnosis use audit-test-flaky.
author: Oleg Shulyakov
license: MIT
version: 1.0.0
---

# codegen-test

Router skill for generating test code. Detect the test variant from the user's request and repository context, then read exactly one variant reference before implementing or drafting the test suite.

## Variant Detection

Check signals in this order:

1. Explicit user intent: "E2E", "browser", "API", "contract", "load", "performance", "AI eval", "LLM eval", "tool use", "RAG", "prompt regression", "cost", "latency", "k6", "Playwright", and similar.
2. Existing files and dependencies: `playwright.config.*`, `cypress.config.*`, `selenium`, `supertest`, `newman`, `k6`, `locust`, `jmeter`, `evals/`, `promptfoo`, `deepeval`, `ragas`, `openevals`, model SDK usage, test directories, package scripts, CI jobs.
3. Target surface: UI workflows route to `references/e2e.md`; HTTP endpoints and service contracts route to `references/api.md`; non-AI throughput, latency, soak, spike, and capacity scenarios route to `references/perf.md`; AI answer quality routes to `references/ai-output.md`; AI tool orchestration routes to `references/ai-tool-use.md`; AI cost, latency, token, and throughput benchmarks route to `references/ai-perf.md`.
4. Security and abuse-resistance requests route away from this skill to `audit-security`.
5. If still ambiguous, ask one short clarifying question naming the likely variants.

## Routing Table

| Request | Reference |
| --- | --- |
| Browser flows, smoke tests, page objects, visual user journeys, login/checkout/onboarding paths | `references/e2e.md` |
| Endpoint tests, controller tests, service integration tests, OpenAPI examples, Postman/Newman collections, Supertest suites | `references/api.md` |
| Load, stress, soak, spike, latency budgets, throughput checks, k6/Locust/JMeter scripts | `references/perf.md` |
| LLM output quality, prompt regression, grading rubrics, structured output checks, RAG answer quality | `references/ai-output.md` |
| Agent tool choice, tool arguments, recovery from tool errors, multi-step tool workflows | `references/ai-tool-use.md` |
| AI latency, token usage, cost per task, model-call count, retry rate, throughput, quality-per-dollar | `references/ai-perf.md` |

## Working Rules

- Inspect the repository before writing tests. Reuse its test runner, fixtures, factories, naming conventions, package scripts, and CI patterns.
- Use bundled scripts when they fit: `scripts/validate_evals.py` validates this skill's eval suite, `scripts/scaffold_ai_eval.py` creates starter AI eval folders, and `scripts/summarize_ai_perf.py` summarizes AI benchmark `results.jsonl` files.
- Generate runnable test code, not only prose. If context is insufficient to edit files safely, provide complete file contents and state the assumptions.
- Prefer stable selectors, public API contracts, and deterministic fixtures. Avoid sleeps, hidden network dependencies, shared mutable test data, and order-dependent tests.
- Cover the highest-value happy path plus meaningful negative or edge cases. Do not create broad low-signal tests that only assert that something exists.
- Keep credentials, tokens, and environment-specific values behind environment variables or existing config helpers.
- When adding files, include the minimal command needed to run the tests and any required environment variables.
- For AI evals, measure quality and operational metrics together when possible. Latency and cost without pass/fail quality mostly prove how quickly the system can be wrong.

## Output Format

When editing a repository, finish with changed files, run command, and verification status.

When only drafting code, use this structure:

```text
Assumptions:
- ...

Files:
- path/to/test-file

Run:
- command

Notes:
- ...
```
