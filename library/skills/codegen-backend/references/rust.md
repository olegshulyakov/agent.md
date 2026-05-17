# Rust Backend

Use this reference for Axum, Actix Web, Rocket, Tokio services, and Rust backend code.

Follow the existing module structure and error strategy. Keep handlers focused on extractors, validation, calling domain services, and response mapping. Use typed request/response structs with Serde. Prefer explicit domain errors that implement or map into the framework's response/error traits.

Respect ownership and lifetimes without adding broad cloning to silence the compiler. Use `Arc` for shared application state when the framework pattern requires it. Keep async code non-blocking, and run blocking work through the runtime's blocking facilities where needed. Reuse SQLx, Diesel, SeaORM, or the existing persistence layer. Prefer `Result` with typed errors over panics for recoverable service failures.

Tests should use unit tests for pure services and integration tests with the framework's test utilities when available. Include `cargo fmt`, `cargo clippy`, and `cargo test` in verification when practical.
