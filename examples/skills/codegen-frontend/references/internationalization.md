# Internationalization

Use this reference for locale routing, translation keys, ICU messages, date/number/currency formatting, pluralization, timezone display, RTL layout, and language switchers.

Reuse the project's i18n library and message organization. Do not concatenate translated strings from fragments when grammar can vary by locale. Use ICU plural/select messages or the local equivalent for counts and gendered or conditional text.

Format dates, times, numbers, currencies, and lists with locale-aware utilities. Keep storage formats stable and presentation localized. For RTL, prefer logical CSS properties and test layout direction rather than adding one-off overrides after the fact.
