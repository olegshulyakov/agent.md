# Component Libraries

Use this reference when the project styles UI through component libraries or headless primitives, including MUI, Chakra UI, Mantine, Ant Design, Radix UI, shadcn/ui, Headless UI, React Aria, or local design-system component APIs.

Start with the project's existing components, theme provider, tokens, variants, and composition patterns. Prefer extending or configuring library components over replacing them with custom markup. Keep imports, slot APIs, polymorphic `as` props, variant systems, and styling props consistent with nearby code.

Preserve accessibility behavior supplied by headless or full component libraries. Do not break focus traps, roving tabindex, aria relationships, portal behavior, escape handling, or scroll locking when customizing dialogs, menus, comboboxes, popovers, tabs, and tooltips.

Keep visual overrides narrow. Use theme overrides, component variants, recipe APIs, or wrapper components when changes repeat. Use one-off style props only for local layout constraints. Avoid mixing multiple component libraries in the same surface unless the repository already does.
