---
name: setup-test-framework
description: >
  Generates test framework scaffolding with configuration, folder structure, conventions, example tests,
  and CI integration for the detected tech stack. Use this skill whenever the user wants to set up a
  testing framework from scratch, configure Jest, Pytest, Vitest, Go testing, JUnit, RSpec, or similar,
  add a test folder structure, create test conventions documentation, or asks to "set up testing for this
  project", "configure Jest", "scaffold our test setup", "what's the right test structure for X",
  "create a testing baseline", or "add unit/integration tests to this project". Also trigger for "how
  should we organize tests", "configure test coverage thresholds", and "set up test database".
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# setup-test-framework

Generate **test framework scaffolding** including configuration, folder structure, conventions, and example tests ready to run.

## Framework detection

Identify the framework from context:
1. **Language**: TypeScript/JS → Jest or Vitest, Python → Pytest, Go → stdlib testing, Java → JUnit 5, Ruby → RSpec, Rust → cargo test
2. **Explicit mention**: "Jest", "Vitest", "Pytest", "Jest", "Mocha", "Cypress"
3. **Package files**: `package.json` (check existing test script), `pyproject.toml`, `pom.xml`

**Framework recommendation by stack:**
- Node.js/TypeScript: **Vitest** (faster, native ESM) or **Jest** (more ecosystem)
- React/Vue apps: **Vitest** + **Testing Library**
- Python: **Pytest** + **pytest-cov** + **httpx** (for API testing)
- Go: **stdlib testing** + **testify** for assertions
- Java/Spring: **JUnit 5** + **Mockito** + **TestContainers**

## Output structure

Produce:
1. Configuration files (jest.config.ts, pytest.ini, etc.)
2. Folder structure with README
3. Test utilities (factories, fixtures, helpers)
4. Example test files (unit + integration)
5. CI integration snippet
6. Coverage configuration

---

## Node.js / TypeScript (Vitest)

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',  // or 'jsdom' for frontend
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'dist/', '**/*.d.ts', '**/__mocks__/**'],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 70,
        statements: 80,
      },
    },
    setupFiles: ['./src/test/setup.ts'],
  },
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') },
  },
});
```

```typescript
// src/test/setup.ts — global test setup
import { beforeAll, afterAll, beforeEach } from 'vitest';

// Database setup for integration tests
beforeAll(async () => {
  // await db.migrate.latest()
});

afterAll(async () => {
  // await db.destroy()
});

beforeEach(async () => {
  // await db.seed.run() — or truncate tables for isolation
});
```

```typescript
// src/test/factories/user.factory.ts — test data builder
import { User } from '../../models/user';

let counter = 0;

export function buildUser(overrides: Partial<User> = {}): User {
  counter++;
  return {
    id: counter,
    email: `user-${counter}@example.com`,
    name: `Test User ${counter}`,
    role: 'viewer',
    createdAt: new Date(),
    ...overrides,
  };
}
```

```typescript
// Example unit test: src/services/__tests__/user.service.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { UserService } from '../user.service';
import { UserRepository } from '../../repositories/user.repository';
import { buildUser } from '../../test/factories/user.factory';

vi.mock('../../repositories/user.repository');

describe('UserService', () => {
  let userService: UserService;
  let mockRepo: UserRepository;

  beforeEach(() => {
    mockRepo = new UserRepository() as vi.Mocked<UserRepository>;
    userService = new UserService(mockRepo);
  });

  describe('findById', () => {
    it('returns user when found', async () => {
      const user = buildUser({ id: 1 });
      vi.mocked(mockRepo.findById).mockResolvedValue(user);

      const result = await userService.findById(1);

      expect(result).toEqual(user);
      expect(mockRepo.findById).toHaveBeenCalledWith(1);
    });

    it('throws NotFoundError when user does not exist', async () => {
      vi.mocked(mockRepo.findById).mockResolvedValue(null);

      await expect(userService.findById(999)).rejects.toThrow('User not found');
    });
  });
});
```

---

## Python (Pytest)

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
addopts = [
  "--cov=src",
  "--cov-report=term-missing",
  "--cov-report=html",
  "--cov-fail-under=80",
  "-v",
]

[tool.coverage.report]
exclude_lines = [
  "pragma: no cover",
  "if TYPE_CHECKING:",
  "raise NotImplementedError",
]
```

```
tests/
├── conftest.py          # Shared fixtures
├── factories/
│   └── user_factory.py  # Test data builders
├── unit/
│   └── services/
│       └── test_user_service.py
└── integration/
    └── api/
        └── test_users_api.py
```

```python
# tests/conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.main import app
from src.database import Base

TEST_DB_URL = "postgresql+asyncpg://test:test@localhost:5432/testdb"

@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def db(engine):
    async with AsyncSession(engine) as session:
        yield session
        await session.rollback()

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
```

---

## Folder structure conventions

```
src/
└── services/
    ├── user.service.ts
    └── __tests__/
        ├── user.service.test.ts      # unit tests
        └── user.service.int.test.ts  # integration tests

tests/                # Alternative: top-level test directory
├── unit/
├── integration/
└── e2e/
```

**Naming conventions:**
- Unit tests: `*.test.ts` / `test_*.py` — test a single unit in isolation (mock dependencies)
- Integration tests: `*.int.test.ts` / `test_*_integration.py` — test with real database/services
- E2E: see `codegen-test-e2e` skill

## package.json scripts to add

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "test:unit": "vitest run --testPathPattern=unit",
    "test:integration": "vitest run --testPathPattern=int"
  }
}
```

## CI snippet

```yaml
# Add to your CI pipeline
- name: Run tests
  run: npm run test:coverage
- name: Upload coverage
  uses: codecov/codecov-action@v4
  with:
    files: ./coverage/coverage-final.json
```
