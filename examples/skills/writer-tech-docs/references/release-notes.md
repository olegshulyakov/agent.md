# writer-tech-docs — release-notes variant

Produce **user-facing release notes** that communicate new features, improvements, fixes, and upgrade guidance.

## What makes great release notes

User-facing release notes are marketing and communication, not just documentation. Write for someone who doesn't know what you changed — they know what they do with the product, not how you built it.

**Key differences from developer changelog:**

- No internal jargon (no PR numbers, commit hashes, class names)
- Focus on benefit to user, not technical implementation
- Tone matches the product (playful app vs. enterprise software)
- Include visuals/screenshots where possible
- Highlight top 3 features prominently

## Information gathering

- **Version / date**: v2.1.0? "Spring 2024"? "This week's update"?
- **Changes**: What was shipped? (technical changelog, PR list, or description)
- **Product type**: Mobile app, SaaS, CLI, library, OS?
- **Audience**: End users, developers, enterprise IT admins?
- **Tone**: Professional, friendly, playful, neutral?

## Output format

````markdown
# Release Notes: [Product Name] [Version] — [Date]

---

## What's New 🎉

### [Feature 1 Headline — make it compelling]

[2–3 sentences describing what the feature does and why users will love it. "You can now..." or "We've made it easier to..."]

### [Feature 2 Headline]

[Description focusing on user benefit]

---

## Improvements ✨

- **[Improvement area]**: [What changed and why it matters — e.g., "Dashboard loads 3× faster on mobile"]

---

## Bug Fixes 🐛

- Fixed an issue where [user-visible symptom]
- Fixed [symptom — e.g., "the export button sometimes showed a blank file"]

---

## Known Issues ⚠️

_We're aware of the following and working on a fix:_

- [Issue and workaround if available]

---

## Breaking Changes / Action Required

_[Include only if users need to take action]_

- **[Change affecting users]**: [What they need to do]

---

## Upgrade Guide

_For [enterprise users / self-hosted customers / developers]:_

```bash
npm update [package]@[version]
```

---

## What's Coming Next 🚀

_[Optional: teaser of upcoming features]_

- [Upcoming feature — e.g., "AI-powered writing suggestions — coming next month"]

---

## Thank You

[Optional: acknowledge community, beta testers, or customer feedback]

---

_[Version: X.X.X | Released: Date | Platform: iOS/Android/Web/All]_
````

## Tone guide

| Product type           | Tone                            | Opening style                                                        |
| ---------------------- | ------------------------------- | -------------------------------------------------------------------- |
| Consumer mobile app    | Friendly, emoji, "you" language | "We've been busy! Here's what's new..."                              |
| SaaS productivity tool | Professional but warm           | "This release focuses on speed and reliability..."                   |
| Developer tool / CLI   | Technical-friendly, concise     | "v2.1.0 includes three new commands and performance improvements..." |
| Enterprise software    | Formal, precise                 | "Version 4.2 introduces the following capabilities..."               |

## Transforming technical changes

| Technical description                                    | User-facing version                                         |
| -------------------------------------------------------- | ----------------------------------------------------------- |
| "Reduced API latency by 40% via connection pooling"      | "Pages load up to 40% faster"                               |
| "Fixed NPE in OrderService when order contains no items" | "Fixed a crash that occurred when submitting an empty cart" |
| "Added index to user_email column"                       | "Search is now 10× faster when looking up users by email"   |

## App Store format

```markdown
What's New in Version [X.X]:

🚀 [Feature 1]: [1-sentence description]
⚡ [Feature 2]: [1-sentence description]
🐛 Bug fixes and performance improvements

Thank you for your feedback! Rate us ⭐⭐⭐⭐⭐ if you love the app.
```

## Calibration

- **SaaS product update**: Full format, professional tone, include screenshots placeholder
- **Mobile app (App Store)**: Short, emoji-friendly, focus on top 2–3 changes
- **Enterprise software**: Formal tone, detailed breaking changes, version number prominent
- **From changelog**: Convert technical entries to user-facing language using the transformation table
- **Minor/patch release**: Just Improvements + Bug Fixes sections; no headline features
