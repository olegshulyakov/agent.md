# Data Contract: [Data Product Name]

**Version:** [1.0.0]
**Status:** [Draft / Active / Deprecated]
**Domain:** [domain-name]
**Data Product URN:** `urn:dataproduct:[domain]:[name]`

## 1. Ownership & Roles

| Role               | Team/Person      | Contact          |
| ------------------ | ---------------- | ---------------- |
| **Data Producer**  | [team-name]      | [#slack-channel] |
| **Data Steward**   | [name]           | [email]          |
| **Data Consumers** | [team-a, team-b] | —                |

---

## 2. Business Context & Semantics

**Description:** [2–3 sentences: what this data represents in the real world.]

**Grain:** [e.g., "One row per completed order item"]
**Update frequency:** [e.g., "Hourly via batch pipeline"]
**System of record:** [e.g., "PostgreSQL 'Orders' database"]

**Key terms:**

- **[Term]**: [Definition — e.g., "'completed' order means payment was successfully captured"]

---

## 3. Schema Definition

**Format:** [Parquet / Avro / JSON / Snowflake Table]
**Location:** [e.g., `s3://bucket/domain/dataset/` or `db.schema.table`]

| Column Name  | Data Type | Nullable | PII | Description              |
| ------------ | --------- | -------- | --- | ------------------------ |
| `id`         | STRING    | No       | No  | Unique identifier (UUID) |
| `created_at` | TIMESTAMP | No       | No  | UTC timestamp            |

---

## 4. Data Quality & SLAs

**Availability SLA:** Data available within [N hours] of the business event. Uptime: [99.9%].

**Quality Expectations:**

- [Column] must be unique across the dataset.
- [Column] must be >= 0.
- No more than [0.1%] of [FK column]s may be unmatched in [referenced table].

---

## 5. Security & Access Control

- **Classification:** [Confidential / Internal / Public]
- **Access mechanism:** [e.g., IAM group `data-readers-orders`]
- **Masking:** [e.g., `user_email` is SHA-256 hashed in non-prod environments]

---

## 6. Versioning & Change Management

Follows [Semantic Versioning](https://semver.org/).

- **Breaking changes:** Removing/renaming columns, changing types. Requires 30 days notice.
- **Non-breaking changes:** Adding optional columns. Requires 7 days notice.

**Changelog:**

- `1.0.0` ([Date]) — Initial contract definition.
