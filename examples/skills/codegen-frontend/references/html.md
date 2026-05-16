# HTML

Use this reference for plain HTML, server-rendered templates, static pages, Web Components markup, semantic document structure, metadata, tables, forms, media, and progressive enhancement surfaces.

Start with meaningful document structure: landmarks, headings in order, lists for lists, buttons for actions, links for navigation, tables for tabular data, and form controls with labels. Keep markup readable and durable before adding framework behavior or styling hooks.

Use metadata deliberately: title, description, viewport, canonical links, social metadata, preload or preconnect hints only when justified, and structured data when the project already uses it. Include `lang`, direction, image dimensions, lazy loading, captions, and alternative text where relevant.

For templates, follow the server framework's escaping, partial, layout, and component conventions. Do not interpolate untrusted content without the framework's safe escaping path. Keep progressive enhancement intact: core content and form flows should remain understandable before JavaScript loads when the product surface supports it.

For Web Components or custom elements, preserve native semantics where possible, expose accessible names and states, and avoid hiding essential content in shadow DOM without a plan for labels, focus, and forms.
