# Remix

Use this reference for Remix and React Router data-router applications with loaders, actions, nested routes, and progressive enhancement.

Keep data reads in loaders and mutations in actions unless the repo has a deliberate client-fetching pattern. Use `Form`, `useFetcher`, `useNavigation`, route error boundaries, and pending UI to make transitions explicit. Validate action inputs on the server and mirror helpful client validation without trusting it.

Respect nested layout boundaries and route module conventions. Keep responses typed or schema-validated when the project uses generated types. Handle redirects, thrown responses, and catch boundaries consistently.
