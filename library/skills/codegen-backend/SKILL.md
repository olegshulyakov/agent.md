---
name: codegen-backend
description: >
  Generate production-ready backend code. Use for API routes, services, middleware,
  workers, persistence, validation, auth integration, and backend tests across common
  backend languages, including TIOBE top-language ecosystems.
author: Oleg Shulyakov
license: MIT
version: 1.0.0
---

# codegen-backend

Router skill for implementing backend code. Detect the target language and framework from the user's request and repository context, then read exactly one language reference before editing or drafting code. If one framework is clearly identified, also read the matching flat framework reference from `references/`.

## Variant Detection

Check signals in this order:

1. Explicit user intent: language names, framework names, package managers, runtime names, file paths, or extensions.
2. Existing files and dependencies: `pyproject.toml`, `requirements.txt`, `package.json`, `go.mod`, `pom.xml`, `build.gradle`, `Gemfile`, `Cargo.toml`, `.csproj`, `composer.json`, `mix.exs`, source folders, imports, test directories, and CI jobs.
3. Target surface: HTTP routes, controllers, services, repositories, jobs, workers, middleware, validators, persistence, configuration, observability, and tests route to the language owning the existing backend surface.
4. Contract-first API requests route away to `design-api` unless the user explicitly asks to implement from an existing contract.
5. Specialized auth, GraphQL, real-time, database-only SQL, and test-only requests should use `patterns-auth`, `patterns-graphql`, `patterns-realtime`, `writer-sql`, or `codegen-test` when those are the primary artifact.
6. If still ambiguous, ask one short clarifying question naming the likely languages.

## Language Routing Table

| Signal | Reference |
| --- | --- |
| FastAPI, Django, Flask, Pydantic, SQLAlchemy, pytest, `pyproject.toml`, `.py` | `references/python.md` |
| Express, Fastify, NestJS, Hono, Zod, Prisma, Vitest/Jest, `package.json`, `.js`, `.ts` | `references/nodejs.md` |
| `net/http`, Chi, Gin, Echo, sqlc, GORM, `go.mod`, `.go` | `references/go.md` |
| Spring Boot, Jakarta, Maven, Gradle, JPA, JUnit, `pom.xml`, `.java` | `references/java.md` |
| Rails, Sinatra, ActiveRecord, Sidekiq, RSpec, `Gemfile`, `.rb` | `references/ruby.md` |
| Axum, Actix Web, Tokio, SQLx, Diesel, `Cargo.toml`, `.rs` | `references/rust.md` |
| ASP.NET Core, Minimal APIs, Controllers, EF Core, xUnit, `.csproj`, `.cs` | `references/csharp.md` |
| Laravel, Symfony, Eloquent, Artisan, Pest/PHPUnit, `composer.json`, `.php` | `references/php.md` |
| Ktor, Kotlin Spring Boot, coroutines, Exposed, Gradle Kotlin DSL, `.kt` | `references/kotlin.md` |
| Phoenix, Plug, Ecto, Oban, ExUnit, `mix.exs`, `.ex`, `.exs` | `references/elixir.md` |
| C services, embedded backends, POSIX sockets, libuv, Mongoose/CivetWeb, CMake, Make, `.c`, `.h` | `references/c.md` |
| C++ services, Boost.Asio/Beast, Drogon, Pistache, gRPC, CMake, Conan, vcpkg, `.cpp`, `.hpp` | `references/cpp.md` |
| VB.NET, ASP.NET, .NET Framework, Windows services, `.vbproj`, `.vb` | `references/visual-basic.md` |
| plumber, Shiny APIs, RServe, batch analytics services, `renv.lock`, `.R`, `.Rmd` | `references/r.md` |
| Delphi/Object Pascal services, RAD Server, DataSnap, Horse, Lazarus, `.pas`, `.dpr` | `references/delphi.md` |
| Fortran numerical services, ISO_C_BINDING, fpm, CMake, batch compute jobs, `.f90`, `.f` | `references/fortran.md` |
| Perl web services, Mojolicious, Dancer2, Catalyst, DBI, CPAN, `cpanfile`, `.pl`, `.pm` | `references/perl.md` |
| Swift server code, Vapor, Hummingbird, SwiftNIO, Package.swift, `.swift` | `references/swift.md` |
| Ada services, GNAT, Alire, SPARK, AWS Ada Web Server, `.adb`, `.ads` | `references/ada.md` |
| MATLAB production server code, batch workers, toolboxes, `.m`, `.mlx`, `startup.m` | `references/matlab.md` |

