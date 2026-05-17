---
name: codegen-frontend
description: >
  Generate production-ready frontend code. Use for components, pages, routes,
  client state, forms, styling, accessibility, performance, PWA behavior, and
  data visualization in modern web frameworks.
author: Oleg Shulyakov
license: MIT
version: 1.0.0
---

# codegen-frontend

Router skill for implementing frontend code. Detect the target language/runtime, framework, styling system, and user-facing capability from the user's request and repository context. Read the smallest useful set of references before editing or drafting code.

## Variant Detection

Check signals in this order:

1. Explicit user intent: framework names, route/page names, component libraries, state libraries, CSS systems, test tools, file paths, or extensions.
2. Existing files and dependencies: `package.json`, lockfiles, `vite.config.*`, `next.config.*`, `remix.config.*`, `nuxt.config.*`, `angular.json`, `svelte.config.*`, `astro.config.*`, `tsconfig.json`, source folders, imports, design tokens, Storybook, and CI jobs.
3. Target surface: components, pages, layouts, routes, loaders/actions, forms, stores, queries, charts, responsive styling, accessibility fixes, PWA behavior, and performance work route to this skill.
4. Test-only requests route to `codegen-test`. API contract design routes to `design-api`. Backend implementation routes to `codegen-backend`. UI/UX design-only specs route to `writer-spec` or a design skill when no code is requested.
5. If still ambiguous, ask one short clarifying question naming the likely framework or styling options.

## Reference Routing

Read one language or markup reference first:

| Signal | Reference |
| --- | --- |
| HTML, templates, server-rendered views, static pages, Web Components markup, `.html`, `.htm` | `references/html.md` |
| TypeScript, `.ts`, `.tsx`, strict typing, typed components, `tsconfig.json` | `references/typescript.md` |
| JavaScript, `.js`, `.jsx`, no TypeScript configuration | `references/javascript.md` |

Read one framework reference when detected:

| Signal | Reference |
| --- | --- |
| React, JSX, hooks, React Query, Redux, Zustand | `references/javascript-react.md` |
| Next.js, App Router, Pages Router, RSC, server actions | `references/javascript-react-nextjs.md` |
| Remix, React Router data APIs, loaders, actions | `references/javascript-react-remix.md` |
| Vue, Composition API, Pinia, Vue Router | `references/javascript-vue.md` |
| Nuxt, Nitro, auto-imported composables, file routes | `references/javascript-vue-nuxt.md` |
| Angular, standalone components, services, RxJS, signals | `references/javascript-angular.md` |
| Svelte | `references/javascript-svelte.md` |
| SvelteKit | `references/javascript-svelte-sveltekit.md` |
| Astro, islands, content collections | `references/javascript-astro.md` |
| SolidJS, signals, SolidStart | `references/javascript-solidjs.md` |

Read styling references only when relevant:

| Signal | Reference |
| --- | --- |
| CSS modules, vanilla CSS, Sass, design tokens, layout, responsive styling | `references/css.md` |
| Tailwind, utility classes, variants, `tailwind.config.*` | `references/css-tailwind.md` |
| Bootstrap, React-Bootstrap, Bootstrap grid/utilities | `references/css-bootstrap.md` |
| MUI, Chakra, Mantine, Ant Design, Radix, shadcn/ui, Headless UI, design-system component APIs | `references/css-component-libraries.md` |

Read capability references when the work touches that concern:

| Request | Reference |
| --- | --- |
| WCAG, keyboard UX, focus, semantics, screen readers | `references/accessibility.md` |
| Locales, ICU messages, formatting, RTL, locale routing | `references/internationalization.md` |
| Validation, complex inputs, dirty state, error display | `references/forms.md` |
| Client/server state, caching, stores, optimistic UX | `references/state.md` |
| Bundle size, rendering, Core Web Vitals | `references/performance.md` |
| Service workers, manifest, offline mode, installability | `references/pwa.md` |
| Charts, dashboards, dense tables, interactive data | `references/visualization.md` |

## Working Rules

- Inspect the repository before writing code. Reuse its component boundaries, routing conventions, data-fetching layer, styling system, design tokens, test setup, lint rules, and accessibility patterns.
- Keep the implementation as simple as the workflow allows. Do not introduce new component layers, state stores, providers, or utility abstractions unless they remove real duplication or match established project patterns.
- Build the actual user-facing workflow, not a decorative placeholder. Prefer complete states: loading, empty, error, success, disabled, optimistic, validation, and permission states when they apply.
- Keep components cohesive. Put reusable primitives near the existing design system, route-specific composition near routes/pages, and side effects in the project's established data or state layer.
- Apply SOLID as frontend design guidance, not vocabulary theater: components should have clear responsibilities, props should stay small and explicit, and dependencies should flow through the project's existing hooks, context, loaders, or services.
- Preserve existing visual language. Do not add a new UI kit, styling library, icon set, state manager, chart library, or form library unless the request or repository already points there.
- Treat accessibility as implementation work, not a final checklist. Use semantic elements, labels, keyboard navigation, visible focus, reduced-motion behavior, useful alt text, and status announcements where needed.
- Keep responsive behavior explicit with stable layout constraints. Avoid text overlap, layout shift, viewport-scaled typography, and controls whose size changes when labels or icons appear.
- Validate user input at the UI boundary and keep client-side validation consistent with server constraints. Never rely on frontend checks as the only enforcement for authorization or sensitive rules.
- Add or update focused tests when the repository has a frontend test setup. Prefer component, interaction, or route tests that cover behavior over shallow render-only tests.
- Run the narrowest relevant formatter, linter, typecheck, build, and tests available. If a command cannot be run, state why and include the command the user should run.

## Output Format

When editing a repository, finish with changed files, run commands, and verification status.

When only drafting code, use this structure:

```text
Assumptions:
- ...

Files:
- path/to/file

Run:
- command

Notes:
- ...
```
