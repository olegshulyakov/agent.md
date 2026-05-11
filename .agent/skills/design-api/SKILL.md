---
name: design-api
description: >
  Produces a contract-first API specification in OpenAPI (REST) or AsyncAPI (event-driven) format,
  before any implementation code is written. Use this skill whenever the user wants to design an API,
  write an API spec, define endpoints and schemas, create an OpenAPI or Swagger spec, define a REST API
  contract, document request/response shapes, design an async messaging API, or asks "what should the API
  look like?" Trigger even if they say "API design", "API contract", "endpoint design", or "define the interface".
  Distinct from writer-api-docs (which documents an already-existing API).
---

# design-api

Produce a **contract-first API specification** in OpenAPI 3.1 (REST) or AsyncAPI 2.x (event-driven), fully defining the interface before implementation begins.

## Why contract-first matters

Writing the spec before the code forces clarity on data shapes, error modes, and versioning before any implementation lock-in. It enables frontend and backend teams to work in parallel against a shared contract, and serves as living documentation.

## Detect the API style

Determine which spec format to use from context:

| Signal                                            | Format                                                                                     |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| REST, HTTP, endpoints, CRUD                       | OpenAPI 3.1                                                                                |
| Events, messages, pub/sub, Kafka, WebSocket, AMQP | AsyncAPI 2.x                                                                               |
| User says "GraphQL"                               | Note this skill covers REST/async; offer to describe a GraphQL schema in plain SDL instead |
| Ambiguous                                         | Default to OpenAPI 3.1 and note the assumption                                             |

## Information gathering

Extract from the user's input:

- **Resource(s)** being exposed (e.g., users, orders, notifications)
- **Operations** needed (CRUD, search, bulk, streaming)
- **Auth scheme** (API key, Bearer JWT, OAuth2, none)
- **Key constraints**: pagination style, max payload size, versioning strategy
- **Consumers**: who calls this API? (helps design response shapes)

## Output: OpenAPI 3.1 (REST)

Produce a complete YAML file. Include real schemas, not placeholder comments.

```yaml
openapi: "3.1.0"
info:
  title: "[Service Name] API"
  version: "1.0.0"
  description: |
    [One paragraph: what this API does and who consumes it.]

servers:
  - url: "https://api.example.com/v1"
    description: Production
  - url: "https://api.staging.example.com/v1"
    description: Staging

security:
  - bearerAuth: []

paths:
  /[resource]:
    get:
      summary: List [resources]
      operationId: list[Resources]
      tags: ["[Resource]"]
      parameters:
        - name: page
          in: query
          schema: { type: integer, default: 1 }
        - name: limit
          in: query
          schema: { type: integer, default: 20, maximum: 100 }
      responses:
        "200":
          description: Paginated list of [resources]
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/[Resource]ListResponse"
        "401":
          $ref: "#/components/responses/Unauthorized"

    post:
      summary: Create [resource]
      operationId: create[Resource]
      tags: ["[Resource]"]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Create[Resource]Request"
      responses:
        "201":
          description: Created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/[Resource]"
        "400":
          $ref: "#/components/responses/ValidationError"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "409":
          $ref: "#/components/responses/Conflict"

  /[resource]/{id}:
    parameters:
      - name: id
        in: path
        required: true
        schema: { type: string, format: uuid }
    get:
      summary: Get [resource] by ID
      operationId: get[Resource]ById
      tags: ["[Resource]"]
      responses:
        "200":
          description: "[Resource] found"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/[Resource]"
        "404":
          $ref: "#/components/responses/NotFound"
    patch:
      summary: Update [resource]
      operationId: update[Resource]
      tags: ["[Resource]"]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Update[Resource]Request"
      responses:
        "200":
          description: Updated [resource]
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/[Resource]"
        "400":
          $ref: "#/components/responses/ValidationError"
        "404":
          $ref: "#/components/responses/NotFound"
    delete:
      summary: Delete [resource]
      operationId: delete[Resource]
      tags: ["[Resource]"]
      responses:
        "204":
          description: Deleted
        "404":
          $ref: "#/components/responses/NotFound"

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    [Resource]:
      type: object
      required: [id, createdAt, updatedAt]
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        createdAt:
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          type: string
          format: date-time
          readOnly: true
        # [domain-specific fields below]

    Create[Resource]Request:
      type: object
      required: []
      properties: {}

    Update[Resource]Request:
      type: object
      properties: {}

    [Resource]ListResponse:
      type: object
      required: [data, pagination]
      properties:
        data:
          type: array
          items:
            $ref: "#/components/schemas/[Resource]"
        pagination:
          $ref: "#/components/schemas/Pagination"

    Pagination:
      type: object
      required: [page, limit, total, totalPages]
      properties:
        page: { type: integer }
        limit: { type: integer }
        total: { type: integer }
        totalPages: { type: integer }

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
            properties:
              field: { type: string }
              message: { type: string }

  responses:
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
          example:
            code: UNAUTHORIZED
            message: "Bearer token is missing or invalid"
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
          example:
            code: NOT_FOUND
            message: "Resource not found"
    ValidationError:
      description: Request validation failed
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
    Conflict:
      description: Conflict with existing resource
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
```

## Output: AsyncAPI 2.x (event-driven)

For event-driven APIs, produce AsyncAPI YAML instead:

```yaml
asyncapi: "2.6.0"
info:
  title: "[Service] Event API"
  version: "1.0.0"
  description: |
    [What events this service publishes or consumes and why.]

servers:
  production:
    url: "kafka.example.com:9092"
    protocol: kafka

channels:
  [resource].[event]:
    description: "[Published when X happens]"
    publish:
      operationId: publish[Resource][Event]
      message:
        $ref: "#/components/messages/[Resource][Event]"

components:
  messages:
    [Resource][Event]:
      name: "[Resource][Event]"
      payload:
        type: object
        required: [eventId, occurredAt, data]
        properties:
          eventId: { type: string, format: uuid }
          occurredAt: { type: string, format: date-time }
          data:
            $ref: "#/components/schemas/[Resource]"
  schemas:
    [Resource]:
      type: object
      properties: {}
```

## Design principles to encode

- **IDs as UUIDs** (not auto-increment integers) — avoids enumeration attacks and enables distributed generation
- **Consistent error envelope** — every 4xx/5xx uses the same `ErrorResponse` shape
- **Soft deletes**: if mentioned, include an `archivedAt` field, not a boolean
- **Pagination**: default to cursor or offset+limit; note which and why
- **Idempotency**: for mutations, consider an `Idempotency-Key` header
- **Versioning**: URL path versioning (`/v1/`) is the safe default; note if the user wants header versioning instead

## After the spec

Once the spec is written, note:

> "This spec is ready to be validated with tools like `swagger-cli`, `spectral`, or the Swagger Editor. Want me to help generate server stubs or client SDKs from this?"
