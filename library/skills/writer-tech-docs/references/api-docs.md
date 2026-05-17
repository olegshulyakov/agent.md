# writer-tech-docs — api-docs variant

Produce **API reference documentation** for existing endpoints, ready for a developer portal or README.

## What makes great API docs

Great API docs answer: What does this endpoint do? What do I send? What do I get back? What can go wrong? Show me an example. Developers read docs to unblock themselves — every missing field or ambiguous description is a support ticket.

## Information gathering

- **Source**: Route handler code, OpenAPI spec, endpoint descriptions, or combination
- **API style**: REST, GraphQL, gRPC, WebSocket
- **Auth**: Bearer token, API key, session cookie, OAuth2?
- **Audience**: Internal developers, external partners, public developers?
- **Format**: Markdown docs, OpenAPI annotation enrichment, README section?

## Output format

Per endpoint:

````markdown
# API Reference: [API Name or Service]

**Base URL:** `https://api.example.com/v1`
**Authentication:** Bearer token via `Authorization: Bearer <token>` header
**Content-Type:** `application/json`

---

## [Resource Name]

### [METHOD] [Path]

[One sentence describing what this endpoint does.]

**Authentication:** Required / Optional / None
**Rate limit:** [N requests per minute] _(if applicable)_

#### Path Parameters

| Parameter | Type            | Required | Description                   |
| --------- | --------------- | -------- | ----------------------------- |
| `id`      | `string (UUID)` | ✅ Yes   | The unique ID of the resource |

#### Query Parameters

| Parameter | Type      | Required | Default      | Description                               |
| --------- | --------- | -------- | ------------ | ----------------------------------------- |
| `page`    | `integer` | ❌ No    | `1`          | Page number (1-indexed)                   |
| `limit`   | `integer` | ❌ No    | `20`         | Results per page. Max: 100                |
| `sort`    | `string`  | ❌ No    | `created_at` | Sort field. Options: `created_at`, `name` |

#### Request Body

```json
{
  "email": "user@example.com",
  "name": "Jane Smith",
  "role": "editor"
}
```

| Field   | Type     | Required | Description                                                        |
| ------- | -------- | -------- | ------------------------------------------------------------------ |
| `email` | `string` | ✅ Yes   | User's email address. Must be valid email format.                  |
| `name`  | `string` | ✅ Yes   | Display name. 1–100 characters.                                    |
| `role`  | `string` | ❌ No    | User role. One of: `admin`, `editor`, `viewer`. Default: `viewer`. |

#### Response

**200 OK**

```json
{
  "id": "usr_01h2x3y4z",
  "email": "user@example.com",
  "name": "Jane Smith",
  "role": "editor",
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

| Field       | Type                | Description                          |
| ----------- | ------------------- | ------------------------------------ |
| `id`        | `string`            | Unique identifier with `usr_` prefix |
| `email`     | `string`            | User's email address                 |
| `name`      | `string`            | Display name                         |
| `role`      | `string`            | Current role                         |
| `createdAt` | `string (ISO 8601)` | Timestamp of creation                |
| `updatedAt` | `string (ISO 8601)` | Timestamp of last update             |

#### Error Responses

| Status             | Error code         | Description                                |
| ------------------ | ------------------ | ------------------------------------------ |
| `400 Bad Request`  | `VALIDATION_ERROR` | Request body failed validation             |
| `401 Unauthorized` | `UNAUTHORIZED`     | Missing or invalid auth token              |
| `403 Forbidden`    | `FORBIDDEN`        | Authenticated but insufficient permissions |
| `409 Conflict`     | `EMAIL_TAKEN`      | An account with this email already exists  |

**Error response body:**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "errors": [{ "field": "email", "message": "Email is required" }]
  }
}
```

#### Example

**Request:**

```bash
curl -X POST https://api.example.com/v1/users \
  -H "Authorization: Bearer eyJhbG..." \
  -H "Content-Type: application/json" \
  -d '{"email": "jane@example.com", "name": "Jane Smith"}'
```

**Response:**

```json
{
  "id": "usr_01h2x3y4z",
  "email": "jane@example.com",
  "name": "Jane Smith",
  "role": "viewer",
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z"
}
```
````

### Authentication section (global)

````markdown
## Authentication

All requests require a Bearer token:

```http
Authorization: Bearer <your-token>
```

Obtain tokens via `POST /auth/login`. Tokens expire after 15 minutes.
Use `POST /auth/refresh` with your refresh token to get a new access token.
````

### Common errors section (global)

```markdown
## Common Errors

| Status | When it happens                                                              |
| ------ | ---------------------------------------------------------------------------- |
| `401`  | Token missing, expired, or invalid                                           |
| `403`  | Authenticated but not permitted to perform this action                       |
| `404`  | Resource not found (or not accessible to this user)                          |
| `429`  | Rate limit exceeded — see `Retry-After` response header                      |
| `500`  | Internal server error — contact support with the `X-Request-Id` header value |
```

## Quality checklist

- [ ] Every field has a type AND description
- [ ] Required vs optional is explicit for every field
- [ ] Constraints are documented (max length, valid values, format)
- [ ] Every response field is documented (not just the request)
- [ ] At least one curl example per endpoint
- [ ] All error codes for that endpoint are listed
- [ ] Sensitive fields (passwords, tokens) are noted as write-only (not returned)

## Calibration

- **Code provided**: Document from the actual implementation; flag any undocumented behaviors
- **Spec/description provided**: Generate docs from the description; mark assumptions with `[assumed]`
- **OpenAPI YAML provided**: Enrich with prose explanations, examples, and developer guidance
- **Multiple endpoints**: Group by resource (Users, Products, Orders) with one H2 per group
