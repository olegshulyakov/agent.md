# React

Use this reference for React components, hooks, context, client state, React Query/TanStack Query, Redux, Zustand, Vite React apps, and shared component libraries.

Keep rendering pure. Put side effects in effects, event handlers, loaders, or query/mutation hooks. Split components by responsibility: route containers coordinate data and navigation, presentational components render props, and shared primitives belong in the existing design system.

Follow hook rules and local naming conventions. Prefer controlled inputs for forms that need validation or conditional behavior. Use stable keys from domain data, not array indexes for mutable lists. Avoid duplicating server state in local state; derive it or use the project's query/cache layer.

For client performance, memoize only when there is a measured or obvious render cost. Keep suspense, error boundaries, and loading states consistent with the surrounding app.
