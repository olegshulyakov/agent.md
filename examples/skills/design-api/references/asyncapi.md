# AsyncAPI Contract

Produce valid AsyncAPI 2.6 YAML. Start directly with `asyncapi: "2.6.0"` unless the user asked for explanation.

## Required Shape

Include `info`, `servers`, `channels`, and `components`. Define reusable messages in `components.messages` and payload schemas in `components.schemas`.

For each channel, specify whether the service `publish`es or `subscribe`s from the perspective of the API owner. If ownership is ambiguous, state the assumption once.

## Event Defaults

Use channel names that match platform conventions, such as `orders.created.v1` for Kafka topics or `/orders/{orderId}/events` for WebSocket streams. Include a version in the channel or message name when compatibility matters.

Every event payload uses this envelope unless the user requires a different format:

```yaml
EventEnvelope:
  type: object
  required: [eventId, eventType, occurredAt, producer, data]
  properties:
    eventId: { type: string, format: uuid }
    eventType: { type: string }
    occurredAt: { type: string, format: date-time }
    producer: { type: string }
    correlationId: { type: string, format: uuid }
    data:
      type: object
```

## Message Design

Define one message per event type. Name messages with domain verbs, such as `OrderCreated`, `PaymentFailed`, or `InventoryReserved`.

Payload schemas must include concrete domain fields, required arrays, enum values, and IDs for referenced entities. Include examples only for complex payloads.

## Reliability Notes

Add concise notes in channel or message descriptions for ordering key, idempotency key, retention, retry/dead-letter expectations, and compatibility rules when those affect consumers.

## Quality Bar

Do not output generic `ResourceEvent` messages unless the prompt is genuinely generic. Avoid empty payload schemas and placeholder channel names.
