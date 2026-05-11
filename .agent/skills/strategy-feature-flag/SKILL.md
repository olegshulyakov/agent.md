---
name: strategy-feature-flag
description: >
  Produces a feature flag strategy with rollout plan, flag lifecycle management, kill switch patterns,
  and implementation guidance. Use this skill whenever the user wants to implement feature flags, design
  a feature toggle strategy, plan a gradual feature rollout, manage dark launches, or asks to "how
  should I implement feature flags", "design a feature flag strategy", "plan a gradual rollout",
  "implement a kill switch for this feature", "set up LaunchDarkly", "write a feature toggle policy",
  "how do I safely release this feature", or "dark launch this feature". Also trigger for "canary
  release via flags", "A/B testing setup", "feature toggle lifecycle", "flag cleanup policy", and
  "percentage rollout". Distinct from setup-pipeline-cicd (which handles CI/CD deployment pipelines)
  and checklist-release (which covers the deployment checklist).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# strategy-feature-flag

Produce a **feature flag strategy** with rollout plan, flag types, lifecycle management, and implementation patterns.

## What makes a great feature flag strategy

Feature flags are powerful but dangerous if left unmanaged — they accumulate into "flag debt" that makes code hard to reason about. A good strategy has clear rules for when to use flags, how to name them, and crucially, when to delete them. The flag lifecycle is as important as the flag itself.

## Flag types

| Type | Purpose | Example | Lifetime |
|------|---------|---------|---------|
| **Release flag** | Hide in-progress work behind a flag | `new_checkout_flow_enabled` | Weeks; remove after full rollout |
| **Experiment flag** | A/B testing; measure impact | `checkout_v2_experiment` | Until experiment concludes |
| **Ops flag** | Kill switch for risky features | `payment_service_v2` | Permanent or until feature is stable |
| **Permission flag** | Control access by user group | `beta_dashboard_users` | Long-lived; managed by product |
| **Infrastructure flag** | Control technical behavior | `use_redis_cache` | Until migration completes |

## Information gathering

From context, identify:
- **Feature**: What is being flagged?
- **Flag type**: Release, experiment, ops, or permission?
- **Rollout target**: % of users, specific users, by geography, by plan tier?
- **Risk level**: What's the impact if the feature causes issues?
- **Flag service**: LaunchDarkly, Unleash, Flagsmith, custom, env vars?

## Output format

```markdown
# Feature Flag Strategy: [Feature Name]

**Feature:** [What the flag controls]
**Flag name:** `[feature_flag_name]` *(snake_case, descriptive, prefixed by type if applicable)*
**Flag type:** [Release / Experiment / Ops / Permission]
**Owner:** [team]
**Planned rollout date:** [date]
**Planned removal date:** [date] *(required for release flags)*

---

## Flag Definition

```json
{
  "key": "new_checkout_flow_enabled",
  "name": "New Checkout Flow",
  "description": "Enables the redesigned checkout experience with one-click payment",
  "type": "boolean",
  "defaultValue": false,
  "temporary": true,
  "tags": ["checkout", "Q2-2024", "release"],
  "owner": "commerce-team",
  "createdDate": "2024-01-15",
  "plannedRemovalDate": "2024-04-15"
}
```

---

## Rollout Plan

### Phase 1: Internal (Week 1)
- Target: Team members only (`user.email in ['@company.com']`)
- Goal: Basic functionality validation; catch obvious bugs
- Success criteria: No P0/P1 bugs reported; team gives green light

### Phase 2: Beta / Early Access (Week 2)
- Target: 5% of users — prefer engaged, technically savvy users
- Goal: Real-world validation; performance under actual load
- Success criteria: Error rate within [0.5%] of baseline; no data integrity issues

### Phase 3: Gradual Rollout (Weeks 3–4)
- Target: 25% → 50% → 75% → 100%
- Hold time between steps: [24–48 hours]
- Monitor at each step: Error rate, latency, conversion rate, support tickets

### Phase 4: Full Rollout (Week 5)
- Target: 100% of users
- Announcement: Internal changelog; customer communications if user-visible
- Remove flag: [Date — 2–4 weeks after full rollout]

---

## Targeting Rules

```
Priority order (first matching rule wins):

1. Internal employees → always ON (for development)
2. Beta program members → ON
3. User ID modulo 100 < percentage_threshold → ON
4. Default → OFF
```

```javascript
// LaunchDarkly targeting rules example
{
  "rules": [
    {
      "description": "Internal employees",
      "clauses": [{ "attribute": "email", "op": "endsWith", "values": ["@company.com"] }],
      "variation": true
    },
    {
      "description": "Beta users",
      "clauses": [{ "attribute": "betaMember", "op": "in", "values": [true] }],
      "variation": true
    }
  ],
  "fallthrough": {
    "rollout": {
      "variations": [
        { "variation": 0, "weight": 90000 },  // 90% OFF
        { "variation": 1, "weight": 10000 }   // 10% ON
      ]
    }
  }
}
```

---

## Implementation

### Server-side (Node.js with LaunchDarkly)

```typescript
import * as ld from '@launchdarkly/node-server-sdk';

