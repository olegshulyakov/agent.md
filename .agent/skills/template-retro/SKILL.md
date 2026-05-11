---
name: template-retro
description: >
  Produces a retrospective template with structured prompts for what went well, what to improve, and
  action items. Use this skill whenever the user wants to run a sprint retrospective, create a retro
  template, facilitate a team reflection session, or asks to "create a retro template", "write a
  retrospective agenda", "help us run a sprint retro", "create a lessons learned document", "write
  a team retrospective", "design a retro format", or "what went well / delta / actions format".
  Also trigger for "blameless retrospective", "start/stop/continue retro", "4Ls retrospective",
  "sailboat retro", and "post-sprint reflection". Distinct from writer-postmortem (which is for
  incident analysis) and planner-sprint (which plans the next sprint).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# template-retro

Produce a **retrospective template** with structured prompts, facilitation guidance, and action items.

## Retrospective formats

| Format | Best for | Structure |
|--------|----------|-----------|
| **What Went Well / Delta / Actions** (default) | Standard sprint retro | Simple, easy to run |
| **Start / Stop / Continue** | Changing team behaviors | Action-oriented |
| **4Ls: Liked, Learned, Lacked, Longed For** | In-depth reflection | More nuanced |
| **Sailboat** | Visual thinkers; fun engagement | Metaphor: wind=helps, anchors=slows, rocks=risks |
| **Mad / Sad / Glad** | Team morale check-in | Emotional check-in first |

Generate the format the user requests. Default to **What Went Well / Delta / Actions**.

## Output format

### Standard retro template (What Went Well / Delta / Actions)

```markdown
# Sprint [N] Retrospective

**Date:** [date]
**Sprint:** [Sprint N — Start Date → End Date]
**Facilitator:** [Scrum Master / name]
**Team:** [Team name]
**Attendees:** [list]

---

## Agenda (60 minutes)

| Time | Activity |
|------|----------|
| 0–5 min | Check-in / icebreaker |
| 5–20 min | Individual reflection & sticky note writing |
| 20–35 min | Group by theme; dot voting |
| 35–50 min | Discuss top themes; identify root causes |
| 50–60 min | Define action items with owners |

---

## Check-in

*Icebreaker question (pick one or make your own):*
- "In one word, how did this sprint feel?"
- "What's one thing that surprised you this sprint?"
- Rate the sprint: 👎 1 — 5 👍

**Team mood temperature:**

| Name | Mood (1–5) | One word |
|------|-----------|---------|
| [Name] | [N] | [word] |

---

## Section 1: What Went Well? 🌟

*Individual reflection: What should we keep doing? What are we proud of?*

*(Allow 5–10 min for everyone to add sticky notes — real or virtual)*

| # | Item | Votes | Theme |
|---|------|-------|-------|
| 1 | [e.g., "Daily standups were focused and short"] | [👍 N] | Process |
| 2 | [e.g., "Clear acceptance criteria reduced rework"] | [👍 N] | Quality |
| 3 | | | |

**Top themes from this section:**
1. [Theme 1]
2. [Theme 2]

---

## Section 2: What Could Be Better? 🔧

*Individual reflection: What caused friction? What slowed us down?*

| # | Item | Votes | Theme |
|---|------|-------|-------|
| 1 | [e.g., "PR reviews took 2+ days"] | [👍 N] | Process |
| 2 | [e.g., "Requirements were unclear mid-sprint"] | [👍 N] | Requirements |
| 3 | | | |

**Root cause discussion (for top-voted items):**

**Item:** [Top improvement item]
- **Why did this happen?** [Team's root cause analysis — ask "5 Whys" if needed]
- **What would success look like?** [Desired state]
- **Action:** → [see action items below]

---

## Section 3: Questions & Puzzles ❓

*Things we're curious or confused about — not complaints, genuine questions*

| # | Question |
|---|----------|
| 1 | [e.g., "Why did the staging deploy take 45 minutes?"] |
| 2 | |

---

## Action Items

*Keep it to 2–3 actions max — quality over quantity. Vague actions get ignored.*

| # | Action | Owner | By When | Done? |
|---|--------|-------|---------|-------|
| 1 | [Specific, measurable action] | [Name] | [Sprint N+1 / Date] | [ ] |
| 2 | [e.g., "Add PR size limit to contributor guide: max 400 lines; break larger PRs"] | [Name] | [Next retro] | [ ] |
| 3 | | | | |

**Review previous actions:**

| Previous Action | Owner | Status |
|----------------|-------|--------|
| [Action from last retro] | [Name] | ✅ Done / 🔄 In Progress / ❌ Not Done |

---

## Sprint Metrics (optional — for data-driven teams)

| Metric | This Sprint | Previous Sprint | Trend |
|--------|-------------|----------------|-------|
| Velocity | [N pts] | [N pts] | ↑ / ↓ / → |
| Stories completed | [N/N planned] | [N/N] | |
| Bugs introduced | [N] | [N] | |
| PR cycle time (avg) | [X days] | [X days] | |
| CI pass rate | [X%] | [X%] | |

---

## Team Health Pulse *(optional, anonymous)*

Rate each dimension 1–5. Facilitator can collect anonymously via poll.

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Clarity of goals | [avg] | |
| Psychological safety | [avg] | |
| Collaboration | [avg] | |
| Technical quality | [avg] | |
| Work-life balance | [avg] | |
| Fun / energy | [avg] | |

---

## Shoutouts 🙌

*Recognize team members for specific contributions*

- [Name] — [what they did that deserves recognition]
- [Name] — [...]

---

## Next Steps

- [ ] Facilitator shares this document with the team
- [ ] Action items added to next sprint backlog
- [ ] Action items reviewed at next retro
```

