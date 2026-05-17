---
name: design-api
description: >
  Contract-first API design. Use when asked to design an API contract, OpenAPI/Swagger spec,
  AsyncAPI event contract, GraphQL schema, endpoints, schemas, request/response shapes, or
  "what should the API look like?" Produces an interface spec before implementation.
author: Oleg Shulyakov
license: MIT
version: 1.1.0
---

# design-api

Produce a contract-first API specification before implementation code exists. Route to the right reference, load only that file, and output the finished contract in the requested format.

## Route

| User signal | Load | Output |
| --- | --- | --- |
| REST, HTTP, CRUD, endpoints, resources, OpenAPI, Swagger | `references/openapi.md` | OpenAPI 3.1 YAML |
| Events, messages, pub/sub, Kafka, RabbitMQ, AMQP, WebSocket event streams | `references/asyncapi.md` | AsyncAPI 2.6 YAML |
| GraphQL, schema, queries, mutations, subscriptions, resolvers | `references/graphql.md` | GraphQL SDL plus operation notes |
| Ambiguous API design request | `references/openapi.md` | OpenAPI 3.1 YAML, with the assumption stated once |

If the prompt mixes styles, produce separate contract sections only when both are clearly required. Otherwise choose the primary style from the user's nouns and verbs.

## Shared Rules

Extract resources, operations, consumers, auth, data ownership, pagination, versioning, idempotency, and error behavior from the prompt. If details are missing, make conservative assumptions and mark them with `[assumed]`; ask one question only when a missing decision would change the contract shape.

Always produce concrete names and fields from the domain. Do not leave bracket placeholders, empty schemas, TODOs, or "domain-specific fields go here" comments in the final contract.

Use stable public identifiers: UUIDs for externally visible resource IDs, ISO 8601 timestamps, explicit enum values, and consistent error/event envelopes. Include examples only when they clarify the contract without bloating it.

## Boundary

This skill designs an API contract. It does not generate server code, client SDKs, implementation patterns, or reference documentation for an already-built API unless the user explicitly asks for those after the contract.
