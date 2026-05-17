# Performance Test Generation

Use this reference for load, stress, spike, soak, capacity, and latency-budget tests.

## Tool Selection

Prefer the existing tool. If no tool exists:

| Need | Tool |
| --- | --- |
| HTTP load tests with CI-friendly scripts | k6 |
| Python-heavy team or custom user behavior | Locust |
| Existing enterprise/JVM performance setup | JMeter |

Default to k6 for new HTTP performance scripts because it is scriptable, CI-friendly, and easy to review.

## Implementation Pattern

- Define the objective first: smoke performance, load, stress, spike, soak, or regression budget.
- Model realistic traffic with setup data, weighted scenarios, think time, and representative payloads.
- Keep target URLs, credentials, and thresholds configurable through environment variables.
- Add thresholds for the user-visible budget, not only generic averages. Prefer percentile checks such as `p95`.
- Validate responses inside the script so performance failures are not masked by fast error pages.
- Avoid destructive writes against production-like systems unless the user explicitly requested that and cleanup is defined.

## Scenario Defaults

For k6, include:

- `BASE_URL` environment variable.
- `options.thresholds` for `http_req_failed` and `http_req_duration`.
- A smoke or ramping scenario appropriate to the request.
- `check` calls for status and important response content.
- Short setup comments explaining how to run locally and in CI.

## k6 Example

```js
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';

export const options = {
  scenarios: {
    steady_load: {
      executor: 'ramping-vus',
      stages: [
        { duration: '1m', target: 10 },
        { duration: '3m', target: 10 },
        { duration: '1m', target: 0 },
      ],
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500'],
  },
};

export default function () {
  const response = http.get(`${BASE_URL}/health`);

  check(response, {
    'status is 200': (res) => res.status === 200,
  });

  sleep(1);
}
```

## Locust Pattern

Use one `HttpUser` per actor type, tasks weighted by expected traffic, and environment variables for host and credentials. Keep setup and teardown idempotent.

## JMeter Pattern

When asked for JMeter, generate a `.jmx` plan or a clear XML snippet only if the project already stores JMeter files. Otherwise provide the test plan structure plus CLI invocation.
