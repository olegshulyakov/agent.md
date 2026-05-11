---
name: writer-use-case
description: >
  Produces a formal Use Case document detailing actors, preconditions, main success scenario,
  alternate flows, and postconditions. Use this skill whenever the user wants to write a detailed
  use case, document user-system interactions, specify alternate flows or edge cases for a feature,
  or asks to "write a use case for X", "document the main flow and alternate flows", or "create a
  use case specification". Distinct from writer-story-task (which writes Agile user stories) and
  writer-spec-functional (which defines the entire system's functional requirements).
---

# writer-use-case

Produce a **formal Use Case** document detailing actors, flows, and conditions.

## Output format

```markdown
# Use Case: [Use Case Name]

**Use Case ID:** UC-[001]
**Primary Actor:** [e.g., Registered User, Admin, System Timer]
**Secondary Actors:** [e.g., Payment Gateway, Email Service]
**Goal in Context:** [Brief description of what the actor wants to achieve]

---

## Preconditions
*What must be true before this use case can start?*
1. [e.g., User is authenticated]
2. [e.g., User has items in their shopping cart]

## Postconditions
*What is the state of the system after successful completion?*
1. [e.g., Order is created in the database with status 'Pending']
2. [e.g., User's cart is emptied]

---

## Main Success Scenario (Happy Path)

| Step | Action |
|------|--------|
| 1 | Actor navigates to the Checkout page. |
| 2 | System displays the order summary and requests payment details. |
| 3 | Actor enters payment details and clicks 'Submit Order'. |
| 4 | System validates payment details format. |
| 5 | System sends payment authorization request to Payment Gateway. |
| 6 | Payment Gateway authorizes the payment and returns a success token. |
| 7 | System saves the order and empties the cart. |
| 8 | System displays the Order Confirmation page. |

---

## Extensions (Alternate Flows)

*What happens when things go wrong or the user takes a different path?*

**4a. Payment details format is invalid:**
1. System displays an inline error message next to the invalid fields.
2. Return to Step 3.

**6a. Payment Gateway declines the authorization (insufficient funds):**
1. System logs the declined attempt.
2. System displays an error message: "Payment declined. Please try another card."
3. Return to Step 3.

**6b. Payment Gateway times out or is unreachable:**
1. System displays an error message: "Unable to process payment at this time. Please try again later."
2. System retains items in the user's cart.
3. Use case aborts.

---

## Business Rules
- [e.g., BR-01: Orders over $10,000 require manual review before fulfillment.]
- [e.g., BR-02: Discount codes cannot be applied to sale items.]

## Non-Functional Requirements (Specific to this Use Case)
- [e.g., Payment authorization step must complete within 3 seconds or time out.]
```
