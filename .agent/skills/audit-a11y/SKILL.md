---
name: audit-a11y
description: >
  Produces an accessibility audit report with annotated findings and fix recommendations against WCAG 2.1/2.2 standards.
  Use this skill whenever the user wants to audit a UI for accessibility, check WCAG compliance, find accessibility
  violations, review a component or page for a11y issues, or asks to "make this accessible", "run an accessibility
  check", "find WCAG violations", "audit this for screen reader support", or "check color contrast". Also trigger
  when the user mentions ARIA attributes, keyboard navigation, focus management, or accessible forms.
  Distinct from codegen-frontend (which generates code) and writer-spec-design (which writes design specs).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# audit-a11y

Produce a **structured accessibility audit report** for the provided UI, component, page, or codebase.

## What makes a great a11y audit

The best audits are actionable — each finding maps directly to a specific WCAG criterion, a severity level, and a concrete fix. Don't just list violations; explain why they matter (screen reader impact, keyboard trap, legal risk) and provide corrected code where possible.

## Information gathering

Before auditing, identify from context:

- **Scope**: Is this a single component, a page, an entire app?
- **Standard**: WCAG 2.1 AA (default) or 2.2 / AAA if specified
- **Platform**: Web (HTML/CSS/JS), React/Vue/Angular component, native mobile
- **Input**: Markup/code provided directly, or a URL/description of the UI

If code or markup is provided, analyze it directly. If only a description is given, audit the described patterns and flag what can't be verified without seeing the code.

## Output format

Always produce a Markdown document using this structure:

```
# Accessibility Audit: [Component / Page / Scope]

## Summary
**Standard:** WCAG [version] [level]
**Date:** [date]
**Total findings:** [N] ([critical] critical, [serious] serious, [moderate] moderate, [minor] minor)

## Findings

### [FINDING-001] [Short title]
- **WCAG criterion:** [e.g., 1.4.3 Contrast (Minimum)]
- **Severity:** Critical / Serious / Moderate / Minor
- **Impact:** [Who is affected and how — e.g., "Screen reader users will not hear the button label"]
- **Location:** [Element, component, line number if available]
- **Current code:**
  ```html
  <!-- failing snippet -->
  ```
- **Fix:**
  ```html
  <!-- corrected snippet -->
  ```
- **Reference:** [WCAG link or explanation]

[Repeat for each finding]

## Passed Checks
- [List of criteria that were explicitly verified and passed]

## Cannot Verify (needs manual or automated testing)
- [Items that require browser testing, screen reader, or user testing]

## Recommendations
[Prioritized fix list: what to tackle first, tooling suggestions, process recommendations]
```

## Severity definitions

| Severity | Meaning |
|----------|---------|
| **Critical** | Blocks access entirely for some users (e.g., keyboard trap, missing alt on form control) |
| **Serious** | Significantly degrades the experience (e.g., insufficient contrast on body text) |
| **Moderate** | Causes confusion but has a workaround (e.g., missing landmark roles) |
| **Minor** | Best-practice deviation with minimal user impact |

## Key WCAG criteria to always check

**Perceivable**
- 1.1.1 Non-text content (alt text for images)
- 1.3.1 Info and relationships (semantic HTML, ARIA roles)
- 1.3.5 Identify input purpose (autocomplete attributes)
- 1.4.1 Use of color (not the only visual means of conveying info)
- 1.4.3 Contrast Minimum (4.5:1 normal text, 3:1 large text)
- 1.4.11 Non-text contrast (UI components: 3:1)

**Operable**
- 2.1.1 Keyboard (all functionality operable via keyboard)
- 2.1.2 No keyboard trap
- 2.4.3 Focus order (logical tab sequence)
- 2.4.7 Focus visible
- 2.5.3 Label in name (visible label in accessible name)

**Understandable**
- 3.1.1 Language of page
- 3.2.2 On input (no unexpected context changes)
- 3.3.1 Error identification (descriptive error messages)
- 3.3.2 Labels or instructions

**Robust**
- 4.1.2 Name, role, value (correct ARIA usage)
- 4.1.3 Status messages

## Common patterns and fixes

**Missing alt text:**
```html
<!-- bad -->
<img src="chart.png">
<!-- good -->
<img src="chart.png" alt="Bar chart showing Q4 revenue by region">
```

**Inaccessible custom button:**
```html
<!-- bad -->
<div onclick="submit()">Submit</div>
<!-- good -->
<button type="submit">Submit</button>
```

**Missing form label:**
```html
<!-- bad -->
<input type="email" placeholder="Email">
<!-- good -->
<label for="email">Email address</label>
<input type="email" id="email" autocomplete="email">
```

**Missing focus indicator:**
```css
/* bad */
*:focus { outline: none; }
/* good */
*:focus-visible { outline: 2px solid #005fcc; outline-offset: 2px; }
```

## Calibration by input type

- **Markup/code**: Audit directly; provide corrected snippets for every finding
- **Description only**: Audit the described patterns; flag what requires visual or interactive verification
- **Screenshot/design**: Focus on color contrast, label visibility, and layout structure; note limits of static analysis
- **Framework component**: Note whether findings are in JSX, template syntax, or generated HTML
