# AI Output Eval Generation

Use this reference for testing model answers, generated artifacts, RAG responses, structured outputs, and prompt regressions.

Do not use this reference for jailbreak, prompt-injection, data leakage, or safety-policy audits. Route those to `audit-security`.

## What To Test

- Task success: the response solves the user's actual request.
- Completeness: required sections, constraints, edge cases, or artifacts are present.
- Factual grounding: claims are supported by provided context, retrieved documents, or citations.
- Structured output validity: JSON, YAML, XML, SQL, code, OpenAPI, or other schemas parse and validate.
- Instruction following: formatting, tone, length, refusal boundaries, and required/forbidden content.
- Regression behavior: prompt, model, retrieval, or tool changes do not degrade known scenarios.

## Eval Case Shape

Each eval case should include:

- `id`: stable identifier.
- `input`: user prompt plus relevant context.
- `expected`: exact value, semantic expectation, or rubric.
- `assertions`: deterministic checks first, model-graded checks only where needed.
- `metadata`: scenario type, difficulty, source fixture, and owner.

Prefer a mix of deterministic and rubric checks. Deterministic checks catch boring breakage cheaply; rubrics catch semantic failures where exact matching would be theater with a JSON costume.

## Assertion Types

Use deterministic assertions when possible:

- Parses as the required format.
- Matches JSON Schema, Zod, Pydantic, OpenAPI, or protobuf schema.
- Contains required fields and no forbidden fields.
- Cites only source IDs that exist in the retrieval context.
- Refuses or asks a clarification only when the expected behavior says so.

Use rubric assertions for quality:

```text
Score 0: Fails the task or contradicts context.
Score 1: Partially correct but misses important constraints or invents unsupported facts.
Score 2: Correct, grounded, complete, and follows the requested format.
Pass threshold: score >= 2.
```

## RAG-Specific Checks

For retrieval-augmented generation, separate retrieval quality from answer quality:

- Retrieval assertions: expected source appears in top-k, irrelevant source count stays below a limit, source metadata is preserved.
- Grounding assertions: answer uses retrieved context, unsupported claims are flagged, citations point to the right source chunks.
- Missing-context behavior: when retrieval has no answer, the model says it cannot determine the answer instead of improvising. Improvisation is charming at jazz night, less so in support automation.

## Prompt Regression Harness

Generate or extend a runner that:

- Loads eval cases from a fixture file.
- Calls the model or application entry point with the same settings each run.
- Records model name, prompt version, temperature, retrieval index version, and dependency versions.
- Stores raw outputs and assertion results.
- Fails CI only on stable, deterministic checks unless the team explicitly accepts model-graded CI gates.

## Output Files

Common outputs:

- `evals/<feature>.jsonl` or `evals/<feature>.yaml` for cases.
- `evals/run_<feature>.*` for the runner.
- `evals/rubrics/<feature>.md` for human/model grading criteria.
- `evals/reports/` for generated run results when the repo already stores benchmark artifacts.
