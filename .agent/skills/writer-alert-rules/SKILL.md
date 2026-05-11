---
name: writer-alert-rules
description: >
  Produces alert rule definitions with conditions, severity levels, runbook links, and notification
  routing for Prometheus, Grafana, PagerDuty, or similar systems. Use this skill whenever the user
  wants to write alert rules, configure monitoring alerts, define SLO-based alerts, create on-call
  alert definitions, or asks to "write alert rules for this service", "create Prometheus alerting
  rules", "define when to page on-call", "write a Grafana alert", "set up PagerDuty alerts",
  "create alerting rules for my API", "alert when latency is high", or "define error rate alerts".
  Also trigger for "alerting thresholds", "SLO burn rate alerts", "dead man's switch", "heartbeat
  alert", and "multi-window multi-burn-rate". Distinct from writer-slo (which defines the SLO targets
  themselves) and writer-runbook-oncall (which documents the response procedures).
---

# writer-alert-rules

Produce **alert rule definitions** with conditions, severity, routing, and runbook links for your monitoring system.

## Alert quality principles

Good alerts are **actionable** (someone knows exactly what to do), **accurate** (low false positive rate), and **urgent** (pages only when human action is needed now). The most common mistake is alerting on symptoms instead of user impact — an alert on "CPU > 80%" is less useful than "error rate > 1%".

## Information gathering

From context, identify:
- **Monitoring system**: Prometheus + Alertmanager? Grafana Cloud? Datadog? PagerDuty?
- **Service**: What service or system needs alerts?
- **SLOs**: Do you have error budget and latency targets?
- **Alert channels**: PagerDuty, Slack, email? Who gets paged vs. notified?

## Output format

### Prometheus alert rules (`alerts.yaml`)

```yaml
# alerts/[service-name].yaml
# Apply with: kubectl apply -f alerts/[service-name].yaml
# Or: prometheus reload with --web.enable-lifecycle

groups:
  - name: [service-name].availability
    interval: 30s          # How often rules are evaluated
    rules:

      # ── Error rate ─────────────────────────────────────────────────────
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{job="[service]", status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total{job="[service]"}[5m])) > 0.01
        for: 5m            # Must be true for this long before firing
        labels:
          severity: critical
          team: [team-name]
          service: [service-name]
        annotations:
          summary: "High error rate on [service]"
          description: "Error rate is {{ $value | humanizePercentage }} (threshold: 1%). This is likely impacting users."
          runbook_url: "https://wiki.internal/runbooks/[service]-high-error-rate"
          dashboard_url: "https://grafana.internal/d/[dashboard-id]"

      - alert: ModerateErrorRate
        expr: |
          sum(rate(http_requests_total{job="[service]", status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total{job="[service]"}[5m])) > 0.005
        for: 10m
        labels:
          severity: warning
          team: [team-name]
        annotations:
          summary: "Moderate error rate on [service]"
          description: "Error rate is {{ $value | humanizePercentage }} — trending toward SLO breach."
          runbook_url: "https://wiki.internal/runbooks/[service]-high-error-rate"

      # ── Latency ────────────────────────────────────────────────────────
      - alert: HighLatencyP95
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket{job="[service]"}[5m]))
            by (le, route)
          ) > 0.5
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "p95 latency > 500ms on [service] {{ $labels.route }}"
          description: "p95 latency is {{ $value | humanizeDuration }} on route {{ $labels.route }}. SLO target: 500ms."
          runbook_url: "https://wiki.internal/runbooks/[service]-high-latency"

      # ── Availability ───────────────────────────────────────────────────
      - alert: ServiceDown
        expr: up{job="[service]"} == 0
        for: 1m
        labels:
          severity: critical
          page: "true"     # Custom label to route to PagerDuty
        annotations:
          summary: "Service [service] is DOWN"
          description: "Instance {{ $labels.instance }} of [service] has been unreachable for 1 minute."
          runbook_url: "https://wiki.internal/runbooks/[service]-down"

      # ── Saturation ─────────────────────────────────────────────────────
      - alert: HighMemoryUsage
        expr: |
          (container_memory_working_set_bytes{pod=~"[service]-.*"}
          / container_spec_memory_limit_bytes{pod=~"[service]-.*"}) > 0.85
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "[service] memory usage above 85%"
          description: "Pod {{ $labels.pod }} memory: {{ $value | humanizePercentage }} of limit."

      # ── Queue / Backlog ────────────────────────────────────────────────
      - alert: HighQueueDepth
        expr: rabbitmq_queue_messages{queue="[service]-work"} > 10000
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Message queue depth high: [service]-work"
          description: "Queue depth is {{ $value }} (threshold: 10,000). Workers may be backed up."
          runbook_url: "https://wiki.internal/runbooks/queue-consumer-lag"

  - name: [service-name].slo
    rules:

      # ── SLO burn rate alerts (multi-window) ────────────────────────────
      # Fast burn: consuming 5% of monthly error budget in 1 hour
      - alert: SLOBurnRateFast
        expr: |
          (
            sum(rate(http_requests_total{job="[service]", status=~"5.."}[1h]))
            / sum(rate(http_requests_total{job="[service]"}[1h]))
          ) > (14.4 * 0.01)   # 14.4x burn rate for 1h window (99% SLO → 1% budget)
        for: 2m
        labels:
          severity: critical
          page: "true"
        annotations:
          summary: "Fast SLO burn rate: [service] error budget consumed at 14.4x rate"
          description: "At this rate, the monthly error budget will be exhausted in ~5 days."

      # Slow burn: consuming 10% of monthly budget in 6 hours
      - alert: SLOBurnRateSlow
        expr: |
          (
            sum(rate(http_requests_total{job="[service]", status=~"5.."}[6h]))
            / sum(rate(http_requests_total{job="[service]"}[6h]))
          ) > (6 * 0.01)      # 6x burn rate
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Slow SLO burn rate: [service] consuming error budget faster than expected"
```

