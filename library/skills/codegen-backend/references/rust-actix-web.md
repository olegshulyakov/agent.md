# Rust Actix Web Backend

Use this framework reference after `references/rust.md` when the backend uses Actix Web.

Follow existing route configuration, extractor, app data, middleware, and responder patterns. Keep handlers focused on request extraction, auth context, service calls, and response mapping.

Reuse the project's shared state, error types, validation approach, tracing, and persistence abstractions. Do not introduce blocking operations into async handlers without using the project's established isolation pattern.

Tests should use the local Actix test utilities, fixtures, and service or repository fakes. Cover success, bad input, auth failure when relevant, and one service or persistence edge case.
