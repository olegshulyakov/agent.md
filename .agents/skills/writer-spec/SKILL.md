---
name: writer-spec
description: >
  Use this skill whenever the user wants to write a spec, document system behavior, define requirements, or design a contract.
  Triggers include:
    - "write a spec",
    - "write a tech spec",
    - "write a design doc",
    - "write a TDD",
    - "functional requirements",
    - "non-functional requirements",
    - "NFR document",
    - "data contract",
    - "UI spec",
    - "handoff doc",
  "system requirements", "design specification", "what should the system do", "document this feature".
author: Oleg Shulyakov
licence: MIT
version: 1.2.0
---

# writer-spec

A **router** skill to generate specific document types. Identify user intent, select the matching spec type, and produce the document using its reference format. For ambiguous or multi-type requests, combine sections and note the merged types.

## Routing Table

| Request Type                                       | Reference                      |
| :------------------------------------------------- | :----------------------------- |
| Tech spec, design doc, TDD, end-to-end spec        | `references/technical.md`      |
| Functional requirements, use cases, business rules | `references/functional.md`     |
| Non-functional requirements, SLAs, performance     | `references/non-functional.md` |
| Data contract, event schema, data SLA              | `references/data-contract.md`  |
| UI/UX spec, design handoff, component states       | `references/design-ui.md`      |

## Writing Rules (All Specs)

- **Be specific & testable**: Requirements must translate directly to test cases (e.g., "Token expires after 15m").
- **Behavioral, not implementational**: Describe what it does, not how it's built.
- **Mandatory Error Paths**: Requirements lacking error conditions are incomplete.
- **Document Omissions**: Explicitly state what is out of scope.
- **Mark Inferences**: Flag assumed details with `[assumed]`.
