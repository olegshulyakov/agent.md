# Frontend State

Use this reference for client state, server state, stores, caches, optimistic updates, URL state, and cross-component coordination.

Separate server state from client UI state. Use the existing query/cache layer for remote data and the existing store/context mechanism for shared client state. Keep transient local interaction state inside components unless multiple surfaces truly need it.

Prefer URL state for filters, search, pagination, and shareable views when the app already supports it. Make optimistic updates reversible and handle conflict, retry, and failure states. Avoid global stores for one route's temporary controls.
