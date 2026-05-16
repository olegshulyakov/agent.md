# Go Chi Backend

Use this framework reference after `references/go.md` when the backend uses Chi.

Follow existing router composition, middleware, and handler package conventions. Keep handlers focused on parsing input, checking auth context, calling services, and writing responses.

Use the repository's JSON decoding, validation, response, and error helpers. Pass request context through downstream calls. Keep route registration near the existing route grouping rather than creating a parallel router shape.

Tests should use `httptest`, local route builders, fixtures, and service fakes or mocks. Cover success, malformed input, permission behavior when relevant, and one service-level edge case.
