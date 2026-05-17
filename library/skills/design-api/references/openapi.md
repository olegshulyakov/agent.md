# OpenAPI Contract

Produce valid OpenAPI 3.1 YAML. Start directly with `openapi: "3.1.0"` unless the user asked for explanation.

## Required Shape

Include `info`, `servers`, top-level `security` when authenticated, `paths`, and `components`. Every operation needs `summary`, `operationId`, `tags`, parameters or request body where relevant, at least one success response, and appropriate error responses.

Use `components.schemas` for all request and response bodies. Use `components.responses` for shared errors. Use `components.securitySchemes` for auth.

## REST Defaults

Use resource-oriented paths such as `/posts`, `/posts/{postId}`, and nested paths only when the child resource has no useful standalone identity. Use plural nouns, path versioning (`/v1`) in server URLs, and PATCH for partial updates.

Default list endpoints to cursor pagination:

```yaml
parameters:
  - name: cursor
    in: query
    schema: { type: string }
  - name: limit
    in: query
    schema: { type: integer, default: 25, maximum: 100 }
```

Represent list responses as `{ data, pageInfo }`, where `pageInfo` includes `nextCursor` and `hasMore`.

For mutating operations, include an optional `Idempotency-Key` header unless the operation is naturally idempotent.

## Error Model

All 4xx/5xx responses use one envelope:

```yaml
ErrorResponse:
  type: object
  required: [code, message]
  properties:
    code: { type: string }
    message: { type: string }
    details:
      type: array
      items:
        type: object
        required: [field, message]
        properties:
          field: { type: string }
          message: { type: string }
```

Use `400` for validation, `401` for unauthenticated, `403` for unauthorized, `404` for missing resources, `409` for conflicts, `422` for semantic validation when useful, and `429` when rate limits are part of the contract.

## Quality Bar

Schemas must include required fields, formats, enums, read-only server fields, and separate create/update request schemas. Do not emit placeholder keys or empty `properties`.