const client = ld.init(process.env.LD_SDK_KEY!);

// In request handler or service
async function getCheckoutFlow(userId: string, userAttributes: Record<string, any>) {
  const context = {
    kind: 'user',
    key: userId,
    email: userAttributes.email,
    plan: userAttributes.plan,
    betaMember: userAttributes.betaMember,
  };

  const useNewFlow = await client.variation(
    'new_checkout_flow_enabled',
    context,
    false  // Default value if SDK fails — fail safe
  );

  return useNewFlow ? newCheckoutService : legacyCheckoutService;
}
```

### Client-side (React)

```typescript
import { useFlags } from 'launchdarkly-react-client-sdk';

function CheckoutPage() {
  const { newCheckoutFlowEnabled } = useFlags();

  return newCheckoutFlowEnabled
    ? <NewCheckoutFlow />
    : <LegacyCheckoutFlow />;
}
```

### Environment variable flags (simplest; no service required)

```typescript
// config/features.ts
export const features = {
  newCheckoutFlow: process.env.FEATURE_NEW_CHECKOUT_FLOW === 'true',
  paymentServiceV2: process.env.FEATURE_PAYMENT_V2 === 'true',
} as const;

// Usage
if (features.newCheckoutFlow) {
  // ...
}
```

---

## Kill Switch Pattern

For high-risk features, implement a kill switch that can be flipped instantly:

```typescript
// Ops flag — can be disabled instantly if issues arise
const paymentV2Enabled = await client.variation('payment_service_v2', context, false);

if (!paymentV2Enabled) {
  // Automatic fallback to stable v1
  return legacyPaymentService.process(payment);
}

try {
  return await paymentServiceV2.process(payment);
} catch (err) {
  // Circuit breaker: if errors spike, alert and auto-disable
  await metrics.increment('payment_v2_error');
  if (await metrics.errorRate('payment_v2', '5m') > 0.05) {
    await flagClient.disable('payment_service_v2');
    await alerting.notify('payment_v2_auto_disabled', { reason: err.message });
  }
  throw err;
}
```

---

## Monitoring Per Flag

For each active flag, track:

| Metric | Where to measure | Threshold to investigate |
|--------|-----------------|--------------------------|
| Error rate (on vs off) | Observability platform | > 2× baseline when ON |
| Latency p95 | Observability platform | > 20% regression when ON |
| Conversion rate (for experiments) | Analytics | Statistically significant change |
| Support tickets | Zendesk / Jira | Spike correlating with rollout |

```javascript
// Tag metrics with flag state for comparison
metrics.histogram('checkout.duration', duration, {
  feature: 'new_checkout_flow',
  enabled: String(useNewFlow),
});
```

---

## Flag Lifecycle Policy

| Stage | Action | Who |
|-------|--------|-----|
| **Created** | Flag defined in service; default = OFF; JIRA ticket for removal created | Dev |
| **Rolling out** | Follow rollout plan; monitor metrics at each step | Dev + PM |
| **At 100%** | Announce full rollout; schedule flag removal | PM |
| **Removal** | Remove flag and dead code branches; PR review; close tracking ticket | Dev |
| **Overdue** | Flag older than [90 days] past planned removal → auto-alert owner | Automation |

### Flag cleanup

```bash
# Find all flag references in code
grep -r "new_checkout_flow_enabled" --include="*.ts" src/

# After removing: the code in the ON branch stays; delete the flag check + OFF branch
```

---

## Flag Naming Convention

```
[type_prefix_][feature_name][_context]

Examples:
  new_checkout_flow_enabled      (release flag — no prefix needed)
  exp_checkout_button_color      (experiment flag)
  ops_payment_service_v2         (ops/kill-switch flag)
  beta_dashboard_pro_users       (permission flag)
  infra_use_redis_session_cache  (infrastructure flag)
```

Rules:
- Snake_case
- Descriptive: someone unfamiliar should understand the flag's purpose
- Avoid negatives: `new_feature_enabled` not `old_feature_disabled`
- Include context in experiment flags: `exp_checkout_[what is being tested]`

---

## Flag Registry

Maintain a registry (wiki, spreadsheet, or flag service's built-in tags):

| Flag | Type | Owner | Created | Remove By | Status |
|------|------|-------|---------|-----------|--------|
| `new_checkout_flow_enabled` | Release | Commerce | 2024-01-15 | 2024-04-15 | 🟡 Rolling out (75%) |
| `ops_payment_v2` | Ops | Payments | 2024-02-01 | Never | 🟢 100% |
| `exp_checkout_cta` | Experiment | Growth | 2024-03-01 | 2024-04-01 | 🔵 Running (50%) |
```

## Calibration

- **Simple release flag**: Flag definition + rollout plan + removal date; skip kill switch and monitoring sections
- **Ops/kill switch**: Emphasize the kill switch pattern + auto-disable on error spike
- **A/B experiment**: Add metric tracking and statistical significance guidance
- **No flag service**: Use environment variables pattern; explain trade-offs
