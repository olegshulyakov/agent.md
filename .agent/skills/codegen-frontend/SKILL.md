---
name: codegen-frontend
description: >
  Generates production-ready frontend code including components, pages, state management, routing, and data
  fetching for all major frameworks: React, Vue, Angular, Svelte, Next.js, Nuxt, Remix, Astro, SolidJS.
  Use this skill whenever the user wants to write frontend code, create a UI component, build a page,
  implement state management, add routing, write data fetching logic, create a form, build a layout,
  implement a design system component, or asks "build this UI", "write a component for X",
  "implement this screen", "add this feature to the frontend", or "scaffold a page". Detects the framework
  from context automatically. Distinct from design-css (design tokens/style guide) and audit-a11y (accessibility audit).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# codegen-frontend

Generate **production-ready frontend code** — components, pages, state, routing, and data fetching — for the detected framework.

## Framework detection

Identify the framework from context. Check in this order:

1. **File extensions**: `.tsx` + React imports → React/Next.js; `.vue` → Vue/Nuxt; `.svelte` → Svelte/SvelteKit
2. **Import statements**: `import React from 'react'`, `import { ref } from 'vue'`, `from '@angular/core'`
3. **Project files**: `package.json` dependencies, `next.config.js`, `nuxt.config.ts`, `svelte.config.js`, `astro.config.mjs`
4. **File structure**: `pages/` directory → Next.js pages router; `app/` directory → Next.js app router or Remix; `src/routes/` → SvelteKit
5. **Explicit user mention**
6. **If ambiguous**: default to **React with TypeScript** and note the assumption; or ask once

Once identified, read the dialect-specific reference:

- **React** → `references/react.md`
- **Vue 3** → `references/vue.md`
- **Angular** → `references/angular.md`
- **Svelte / SvelteKit** → `references/svelte.md`
- **Next.js** → `references/nextjs.md`
- **Nuxt** → `references/nuxt.md`
- **Remix** → `references/remix.md`
- **Astro** → `references/astro.md`
- **SolidJS** → `references/solidjs.md`

## Universal output principles

Regardless of framework, all frontend code must:

### 1. Use TypeScript

Always generate TypeScript unless the user's project is clearly JavaScript. Type safety prevents an entire class of bugs.

```typescript
// Always type props
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: "primary" | "secondary" | "destructive";
  disabled?: boolean;
}
```

### 2. Separate concerns cleanly

- **UI components**: pure rendering, no business logic, no direct API calls
- **Container / page components**: compose UI components, manage data fetching, handle state
- **Hooks / composables / services**: reusable logic extracted from components

### 3. Handle all UI states

Every data-driven component must handle:

- **Loading** — skeleton, spinner, or optimistic update
- **Error** — user-visible message, retry option
- **Empty** — zero-state with a helpful prompt
- **Success** — the happy path

### 4. Accessibility is not optional

- Use semantic HTML (`<button>`, `<nav>`, `<main>`, `<section>`, not just `<div>`)
- Every interactive element needs a label (`aria-label`, `aria-labelledby`, or visible text)
- Focus management for modals and dynamic content
- Color is never the only signal (icon + text, not just red vs green)

### 5. Performance defaults

- Lazy-load heavy components (`React.lazy`, `defineAsyncComponent`, dynamic imports)
- Images: use the framework's optimized `<Image>` component when available
- Memoize expensive computations; don't premature-optimize renders

### 6. Forms: controlled + validated

Always use a form library for non-trivial forms (React Hook Form, VeeValidate, Angular Reactive Forms). Never build form state from scratch.

## Code structure

Show file path at the top of each file. Structure output as:

```
src/
├── components/
│   └── [Feature]/
│       ├── [Feature].tsx          # Presentational component
│       └── [Feature].test.tsx     # Unit tests
├── pages/ (or app/)
│   └── [route]/
│       └── page.tsx               # Page / route component
├── hooks/ (or composables/)
│   └── use[Feature].ts            # Data-fetching / state hook
└── types/
    └── [feature].types.ts         # Shared type definitions
```

## Component template (React/TypeScript)

```typescript
// src/components/[Feature]/[Feature].tsx
import { useState } from 'react';

interface [Feature]Props {
    // explicit prop types — no `any`
}

export function [Feature]({ ...props }: [Feature]Props) {
    const [state, setState] = useState<[Type]>([initial]);

    if (isLoading) return <[Feature]Skeleton />;
    if (error) return <ErrorMessage message={error.message} onRetry={retry} />;
    if (!data || data.length === 0) return <EmptyState />;

    return (
        <section aria-label="[Descriptive label]">
            {/* content */}
        </section>
    );
}
```

## Data fetching patterns

Use the framework's idiomatic data fetching approach (see reference files). Generally:

- **Next.js App Router**: Server Components for data fetching; `use client` only for interactivity
- **React**: React Query / SWR for client-side fetching; avoid raw `useEffect` for data
- **Vue**: Pinia store or composables with `useFetch` / `useAsyncData`
- **Remix**: `loader` functions for server-side data

## State management guidance

Choose the right tool for the scope:

- **Component-local state**: `useState`, `ref`, `signal` — default choice
- **Shared cross-component state**: Context API (small apps) or Zustand/Pinia/Jotai (larger apps)
- **Server state**: React Query, SWR, or the framework's data layer — not Redux for API data
- **Global UI state** (theme, auth, modals): Context or a lightweight store

## Testing

For each component, produce:

```typescript
// Component unit test
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('[Feature]', () => {
    it('renders the [primary element]', () => {
        render(<[Feature] [props] />);
        expect(screen.getByRole('[role]', { name: '[name]' })).toBeInTheDocument();
    });

    it('calls [handler] when [action]', async () => {
        const handler = vi.fn();
        render(<[Feature] on[Action]={handler} [props] />);
        await userEvent.click(screen.getByRole('button', { name: '[label]' }));
        expect(handler).toHaveBeenCalledWith([expected args]);
    });
});
```

## What to include in output

- Full file content (not snippets unless requested)
- All import statements
- TypeScript types for all props, state, and API responses
- Loading/error/empty states
- Accessibility attributes
- Inline comments on non-obvious decisions
