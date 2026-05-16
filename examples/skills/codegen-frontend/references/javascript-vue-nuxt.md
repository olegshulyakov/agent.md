# Nuxt

Use this reference for Nuxt applications with file routing, layouts, server routes, Nitro, auto-imported composables, and SSR/SSG behavior.

Follow Nuxt directory conventions for `pages`, `layouts`, `components`, `composables`, `server`, and middleware. Use `useAsyncData`, `useFetch`, route rules, and runtime config consistently. Keep private runtime config on the server and expose only intended public config.

Handle hydration carefully: avoid client-only APIs during server render unless guarded or wrapped in Nuxt client-only patterns. Keep SEO metadata, loading, error, and navigation behavior aligned with nearby pages.
