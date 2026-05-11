---
name: design-css
description: >
  Produces a design system with CSS custom properties (tokens), component style guide, spacing scale,
  typography system, and color palette. Use this skill whenever the user wants to create a design system,
  define CSS variables, establish a visual design language, set up a component style guide, create design
  tokens, define a color palette or typography scale, or asks to "set up design tokens", "create a CSS
  design system", "define our spacing and typography", "establish a visual style guide", "generate CSS
  custom properties", "build a component library foundation", "create a design language", or "what CSS
  variables should I define?". Also trigger for "brand tokens", "style guide", "theming setup", and
  "dark mode implementation". Distinct from codegen-frontend (which generates component code) and
  writer-spec-design (which documents design specs for a specific component or screen).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# design-css

Produce a **CSS design system** with design tokens, typography, color palette, spacing scale, and component patterns.

## What makes a great design system

A design system is most valuable when it's opinionated enough to ensure consistency but flexible enough for real-world variation. Use CSS custom properties (variables) as the single source of truth — everything else derives from them. Document the "why" behind choices so future developers can extend rather than override.

## Information gathering

From context, identify:
- **Brand**: Existing colors, fonts, brand guidelines?
- **Product type**: Marketing site, app dashboard, mobile-first, document-heavy?
- **Dark mode**: Required? System-preference or toggle?
- **Framework**: Vanilla CSS, CSS Modules, Sass?
- **Existing constraints**: Must use specific font, must match existing components?

## Output structure

Generate a `tokens.css` file with all custom properties, plus optional `typography.css`, `components.css`, and a brief usage guide. Adjust scope based on what the user asks for.

### `tokens.css` — Core Design Tokens

```css
:root {
  /* ── Color palette ── */
  --color-neutral-0:   #ffffff;
  --color-neutral-50:  #f9fafb;
  --color-neutral-100: #f3f4f6;
  --color-neutral-200: #e5e7eb;
  --color-neutral-400: #9ca3af;
  --color-neutral-500: #6b7280;
  --color-neutral-600: #4b5563;
  --color-neutral-700: #374151;
  --color-neutral-800: #1f2937;
  --color-neutral-900: #111827;
  --color-neutral-950: #030712;

  --color-primary-50:  #eff6ff;
  --color-primary-500: #3b82f6;
  --color-primary-600: #2563eb;
  --color-primary-700: #1d4ed8;

  --color-success-500: #22c55e;
  --color-warning-500: #f59e0b;
  --color-error-500:   #ef4444;

  /* ── Semantic aliases (use these in components) ── */
  --color-bg-primary:    var(--color-neutral-0);
  --color-bg-secondary:  var(--color-neutral-50);
  --color-bg-tertiary:   var(--color-neutral-100);

  --color-text-primary:   var(--color-neutral-900);
  --color-text-secondary: var(--color-neutral-600);
  --color-text-disabled:  var(--color-neutral-400);
  --color-text-inverse:   var(--color-neutral-0);

  --color-border-default: var(--color-neutral-200);
  --color-border-strong:  var(--color-neutral-400);

  --color-interactive:       var(--color-primary-600);
  --color-interactive-hover: var(--color-primary-700);

  /* ── Typography ── */
  --font-family-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-family-mono: 'JetBrains Mono', 'Fira Code', monospace;

  --font-size-xs:   0.75rem;   /* 12px */
  --font-size-sm:   0.875rem;  /* 14px */
  --font-size-base: 1rem;      /* 16px */
  --font-size-lg:   1.125rem;  /* 18px */
  --font-size-xl:   1.25rem;   /* 20px */
  --font-size-2xl:  1.5rem;    /* 24px */
  --font-size-3xl:  1.875rem;  /* 30px */
  --font-size-4xl:  2.25rem;   /* 36px */

  --font-weight-regular:  400;
  --font-weight-medium:   500;
  --font-weight-semibold: 600;
  --font-weight-bold:     700;

  --line-height-tight:  1.25;
  --line-height-normal: 1.5;
  --line-height-loose:  1.75;

  /* ── Spacing (4px base) ── */
  --space-1:  0.25rem;  /* 4px */
  --space-2:  0.5rem;   /* 8px */
  --space-3:  0.75rem;  /* 12px */
  --space-4:  1rem;     /* 16px */
  --space-5:  1.25rem;  /* 20px */
  --space-6:  1.5rem;   /* 24px */
  --space-8:  2rem;     /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */

  /* ── Border radius ── */
  --radius-sm:   0.25rem;   /* 4px */
  --radius-md:   0.375rem;  /* 6px */
  --radius-lg:   0.5rem;    /* 8px */
  --radius-xl:   0.75rem;   /* 12px */
  --radius-full: 9999px;

  /* ── Shadow ── */
  --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);

  /* ── Animation ── */
  --duration-fast:   100ms;
  --duration-normal: 200ms;
  --duration-slow:   300ms;
  --easing-default:  cubic-bezier(0.4, 0, 0.2, 1);

  /* ── Z-index ── */
  --z-base:     0;
  --z-raised:   10;
  --z-dropdown: 100;
  --z-sticky:   200;
  --z-modal:    400;
  --z-toast:    500;
}
```

### Dark Mode

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg-primary:    var(--color-neutral-950);
    --color-bg-secondary:  var(--color-neutral-900);
    --color-bg-tertiary:   var(--color-neutral-800);
    --color-text-primary:   var(--color-neutral-50);
    --color-text-secondary: var(--color-neutral-400);
    --color-border-default: var(--color-neutral-700);
  }
}
/* Manual toggle: .dark class on <html> */
```

### Component Patterns (`components.css`)

```css
/* Button */
.btn {
  display: inline-flex; align-items: center; gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm); font-weight: var(--font-weight-medium);
  cursor: pointer; border: 1px solid transparent;
  transition: all var(--duration-normal) var(--easing-default);
}
.btn-primary { background: var(--color-interactive); color: var(--color-text-inverse); }
.btn-primary:hover { background: var(--color-interactive-hover); }

/* Input */
.input {
  width: 100%; padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-border-default); border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  background: var(--color-bg-primary); color: var(--color-text-primary);
}
.input:focus { outline: none; border-color: var(--color-interactive); }

/* Card */
.card {
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-xl); padding: var(--space-6); box-shadow: var(--shadow-sm);
}
```

## Usage Rules

Always include these rules in output:
- **Never use raw palette values in components** — always use semantic aliases
- **Spacing**: Use `var(--space-N)` tokens, never raw `px` values in layout
- **Dark mode**: Override semantic aliases only, not raw palette colors

## Calibration

- **Brand-specific**: Generate palette from provided brand colors using tints/shades
- **Minimal request**: Just tokens + typography, no component patterns
- **Tailwind extension**: Provide the `theme.extend` config to map tokens to Tailwind
- **Specific component**: CSS for that component using the token system
- **Sass/Less**: Output in the appropriate variable syntax
