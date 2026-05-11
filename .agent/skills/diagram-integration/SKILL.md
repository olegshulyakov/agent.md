---
name: diagram-integration
description: >
  Produces an integration map showing system boundaries, APIs, data flows, ownership, and integration
  patterns between services. Use this skill whenever the user wants to document system integrations,
  map how services connect, show API dependencies, visualize the integration landscape, understand
  data exchange between systems, or asks to "draw an integration diagram", "map our system integrations",
  "show how our services connect", "document the API dependencies", "create an integration map",
  "show what talks to what", or "document our third-party integrations". Also trigger for "service mesh
  diagram", "API dependency map", "integration landscape", and "show the boundaries between systems".
  Distinct from diagram-c4 (which models software architecture levels) and diagram-dfd (which models
  data flows through processes).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# diagram-integration

Produce an **integration map** showing how systems connect — their boundaries, APIs, data exchanges, protocols, and ownership.

## What makes a great integration diagram

The most useful integration diagrams answer: who calls whom, with what protocol, carrying what data, and who owns each system. They're used during incident response, onboarding, and architecture reviews. Focus on the connections that matter — not every internal function call, but service-to-service and system-to-external boundaries.

## Information gathering

From context, identify:
- **Systems/services**: What services, databases, third-party APIs, and external systems are involved?
- **Integration points**: What calls what? Which direction? Sync or async?
- **Protocols**: REST, gRPC, GraphQL, message queue, webhook, file transfer, etc.
- **Data exchanged**: What data crosses each boundary?
- **Ownership**: Which team owns each system?
- **Scope**: Specific feature, all integrations for a service, or entire landscape?

## Integration patterns to identify

| Pattern | Visual cue | Description |
|---------|-----------|-------------|
| **Sync API call** | Solid arrow → | REST/gRPC; caller waits for response |
| **Async message** | Dashed arrow → | Queue/event bus; fire and forget |
| **Webhook** | Solid arrow, reversed | External system pushes to your endpoint |
| **Polling** | Arrow with loop | Caller periodically checks for updates |
| **File/Batch** | Arrow with document icon | Scheduled file transfers |
| **Shared DB** | Both pointing to DB | Anti-pattern — note if present |

## Output format — Mermaid

```mermaid
graph LR
    %% ── External systems ─────────────────────────────────
    ext_stripe([Stripe API]):::external
    ext_sendgrid([SendGrid]):::external
    ext_auth0([Auth0]):::external
    ext_s3([AWS S3]):::external

    %% ── Internal services ────────────────────────────────
    api_gw["API Gateway\n[Team: Platform]"]:::internal
    svc_orders["Order Service\n[Team: Commerce]"]:::internal
    svc_inventory["Inventory Service\n[Team: Commerce]"]:::internal
    svc_notifications["Notification Service\n[Team: Platform]"]:::internal
    svc_reports["Reports Service\n[Team: Analytics]"]:::internal

    %% ── Data stores ──────────────────────────────────────
    db_orders[("Orders DB\n[PostgreSQL]")]:::datastore
    db_inventory[("Inventory DB\n[PostgreSQL]")]:::datastore
    mq_events[["Event Bus\n[Kafka]"]]:::queue

    %% ── Client ───────────────────────────────────────────
    client([Web / Mobile Client]):::actor

    %% ── Integrations ─────────────────────────────────────
    client -->|"HTTPS / JWT"| api_gw
    api_gw -->|"REST / JWT"| svc_orders
    api_gw -->|"REST / JWT"| svc_inventory
    api_gw -->|"OAuth2 token validation"| ext_auth0

    svc_orders -->|"Charge / Refund\n[Stripe REST API]"| ext_stripe
    svc_orders --- db_orders
    svc_orders -->|"order.created event\n[JSON, async]"| mq_events

    svc_inventory --- db_inventory
    svc_inventory -->|"stock.updated event\n[JSON, async]"| mq_events

    mq_events -->|"order.created\n[consumed]"| svc_notifications
    svc_notifications -->|"Send Email\n[SendGrid REST API]"| ext_sendgrid

    mq_events -->|"all events\n[consumed]"| svc_reports
    svc_reports -->|"Upload Reports\n[S3 PutObject]"| ext_s3

    %% ── Styles ───────────────────────────────────────────
    classDef external fill:#fef3c7,stroke:#d97706,color:#000
    classDef internal fill:#dbeafe,stroke:#2563eb,color:#000
    classDef datastore fill:#f0fdf4,stroke:#16a34a,color:#000
    classDef queue    fill:#f3e8ff,stroke:#7c3aed,color:#000
    classDef actor    fill:#f9fafb,stroke:#6b7280,color:#000
```

## Integration Inventory Table

Always accompany the diagram with a table:

```markdown
## Integration Inventory

| From | To | Protocol | Data | Direction | SLA / Notes |
|------|----|----------|------|-----------|-------------|
| API Gateway | Order Service | REST over HTTPS | Order CRUD, JWT auth | Sync | < 200ms p95 |
| API Gateway | Auth0 | OAuth2 token validation | JWT | Sync | Called on every request |
| Order Service | Stripe | REST (Stripe SDK) | Payment intent, amount, currency | Sync | Idempotency key required |
| Order Service | Kafka | Produce | `order.created` event (JSON) | Async | At-least-once delivery |
| Notification Service | Kafka | Consume | `order.created` | Async | DLQ after 3 retries |
| Notification Service | SendGrid | REST | Email body, recipient, template ID | Async | Rate limit: 100/sec |
| Reports Service | AWS S3 | AWS SDK | Parquet files | Async (nightly) | Bucket: reports-prod |

## Third-Party Dependencies

| System | Owner | Auth Method | Rate Limits | Fallback |
|--------|-------|-------------|-------------|----------|
| Stripe | Finance team | API key (secret) | 100 req/s | Retry with backoff; fail open for non-payment flows |
| Auth0 | Platform team | OAuth2 client credentials | 1000 req/min | Cache tokens; fail closed |
| SendGrid | Platform team | API key | 100 emails/s | Queue in Redis; retry |
| AWS S3 | DevOps | IAM role | No hard limit | Local file fallback |
```

## Ownership & Contact Map

```markdown
## System Ownership

| System | Team | Slack Channel | On-call |
|--------|------|--------------|---------|
| Order Service | Commerce | #team-commerce | PagerDuty: commerce-oncall |
| Inventory Service | Commerce | #team-commerce | PagerDuty: commerce-oncall |
| Notification Service | Platform | #team-platform | PagerDuty: platform-oncall |
| API Gateway | Platform | #team-platform | PagerDuty: platform-oncall |
```

## Integration Risk Assessment

```markdown
## Risk Notes

| Integration | Risk | Mitigation |
|-------------|------|------------|
| Order Service → Stripe | External dependency; Stripe outage = no payments | Circuit breaker + retry; monitor Stripe status page |
| Shared Orders DB | Schema changes break multiple consumers | Strict migration policy; backward-compatible changes only |
| Kafka event bus | Consumer lag = delayed notifications | Alert on consumer lag > 1000 messages |
```

## Calibration

- **Single service integration map**: Show only the integrations of one service to everything it touches
- **Third-party dependencies only**: Focus table on external systems, auth, rate limits, fallbacks
- **Event-driven architecture**: Emphasize producer/consumer relationships, event schemas, topics
- **Legacy integration landscape**: Show anti-patterns (shared DB, synchronous chains) with risk notes
- **New feature impact**: Show which existing integrations a new feature will touch or need
