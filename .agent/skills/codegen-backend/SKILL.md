---
name: codegen-backend
description: >
  Generates production-ready backend code including routes, services, middleware, repositories, and tests
  across multiple languages and frameworks (Python/FastAPI/Django, Node.js/Express/Fastify, Go, Java/Spring Boot,
  Ruby/Rails, Rust/Axum, C#/.NET, PHP/Laravel, Kotlin/Ktor, Elixir/Phoenix). Use this skill whenever
  the user wants to generate backend code, write a REST endpoint, implement a service, create middleware,
  build a controller, write server-side logic, scaffold a backend feature, or implement an API handler.
  Also trigger for "write the backend for X", "implement this endpoint", "create a service class",
  "add authentication", or "generate CRUD operations". Detect the language/framework from context automatically.
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# codegen-backend

Generate **production-ready backend code** — routes, services, middleware, repositories, and tests — for the detected language and framework.

## Variant detection

Identify the language/framework from context. Check in this order:

1. **File extensions in context**: `.py` → Python, `.ts`/`.js` + Express/Fastify → Node.js, `.go` → Go, `.java` → Java, `.rb` → Ruby, `.rs` → Rust, `.cs` → C#, `.php` → PHP, `.kt` → Kotlin, `.ex`/`.exs` → Elixir
2. **Import statements / package names**: `from fastapi import`, `require('express')`, `import gin`, `@SpringBootApplication`, `use actix_web`
3. **Project files**: `pyproject.toml`/`requirements.txt`, `package.json`, `go.mod`, `pom.xml`/`build.gradle`, `Gemfile`, `Cargo.toml`, `.csproj`, `composer.json`, `build.gradle.kts`
4. **Explicit user mention**
5. **If ambiguous**: ask once — "Which backend language are you using? (Python, Node.js, Go, Java, Ruby, Rust, C#, PHP, Kotlin, Elixir)"

Once identified, read the dialect-specific reference:

- **Python (FastAPI/Django)** → `references/python.md`
- **Node.js (Express/Fastify)** → `references/nodejs.md`
- **Go** → `references/go.md`
- **Java (Spring Boot)** → `references/java.md`
- **Ruby (Rails)** → `references/ruby.md`
- **Rust (Axum)** → `references/rust.md`
- **C# (.NET)** → `references/csharp.md`
- **PHP (Laravel)** → `references/php.md`
- **Kotlin (Spring/Ktor)** → `references/kotlin.md`
- **Elixir (Phoenix)** → `references/elixir.md`

## Universal output principles

Regardless of language, every code output must:

### 1. Follow the layered architecture

```
Route / Controller → Service → Repository → Database
```

Each layer has one responsibility. Routes handle HTTP; services hold business logic; repositories handle data access. Never put business logic in routes or raw SQL in services.

### 2. Validate inputs at the boundary

All incoming data is validated at the route/controller layer before reaching the service. Use the framework's native validation (Pydantic, Zod, Joi, Bean Validation, etc.).

### 3. Handle errors explicitly

Return meaningful HTTP status codes and error messages. Never let exceptions bubble as 500s when the cause is a client error.

```
400 Bad Request     — validation failure, malformed input
401 Unauthorized    — missing/invalid auth token
403 Forbidden       — authenticated but lacks permission
404 Not Found       — resource doesn't exist
409 Conflict        — unique constraint violation
422 Unprocessable   — semantically invalid (valid structure, invalid content)
429 Too Many Req.   — rate limit exceeded
500 Internal Error  — unexpected server-side failure (log + generic message)
```

### 4. Use dependency injection

Services and repositories should be injected, not instantiated inline. This enables testing.

### 5. Write idiomatic code

Match the community conventions for the detected language. Don't write Java-style code in Go or Python-style code in Java. The language reference files contain the idiomatic patterns.

### 6. Include tests

For every non-trivial piece of logic, produce at minimum a unit test for the service layer and an integration/route test for the endpoint.

## Code structure per feature

Produce files in this order:

1. **Model / Schema** — data shape (Pydantic model, Zod schema, struct, record class)
2. **Repository** — data access layer with CRUD operations
3. **Service** — business logic, orchestration, validation
4. **Route / Controller** — HTTP handling, input validation, response mapping
5. **Tests** — unit tests for service, integration tests for routes

Always show the file path as a comment at the top of each file:

```python
# src/users/user.service.py
```

## Authentication patterns

When auth is mentioned:

- **JWT**: validate in middleware; inject user context into route handlers
- **API key**: validate in middleware; rate-limit by key
- Never implement auth from scratch — use the framework's established libraries

## Example prompt → output mapping

**Input:** "Write a POST /users endpoint in FastAPI that creates a user with email and password, validates uniqueness, and returns the created user."

**Output:** (see references/python.md for FastAPI-specific patterns)

- `schemas/user.py` — Pydantic input/output models
- `repositories/user_repository.py` — DB operations
- `services/user_service.py` — business logic (hash password, check uniqueness)
- `routers/users.py` — FastAPI router with the POST endpoint
- `tests/test_users.py` — pytest tests for service and route

## Async considerations

- Python: use `async def` for FastAPI routes; use async DB drivers (asyncpg, SQLAlchemy async)
- Node.js: always async/await; never callbacks in new code
- Go: use goroutines appropriately; avoid blocking in handlers
- Kotlin: use coroutines for I/O

## What to include in output

For each file produced:

- Full file content (not snippets unless the user asked for a snippet)
- Import statements
- Error handling
- At least the signature of companion test functions (full tests when the logic is non-trivial)
- Brief inline comments on non-obvious decisions
