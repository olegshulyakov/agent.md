# Java Spring Boot Backend

Use this framework reference after `references/java.md` when the backend is Spring Boot.

Follow existing package layering for controllers, services, repositories, DTOs, entities, mappers, configuration, and exception handling. Keep controllers thin and put transactional business behavior in services.

Use constructor injection, Jakarta Bean Validation, the project's mapper style, and the existing error response format. Put `@Transactional` on service methods that own consistency, and avoid returning JPA entities from public APIs unless that is already the explicit convention.

Tests should use the local mix of JUnit, Mockito, AssertJ, `@WebMvcTest`, `@SpringBootTest`, WebTestClient, or Testcontainers. Cover validation, error mapping, authorization when relevant, and service transaction behavior for writes.
