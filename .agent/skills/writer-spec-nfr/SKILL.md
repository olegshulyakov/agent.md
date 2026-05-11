---
name: writer-spec-nfr
description: >
  Produces a Non-Functional Requirements (NFR) specification covering performance, scalability,
  security, availability, and compliance constraints. Use this skill whenever the user wants to
  document non-functional requirements, write an NFR document, specify system constraints, define
  performance targets, or asks to "write the NFRs for this project", "document system constraints",
  "specify the performance requirements", or "create an NFR spec". Distinct from writer-spec-functional
  (which describes what the system does) and writer-spec-tech (which orchestrates both into a full design).
---

# writer-spec-nfr

Produce a **Non-Functional Requirements (NFR)** specification covering performance, scalability, security, availability, and compliance.

## Output format

```markdown
# Non-Functional Requirements: [System / Feature Name]

**Version:** [1.0]
**Date:** [date]

## 1. Performance & Responsiveness

| Requirement ID | Description | Target | Measure |
|----------------|-------------|--------|---------|
| NFR-PERF-01 | API Response Time | p95 < 200ms | Measured at the API gateway under normal load |
| NFR-PERF-02 | Page Load Time (TTI) | < 2.0s | Measured on 3G network / Mobile device |
| NFR-PERF-03 | Batch Processing | < 1 hour | Time to process 1M daily records |

## 2. Scalability & Throughput

| Requirement ID | Description | Target | Measure |
|----------------|-------------|--------|---------|
| NFR-SCAL-01 | Concurrent Users | 5,000 | Number of active websocket connections |
| NFR-SCAL-02 | Request Throughput | 500 RPS | Peak requests per second |
| NFR-SCAL-03 | Data Growth | 50GB/month | Expected database storage growth |
| NFR-SCAL-04 | Elasticity | < 5 mins | Time to scale up new instances automatically |

## 3. Availability & Reliability

| Requirement ID | Description | Target | Measure |
|----------------|-------------|--------|---------|
| NFR-AVAIL-01 | Uptime (SLO) | 99.9% | 43.8 minutes downtime allowed per month |
| NFR-AVAIL-02 | RPO (Data Loss) | < 1 hour | Maximum acceptable data loss in disaster |
| NFR-AVAIL-03 | RTO (Recovery Time) | < 4 hours | Maximum time to restore service from backup |
| NFR-AVAIL-04 | Fault Tolerance | Yes | System remains operational if one AZ fails |

## 4. Security & Privacy

| Requirement ID | Description | Target |
|----------------|-------------|--------|
| NFR-SEC-01 | Encryption at Rest | AES-256 for all database and object storage |
| NFR-SEC-02 | Encryption in Transit | TLS 1.3 for all external traffic |
| NFR-SEC-03 | Authentication | MFA required for all administrative access |
| NFR-SEC-04 | PII Handling | Email addresses and phone numbers must be masked in logs |

## 5. Usability & Accessibility

| Requirement ID | Description | Target |
|----------------|-------------|--------|
| NFR-UX-01 | Accessibility | WCAG 2.1 Level AA compliance |
| NFR-UX-02 | Device Support | iOS 15+, Android 12+, latest 2 versions of major browsers |
| NFR-UX-03 | Localization | UI must support English, Spanish, and French |

## 6. Maintainability & Operability

| Requirement ID | Description | Target |
|----------------|-------------|--------|
| NFR-OPS-01 | Observability | All services must export metrics to Prometheus and logs to ELK |
| NFR-OPS-02 | Deployability | Zero-downtime deployments via CI/CD pipeline |
| NFR-OPS-03 | Test Coverage | > 80% line coverage for new backend code |
```
