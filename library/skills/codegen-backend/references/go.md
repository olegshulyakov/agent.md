# Go Backend

Use this reference for Go HTTP services, workers, and backend packages.

Follow the existing package layout. Keep handlers focused on decoding, validation, auth context extraction, calling services, and encoding responses. Put domain behavior in small services with explicit dependencies. Pass `context.Context` through request-scoped calls. Return errors with enough context for logs while mapping them to stable API responses at the boundary.

Prefer stdlib patterns when the project uses them; otherwise match existing routers such as Chi, Gin, Echo, or Fiber. Use the established persistence layer, whether database/sql, sqlc, GORM, Ent, or repository interfaces. Avoid package-level mutable state for test-sensitive dependencies. Wrap errors with context using `%w`; compare errors with `errors.Is`/`errors.As`.

Tests should be table-driven where useful. Use `httptest` for handlers, fakes for interfaces, and repository integration tests only when the repo already has database test setup. Verify with `gofmt`, `go test ./...`, and `go vet ./...` when practical.
