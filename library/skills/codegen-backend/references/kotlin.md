# Kotlin Backend

Use this reference for Kotlin Spring Boot, Ktor, and Kotlin backend services.

Follow the existing framework and layering. In Spring Boot, keep controllers thin, validate DTOs, put transactional work in services, and use repositories or Exposed according to the project. In Ktor, keep routing modules focused on transport behavior and delegate business logic to services.

Use data classes for request/response models and domain values where appropriate. Prefer coroutines for async work when the stack uses them, and avoid blocking calls on coroutine dispatchers unless the project isolates them. Use nullability as part of the contract; avoid `!!` in new code unless a local invariant makes it unavoidable.

Tests should use JUnit, Kotest, MockK, Spring test utilities, or Ktor test application helpers as configured. Cover success, validation failure, authorization failure when relevant, and service-level edge cases. Verify with the existing Gradle/Maven test task and ktlint/detekt if configured.
