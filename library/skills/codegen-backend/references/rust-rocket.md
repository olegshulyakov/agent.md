# Rust Rocket Backend

Use this framework reference after `references/rust.md` when the backend uses Rocket.

Follow existing route, guard, managed state, fairing, responder, and error catcher conventions. Keep handlers focused on request guards, validation, service calls, and response conversion.

Use Rocket's typed request guards and managed state rather than global clients. Preserve the project's async, database pool, serialization, and error response patterns. Avoid blocking operations in async handlers unless the project already isolates them.

Tests should use Rocket's local client or the repository's integration setup. Cover successful handling, guard or validation failure, auth failure when relevant, and one service or persistence edge case.
