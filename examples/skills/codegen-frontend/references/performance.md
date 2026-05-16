# Frontend Performance

Use this reference for bundle size, rendering cost, Core Web Vitals, loading behavior, image/media optimization, hydration, and perceived speed.

Measure or infer the likely bottleneck before changing architecture. Prefer smaller bundles, route-level code splitting, lazy loading for below-the-fold or rarely used UI, optimized images, and fewer client-only dependencies. Avoid adding heavy libraries for simple UI behavior.

Keep loading states useful and layout-stable. Reserve media dimensions, avoid large layout shifts, and defer non-critical work. Use virtualization for long lists only when it is needed and when accessibility remains acceptable.

Verify with the project's build, analyzer, Lighthouse setup, browser performance tooling, or framework diagnostics when available.
