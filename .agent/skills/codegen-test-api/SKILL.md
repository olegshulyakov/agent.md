---
name: codegen-test-api
description: >
  Generates API test suites with happy path, edge case, error, and contract tests for REST and GraphQL APIs,
  using frameworks like Pytest, Jest/Supertest, RestAssured, k6, Postman/Newman, or Pact. Use this skill whenever
  the user wants to write API tests, test HTTP endpoints, create contract tests, test request/response schemas,
  add integration tests for an API, or asks to "write tests for this API", "generate API test cases", "test
  this endpoint", "add contract tests", or "create a Postman collection". Also trigger for "test this REST API",
  "write assertions for this response", and "generate fixtures for API testing". Distinct from codegen-test-e2e
  (browser/UI flow tests) and codegen-test-perf (load/performance tests).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# codegen-test-api

Generate **comprehensive API test suites** covering happy paths, edge cases, error handling, and contract validation.

## Variant detection

Identify the testing framework and language from context:

1. **Language/framework files**: `requirements.txt`/`pytest` → Python/Pytest, `package.json`/`jest`+`supertest` → Node.js, `pom.xml`/`RestAssured` → Java, `pubspec.yaml` → Dart
2. **Explicit mention**: "pytest", "jest", "supertest", "RestAssured", "Pact", "Postman", "Newman", "k6"
3. **Project language**: Python → Pytest + httpx, Node.js → Jest + supertest, Java → REST Assured, Go → testing + net/http/httptest
4. **If unclear**: Use Pytest (most readable, language-agnostic concepts)

## What to test in every API

For each endpoint, generate tests covering:

**Happy paths**
- Successful request with all required params → correct 2xx response and response body shape
- Paginated responses → correct page structure

**Edge cases**
- Boundary values (empty string, 0, max int, very long strings)
- Optional parameters omitted vs provided

**Error cases**
- Missing required fields → 400 with descriptive error
- Invalid types or formats → 400
- Unauthorized access → 401
- Forbidden (authenticated but wrong role) → 403
- Not found → 404
- Duplicate resource → 409

**Contract tests**
- Response schema matches expected shape (all required fields present and correct type)
- Response includes no sensitive fields (passwords, internal IDs, etc.)

## Output format

Produce complete test files. Include:
1. Test file(s) with imports, setup, teardown, and test cases
2. Fixture files if needed
3. Setup instructions (install dependencies, env vars, how to run)

### Example structure (Pytest)

```python
# tests/api/test_users.py
import pytest
import httpx

BASE_URL = "http://localhost:8000"

@pytest.fixture
def client():
    with httpx.Client(base_url=BASE_URL) as c:
        yield c

@pytest.fixture
def auth_headers(client):
    response = client.post("/auth/login", json={"email": "test@example.com", "password": "testpass"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

class TestGetUser:
    def test_returns_user_for_valid_id(self, client, auth_headers):
        response = client.get("/users/1", headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert "id" in body
        assert "email" in body
        assert "password" not in body  # sensitive field not exposed

    def test_returns_404_for_unknown_id(self, client, auth_headers):
        response = client.get("/users/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_returns_401_without_auth(self, client):
        response = client.get("/users/1")
        assert response.status_code == 401
```

### Example structure (Jest + Supertest)

```typescript
// tests/api/users.test.ts
import request from 'supertest';
import app from '../../src/app';

describe('GET /users/:id', () => {
  let authToken: string;

  beforeAll(async () => {
    const res = await request(app)
      .post('/auth/login')
      .send({ email: 'test@example.com', password: 'testpass' });
    authToken = res.body.access_token;
  });

  it('returns 200 with user data for valid id', async () => {
    const res = await request(app)
      .get('/users/1')
      .set('Authorization', `Bearer ${authToken}`);
    
    expect(res.status).toBe(200);
    expect(res.body).toMatchObject({ id: expect.any(Number), email: expect.any(String) });
    expect(res.body).not.toHaveProperty('password');
  });

  it('returns 401 without authentication', async () => {
    const res = await request(app).get('/users/1');
    expect(res.status).toBe(401);
  });

  it('returns 404 for non-existent user', async () => {
    const res = await request(app)
      .get('/users/99999')
      .set('Authorization', `Bearer ${authToken}`);
    expect(res.status).toBe(404);
  });
});
```

## Test organization conventions

- Group tests by resource/endpoint (one file per resource)
- Name tests in the format: `[action] [condition]` → `returns 200 when user exists`
- Keep test data deterministic — use fixed IDs or seeded test data, not random
- Isolate tests — each test should be runnable independently
- Clean up created data in `afterEach`/teardown when testing mutations

## Contract testing with Pact

When the user asks for contract tests between a consumer and provider:

```python
# Consumer side (what the consumer expects)
from pact import Consumer, Provider

pact = Consumer('frontend').has_pact_with(Provider('user-api'))

pact.given('user 1 exists').upon_receiving('a request for user 1').with_request(
    method='GET', path='/users/1',
    headers={'Authorization': 'Bearer token'}
).will_respond_with(
    status=200,
    body={'id': 1, 'email': 'user@example.com', 'name': 'Test User'}
)
```

## Calibration

- **OpenAPI spec provided**: Generate tests for all endpoints in the spec
- **Code provided**: Infer endpoints from route handlers
- **Description only**: Generate tests for the described endpoints with `[TODO: update base URL and auth]` markers
- **GraphQL**: Generate query/mutation tests with variables and error cases
