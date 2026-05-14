# GraphQL Contract

Produce GraphQL SDL for the public schema plus short operation notes. Start with `schema { ... }` or the first type definition unless the user asked for explanation.

## Required Shape

Include `Query` for reads, `Mutation` for writes, and `Subscription` only when real-time updates are requested. Define object types, input types, enums, pagination types, and error/user-error types.

Use IDs as `ID!`, timestamps as a custom `DateTime` scalar, and money/decimal values as explicit custom scalars when needed.

## GraphQL Defaults

Use Relay-style connections for lists unless the user asks for offset pagination:

```graphql
type PageInfo {
  hasNextPage: Boolean!
  endCursor: String
}
```

Mutation payloads should return the changed entity plus `userErrors`, not just a boolean.

```graphql
type UserError {
  field: [String!]
  message: String!
  code: String!
}
```

## Operation Notes

After SDL, include concise notes for auth boundaries, resolver ownership, N+1 risks, pagination behavior, and versioning/deprecation strategy. Keep notes specific to the schema.

## Quality Bar

Do not describe GraphQL through OpenAPI. Do not leave resolver TODOs. The SDL must use concrete domain names, non-null markers where appropriate, and enum values for finite states.
