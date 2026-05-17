# PRD Output Format

Use this reference when drafting the final PRD.

## Template

Always produce a Markdown file. Use this structure exactly:

```md
# PRD: [Product / Feature Name]

## Status

[Draft | In Review | Approved] — [Date]
**Author:** [if known, else omit]
**Stakeholders:** [list if mentioned, else omit]

## Problem Statement

[1–3 paragraphs. What pain exists? Who feels it? What's the cost of inaction?]

## Goals [optional]

- ...

## Target Users / Personas

[For each persona: role, context, key jobs-to-be-done, frustrations]

## Scope

### In Scope

- [Concrete capability or deliverable]

### Out of Scope [optional]

- [Explicit exclusions to prevent scope creep]

## Functional Requirements

[Numbered list of WHAT the system must do. Use "The system shall..." or "Users can..." phrasing. Group by user journey or capability area.]

1. **[Capability Area]**
   1.1 ...
   1.2 ...

## Non-Functional Requirements (summary)

[Performance, availability, security, compliance highlights. If deep NFRs are needed, recommend writer-spec-nfr.]

## User Journeys / Key Flows [optional]

[1–3 critical flows described as numbered steps. Diagrams optional but welcome.]

## Assumptions & Dependencies [optional]

| Item | Type                    | Detail |
| ---- | ----------------------- | ------ |
| ...  | Assumption / Dependency | ...    |

## Open Questions [optional]

- [ ] [Question that must be resolved before implementation]

## Appendix [optional]

[Glossary, related docs, links — only if needed]
```
