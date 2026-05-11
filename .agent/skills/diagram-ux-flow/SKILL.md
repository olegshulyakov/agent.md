---
name: diagram-ux-flow
description: >
  Produces user flow diagrams and journey maps in structured Mermaid or text format. Use this skill
  whenever the user wants to create a user flow, map a user journey, visualize screens and transitions,
  document navigation flows, create wireflow annotations, or asks to "draw a user flow", "create a
  journey map", "map the user flow for this feature", "show the screens and navigation", "document the
  happy path for this feature", "create a flow diagram for the onboarding process", or "show the
  decision points in this user journey". Also trigger for "task flow diagram", "screen flow", "UX flow",
  "navigation map", "user path", and "interaction flow". Distinct from diagram-dfd (data flows through
  system processes) and diagram-c4 (software architecture).
---

# diagram-ux-flow

Produce **user flow diagrams and journey maps** that visualize how users move through a product.

## Flow types

| Type | Best for | Output |
|------|----------|--------|
| **Task Flow** | Single task from entry to completion | Linear or branching flowchart |
| **User Flow** | Multiple entry points, decision points, and outcomes | Full flowchart with decisions |
| **Journey Map** | Emotional arc, touchpoints, pain points across a longer experience | Table + narrative |
| **Screen Flow** | Screen-by-screen navigation with transitions | Sequence of screens with arrows |

Generate the type the user requests. Default to User Flow if unclear.

## Information gathering

From context, identify:
- **Feature/task**: What is the user trying to accomplish?
- **User type**: Persona or role (first-time user, admin, returning customer)?
- **Entry points**: Where do users start? (Home, email link, direct URL, notification?)
- **Key decisions**: What choices do users make that branch the flow?
- **Success state**: What does task completion look like?
- **Error states**: What happens when something fails?

## Output format — Mermaid Flowchart

### User / Task Flow

```mermaid
flowchart TD
    %% Entry points
    start([Start: User opens app])
    direct_url([Start: Clicks email link])

    %% Screens / States
    home["🏠 Home Screen"]
    login["🔐 Login Screen"]
    register["📝 Registration"]
    dashboard["📊 Dashboard"]
    product_list["📦 Product List"]
    product_detail["🔍 Product Detail"]
    cart["🛒 Cart"]
    checkout["💳 Checkout"]
    payment["💰 Payment"]
    confirmation["✅ Order Confirmation"]

    %% Error / Edge states
    login_error["❌ Login Error\n'Invalid credentials'"]
    payment_error["❌ Payment Failed\n'Card declined'"]
    empty_cart["⚠️ Empty Cart\n'Add items to continue'"]

    %% Decisions (diamond shape)
    has_account{Has account?}
    cart_empty{Cart empty?}
    payment_ok{Payment\nsuccessful?}

    %% Flows
    start --> home
    direct_url --> login
    home --> has_account
    has_account -->|"Yes"| login
    has_account -->|"No"| register
    register --> dashboard
    login -->|"Success"| dashboard
    login -->|"Failure"| login_error
    login_error -->|"Retry"| login

    dashboard --> product_list
    product_list --> product_detail
    product_detail -->|"Add to cart"| cart
    cart --> cart_empty
    cart_empty -->|"Yes"| empty_cart
    cart_empty -->|"No"| checkout
    empty_cart -->|"Browse"| product_list
    checkout --> payment
    payment --> payment_ok
    payment_ok -->|"Yes"| confirmation
    payment_ok -->|"No"| payment_error
    payment_error -->|"Retry"| payment
    payment_error -->|"Cancel"| cart

    %% Styling
    style confirmation fill:#d1fae5,stroke:#059669
    style login_error fill:#fee2e2,stroke:#dc2626
    style payment_error fill:#fee2e2,stroke:#dc2626
    style empty_cart fill:#fef3c7,stroke:#d97706
```

### Screen Flow (Sequence style)

```mermaid
stateDiagram-v2
    [*] --> Home
    Home --> Login: Tap "Sign In"
    Home --> Browse: Tap "Browse"
    Login --> Dashboard: Auth success
    Login --> Home: Cancel
    Browse --> ProductDetail: Tap product
    Dashboard --> Browse: Tap "Shop"
    ProductDetail --> Cart: Add to cart
    Cart --> Checkout: Proceed
    Checkout --> Payment: Enter details
    Payment --> Confirmation: Payment success
    Payment --> Cart: Payment failed
    Confirmation --> [*]
```

## Journey Map format (when requested)

```markdown
## User Journey Map: [Feature Name]

**Persona:** [User type — e.g., "First-time buyer"]
**Goal:** [What they're trying to accomplish]
**Scenario:** [Context — e.g., "User receives a promotional email and wants to buy a product"]

---

| Phase | Action | Touchpoint | Thoughts / Feelings | Pain Points | Opportunities |
|-------|--------|-----------|---------------------|-------------|---------------|
| **Awareness** | Receives email | Email | "Oh, this looks interesting" | Email looks like spam | Better subject line; personalization |
| **Arrival** | Clicks link → Landing page | Web | "Where do I even start?" | Page is overwhelming | Clear CTA, guided onboarding |
| **Discovery** | Browses products | Product list | "I can't find what I want" | Poor search/filter | Improve search; add facets |
| **Consideration** | Views product detail | Product page | "Is this the right one?" | No reviews, unclear specs | Add reviews; comparison feature |
| **Decision** | Adds to cart | Cart | "Okay, let's do this" | Unexpected shipping cost | Show shipping cost earlier |
| **Purchase** | Completes checkout | Checkout | "This is taking forever" | Too many form fields | Guest checkout; autofill |
| **Post-purchase** | Receives confirmation | Email | "Did it actually work?" | No tracking info | Real-time order tracking |

**Emotional Arc:**
😐 → 🤔 → 😕 → 😕 → 😒 → 😤 → 😊

**Top 3 Pain Points:**
1. [Most impactful pain point]
2. [Second pain point]
3. [Third pain point]

**Top 3 Opportunities:**
1. [Highest impact improvement]
2. [Second improvement]
3. [Third improvement]
```

## Annotation guidelines

Add these to flows as needed:
- **Decisions**: Use diamond shapes `{question}` — always labeled with both Yes/No paths
- **Error states**: Use `❌` prefix and red styling — always show recovery path
- **External systems**: Use `([rounded])` shape — indicates system boundary crossing
- **Success states**: Use `✅` prefix and green styling

## Calibration

- **Happy path only**: Simple linear flow, no error states — use for initial sketches
- **Full flow with errors**: Include all error and edge case paths
- **Mobile-specific**: Label interactions as "Tap", "Swipe", "Long press" rather than "Click"
- **Multi-persona**: Show parallel tracks with swimlanes
- **Journey map**: When emotional experience and pain points matter more than UI transitions
