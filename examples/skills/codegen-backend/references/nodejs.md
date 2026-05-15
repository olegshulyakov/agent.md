# Node.js Backend

Use this reference for Express, Fastify, NestJS, Hono, or Node.js/TypeScript service code.

Prefer TypeScript when the project uses it. Keep route handlers thin, validate request bodies and params with the existing validator, commonly Zod, Joi, class-validator, or framework schemas, and put business behavior in services/use cases. Reuse the existing database client, ORM, or query builder such as Prisma, TypeORM, Drizzle, Knex, or Sequelize.

Propagate async failures through the framework's error path. Use the existing error class/envelope and avoid throwing plain strings. Keep environment access centralized in config modules. For external integrations, include timeout, retry, and idempotency behavior where the domain needs it. Keep ESM/CommonJS, path aliases, and runtime validation style consistent with the repository.

Tests should use the local runner, usually Vitest, Jest, Mocha, Supertest, or the framework test utilities. Cover success, validation failure, authorization failure when relevant, and service-level edge cases without relying on real network services. Verify with existing `test`, `lint`, and `typecheck` scripts when available.