## Framework References

After reading the language reference, read at most one framework reference when the signal is explicit or unambiguous from repository dependencies and file layout. Keep framework files flat in `references/`.

| Signal | Framework reference |
| --- | --- |
| FastAPI, Starlette route dependencies | `references/python-fastapi.md` |
| Django, Django REST Framework, `manage.py` | `references/python-django.md` |
| Flask, Flask blueprints | `references/python-flask.md` |
| Express, Express Router | `references/nodejs-express.md` |
| Fastify, Fastify plugins | `references/nodejs-fastify.md` |
| NestJS, modules, providers, decorators | `references/nodejs-nestjs.md` |
| Hono | `references/nodejs-hono.md` |
| Nitro, h3 server handlers | `references/nodejs-nitro.md` |
| Gin | `references/go-gin.md` |
| Chi | `references/go-chi.md` |
| Echo | `references/go-echo.md` |
| Fiber | `references/go-fiber.md` |
| Spring Boot | `references/java-spring-boot.md` |
| Quarkus | `references/java-quarkus.md` |
| Micronaut | `references/java-micronaut.md` |
| Ktor | `references/kotlin-ktor.md` |
| Rails | `references/ruby-rails.md` |
| Sinatra | `references/ruby-sinatra.md` |
| Laravel | `references/php-laravel.md` |
| Symfony | `references/php-symfony.md` |
| Axum | `references/rust-axum.md` |
| Actix Web | `references/rust-actix-web.md` |
| Rocket | `references/rust-rocket.md` |
| ASP.NET Core, Minimal APIs, controllers | `references/csharp-aspnet-core.md` |
| Phoenix | `references/elixir-phoenix.md` |

## Working Rules

- Inspect the repository before writing code. Reuse its architecture, naming, dependency injection, error handling, validation, logging, tests, factories, and migration conventions.
- Keep the change as simple as the request allows. Prefer the smallest complete route, service, persistence, and test updates over speculative framework work or unused extension points.
- Prefer small, cohesive changes across route/controller, service/domain logic, persistence, validation, and tests. Do not hide business rules in transport handlers when the existing project has a service layer.
- Apply SOLID pragmatically: keep handlers thin, give services and domain objects clear responsibilities, keep interfaces narrow, and depend on abstractions only when the project already uses them or the boundary improves testing or integration safety.
- Treat public API behavior as a contract. Preserve backward compatibility unless the user explicitly asks for a breaking change, and update docs or generated specs when the repo already keeps them in sync.
- Validate input at the boundary, enforce authorization before side effects, and keep secrets in existing configuration mechanisms or environment variables.
- Use transactions around multi-write operations. Make idempotency, retries, and concurrency behavior explicit for jobs, webhooks, payments, and external integrations.
- Return consistent errors using the project's existing envelope or framework conventions. Avoid leaking stack traces, raw SQL errors, tokens, or internal IDs in user-facing responses.
- Add or update focused tests for the changed behavior. Use the repository's test runner and fixtures instead of inventing parallel test infrastructure.
- Run the narrowest relevant formatter, linter, typecheck, and tests available. If a command cannot be run, state why and include the command the user should run.

## Output Format

When editing a repository, finish with changed files, run commands, and verification status.

When only drafting code, use this structure:

```text
Assumptions:
- ...

Files:
- path/to/file

Run:
- command

Notes:
- ...
```
