# Next.js

Use this reference for Next.js App Router or Pages Router projects.

Detect the router style from `app/`, `pages/`, imports, and config. In App Router, keep server components server-first by default and add `"use client"` only where browser state, effects, event handlers, or client-only libraries are required. Place metadata, layouts, route groups, loading, error, and not-found files according to local conventions.

Use server actions, route handlers, or existing API clients consistently with the repo. Keep cache behavior explicit with `revalidate`, `fetch` cache options, tags, or dynamic route settings when data freshness matters. Do not pass secrets into client components.

For Pages Router, follow `getServerSideProps`, `getStaticProps`, API route, and layout conventions already present. Verify with the project's typecheck, lint, and build because Next.js failures often hide at build time.
