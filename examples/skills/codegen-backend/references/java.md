# Java Backend

Use this reference for Spring Boot, Jakarta, or Java service code.

Follow the existing layering, usually controller, service, repository, DTO, and entity. Keep controllers thin, validate DTOs with Jakarta Bean Validation or the local convention, and keep transactional business logic in services. Use records for immutable DTOs when the project already targets a Java version that supports them.

Reuse Spring configuration, dependency injection, error handlers, and persistence conventions. Put `@Transactional` on service methods that own write consistency, not on controllers. Do not leak JPA entities directly through public APIs unless the existing project intentionally does that. Avoid lazy-loading surprises in response mapping; fetch explicitly when the API needs related data.

Tests should use the local mix of JUnit, Mockito, AssertJ, Spring MVC/WebTestClient, or Testcontainers. Cover service behavior and controller validation/error mapping at the narrowest practical level. Verify with the existing Maven or Gradle test task and formatter/checkstyle task when present.
