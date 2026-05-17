# API Test Generation

Use this reference for HTTP endpoint, controller, contract, and service integration test suites.

## Framework Selection

Prefer the repository's existing stack:

| Signal | Pattern |
| --- | --- |
| Node with `supertest`, `jest`, `vitest`, `mocha` | Supertest plus the existing runner |
| Postman collection or Newman scripts | Postman/Newman collection tests |
| Python with `pytest`, `httpx`, `requests`, FastAPI/Flask/Django tests | Existing pytest/client fixture |
| Java/Kotlin with Spring test dependencies | MockMvc, WebTestClient, or REST-assured |
| Go with `net/http/httptest` | Standard library HTTP tests |

## Implementation Pattern

- Reuse app factories, test clients, database fixtures, auth helpers, and factories already in the repo.
- Assert status, response shape, important headers, and durable side effects. Avoid snapshotting whole payloads unless the repo already does so.
- Include negative tests for validation, missing auth, forbidden access, nonexistent resources, and idempotency where relevant.
- Keep tests independent by creating fresh data or using rollback fixtures.
- Use contract examples from OpenAPI/AsyncAPI schemas when available, and keep generated payloads realistic.
- Never hard-code secrets. Use test tokens, factories, or environment variables.

## Suite Shape

For each endpoint or resource, cover:

- Successful create/read/update/delete or command/query behavior.
- Validation failure with specific field-level expectations.
- Authentication or authorization failure.
- Not-found or conflict behavior where the API exposes it.
- Side effects such as emitted events, database rows, or downstream calls when the repo has test hooks for them.

## Supertest Example

```ts
import request from 'supertest';
import { createApp } from '../src/app';

describe('POST /api/widgets', () => {
  it('creates a widget', async () => {
    const app = createApp();

    const response = await request(app)
      .post('/api/widgets')
      .send({ name: 'Launch checklist' })
      .expect(201);

    expect(response.body).toMatchObject({
      name: 'Launch checklist',
      status: 'active',
    });
  });
});
```

## Postman/Newman Pattern

When producing a collection, include request examples, environment variables, pre-request auth setup if needed, and tests for status code plus key JSON fields. Keep environment-specific base URLs as variables.

## Pytest API Pattern

Use the app's test client fixture. Prefer explicit payload factories over inline repetition when multiple tests use the same shape.
