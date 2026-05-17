# Kotlin Ktor Backend

Use this framework reference after `references/kotlin.md` when the backend uses Ktor.

Follow existing Ktor module, route, plugin, serialization, authentication, and configuration conventions. Keep route handlers focused on call parsing, validation, auth context, service calls, and response mapping.

Use Kotlin serialization, Jackson, or the project's existing serializer consistently. Preserve coroutine boundaries and avoid blocking calls on request coroutines unless the project already dispatches them explicitly. Keep dependency wiring in the established application module or DI framework.

Tests should use Ktor's test application utilities, local fixtures, and service fakes or mocks. Cover success, invalid input, auth failure when relevant, and service-level edge cases.
