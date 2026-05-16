# Node.js NestJS Backend

Use this framework reference after `references/nodejs.md` when the backend is NestJS.

Respect Nest module boundaries. Add controllers, providers, DTOs, guards, pipes, interceptors, and repositories in the existing style, and wire dependencies through constructor injection rather than module-level singletons.

Keep controllers thin and put business behavior in injectable services or command/query handlers. Use DTOs with `class-validator`, `class-transformer`, Zod, or the project's chosen validation approach. Reuse exception filters, guards, interceptors, and persistence abstractions already present.

Tests should use the local Nest testing module, Jest or Vitest setup, and mocks/fakes already used by the project. Cover service behavior, controller validation/error mapping, and guard or permission behavior when relevant.
