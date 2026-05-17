# Tailwind CSS

Use this reference when the project uses Tailwind utilities, `tailwind.config.*`, `@tailwind`, shadcn/ui, Headless UI, Radix with Tailwind, or utility-first styling.

Reuse configured tokens and semantic component variants. Prefer existing `cn`, `cva`, `tailwind-merge`, or variant helpers when present. Keep class lists readable by grouping layout, spacing, typography, color, state, and responsive utilities in a consistent order.

Do not hard-code arbitrary values unless they encode a truly local constraint. Put repeated visual decisions into component variants or design tokens. Use responsive and state variants deliberately, including `focus-visible`, `disabled`, `aria-*`, `data-*`, `motion-reduce`, and dark-mode variants if the project supports them.
