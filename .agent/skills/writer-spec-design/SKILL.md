---
name: writer-spec-design
description: >
  Produces a UI/UX design specification with component states, interaction patterns, design tokens,
  and responsive breakpoints. Use this skill whenever the user wants to document a UI design, write
  a handoff spec for developers, define component behaviors, or asks to "write a design spec",
  "document this UI component", "create a handoff document", "define the states for this button",
  or "write the UX spec for this feature". Distinct from design-css (which generates the actual CSS
  code) and codegen-frontend (which generates React/Vue code).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# writer-spec-design

Produce a **UI/UX Design Specification** (Developer Handoff Spec) detailing states, interactions, and tokens.

## Output format

```markdown
# Design Specification: [Component / Feature Name]

**Status:** [Draft / Final / Ready for Dev]
**Designer:** [name]
**Figma Link:** [url]

---

## 1. Overview & Purpose

[Brief description of what this UI element does and when it should be used.]

---

## 2. Visual Attributes & Tokens

| Element | Property | Token / Value | Notes |
|---------|----------|---------------|-------|
| Background | Color | `var(--color-surface-elevated)` | White in light mode, dark gray in dark mode |
| Text (Primary) | Color | `var(--text-primary)` | |
| Text (Secondary)| Color | `var(--text-secondary)` | Used for timestamps and metadata |
| Border | Radius | `var(--radius-md)` (8px) | |
| Container | Padding | `var(--space-4)` (16px) | |
| Shadow | Box Shadow | `var(--shadow-sm)` | Only applied on hover |

---

## 3. States

Describe how the component looks in different states:

- **Default (Resting):** [Description of the standard state]
- **Hover:** [e.g., "Cursor changes to pointer. Background shifts to `--color-surface-hover`. Shadow increases to `--shadow-md`."]
- **Active / Pressed:** [e.g., "Scale transforms to 0.98. Shadow reduces to `--shadow-sm`."]
- **Focus (Keyboard navigation):** [e.g., "Standard browser outline is replaced with a 2px solid `--color-focus-ring` with a 2px offset."]
- **Disabled:** [e.g., "Opacity reduced to 50%. Cursor changes to `not-allowed`. Hover effects are disabled."]
- **Loading:** [e.g., "Text is hidden; a spinner appears centered. Component maintains its resting width/height."]
- **Error:** [e.g., "Border turns `--color-error`. An error icon appears on the right."]

---

## 4. Interaction & Motion

**Trigger:** [e.g., "Clicking the 'Submit' button"]
**Action:** [e.g., "Transitions to Loading state immediately."]
**Animation:**
- **Property:** [e.g., `background-color`, `transform`]
- **Duration:** [e.g., 200ms]
- **Easing:** [e.g., `ease-in-out` or `cubic-bezier(0.4, 0, 0.2, 1)`]

---

## 5. Responsive Behavior

| Breakpoint | Behavior / Layout Change |
|------------|--------------------------|
| **Mobile** (< 768px) | Elements stack vertically. Width is 100%. Padding reduces to 12px. |
| **Tablet** (768px - 1024px) | Elements sit side-by-side. Width is 50%. |
| **Desktop** (> 1024px) | Maximum width constrained to 400px. |

---

## 6. Edge Cases & Content Scaling

- **Long text:** [e.g., "If the user's name is too long, truncate with an ellipsis (`text-overflow: ellipsis`) on a single line."]
- **Missing data:** [e.g., "If the avatar image fails to load or is missing, fall back to a colored circle with the user's initials."]
- **Localization:** [e.g., "Button must accommodate German translations (which may be up to 50% longer). Do not set fixed widths on the button."]
```
