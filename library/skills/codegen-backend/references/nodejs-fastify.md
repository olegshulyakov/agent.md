# Node.js Fastify Backend

Use this framework reference after `references/nodejs.md` when the backend is Fastify.

Follow the existing plugin structure, decoration pattern, schema validation, and request typing. Register routes through the local module/plugin convention, and keep handlers focused on transport concerns while services own business behavior.

Use Fastify schemas or the project's validator for params, query, body, and response shapes. Reuse existing error handlers, logging, hooks, auth decorators, and database clients. Preserve encapsulation boundaries between plugins.

Tests should use the local `fastify.inject()` or HTTP integration setup. Cover schema validation, hook/auth behavior when relevant, successful handling, and service or persistence edge cases.
