# Swift Backend

Use this reference for server-side Swift, Vapor, Hummingbird, SwiftNIO, and Package.swift backend projects.

Follow the existing package structure, async style, and framework conventions. Keep route handlers thin, validate request content at the boundary, and put business behavior into services. Use Swift concurrency or EventLoopFuture consistently with the project; avoid mixing them casually.

Reuse Fluent, SQLKit, PostgresNIO, or the local persistence layer. Make transaction boundaries explicit for multi-write workflows. Preserve response and error middleware behavior. Keep `Sendable`, actor isolation, and event-loop affinity intact; do not block event loops with synchronous I/O.

Tests should use XCTest or the framework's testing helpers. Cover success, validation failure, authorization failure when relevant, and async error handling. Verify with `swift test`, formatting/linting tools, and package resolution checks when configured.
