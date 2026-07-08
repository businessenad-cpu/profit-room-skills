---
name: personalize
description: Set up (or update) your brand profile so every other skill in this pack writes in YOUR voice, for YOUR offer and audience. Run this ONCE before using the content, YouTube, or money skills. Trigger whenever the user says "personalize", "set up my brand", "set up my profile", "make these skills mine", "update my brand info", or when another skill reports that the brand profile is missing or incomplete.
---

# Personalize — your one-time brand setup

Every content and money skill in this pack reads a single file — `~/.claude/brand-profile.md` — so it can write in your voice, for your offer, to your audience, without you re-explaining yourself every time. This skill creates or updates that file by interviewing you. **You only do this once** (edit it anytime by running `personalize` again).

## What to do

### 1. Check for an existing profile
Read `~/.claude/brand-profile.md`.
- If it exists and looks complete, show the user a short summary and ask if they want to update any section. Only re-ask the sections they want to change.
- If it's missing or thin, run the interview below.

### 2. Interview (keep it fast and human)
Ask these as small groups, **one group per message**, not all at once. Accept short answers and infer sensible defaults; never lecture. If the user says "I don't know yet" for the offer/proof, record that honestly (skills will then ask lighter or omit claims) rather than inventing anything.

**Group A — You**
- Your name (how it should appear in content)?
- What you do / your area of expertise, in one plain sentence?

**Group B — Your audience**
- Who are you trying to reach (their role/situation)?
- What's the main pain or goal you help them with?

**Group C — Your offer**
- What do you sell (or plan to sell), and roughly at what price?
- What's the transformation someone gets from it?

**Group D — Your voice**
- Any words/phrases you love or ban? (e.g. no em dashes, lowercase DMs, no jargon)
- Tone in three words (e.g. "direct, warm, concrete")?

**Group E — Proof & links** (optional — skip anything they don't have)
- Any real results, credentials, or wins you're comfortable citing?
- Your website, main social handle(s), and booking/checkout link?
- Which platforms do you post on most?
- Your default call-to-action (what you want people to do)?

### 3. Write the profile
Write `~/.claude/brand-profile.md` using the exact template in `references/brand-profile-template.md` (copy it, fill in every answer, leave honest `(not set yet)` markers for blanks). Confirm the path back to the user and tell them: *"Done — every content and money skill will now use this automatically. Run `personalize` anytime to update it."*

## Rules
- Never fabricate results, revenue, follower counts, or credentials. Blanks stay blank until the user gives you something real.
- Keep the interview to ~5 short exchanges. Respect a user who wants to answer everything in one message.
- This file is personal; it lives in `~/.claude/`, never inside a project or repo.
