# JavaScript Frontend

Use this reference for JavaScript frontend code, including `.js`, `.jsx`, plain Vite apps, framework projects without TypeScript, and progressive enhancement scripts.

Follow the project's module style, lint rules, and component conventions. Keep data shapes clear with small helper functions, JSDoc annotations when the repo uses them, and runtime checks at untrusted boundaries. Avoid broad object mutation when rendering depends on predictable state updates.

Prefer readable composition over clever abstractions. Keep side effects in lifecycle hooks, loaders, services, or existing state utilities. Use named exports and file organization consistent with the repository. If the surrounding project is migrating toward TypeScript, avoid adding patterns that make a later conversion harder.
