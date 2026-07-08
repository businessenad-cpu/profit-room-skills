---
name: substack
description: "Generate a weekly newsletter issue (or a short note) in the user's voice, ready to paste into Substack. Finds the week's signal, picks the angle, writes the draft to a local file, and gives clean publish steps. Use when the user says /substack, 'write the newsletter', 'draft this week's issue', 'substack this week', or 'write a newsletter note'."
allowed-tools: Bash, WebSearch, WebFetch, Read, Write, Agent
metadata:
  argument-hint: "/substack  (weekly article)  ·  /substack note  (short note)"
---

# Weekly Newsletter Generator

Finds the signal, picks the angle, writes the draft in the user's voice, and saves it as a clean
Markdown file the user pastes into Substack. No external publishing scripts required.

Invoke with no args for the **weekly article**. For a short **note**: `/substack note`.

## Personalization
This skill writes in *your* voice, about *your* week. Before running, load the brand profile at
`~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your niche, audience, and
  what you're building — I'll create it).
- Pull Tone, Words-to-avoid, Audience, Transformation, Proof, and Default-CTA from the profile. Every
  hook and the closing CTA must come from real facts in the profile — never invent results, numbers, or
  client wins.
- If a field this skill needs is blank, ask one quick question and save the answer back to the profile.

## Requirements
- **Publishing is manual by default.** This skill writes a ready-to-paste Markdown draft to a local
  file; the user copies it into the Substack editor and hits publish. No API keys needed.
- Optional: if the user has their own Substack automation (a script, a Zapier/Make flow), they can wire
  the final file into it — but nothing here depends on it.

---

## NOTE MODE (`/substack note`)

A short, punchy note (50-200 words) — one scene, one point.

1. **Pick a target length:** randomly choose 50, 100, 150, or 200 words. State it before drafting.
2. **Find the moment:** pull one real moment from the profile's Proof/Transformation, or ask the user
   for one thing that happened this week worth writing down. Notes are grounded in a real moment, never
   an abstract observation ("most people do X" is filler, not a hook).
3. **Draft it** in the user's voice:
   - **Hook:** lead with the transformation or the moment in concrete terms (real numbers where the
     user has them). Make the reader want it.
   - **Body:** diary-like, personal, plain language. What actually happened. No quote-card aphorisms.
   - **Close:** hand the reader something concrete — how this benefits them and what they could do
     differently. Never assume their situation; state what's true for the user and let them draw the
     parallel.
   - No em dashes, no filler, short sentences, line breaks. Reads in 60 seconds.
4. **Save** to `~/newsletter/notes/<YYYY-MM-DD>-<slug>.txt` and show it to the user to paste into
   Substack Notes.

---

## WEEKLY ARTICLE MODE (default)

### Step 1 — Gather this week's context (run in parallel)

Fire these together:

**A) What the user worked on this week.** Ask: "What did you build, ship, learn, or figure out this
week?" (One line is enough.) If the user keeps a work log or project notes, offer to read a path they
give you. This becomes the "What I Built / Learned This Week" anchor — the realest, most specific part.

**B) What's happening in the user's niche this week** — 2-3 WebSearches scoped to their field, e.g.:
- `[user's niche] new tool OR release OR update after:[date 7 days ago]`
- `[user's niche] news this week site:techcrunch.com OR site:theverge.com`
- one search on a specific topic the user is watching

**C) The user's own recent content** (optional). If they want to embed a video/post, ask for the URL.

### Step 2 — Pick topic + built anchor

Choose the "What I Built This Week" anchor by this priority:
1. **A real build/ship from this week** (best — real, specific, theirs).
2. **An idea or insight** that clicked this week (strong).
3. **A niche news drop** to react to (fallback — commentary, never a fabricated personal build).

Then pick a **topic angle** that connects naturally to that anchor and hasn't run in recent issues.
Good evergreen angles (adapt to the user's niche):
- Attention that doesn't convert (engagement vs. income)
- The build-before-launch trap (building instead of selling)
- The sequencing mistake (tools before offer, complexity before proof)
- Permission to ship imperfect
- Selling the outcome, not the tool
- Niche clarity — picking a lane

The built anchor illustrates the topic; the topic reframes what the build revealed. They should feel
like one idea. State the chosen topic + anchor + why they connect before drafting.

### Step 3 — Write the draft

Write the full issue in the user's voice. Follow the ARTICLE STRUCTURE below. Save to
`~/newsletter/<YYYY-MM-DD>-<topic-slug>.md`. Print the path and the first ~300 characters so the user
can sanity-check the voice.

### Step 4 — Report back

```
Issue drafted.

Topic:   [topic angle]
Anchor:  [built anchor — one line]
Hook:    [first line]
Proof:   [any real win/number used]
File:    [path to .md]

To publish: open Substack → New post → paste the Markdown → add a cover image (optional) → publish.
```

---

## ARTICLE STRUCTURE REFERENCE

Section order (keep it):
1. **Opener:** Hook → open loop → "this week:" preview bullets → loop closure (what it means → why it
   matters → the shift)
2. **New This Week** (embed a video/post here if the user gave one)
3. **One Thing Worth Stealing** — closes with WHY + the dream outcome (specific: first client, replaced
   income, etc. — never vague)
4. **What I Built / Learned This Week** — story arc: problem → what I did → the teaching moment. A
   blockquote with a real number/stat if one exists, and it must NOT echo the opener. This must be a
   DIFFERENT build from the one embedded in "New This Week."
5. **A Win** (the user's own or a client's, with permission and no real names — "a client who…") — the
   WHY moment before the result; the transformation is what they now KNOW, not just what they got
6. **Pre-CTA question**
7. **CTA** — the user's Default-CTA from the profile

## Voice rules

- Opinion-first — lead with the point, not the setup.
- Short sentences. Specifics over generalities. Real numbers only (the user's actual figures).
- Never hedges, never talks down. Treats the reader as capable.
- Sounds like a diary entry or a text from someone who knows what they're doing — not a marketing email,
  not a quote card.
- No em dashes. No "not X, but Y" constructions. No preachy closing lines — end on something plain.
- Be concrete: name the actual actions a person takes (ship the feature, message a stranger, name a
  price, sit with a no), not abstractions like "building feels like progress." If a sentence could apply
  to almost anything, it's too vague — replace it with the specific thing. This is the most common
  failure in generated drafts; check every paragraph.
- Never use real client/member names — "a client who…", "someone I work with who…". Establish who they
  are before any pronoun.
- Respect the profile's Words-to-avoid.
