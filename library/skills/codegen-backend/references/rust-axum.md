# Rust Axum Backend

Use this framework reference after `references/rust.md` when the backend uses Axum.

Follow existing router composition, extractor, state, middleware, and error response patterns. Keep handlers focused on extraction, authorization context, service calls, and response conversion.

Use typed state and extractors rather than global clients. Preserve the repository's async runtime, tracing, error enum, and serialization conventions. Avoid blocking work in async handlers unless it is isolated with the project's chosen strategy.

Tests should use the local tower service, request builder, fixtures, and test database or repository fakes. Cover successful handling, extractor or validation failure, auth failure when relevant, and one service or persistence edge case.
