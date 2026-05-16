# Accessibility

Use this reference when implementing or fixing semantics, keyboard interaction, focus, labels, ARIA, color contrast, screen reader output, reduced motion, or WCAG-related behavior.

Start with semantic HTML and native controls. Add ARIA only when semantics cannot express the interaction. Every input needs an accessible name, every icon-only control needs a label, and every validation error needs a programmatic relationship to the field it describes.

Custom interactive elements must support keyboard operation, visible focus, disabled state, and expected roles/states. Manage focus for modals, drawers, menus, route transitions, and error summaries. Announce asynchronous status changes with existing live-region patterns when needed.

Check color contrast, target size, motion preferences, text zoom, and responsive reading order. Do not solve accessibility by hiding useful content from one audience to satisfy another.
