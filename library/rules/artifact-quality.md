---
name: artifact-quality
description: Apply KISS, STAR, and SOLID as quality lenses when producing examples, skills, docs, and code.
applies_to: ["**/*"]
priority: medium
---

# Artifact Quality Rules

- Keep examples narrow, direct, and complete. Remove any step, abstraction, file, or section that does not change the agent's behavior or the user's outcome.
- Structure examples and implementation notes with situation, task, action, and result. Omit sections where the context is self-evident.
- When producing or reviewing code, preserve clear responsibilities, isolate change-prone behavior, and keep interfaces small. Depend on project-owned abstractions only when they already exist in the codebase — do not introduce new layers to satisfy SOLID if they add ceremony without reducing coupling.
- Do not force all three lenses onto every artifact. Apply whichever improves the artifact at hand. Prefer plain guidance over naming the acronym.
- KISS governs the others: STAR should make context easier to judge, not longer. SOLID should prevent brittle code, not create it.
