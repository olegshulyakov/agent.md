---
name: diagram-dfd
description: >
  Produces a data flow diagram (DFD) in Mermaid or structured text format, from context level (L0)
  through process detail (L2). Use this skill whenever the user wants to create a data flow diagram,
  show how data moves through a system, document data sources and sinks, model processes and data stores,
  or asks to "draw a DFD", "create a data flow diagram", "show how data flows through the system",
  "model the data flows for this feature", "create a context diagram showing data flows", or
  "document our data processing pipeline as a DFD". Also trigger for "level 0 diagram", "level 1 DFD",
  "show inputs and outputs of the system", and "data flow model". Distinct from diagram-c4 (which models
  software architecture at system/container/component levels) and diagram-integration (which shows
  system integrations and API boundaries).
---

# diagram-dfd

Produce a **data flow diagram (DFD)** that shows how data moves through a system across context, process, and detail levels.

## DFD Levels

| Level | Scope | Shows |
|-------|-------|-------|
| **L0 — Context** | Entire system as a single process | External entities (actors), system boundary, major data flows in/out |
| **L1 — System** | Top-level decomposition | Main processes (3–7), data stores, flows between them and external entities |
| **L2 — Process** | One process from L1 expanded | Sub-processes, detailed data stores, specific data elements |

Generate the level(s) the user requests. If unclear, generate L0 and L1.

## DFD Notation

| Element | Symbol | Description |
|---------|--------|-------------|
| **Process** | Circle / rounded box | Transforms data (verb phrase: "Validate Payment") |
| **External Entity** | Rectangle | Actors outside the system boundary (users, systems) |
| **Data Store** | Open-ended rectangle (D1 label) | Persisted data (databases, files, queues) |
| **Data Flow** | Labeled arrow | Data moving between elements (noun phrase: "Order Details") |

Rules:
- Data flows connect processes to entities, stores, or other processes — **never entity-to-entity or store-to-store directly**
- Every process must have at least one input and one output flow
- Label all flows with the data they carry
- Use verb phrases for processes, noun phrases for flows

## Information gathering

From context, identify:
- **System scope**: What system or feature is being modeled?
- **External entities**: Who/what interacts with the system from outside?
- **Key processes**: What are the main data transformation steps?
- **Data stores**: What data is persisted and where?
- **Target level**: L0, L1, L2, or all?

## Output format

Use Mermaid flowchart syntax (renders in GitHub, Notion, most markdown viewers).

### L0 — Context Diagram

```mermaid
flowchart TD
    %% External entities
    customer([Customer])
    payment_gateway([Payment Gateway])
    email_service([Email Service])

    %% System boundary (single process)
    system["Order Management System"]

    %% Data flows
    customer -->|"Order Request"| system
    system -->|"Order Confirmation"| customer
    system -->|"Payment Request"| payment_gateway
    payment_gateway -->|"Payment Result"| system
    system -->|"Confirmation Email"| email_service
```

### L1 — System Diagram

```mermaid
flowchart TD
    %% External entities
    customer([Customer])
    payment_gw([Payment Gateway])

    %% Processes
    P1["1.0 Validate Order"]
    P2["2.0 Process Payment"]
    P3["3.0 Fulfill Order"]
    P4["4.0 Notify Customer"]

    %% Data stores
    D1[("D1: Orders DB")]
    D2[("D2: Product Catalog")]
    D3[("D3: Inventory DB")]

    %% Flows
    customer -->|"Order Request"| P1
    P1 -->|"Order Details"| D2
    D2 -->|"Product Info"| P1
    P1 -->|"Validated Order"| D1
    P1 -->|"Payment Data"| P2
    P2 <-->|"Payment Request / Result"| payment_gw
    P2 -->|"Payment Status"| D1
    P2 -->|"Approved Order"| P3
    P3 -->|"Stock Query"| D3
    D3 -->|"Available Items"| P3
    P3 -->|"Fulfillment Status"| D1
    P3 -->|"Order Status"| P4
    P4 -->|"Notification"| customer
```

### L2 — Process Detail

Show one process from L1 decomposed:

```mermaid
flowchart TD
    %% External entities at this level
    customer([Customer])
    inventory_svc([Inventory Service])

    %% Sub-processes of "2.0 Validate Order"
    P2_1["2.1 Check Product Availability"]
    P2_2["2.2 Validate Business Rules"]
    P2_3["2.3 Calculate Pricing"]

    %% Data stores
    D_products[("D2: Product Catalog")]
    D_pricing[("D4: Pricing Rules")]

    %% Flows
    customer -->|"Raw Order"| P2_1
    P2_1 -->|"SKU List"| D_products
    D_products -->|"Product Data"| P2_1
    P2_1 <-->|"Stock Query / Availability"| inventory_svc
    P2_1 -->|"Available Items"| P2_2
    P2_2 -->|"Validated Items"| P2_3
    P2_3 -->|"Rule Lookup"| D_pricing
    D_pricing -->|"Pricing Rules"| P2_3
    P2_3 -->|"Priced Order"| customer
```

## Alternative: Structured Text Format

When Mermaid isn't suitable, produce a structured text DFD:

```
[L0 Context Diagram: Order Management System]

External Entities:
  - Customer (actor)
  - Payment Gateway (external system)
  - Email Service (external system)

System Boundary: Order Management System

Data Flows:
  Customer → [System]: Order Request {product_id, quantity, payment_details}
  [System] → Customer: Order Confirmation {order_id, status, estimated_delivery}
  [System] → Payment Gateway: Payment Request {amount, card_token, order_id}
  Payment Gateway → [System]: Payment Result {success, transaction_id, error_code?}
```

## Quality checklist

Before finalizing, verify:
- [ ] Every process has ≥1 input and ≥1 output flow
- [ ] No direct entity-to-entity or store-to-store flows
- [ ] All flows are labeled with data names (nouns)
- [ ] All processes are labeled with actions (verbs)
- [ ] Data stores use D1, D2 etc. identifiers consistently across levels
- [ ] L1 processes are numbered (1.0, 2.0...) so they trace to L2

## Calibration

- **L0 only**: Simple, 1 page — good for executive overview or kickoff documentation
- **L1 only**: Most common request — shows main processes without getting into detail
- **L1 + L2 for one process**: When a specific subprocess needs deep analysis
- **Full L0+L1+L2**: Comprehensive system documentation; produce as separate diagrams
