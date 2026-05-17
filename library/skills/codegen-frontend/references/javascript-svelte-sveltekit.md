# SvelteKit

Use this reference for SvelteKit routes, layouts, load functions, actions, server modules, and progressive enhancement.

Keep data reads in `load` functions and mutations in form actions or server endpoints according to local conventions. Keep secrets in server-only modules and private environment variables. Use `enhance`, `fail`, redirects, and error handling consistently.

Respect universal versus server-only load boundaries. Avoid browser-only APIs during SSR unless guarded. Keep route params, generated types, and invalidation behavior explicit when data changes.
