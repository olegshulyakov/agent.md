---
name: writer-release-notes
description: >
  Produces user-facing release notes with what's new, what's fixed, known issues, and upgrade
  guidance. Use this skill whenever the user wants to write release notes for end users, create
  user-facing documentation about a new version, or asks to "write release notes", "create user-facing
  release notes", "document what's new in version X", "write the announcement for this release",
  "draft the App Store release notes", "create release notes for our SaaS product", "what changed
  for users in this release", or "write the 'what's new' section". Also trigger for "version
  announcement", "product update notes", "feature announcement", and "upgrade notes". Distinct from
  writer-changelog (which is developer-facing technical changelog) and writer-api-docs (which
  documents APIs for developers).
---

# writer-release-notes

Produce **user-facing release notes** that communicate new features, improvements, fixes, and upgrade guidance.

## What makes great release notes

User-facing release notes are marketing and communication, not just documentation. They should make users excited about what's new, clear about what changed, and confident about upgrading. Write for someone who doesn't know what you changed — they know what they do with the product, not how you built it.

**Key differences from developer changelog:**
- No internal jargon (no PR numbers, commit hashes, class names)
- Focus on benefit to user, not technical implementation
- Tone matches the product (playful app vs. enterprise software)
- Include visuals/screenshots where possible
- Highlight top 3 features prominently; don't bury them in a list

## Information gathering

From context, identify:
- **Version / date**: v2.1.0? "Spring 2024"? "This week's update"?
- **Changes**: What was shipped? (technical changelog, PR list, or description)
- **Product type**: Mobile app, SaaS, CLI, library, OS?
- **Audience**: End users, developers, enterprise IT admins?
- **Tone**: Professional, friendly, playful, neutral?

## Output format

```markdown
# Release Notes: [Product Name] [Version] — [Date]

---

## What's New 🎉

### [Feature 1 Headline — make it compelling]

[2–3 sentences describing what the feature does and why users will love it. Write for the user, not the engineer. "You can now..." or "We've made it easier to..."]

[Optional: screenshot or demo GIF here]

### [Feature 2 Headline]

[Description focusing on user benefit]

### [Feature 3 Headline]

[Description]

---

## Improvements ✨

- **[Improvement area]**: [What changed and why it matters to the user — e.g., "Dashboard loads 3× faster on mobile devices"]
- **[Improvement area]**: [e.g., "Search now finds results as you type, without pressing Enter"]
- **[Improvement area]**: [...]

---

## Bug Fixes 🐛

- Fixed an issue where [user-visible symptom — e.g., "notifications weren't sent when using the mobile app in offline mode"]
- Fixed [symptom — e.g., "the export button sometimes showed a blank file when downloading reports with over 10,000 rows"]
- Fixed [symptom — e.g., "an occasional crash on iOS 17 when switching between tabs quickly"]

---

## Known Issues ⚠️

*We're aware of the following and working on a fix:*

- [Issue — e.g., "Some users on older Android devices may experience a delay when loading the home screen. A fix is coming in the next update."]
- [Issue — e.g., "The PDF export feature may not render custom fonts correctly. Workaround: use the PNG export option."]

---

## Breaking Changes / What You Might Need to Do

*[Include this section only if users need to take action — skip for smooth updates]*

- **[Change affecting users]**: [What they need to do — e.g., "If you've set up a custom domain, you'll need to re-verify it in Settings → Domain by [date]."]
- **[Another change]**: [Action required]

---

## Upgrade Guide

*For [enterprise users / self-hosted customers / developers]:*

[Brief upgrade instructions or link to detailed migration guide]

```bash
# Example for a CLI tool
npm update [package]@[version]
```

---

## What's Coming Next 🚀

*[Optional: teaser of upcoming features to build excitement]*

- [Upcoming feature — e.g., "AI-powered writing suggestions — coming next month"]
- [Upcoming feature]

---

## Thank You

[Optional: acknowledge community, beta testers, or customer feedback that shaped this release]

*As always, [contact/feedback channel — e.g., "hit us up in the Discord" or "send feedback from the Help menu"].*

---

*[Version: X.X.X | Released: Date | Platform: iOS/Android/Web/All]*
```

## Tone and style guide

Adjust based on product type:

| Product type | Tone example | Opening style |
|-------------|-------------|--------------|
| Consumer mobile app | Friendly, emoji, "you" language | "We've been busy! Here's what's new..." |
| SaaS productivity tool | Professional but warm | "This release focuses on speed and reliability..." |
| Developer tool / CLI | Technical-friendly, concise | "v2.1.0 includes three new commands and performance improvements..." |
| Enterprise software | Formal, precise | "Version 4.2 introduces the following capabilities and addresses reported defects..." |

## Transforming technical changes to user language

| Technical description | User-facing version |
|----------------------|---------------------|
| "Reduced API latency by 40% via connection pooling" | "Pages load up to 40% faster" |
| "Fixed NPE in OrderService when order contains no items" | "Fixed a crash that occurred when submitting an empty cart" |
| "Upgraded to React 18 with concurrent rendering" | "The app feels more responsive, especially on slower connections" |
| "Added index to user_email column" | "Search is now 10× faster when looking up users by email" |
| "Refactored authentication middleware" | (no user impact — don't include) |

## App Store / Play Store format

For mobile releases (shorter, no markdown):

```
What's New in Version [X.X]:

🚀 [Feature 1]: [1-sentence description]
⚡ [Feature 2]: [1-sentence description]
🐛 Bug fixes and performance improvements

Thank you for your feedback! Rate us ⭐⭐⭐⭐⭐ if you love the app.
```

## Calibration

- **SaaS product update**: Full format with all sections; professional tone; include screenshots placeholder
- **Mobile app (App Store)**: Short, emoji-friendly format; focus on top 2–3 changes
- **Enterprise software**: Formal tone; detailed breaking changes section; include version number prominently
- **From changelog**: Convert technical entries to user-facing language using the transformation table
- **Minor/patch release**: Just Improvements + Bug Fixes sections; no headline features
