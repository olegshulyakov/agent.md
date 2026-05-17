# Java Quarkus Backend

Use this framework reference after `references/java.md` when the backend is Quarkus.

Follow existing Quarkus conventions for REST resources, CDI beans, repositories, Panache, configuration, health checks, and extensions. Keep resource classes focused on HTTP concerns and put business behavior in application services or domain classes.

Use constructor or CDI injection according to the project style. Preserve the existing reactive or imperative stack; do not mix RESTEasy Reactive, blocking persistence, and reactive clients casually. Use Bean Validation for request DTOs, Quarkus config mechanisms for settings, and the established exception mapping approach.

Tests should use the local `@QuarkusTest`, REST-assured, Panache/repository test helpers, mocks, and Testcontainers setup when present. Cover validation, authorization when relevant, successful behavior, and transaction or persistence edge cases.
