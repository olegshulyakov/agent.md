# Node.js Express Backend

Use this framework reference after `references/nodejs.md` when the backend is Express.

Keep routers and middleware small. Validate params, query, and body data before service calls, and propagate async failures through the existing error middleware. Reuse the project's request typing, auth middleware, response helpers, and error classes.

Put business behavior in services, use cases, or controllers according to the local architecture. Avoid adding ad hoc `try/catch` blocks that bypass centralized error handling unless the project already does that for response mapping.

Tests should use the existing Supertest, Jest, Vitest, Mocha, or integration setup. Cover route success, validation failure, auth failure when relevant, and one service-level edge case.
