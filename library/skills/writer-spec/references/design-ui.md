# Design Specification: [Component / Feature Name]

**Status:** [Draft / Final / Ready for Dev]
**Designer:** [name]
**Figma Link:** [url]

---

## 1. Overview & Purpose

[Brief description of what this UI element does and when it should be used.]

---

## 2. Visual Attributes & Tokens

| Element    | Property   | Token / Value                   | Notes         |
| ---------- | ---------- | ------------------------------- | ------------- |
| Background | Color      | `var(--color-surface-elevated)` |               |
| Border     | Radius     | `var(--radius-md)` (8px)        |               |
| Container  | Padding    | `var(--space-4)` (16px)         |               |
| Shadow     | Box Shadow | `var(--shadow-sm)`              | Only on hover |

---

## 3. States

- **Default:** [Description of the standard state]
- **Hover:** [e.g., "Cursor → pointer. Background → `--color-surface-hover`. Shadow → `--shadow-md`."]
- **Active / Pressed:** [e.g., "Scale: 0.98. Shadow → `--shadow-sm`."]
- **Focus:** [e.g., "2px solid `--color-focus-ring` with 2px offset."]
- **Disabled:** [e.g., "Opacity: 50%. Cursor → `not-allowed`. Hover effects disabled."]
- **Loading:** [e.g., "Text hidden; spinner centered. Component maintains resting dimensions."]
- **Error:** [e.g., "Border → `--color-error`. Error icon appears on right."]

---

## 4. Interaction & Motion

**Trigger:** [e.g., "Clicking 'Submit'"]
**Action:** [e.g., "Transitions to Loading state immediately."]
**Animation:**

- Property: [e.g., `background-color`, `transform`]
- Duration: [e.g., 200ms]
- Easing: [e.g., `ease-in-out`]

---

## 5. Responsive Behavior

| Breakpoint              | Behavior                                    |
| ----------------------- | ------------------------------------------- |
| **Mobile** (< 768px)    | Elements stack. Width: 100%. Padding: 12px. |
| **Tablet** (768–1024px) | Side-by-side. Width: 50%.                   |
| **Desktop** (> 1024px)  | Max width: 400px.                           |

---

## 6. Edge Cases & Content Scaling

- **Long text:** [e.g., "Truncate with ellipsis on a single line."]
- **Missing data:** [e.g., "Avatar fails → colored circle with initials."]
- **Localization:** [e.g., "Don't set fixed widths — German strings can be 50% longer."]
