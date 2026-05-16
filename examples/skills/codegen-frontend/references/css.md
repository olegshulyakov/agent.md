# CSS And Design Systems

Use this reference for vanilla CSS, CSS modules, Sass, design tokens, layout, responsive behavior, and component styling.

Start from existing tokens, variables, utility classes, and component primitives. Add new tokens only when a value represents a reusable semantic decision, not a one-off measurement. Keep colors, spacing, typography, borders, and shadows consistent with nearby UI.

Use stable layout primitives: grid or flex tracks, `minmax`, `clamp` for containers rather than viewport-scaled type, `aspect-ratio`, and explicit min/max sizes for controls and media. Make wrapping and overflow behavior deliberate. Interactive controls need visible focus, disabled, hover, active, and loading states when relevant.

Avoid fragile selectors that depend on incidental DOM depth. Prefer component-scoped classes, CSS modules, or the local convention. Test at mobile and desktop widths when visual changes are substantial.
