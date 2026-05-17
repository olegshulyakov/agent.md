# C# ASP.NET Core Backend

Use this framework reference after `references/csharp.md` when the backend is ASP.NET Core.

Follow the existing style for Minimal APIs, controllers, endpoint groups, MediatR/CQRS handlers, services, filters, middleware, and options. Keep endpoints and controllers thin while services or handlers own business behavior.

Use dependency injection, cancellation tokens, model binding, validation, authorization policies, and `ProblemDetails` according to the local conventions. Reuse EF Core, Dapper, or the project's persistence abstraction, and put transaction boundaries around multi-write operations.

Tests should use the local xUnit, NUnit, MSTest, `WebApplicationFactory`, FluentAssertions, mocks, and test database strategy. Cover success, validation failure, authorization failure when relevant, and persistence behavior for writes.
