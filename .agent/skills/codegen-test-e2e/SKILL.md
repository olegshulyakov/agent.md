---
name: codegen-test-e2e
description: >
  Generates end-to-end (E2E) test suites with scenarios, page objects, and assertions for web and mobile applications.
  Use this skill whenever the user wants to write E2E tests, browser tests, integration tests for user flows,
  Playwright tests, Cypress tests, Selenium tests, or asks to "test this user journey", "automate this flow",
  "write UI tests", "generate acceptance tests", or "create end-to-end test coverage". Also trigger for
  "test the happy path", "test the login flow", "write tests for this feature", or "set up E2E testing".
  Distinct from codegen-test-api (API contract tests) and codegen-test-perf (performance/load tests).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# codegen-test-e2e

Generate a **production-ready E2E test suite** covering user flows, page objects, assertions, and test data setup.

## Framework detection

Identify the test framework from context. Check in order:

1. Explicit mention ("playwright", "cypress", "selenium")
2. `package.json` devDependencies
3. Existing test file patterns (`.spec.ts`, `cypress/e2e/`)
4. Project type (Next.js / Vite → likely Playwright; older React → possibly Cypress)
5. If ambiguous: **default to Playwright** (TypeScript) — it's the modern standard; note the assumption

## Output structure

Produce:

```
tests/e2e/
├── [feature].spec.ts       # Test scenarios
├── pages/
│   └── [Feature]Page.ts    # Page Object(s)
└── fixtures/
    └── [feature].fixture.ts  # Test data / fixture setup (if needed)
```

## Page Object Model (POM)

Always use POM. Benefits: resilient to UI changes (selectors in one place), readable test scenarios.

**Page object template (Playwright TypeScript):**

```typescript
import { Page, Locator } from '@playwright/test';

export class [Feature]Page {
    readonly page: Page;

    // Locators — prefer data-testid, then role, then text, never CSS selectors for structure
    readonly [element]: Locator;

    constructor(page: Page) {
        this.page = page;
        this.[element] = page.getByTestId('[data-testid]');
        // or: page.getByRole('button', { name: 'Submit' });
        // or: page.getByLabel('Email');
    }

    async navigate() {
        await this.page.goto('/[path]');
        await this.page.waitForURL('/[path]');
    }

    async [action]([params]: [type]) {
        await this.[input].fill([params]);
        await this.[button].click();
        // Wait for a concrete signal, not a fixed timeout
        await this.page.waitForURL('/[expected-path]');
    }

    async expect[State]() {
        await expect(this.[element]).toBeVisible();
        await expect(this.[element]).toHaveText('[expected]');
    }
}
```

**Cypress variant (if requested):**

```typescript
// cypress/e2e/[feature].cy.ts
describe("[Feature]", () => {
  beforeEach(() => {
    cy.visit("/[path]");
  });

  it("[scenario]", () => {
    cy.findByRole("button", { name: "[label]" }).click();
    cy.url().should("include", "/[path]");
    cy.findByText("[expected]").should("be.visible");
  });
});
```

## Test scenario structure

For each user flow, write:

```typescript
import { test, expect } from '@playwright/test';
import { [Feature]Page } from './pages/[Feature]Page';

test.describe('[Feature] — [User Type]', () => {
    let [feature]Page: [Feature]Page;

    test.beforeEach(async ({ page }) => {
        [feature]Page = new [Feature]Page(page);
        // Setup: seed test data or authenticate if needed
    });

    test.afterEach(async () => {
        // Cleanup test data if needed
    });

    // Happy path — most important flow first
    test('should [do the main thing] successfully', async ({ page }) => {
        await [feature]Page.navigate();
        await [feature]Page.[action]([data]);
        await expect(page).toHaveURL('/[expected-path]');
        await [feature]Page.expect[SuccessState]();
    });

    // Edge cases and error flows
    test('should show error when [condition]', async () => {
        await [feature]Page.navigate();
        await [feature]Page.[actionWithBadData]([invalid]);
        await expect([feature]Page.[errorMessage]).toContainText('[message]');
    });

    // Boundary / accessibility
    test('should be accessible via keyboard navigation', async ({ page }) => {
        await [feature]Page.navigate();
        await page.keyboard.press('Tab');
        // ...
    });
});
```

## Test data strategy

Address test data explicitly:

**Option A — API setup (preferred):** Use `test.beforeEach` to seed via API calls, clean up after:

```typescript
test.beforeEach(async ({ request }) => {
  await request.post("/api/test/seed", {
    data: {
      /* ... */
    },
  });
});
```

**Option B — Database seeding:** Use a fixture file that runs migrations or inserts.

**Option C — Mock API responses:** Use `page.route()` to intercept and mock:

```typescript
await page.route("**/api/users", (route) =>
  route.fulfill({
    status: 200,
    body: JSON.stringify({ users: [{ id: "1", name: "Test User" }] }),
  }),
);
```

Document which strategy is used and why.

## Selector priority

Always prefer in this order (most resilient to least):

1. `data-testid` attributes → `getByTestId('submit-btn')`
2. ARIA roles → `getByRole('button', { name: 'Submit' })`
3. Labels → `getByLabel('Email address')`
4. Text content → `getByText('Login')`
5. **Avoid:** CSS selectors (`.btn-primary`), XPath, nth-child — brittle

## Assertions

Use specific, meaningful assertions:

```typescript
// Good
await expect(page.getByRole("alert")).toContainText("Invalid email address");
await expect(page).toHaveURL("/dashboard");
await expect(page.getByTestId("order-count")).toHaveText("3");

// Avoid
await expect(page.locator(".error")).toBeVisible(); // no content check
await page.waitForTimeout(2000); // arbitrary timeout — use waitFor* instead
```

## Configuration (Playwright)

Include `playwright.config.ts` if setting up from scratch:

```typescript
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  timeout: 30_000,
  expect: { timeout: 5_000 },
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  reporter: [["html"], ["list"]],
  use: {
    baseURL: process.env.BASE_URL ?? "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "firefox", use: { ...devices["Desktop Firefox"] } },
  ],
});
```

## Coverage scope

For each feature, generate tests covering:

1. **Happy path** — the primary success scenario
2. **Validation errors** — required fields, format errors, length limits
3. **Auth boundaries** — unauthenticated access, unauthorized access
4. **Empty states** — no data, first-time user
5. **Concurrent/race conditions** — only if the feature is sensitive to them

Note explicitly what's **not** covered and why, so the user knows the gaps.
