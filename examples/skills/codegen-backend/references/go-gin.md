# Go Gin Backend

Use this framework reference after `references/go.md` when the backend uses Gin.

Keep Gin handlers focused on binding, validation, auth context, and response mapping. Put business logic in services and persistence logic in repositories or stores according to the local package structure.

Use the project's binding tags, validator setup, middleware, logger, and error response helpers. Pass `context.Context` through service and database calls when the project exposes request context. Avoid panics for ordinary request errors.

Tests should use the local Gin test setup, `httptest`, fixtures, and mocks or test stores. Cover successful handling, bind/validation failure, auth failure when relevant, and one service or persistence edge case.
