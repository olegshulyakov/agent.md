---
name: quality-principles
description: Apply KISS, STAR, and SOLID as practical quality lenses for examples, skills, docs, and generated code.
applies_to: ["**/*"]
priority: medium
---

# Quality Principles Rules

- Use KISS to keep examples narrow, direct, and complete. Remove workflow steps, abstractions, files, and sections that do not change the agent's behavior or the user's outcome.
- Use STAR for examples, eval prompts, case studies, incident summaries, and implementation notes: state the situation, the task, the action taken, and the result or expected result.
- Use SOLID when producing or reviewing code-oriented examples. Preserve clear responsibilities, isolate change-prone behavior, keep interfaces small, and depend on project-owned abstractions only when they already exist or clearly reduce coupling.
- Do not force every acronym into every example. Apply the principle that improves the artifact at hand, and prefer plain language over naming the acronym when the guidance is obvious.
- Let KISS govern the other principles: STAR should make context easier to judge, and SOLID should prevent brittle code, not create ceremony.
