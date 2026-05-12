# Non-Functional Requirements: [System / Feature Name]

**Version:** [1.0]
**Date:** [YYYY-MM-DD]

## 1. Performance & Responsiveness

| Requirement ID | Description          | Target      | Measure                                   |
| -------------- | -------------------- | ----------- | ----------------------------------------- |
| NFR-PERF-01    | API Response Time    | p95 < 200ms | Measured at API gateway under normal load |
| NFR-PERF-02    | Page Load Time (TTI) | < 2.0s      | Measured on 3G / Mobile                   |

## 2. Scalability & Throughput

| Requirement ID | Description        | Target      | Measure                          |
| -------------- | ------------------ | ----------- | -------------------------------- |
| NFR-SCAL-01    | Concurrent Users   | 5,000       | Active websocket connections     |
| NFR-SCAL-02    | Request Throughput | 500 RPS     | Peak requests per second         |
| NFR-SCAL-03    | Data Growth        | 50 GB/month | Database storage growth          |
| NFR-SCAL-04    | Elasticity         | < 5 min     | Time to auto-scale new instances |

## 3. Availability & Reliability

| Requirement ID | Description         | Target    | Measure                         |
| -------------- | ------------------- | --------- | ------------------------------- |
| NFR-AVAIL-01   | Uptime (SLO)        | 99.9%     | 43.8 min downtime allowed/month |
| NFR-AVAIL-02   | RPO (Data Loss)     | < 1 hour  | Maximum acceptable data loss    |
| NFR-AVAIL-03   | RTO (Recovery Time) | < 4 hours | Time to restore from backup     |
| NFR-AVAIL-04   | Fault Tolerance     | Yes       | Operational if one AZ fails     |

## 4. Security & Privacy

| Requirement ID | Description           | Target                                  |
| -------------- | --------------------- | --------------------------------------- |
| NFR-SEC-01     | Encryption at Rest    | AES-256 for database and object storage |
| NFR-SEC-02     | Encryption in Transit | TLS 1.3 for all external traffic        |
| NFR-SEC-03     | Authentication        | MFA required for all admin access       |
| NFR-SEC-04     | PII Handling          | Email and phone masked in logs          |

## 5. Usability & Accessibility

| Requirement ID | Description    | Target                                        |
| -------------- | -------------- | --------------------------------------------- |
| NFR-UX-01      | Accessibility  | WCAG 2.1 Level AA                             |
| NFR-UX-02      | Device Support | iOS 15+, Android 12+, latest 2 major browsers |
| NFR-UX-03      | Localization   | English, Spanish, French                      |

## 6. Maintainability & Operability

| Requirement ID | Description   | Target                                   |
| -------------- | ------------- | ---------------------------------------- |
| NFR-OPS-01     | Observability | Metrics to Prometheus, logs to ELK       |
| NFR-OPS-02     | Deployability | Zero-downtime deployments via CI/CD      |
| NFR-OPS-03     | Test Coverage | > 80% line coverage for new backend code |
