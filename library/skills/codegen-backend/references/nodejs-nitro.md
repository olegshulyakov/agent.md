# Node.js Nitro Backend

Use this framework reference after `references/nodejs.md` when the backend uses Nitro or h3 server handlers.

Follow existing server route, event handler, middleware, storage, runtime config, and deployment preset conventions. Keep handlers focused on event parsing, validation, auth context, service calls, and response mapping.

Preserve the target runtime, such as Node.js, serverless, edge, or workers. Use the project's `h3` helpers, runtime config, error utilities, and storage abstractions. Avoid adding APIs that are unavailable in the deployment preset.

Tests should use the local Nuxt/Nitro, h3, or integration setup. Cover success, validation failure, authorization when relevant, and one service or runtime-specific edge case.
