---
name: setup-observability
description: >
  Generates observability stack configuration covering metrics (Prometheus/Grafana or cloud-native),
  structured logging, distributed tracing (OpenTelemetry), and alerting rules. Use this skill whenever
  the user wants to set up monitoring, add metrics to an application, configure logging, add tracing,
  set up Prometheus or Grafana, add OpenTelemetry, or asks to "add observability", "set up monitoring",
  "add metrics to my app", "configure structured logging", "add distributed tracing", "set up Prometheus",
  or "instrument this service". Also trigger for "add health checks", "set up alerting", "configure log
  aggregation", and "instrument for production". Distinct from writer-slo (which defines SLO targets)
  and writer-alert-rules (which writes specific alert rule definitions).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# setup-observability

Generate **observability stack configuration** covering the three pillars: metrics, logs, and traces.

## Stack detection

Identify the observability stack from context:
- **Metrics**: Prometheus+Grafana (self-hosted), Datadog, CloudWatch, Google Cloud Monitoring
- **Logs**: ELK/OpenSearch, Loki+Grafana, Datadog, CloudWatch Logs
- **Traces**: Jaeger, Zipkin, Tempo, Datadog APM, OpenTelemetry (collector + backend)
- **Default**: OpenTelemetry SDK + Prometheus metrics + structured JSON logs (most portable)

## Output structure

Produce configuration for the three pillars plus health checks:

1. **Application instrumentation** — code to add to the service
2. **Collector/agent configuration** — how to collect and forward telemetry
3. **Infrastructure configuration** — Prometheus scrape config, Grafana dashboards
4. **Health check endpoints** — `/health`, `/ready`, `/metrics`

---

## Application instrumentation (OpenTelemetry)

### Node.js / TypeScript

```typescript
// src/observability/index.ts
import { NodeSDK } from '@opentelemetry/sdk-node';
import { PrometheusExporter } from '@opentelemetry/exporter-prometheus';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';
import { resourceFromAttributes } from '@opentelemetry/resources';
import { ATTR_SERVICE_NAME, ATTR_SERVICE_VERSION } from '@opentelemetry/semantic-conventions';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';

const prometheusExporter = new PrometheusExporter({ port: 9464 });

const sdk = new NodeSDK({
  resource: resourceFromAttributes({
    [ATTR_SERVICE_NAME]: process.env.SERVICE_NAME ?? 'my-service',
    [ATTR_SERVICE_VERSION]: process.env.SERVICE_VERSION ?? '0.0.1',
    environment: process.env.NODE_ENV ?? 'development',
  }),
  metricReader: prometheusExporter,
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT ?? 'http://otel-collector:4317',
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
process.on('SIGTERM', () => sdk.shutdown());

// Structured logging setup
import pino from 'pino';
export const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
  base: {
    service: process.env.SERVICE_NAME,
    version: process.env.SERVICE_VERSION,
    env: process.env.NODE_ENV,
  },
});
```

### Python / FastAPI

```python
# src/observability.py
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.resources import Resource
from prometheus_client import start_http_server
import structlog, logging

def setup_observability(service_name: str, service_version: str):
    resource = Resource.create({
        "service.name": service_name,
        "service.version": service_version,
    })
    
    # Tracing
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter())
    )
    
    # Metrics — expose on :9090/metrics
    reader = PrometheusMetricReader()
    metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[reader]))
    start_http_server(9090)
    
    # Structured logging
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
    )
```

---

## Health check endpoints

```typescript
// src/routes/health.ts (Express example)
import { Router } from 'express';
import { db } from '../db';

const router = Router();

// Liveness: is the process running?
router.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Readiness: is the service ready to accept traffic?
router.get('/ready', async (req, res) => {
  try {
    await db.query('SELECT 1');  // DB connectivity check
    res.json({ status: 'ready', checks: { database: 'ok' } });
  } catch (err) {
    res.status(503).json({ status: 'not ready', checks: { database: 'fail' } });
  }
});

export { router as healthRouter };
```

---

## Prometheus configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'my-service'
    static_configs:
      - targets: ['my-service:9464']  # metrics port
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```

---

## OpenTelemetry Collector configuration

```yaml
# otel-collector.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 5s
  resource:
    attributes:
      - key: deployment.environment
        value: ${ENVIRONMENT}
        action: upsert

exporters:
  prometheus:
    endpoint: "0.0.0.0:8889"
  otlp/jaeger:
    endpoint: jaeger:4317
    tls:
      insecure: true
  logging:
    loglevel: warn

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, resource]
      exporters: [otlp/jaeger]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```

---

## Docker Compose for local observability stack

```yaml
# docker-compose.observability.yml
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports: ['9090:9090']

  grafana:
    image: grafana/grafana:latest
    ports: ['3001:3000']
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana-data:/var/lib/grafana

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - '16686:16686'  # UI
      - '4317:4317'    # OTLP gRPC

  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    volumes:
      - ./otel-collector.yaml:/etc/otel-collector.yaml
    command: ['--config=/etc/otel-collector.yaml']
    ports: ['4317:4317', '4318:4318']

volumes:
  grafana-data:
```

## Key metrics to instrument (SLI-driven)

Always instrument these in application code:

```typescript
import { metrics } from '@opentelemetry/api';
const meter = metrics.getMeter('my-service');

// Request rate and latency (for SLOs)
const requestDuration = meter.createHistogram('http_request_duration_ms', {
  description: 'HTTP request duration in milliseconds',
  boundaries: [5, 10, 25, 50, 100, 250, 500, 1000, 2500],
});

// Error rate
const requestErrors = meter.createCounter('http_request_errors_total', {
  description: 'Total HTTP request errors',
});

// Business metrics
const ordersCreated = meter.createCounter('orders_created_total', {
  description: 'Total orders created',
});
```
