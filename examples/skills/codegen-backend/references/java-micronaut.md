# Java Micronaut Backend

Use this framework reference after `references/java.md` when the backend is Micronaut.

Follow existing Micronaut conventions for controllers, singleton services, repositories, configuration properties, validation, filters, and HTTP clients. Keep controllers thin and put business behavior in services or domain modules.

Use constructor injection and compile-time DI patterns. Preserve the project's reactive, coroutine, or blocking style, and avoid adding runtime reflection assumptions that conflict with Micronaut's ahead-of-time model. Keep configuration in `application.yml` or the established config mechanism.

Tests should use the local `@MicronautTest`, HTTP client, mocks, and repository/database setup. Cover successful requests, validation failure, authorization or filter behavior when relevant, and one service or persistence edge case.
