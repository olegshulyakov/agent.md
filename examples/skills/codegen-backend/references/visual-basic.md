# Visual Basic Backend

Use this reference for VB.NET backend code, ASP.NET applications, .NET Framework services, Windows services, and legacy Visual Basic maintenance.

Follow the existing .NET style, project file, dependency injection approach, and error conventions. Keep controllers or service entry points thin, put business behavior in service classes, and reuse local validation and persistence patterns.

For ASP.NET or Web API work, preserve existing response envelopes and authorization behavior. For Windows services or background jobs, make retry, scheduling, logging, and shutdown behavior explicit. Avoid broad rewrites from VB to C# unless the user asks. Respect `Option Strict`, nullable/reference conventions, and legacy .NET Framework constraints.

Tests should use the repository's MSTest, NUnit, xUnit, or integration harness. Cover success, validation failure, authorization failure when relevant, and legacy compatibility behavior. Verify with `dotnet test`, MSBuild, Visual Studio test tasks, or the existing CI commands.
