# Go Fiber Backend

Use this framework reference after `references/go.md` when the backend uses Fiber.

Follow existing app setup, route grouping, middleware, context, validation, and response helper conventions. Keep handlers focused on parsing Fiber context data, checking auth context, calling services, and mapping responses.

Remember that Fiber's context model differs from `net/http`; use the repository's established bridge to `context.Context` for downstream service and database calls. Avoid retaining `*fiber.Ctx` beyond the request lifetime.

Tests should use the local Fiber app test helpers, fixtures, and service fakes or mocks. Cover successful handling, validation failure, auth failure when relevant, and one service or persistence edge case.
