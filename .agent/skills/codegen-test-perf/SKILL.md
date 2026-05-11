---
name: codegen-test-perf
description: >
  Generates performance and load test scripts with load scenarios, ramp-up profiles, thresholds, and
  assertions for APIs, services, and web applications. Use this skill whenever the user wants to write
  performance tests, load tests, stress tests, soak tests, spike tests, or asks to "write a load test",
  "test how many users my app can handle", "generate k6 scripts", "write Gatling scenarios", "create JMeter
  test plans", "benchmark this API", "simulate N concurrent users", "find the breaking point of my service",
  or "add performance testing". Also trigger for "throughput testing", "latency benchmarking", "capacity
  planning tests", "performance regression tests", and "SLO validation tests". Detect the tool from context
  (k6 for JavaScript/Node.js projects, Gatling for JVM, Locust for Python, JMeter as fallback).
  Distinct from strategy-test (which plans what performance tests to write) and setup-test-framework
  (which scaffolds the testing framework).
---

# codegen-test-perf

Generate **performance and load test scripts** with realistic scenarios, ramp-up profiles, and pass/fail thresholds.

## Tool selection

Detect the preferred tool from context:
- **k6** — default for JavaScript/Node.js/Go projects, or if user mentions k6 explicitly
- **Gatling** — JVM projects (Java, Kotlin, Scala); user mentions Gatling
- **Locust** — Python projects; user mentions Locust
- **Artillery** — Node.js; user mentions Artillery
- **JMeter** — enterprise/mixed environments; user requests it explicitly
- **wrk / autocannon** — simple HTTP benchmarking; user wants a quick benchmark

If ambiguous, use k6 (most portable, clean JavaScript DSL).

## Test type selection

| Type | When to use | Key characteristics |
|------|-------------|---------------------|
| **Load test** | Verify system under expected load | Steady state at realistic concurrency |
| **Stress test** | Find the breaking point | Ramp up until errors appear |
| **Soak test** | Detect memory leaks, degradation over time | Sustained load for hours |
| **Spike test** | Simulate sudden traffic burst | Instant jump to high load |
| **Smoke test** | Basic sanity check — is it up? | 1 VU, 1 iteration |

Generate the type the user describes. If unclear, generate a load test with stress options commented out.

## Information gathering

From context, identify:
- **Target**: URL(s), endpoint(s), or user flow to test
- **Expected load**: Concurrent users or RPS target
- **SLOs / thresholds**: p95 latency, error rate, throughput
- **Authentication**: API keys, JWT, session cookies?
- **Data variation**: Fixed data or parameterized requests?
- **Environment**: Dedicated load test env? Rate limiting to work around?

## k6 output template

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('error_rate');
const responseTime = new Trend('response_time_ms', true);

// Test configuration
export const options = {
  // Load profile: ramp up → steady state → ramp down
  stages: [
    { duration: '1m', target: 20 },   // Ramp up to 20 VUs
    { duration: '5m', target: 20 },   // Hold at 20 VUs
    { duration: '30s', target: 0 },   // Ramp down
  ],

  // Thresholds — test fails if these are breached
  thresholds: {
    http_req_duration: ['p(95)<500'],       // 95th percentile < 500ms
    http_req_failed: ['rate<0.01'],         // Error rate < 1%
    error_rate: ['rate<0.01'],
  },
};

// Test data / parameters
const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';
const API_KEY = __ENV.API_KEY || 'test-key';

const headers = {
  'Authorization': `Bearer ${API_KEY}`,
  'Content-Type': 'application/json',
};

export default function () {
  // Scenario: [describe the user journey]
  
  // Step 1: [action]
  const res = http.get(`${BASE_URL}/api/v1/resource`, { headers });
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'response has data': (r) => r.json('data') !== null,
  });
  
  errorRate.add(res.status !== 200);
  responseTime.add(res.timings.duration);
  
  sleep(1); // Think time between requests
}

export function handleSummary(data) {
  return {
    'stdout': textSummary(data, { indent: ' ', enableColors: true }),
    'results/summary.json': JSON.stringify(data),
  };
}
```

## Gatling output template

```scala
import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class [ServiceName]LoadTest extends Simulation {

  val httpProtocol = http
    .baseUrl("[BASE_URL]")
    .header("Content-Type", "application/json")
    .header("Authorization", "Bearer [TOKEN]")

  val scn = scenario("[Scenario name]")
    .exec(
      http("[Request name]")
        .get("/api/v1/resource")
        .check(
          status.is(200),
          responseTimeInMillis.lte(500),
          jsonPath("$.data").exists
        )
    )
    .pause(1)

  setUp(
    scn.inject(
      rampUsers(20).during(1.minute),
      constantUsersPerSec(20).during(5.minutes),
    )
  ).protocols(httpProtocol)
   .assertions(
     global.responseTime.percentile(95).lte(500),
     global.failedRequests.percent.lte(1)
   )
}
```

## Locust output template

```python
from locust import HttpUser, task, between
from locust import events
import json

class [ServiceName]User(HttpUser):
    wait_time = between(1, 3)  # Think time between requests
    
    headers = {
        "Authorization": "Bearer [TOKEN]",
        "Content-Type": "application/json",
    }
    
    def on_start(self):
        """Called when a simulated user starts."""
        pass
    
    @task(3)  # Weight: this task runs 3x more than weight-1 tasks
    def get_resource(self):
        with self.client.get(
            "/api/v1/resource",
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Expected 200, got {response.status_code}")
            elif response.elapsed.total_seconds() > 0.5:
                response.failure("Response too slow")
    
    @task(1)
    def create_resource(self):
        payload = {"name": "test", "value": 42}
        self.client.post("/api/v1/resource", json=payload, headers=self.headers)
```

## Instructions to run (include in output)

Always include a brief "How to run" section with:
- Install command
- Run command with key parameters
- Environment variable documentation
- How to interpret results

## Parameterization

When requests need varied data (avoid cache hits, test realistic load):
- k6: Use `SharedArray` + CSV or JSON data file
- Gatling: Use `feeder` with CSV or JSON
- Locust: Use `random.choice()` from a list

## Scenario realism

Performance tests should simulate realistic user behavior:
- Add `sleep()` / `pause()` / `wait_time` to model think time (typically 1–5 seconds)
- Mix read and write operations in proportions matching production traffic
- Include authentication flows if applicable
- Vary request data to avoid artificial cache hits

## Calibration

- **Single endpoint benchmark**: Simple script, one request, loop, threshold assertions
- **User journey**: Multi-step scenario with checks at each step
- **Microservice integration**: Test the chain (auth → service A → service B)
- **Regression test**: Low VU count, tight thresholds — fails if perf degrades from baseline
