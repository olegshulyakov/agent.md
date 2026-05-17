# Node.js Hono Backend

Use this framework reference after `references/nodejs.md` when the backend uses Hono.

Follow existing Hono app composition, route grouping, middleware, validator, binding, and runtime conventions. Keep handlers focused on request parsing, auth context, service calls, and response mapping.

Preserve the target runtime assumptions, such as Node.js, Bun, Deno, Cloudflare Workers, or another edge runtime. Use the project's typed context variables, environment bindings, error handling, and validation library rather than adding parallel abstractions.

Tests should use the local request/app testing helpers, runtime mocks, and service fakes. Cover success, validation failure, auth failure when relevant, and one service or integration edge case.