### Start / Stop / Continue format

```markdown
# Sprint Retro: Start / Stop / Continue

## START doing
*Things we should introduce or experiment with*

| Item | Votes | Action |
|------|-------|--------|
| [e.g., "Pair programming for complex stories"] | | |

## STOP doing
*Things that aren't adding value or are causing harm*

| Item | Votes | Action |
|------|-------|--------|
| [e.g., "Long status update meetings — replace with async updates"] | | |

## CONTINUE doing
*Things that are working well and should be preserved*

| Item | Votes |
|------|-------|
| [e.g., "No-meeting Wednesday mornings"] | |
```

### Sailboat format

```markdown
# Retro: Sailboat 🚢

*Our ship = the team. Our goal = the island in the distance.*

## ⛵ Wind (what propels us forward)
[What's helping us move fast toward our goals?]

## ⚓ Anchors (what slows us down)
[What's holding us back?]

## 🪨 Rocks (risks ahead)
[What risks do we see on the horizon?]

## ☀️ Island (our goal)
[Reminder: what are we working toward?]
```

## Facilitation tips

Include these for facilitators who are less experienced:

- **Psychological safety first**: Start with an icebreaker. Remind the team retros are blameless — focus on systems and processes, not individuals.
- **Time box each section**: Use a visible timer. Move on even if the discussion is rich — capture unfinished threads as action items.
- **Dot voting**: Give each person 3–5 votes to distribute across items. Reveals the team's shared priorities better than discussion alone.
- **2–3 actions max**: Resist the urge to list 10 improvements. Three well-executed actions are worth more than ten ignored ones.
- **Previous actions first**: Start by reviewing last retro's actions. This builds accountability.

## Calibration

- **Blank template**: Full template ready to fill in during the retro
- **Specific sprint**: Fill in sprint number, dates, metrics from context
- **Remote / async team**: Add virtual collaboration tool guidance (Miro, FigJam, RetroBoard)
- **Team morale issue**: Expand health pulse and psychological safety sections; use Mad/Sad/Glad format
