---
name: patterns-graphql
description: >
  Produces GraphQL schema definitions, resolver implementations, N+1 prevention patterns, pagination
  design, and mutation patterns. Use this skill whenever the user wants to design a GraphQL API, write
  GraphQL schema definitions, implement resolvers, solve the N+1 problem, add GraphQL pagination, write
  GraphQL mutations or subscriptions, or asks to "design a GraphQL schema", "write GraphQL resolvers",
  "fix the N+1 problem in GraphQL", "add cursor pagination to GraphQL", "implement DataLoader", or
  "how should I structure this GraphQL API?". Also trigger for "schema-first vs code-first GraphQL",
  "GraphQL subscriptions", "GraphQL federation", and "Apollo Server setup". Distinct from design-api
  (OpenAPI/REST specs) and codegen-backend (general backend code).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# patterns-graphql

Produce **GraphQL schema definitions, resolver patterns, and N+1 solutions** for robust GraphQL APIs.

## Schema Design

### Type system best practices

```graphql
type Query {
  user(id: ID!): User
  users(filter: UserFilter, pagination: PaginationInput): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
}

type User {
  id: ID!
  name: String!
  email: String!
  posts(pagination: PaginationInput): PostConnection!
}

type Post {
  id: ID!
  title: String!
  author: User!       # Resolved via DataLoader — never fetch in loop
  comments: [Comment!]!
}
```

### Cursor-based pagination (Relay style)

```graphql
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}
type UserEdge { node: User!; cursor: String! }
type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
input PaginationInput { first: Int; after: String; last: Int; before: String }
```

### Mutation payload pattern (errors in payload, not HTTP)

```graphql
input CreateUserInput { name: String!; email: String!; password: String! }

type CreateUserPayload {
  user: User          # null on error
  errors: [UserError!]!
}
type UserError {
  field: String       # null = global error
  message: String!
  code: UserErrorCode!
}
enum UserErrorCode { EMAIL_ALREADY_EXISTS; INVALID_EMAIL; NOT_FOUND; UNAUTHORIZED }
```

## Resolver Implementation

```typescript
// resolvers/user.resolver.ts
export const userResolvers = {
  Query: {
    user: async (_parent, { id }, { user: currentUser, dataSources }) => {
      if (!currentUser) throw new GraphQLError('Unauthenticated', {
        extensions: { code: 'UNAUTHENTICATED' }
      });
      return dataSources.userAPI.findById(id);
    },
  },

  Mutation: {
    createUser: async (_parent, { input }, { dataSources }) => {
      try {
        const user = await dataSources.userAPI.create(input);
        return { user, errors: [] };
      } catch (err) {
        if (err.code === 'EMAIL_EXISTS') {
          return { user: null, errors: [{ field: 'email', message: 'Email in use', code: 'EMAIL_ALREADY_EXISTS' }] };
        }
        throw err;
      }
    },
  },

  // Field resolvers — use DataLoader to batch
  Post: {
    author: (parent, _args, { loaders }) => loaders.userById.load(parent.authorId),
    comments: (parent, _args, { loaders }) => loaders.commentsByPostId.load(parent.id),
  },
};
```

## N+1 Prevention with DataLoader

The N+1 problem: fetching 100 posts and then making 100 separate DB calls for each author. DataLoader batches these into one query.

```typescript
// loaders/index.ts
import DataLoader from 'dataloader';

export function createLoaders() {
  return {
    // Batch: load many users in one DB query
    userById: new DataLoader<string, User | null>(async (ids) => {
      const users = await db.query(`SELECT * FROM users WHERE id = ANY($1)`, [ids]);
      const map = new Map(users.map(u => [u.id, u]));
      return ids.map(id => map.get(id) ?? null); // Must return in same order as ids
    }),

    commentsByPostId: new DataLoader<string, Comment[]>(async (postIds) => {
      const comments = await db.query(
        `SELECT * FROM comments WHERE post_id = ANY($1) ORDER BY created_at`,
        [postIds]
      );
      const grouped = new Map<string, Comment[]>();
      for (const c of comments) {
        if (!grouped.has(c.postId)) grouped.set(c.postId, []);
        grouped.get(c.postId)!.push(c);
      }
      return postIds.map(id => grouped.get(id) ?? []);
    }),
  };
}

// context.ts — IMPORTANT: create new DataLoader instances per request
export function createContext({ req }) {
  return {
    user: authenticate(req),
    loaders: createLoaders(), // Fresh instances per request (fresh cache)
  };
}
```

## Pagination Implementation

```typescript
// Cursor encoding/decoding
const encodeCursor = (node: { id: string; createdAt: Date }) =>
  Buffer.from(JSON.stringify(node)).toString('base64');

const decodeCursor = (cursor: string) =>
  JSON.parse(Buffer.from(cursor, 'base64').toString('utf-8'));

async function paginateQuery(baseQuery, { first = 20, after }: PaginationInput) {
  const limit = Math.min(first, 100);
  const cursor = after ? decodeCursor(after) : null;

  const items = await baseQuery
    .where(cursor ? { createdAt: { lt: cursor.createdAt } } : {})
    .orderBy({ createdAt: 'desc' })
    .limit(limit + 1); // +1 to detect hasNextPage

  const hasNextPage = items.length > limit;
  const edges = items.slice(0, limit).map(node => ({ node, cursor: encodeCursor(node) }));

  return {
    edges,
    pageInfo: { hasNextPage, hasPreviousPage: !!after, startCursor: edges[0]?.cursor, endCursor: edges.at(-1)?.cursor },
    totalCount: await baseQuery.count(),
  };
}
```

## Authorization

```typescript
// Field-level authorization guard
const isAdmin = (user) => user?.roles.includes('ADMIN');

const resolvers = {
  Query: {
    adminReport: (_p, _a, { user }) => {
      if (!isAdmin(user)) throw new GraphQLError('Forbidden', { extensions: { code: 'FORBIDDEN' } });
      return generateReport();
    },
  },
};
```

## Calibration

- **Schema design only**: Type definitions + rationale for naming choices
- **N+1 fix**: Identify the fields causing N+1; generate DataLoader for those fields
- **Mutation with errors**: Show the input/payload pattern
- **Subscriptions**: Use `asyncIterator` with a pub/sub backend
- **Federation**: Use `@key` directive and stub resolvers; load `references/federation.md`
