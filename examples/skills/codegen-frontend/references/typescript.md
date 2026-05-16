# TypeScript Frontend

Use this reference for TypeScript frontend code, including `.ts`, `.tsx`, strict component props, typed routes, typed API clients, stores, hooks, composables, services, and test utilities.

Follow the repository's `tsconfig` strictness instead of weakening it. Prefer explicit domain types at module boundaries and inferred local types inside simple implementation details. Model UI states with discriminated unions when a component can be loading, empty, ready, or failed. Avoid `any`; use `unknown` at untrusted boundaries and narrow it with existing validators or type guards.

Keep public component props small and stable. Derive display data before rendering when it improves readability, but avoid premature memoization. Use framework-native event, ref, route, and async types. Respect path aliases, module format, generated API types, and shared schema packages already present in the repo.

For data from APIs, keep runtime validation if the project already uses Zod, Valibot, io-ts, GraphQL codegen, OpenAPI codegen, or generated clients. Do not treat compile-time types as proof that network data is valid.
