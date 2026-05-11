---
name: strategy-api-versioning
description: >
  Produces an API versioning strategy with deprecation policy, migration guide, and version lifecycle
  management. Use this skill whenever the user wants to design an API versioning approach, plan API
  deprecations, manage backward compatibility, create a version lifecycle policy, or asks to "how should
  I version my API", "design an API versioning strategy", "how do I deprecate an API", "create a
  deprecation policy", "manage breaking changes in my API", "write a migration guide for API changes",
  "should I use URL versioning or header versioning?", or "API backward compatibility policy". Also
  trigger for "semantic versioning for APIs", "breaking vs non-breaking changes", "sunset headers",
  and "API evolution strategy". Distinct from design-api (which designs the initial API contract) and
  writer-api-docs (which documents existing endpoints).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# strategy-api-versioning

Produce an **API versioning strategy** with versioning approach selection, deprecation policy, and consumer migration guidance.

## Versioning approach comparison

| Approach | Example | Pros | Cons | Best for |
|----------|---------|------|------|---------|
| **URL path** | `/api/v2/orders` | Explicit, cacheable, easy to test | URL pollution, can't evolve per-resource | Public APIs, REST |
| **Query parameter** | `?api-version=2024-01-01` | Simple, no URL changes | Easy to forget, less cache-friendly | Azure-style APIs |
| **Header** | `Accept-Version: 2` | Clean URLs, flexible | Less discoverable, harder to share links | Internal APIs |
| **Content negotiation** | `Accept: application/vnd.api+json;version=2` | RESTful, standards-based | Complex for clients | Hypermedia APIs |
| **Date-based** | `2024-01-15` | Clear lifecycle, no integer creep | Requires date tracking | Stripe-style |

**Recommendation logic:**
- Public API with external consumers → **URL path** versioning (most familiar)
- Internal API, frequent evolution → **Header** or **date-based**
- Azure/Microsoft ecosystem → **Query parameter** date-based
- GraphQL → Don't version; evolve schema with deprecation fields

## Information gathering

From context, identify:
- **API type**: Public/external, internal, partner?
- **Client types**: Mobile apps, SPAs, third-party developers, internal services?
- **Change velocity**: How often do breaking changes happen?
- **Existing convention**: Already have versioning?

## Output format

```markdown
# API Versioning Strategy: [API Name]

**Date:** [date]
**Owner:** [team]
**Applies to:** [which APIs]

---

## Versioning Approach

**Selected approach:** [URL Path / Header / Date-based / Query param]

**Rationale:** [Why this approach — consider client types, caching, discoverability]

### Format

```
[API Base URL]/[version]/[resource]
Example: https://api.example.com/v2/orders
```

**Version format:** `v{MAJOR}` (integer increment)
- `v1` → `v2` on breaking changes
- No minor/patch versioning at the URL level — use non-breaking evolution within a version

---

## Change Classification

### Non-breaking changes (no version bump required)
These can be deployed to an existing version without incrementing:

- ✅ Adding new optional request fields
- ✅ Adding new response fields
- ✅ Adding new endpoints
- ✅ Adding new optional query parameters
- ✅ Adding new enum values (if consumers handle unknown values gracefully)
- ✅ Relaxing validation rules (e.g., making a field optional that was required)
- ✅ Expanding maximum field length

### Breaking changes (require a new version)

- 🚫 Removing or renaming fields
- 🚫 Changing field types (string → integer)
- 🚫 Adding required request fields
- 🚫 Changing error response format
- 🚫 Changing authentication mechanism
- 🚫 Removing endpoints
- 🚫 Changing URL structure
- 🚫 Tightening validation rules

---

## Deprecation Policy

### Lifecycle stages

```
Active → Deprecated → Sunset
  ↑          ↑           ↑
launch   announce    remove
```

### Timeline

| API type | Deprecation notice | Sunset period | Total lifecycle |
|----------|-------------------|---------------|----------------|
| External / public | 12 months before sunset | 12 months | ≥ 24 months |
| Partner API | 6 months before sunset | 6 months | ≥ 12 months |
| Internal API | 3 months before sunset | 3 months | ≥ 6 months |

### Deprecation announcement process

1. **Announce** in CHANGELOG, API docs, and developer newsletter
2. **Add `Deprecation` header** to all deprecated endpoint responses:
   ```
   Deprecation: true
   Sunset: Sat, 01 Jun 2026 00:00:00 GMT
   Link: <https://api.example.com/docs/migration/v1-to-v2>; rel="successor-version"
   ```
3. **Email** all registered developers with affected endpoints and migration guide
4. **Monitor usage** — track request counts to deprecated endpoints per consumer
5. **Re-notify** at 3 months and 1 month before sunset
6. **Return 410 Gone** at sunset (not 404)

### Sunset behavior

```json
// Response when calling a sunsetted endpoint
HTTP/1.1 410 Gone
Content-Type: application/json

