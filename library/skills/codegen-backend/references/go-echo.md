# Go Echo Backend

Use this framework reference after `references/go.md` when the backend uses Echo.

Follow the existing route grouping, middleware, binder, validator, and handler conventions. Keep Echo handlers focused on binding, validation, auth context, service calls, and response mapping.

Reuse the project's custom validator, error handler, logger, and context helpers. Pass `context.Context` into services and stores when the local code does that. Avoid mixing unrelated route groups or middleware chains.

Tests should use Echo's request/response recorder setup or the repository's helper wrappers. Cover successful handling, validation failure, auth failure when relevant, and a service or persistence edge case.