### Alertmanager routing (`alertmanager.yaml`)

```yaml
# alertmanager.yaml
global:
  resolve_timeout: 5m

route:
  receiver: default-slack
  group_by: ['alertname', 'service']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  
  routes:
    # Critical alerts → PagerDuty (wake someone up)
    - match:
        severity: critical
      receiver: pagerduty-[team]
      continue: false

    # Warning alerts → Slack only
    - match:
        severity: warning
      receiver: slack-[team]-alerts

receivers:
  - name: pagerduty-[team]
    pagerduty_configs:
      - routing_key: "${PAGERDUTY_INTEGRATION_KEY}"
        severity: "{{ .CommonLabels.severity }}"
        description: "{{ .CommonAnnotations.description }}"
        links:
          - href: "{{ .CommonAnnotations.runbook_url }}"
            text: "Runbook"
          - href: "{{ .CommonAnnotations.dashboard_url }}"
            text: "Dashboard"

  - name: slack-[team]-alerts
    slack_configs:
      - api_url: "${SLACK_WEBHOOK_URL}"
        channel: "#alerts-[team]"
        title: "{{ .GroupLabels.alertname }}"
        text: |
          *Alert:* {{ .CommonAnnotations.summary }}
          *Description:* {{ .CommonAnnotations.description }}
          *Runbook:* {{ .CommonAnnotations.runbook_url }}
        color: '{{ if eq .Status "firing" }}danger{{ else }}good{{ end }}'
```

### Grafana alert (JSON / Terraform)

```json
{
  "alert": {
    "name": "High Error Rate - [service]",
    "message": "Error rate exceeded 1% threshold",
    "conditions": [
      {
        "query": {
          "queryType": "range",
          "refId": "A",
          "expr": "sum(rate(http_requests_total{job=\"[service]\",status=~\"5..\"}[5m])) / sum(rate(http_requests_total{job=\"[service]\"}[5m]))"
        },
        "reducer": { "type": "last" },
        "evaluator": { "type": "gt", "params": [0.01] }
      }
    ],
    "for": "5m",
    "labels": { "severity": "critical" },
    "annotations": {
      "summary": "High error rate detected",
      "runbook_url": "https://wiki.internal/runbooks/..."
    }
  }
}
```

## Alert inventory table

Always accompany rules with a summary table:

| Alert | Trigger | Severity | Who's notified | Runbook |
|-------|---------|----------|----------------|---------|
| `HighErrorRate` | Error rate > 1% for 5m | Critical | PagerDuty: [team]-oncall | [link] |
| `ModerateErrorRate` | Error rate > 0.5% for 10m | Warning | Slack: #alerts-[team] | [link] |
| `HighLatencyP95` | p95 > 500ms for 5m | Critical | PagerDuty: [team]-oncall | [link] |
| `ServiceDown` | `up == 0` for 1m | Critical | PagerDuty: [team]-oncall | [link] |
| `SLOBurnRateFast` | 14.4x burn rate for 2m | Critical | PagerDuty: [team]-oncall | [link] |

## Calibration

- **Prometheus**: Full YAML rules + alertmanager routing
- **Datadog**: Show `datadog_monitor` Terraform resource
- **Grafana Cloud**: Show unified alerting JSON
- **SLO-based only**: Focus on the multi-window burn rate alerts
- **Greenfield service**: Generate a starter set (error rate, latency, availability, saturation)
