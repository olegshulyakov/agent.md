# C# Backend

Use this reference for ASP.NET Core, Minimal APIs, controllers, workers, and .NET backend code.

Follow the existing style: Minimal APIs, controllers, MediatR/CQRS, or service classes. Validate request models with data annotations, FluentValidation, endpoint filters, or the local convention. Keep endpoint methods thin and put business behavior in services/handlers.

Use dependency injection for new collaborators. Reuse EF Core, Dapper, or the existing persistence layer. Put transaction boundaries around multi-write operations and use cancellation tokens for request-scoped async calls. Use `IOptions<T>` or the local options pattern for configuration, and prefer `ProblemDetails` when the project already exposes it.

Tests should use the local xUnit, NUnit, MSTest, FluentAssertions, WebApplicationFactory, or mocking setup. Cover success, invalid input, auth failure when relevant, and persistence behavior at the appropriate test level. Verify with `dotnet test`, `dotnet format`, and nullable analysis conventions when configured.