{
  "error": "endpoint_sunsetted",
  "message": "This API version has been retired. Please migrate to v2.",
  "migration_guide": "https://api.example.com/docs/migration/v1-to-v2",
  "sunsetted_at": "2026-06-01T00:00:00Z"
}
```

---

## Versioning Implementation

### URL routing (Express / Node.js example)

```javascript
// Register version routers
app.use('/api/v1', require('./routes/v1'));
app.use('/api/v2', require('./routes/v2'));

// Redirect root /api calls to latest
app.get('/api', (req, res) => {
  res.redirect('/api/v2');
});

// Deprecation middleware for v1
function deprecationMiddleware(req, res, next) {
  res.set({
    'Deprecation': 'true',
    'Sunset': 'Sat, 01 Jun 2026 00:00:00 GMT',
    'Link': '<https://api.example.com/docs/migration/v1-to-v2>; rel="successor-version"',
  });
  next();
}
app.use('/api/v1', deprecationMiddleware);
```

### Header versioning (alternative)

```javascript
function versionMiddleware(req, res, next) {
  const version = req.headers['accept-version'] || 'latest';
  req.apiVersion = version === 'latest' ? 'v2' : version;
  next();
}
```

---

## Version Coexistence

### Running multiple versions

```
api-gateway (load balancer)
├── /v1 → service-v1 (maintained but no new features)
├── /v2 → service-v2 (active development)
└── /v3 → service-v3 (beta / early access)
```

**Strategies for code sharing:**
- **Shared business logic**: Keep core domain logic version-agnostic; version only the API layer
- **Request/response adapters**: `v1Adapter(v2Request)` transforms old format to new before passing to domain
- **Feature flags**: Use flags to toggle behavior within the same codebase without a full version split

### Database compatibility

When a new API version changes the data model:
- Use additive schema changes (add columns, don't remove)
- Map old format to new in the adapter layer
- Keep backward-compatible DB schema until v1 is sunset

---

## Consumer Migration Guide Template

When releasing a new version, publish a migration guide with this structure:

```markdown
# Migration Guide: v1 → v2

**Migration deadline:** [sunset date]
**Breaking changes:** [count]
**Estimated effort:** [S/M/L]

## What changed and why

[Brief explanation of the motivation for v2]

## Breaking changes

### 1. [Endpoint or field change]

**Before (v1):**
```json
GET /api/v1/orders
{ "status": "shipped" }
```

**After (v2):**
```json
GET /api/v2/orders
{ "fulfillment_status": "shipped", "payment_status": "captured" }
```

**Migration:** Replace `status` with `fulfillment_status`. Use `payment_status` for payment-related checks.

## Non-breaking additions

- [New field added in v2 — can adopt incrementally]

## Migration checklist

- [ ] Update base URL from `/v1` to `/v2`
- [ ] Update field mapping: `status` → `fulfillment_status`
- [ ] Test with v2 in staging
- [ ] Update API client library to [version]

## Support

- Slack: #api-migration
- Email: api-support@example.com
```

---

## Governance

| Decision | Owner | Process |
|----------|-------|---------|
| Classify a change as breaking | API team + consumers | Architecture review |
| Approve a new version | API team | RFC + 2-week comment period |
| Extend sunset deadline | API team | Usage-based; communicate to affected consumers |
| Emergency sunset (security) | Security + API team | 24-hour notice minimum |

---

## Version Inventory

| Version | Status | Released | Sunset | Active consumers |
|---------|--------|---------|--------|-----------------|
| v1 | Deprecated | 2022-01-01 | 2026-06-01 | [N] |
| v2 | Active | 2024-01-01 | TBD | [N] |
| v3 | Beta | 2025-01-01 | TBD | [N] |
```

## Calibration

- **No existing versioning**: Start with the approach selection section and rationale
- **Planning deprecation**: Focus on the deprecation policy and timeline sections
- **Migration guide only**: Use the consumer migration guide template
- **Internal API**: Shorter timeline; simpler process; fewer formal requirements
