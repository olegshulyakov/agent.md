---
name: writer-spec-data-contract
description: >
  Produces a Data Contract specification defining schema, ownership, SLA, semantics, and versioning
  for data products. Use this skill whenever the user wants to write a data contract, define the
  interface for a data pipeline, specify a data schema agreement between teams, or asks to "write a
  data contract", "document this data product", "create a data SLA", "define the schema contract",
  or "document the expectations for this dataset". Also trigger for "data mesh contract", "event
  schema specification", "data quality agreement", and "data producer/consumer agreement". Distinct
  from design-schema (which designs the database tables) and design-api (which designs REST/GraphQL APIs).
---

# writer-spec-data-contract

Produce a **Data Contract Specification** defining schema, ownership, semantics, and service level agreements (SLAs).

## Output format

```markdown
# Data Contract: [Data Product Name]

**Version:** [1.0.0]
**Status:** [Draft / Active / Deprecated]
**Domain:** [domain-name]
**Data Product URN:** `urn:dataproduct:[domain]:[name]`

## 1. Ownership & Roles

| Role | Team/Person | Contact |
|------|-------------|---------|
| **Data Producer** | [team-name] | [#slack-channel] |
| **Data Steward** | [name] | [email] |
| **Data Consumers** | [team-a, team-b] | — |

---

## 2. Business Context & Semantics

**Description:**
[2-3 sentences explaining what this data represents in the real world.]

**Grain:** [e.g., "One row per completed order item"]
**Update frequency:** [e.g., "Hourly via batch pipeline"]
**System of record:** [e.g., "PostgreSQL 'Orders' database"]

**Key terms:**
- **[Term 1]**: [Definition — e.g., "A 'completed' order means payment was successfully captured"]
- **[Term 2]**: [Definition]

---

## 3. Schema Definition

**Format:** [e.g., Parquet / Avro / JSON / Snowflake Table]
**Location:** [e.g., `s3://bucket/domain/dataset/` or `db.schema.table`]

| Column Name | Data Type | Nullable | PII / Sensitive | Description |
|-------------|-----------|----------|-----------------|-------------|
| `order_id` | STRING | No | No | Unique identifier for the order (UUID) |
| `user_id` | STRING | No | No | ID of the user who placed the order |
| `amount` | DECIMAL(10,2) | No | No | Total amount in USD |
| `status` | STRING | No | No | Enum: `PENDING`, `COMPLETED`, `REFUNDED` |
| `created_at` | TIMESTAMP | No | No | UTC timestamp when order was created |
| `user_email` | STRING | Yes | **Yes** | Email address (masked in non-prod environments) |

---

## 4. Data Quality & SLAs

**Availability SLA:**
- Data will be available and updated within [1 hour] of the business event.
- Target uptime: [99.9%]

**Quality Expectations:**
- `order_id` must be unique across the entire dataset.
- `amount` must be >= 0.
- `status` must be one of the defined Enum values.
- No more than [0.1%] of `user_id`s may be unmatched in the users table (referential integrity).

---

## 5. Security & Access Control

- **Classification:** [e.g., Confidential / Internal / Public]
- **Access mechanism:** [e.g., Request via IAM group `data-readers-orders`]
- **Masking:** [e.g., `user_email` is SHA-256 hashed in the `analytics_dev` environment]

---

## 6. Versioning & Change Management

This contract follows [Semantic Versioning](https://semver.org/).

- **Major changes (Breaking):** [e.g., Removing a column, changing a data type, adding a mandatory field]. Requires 30 days notice to consumers.
- **Minor changes (Non-breaking):** [e.g., Adding a new optional column]. Requires 7 days notice.

**Changelog:**
- `1.0.0` (Date) - Initial contract definition.
```
