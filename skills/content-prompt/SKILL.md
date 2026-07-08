---
name: content-prompt
description: Generate a single thought-provoking question for the user to answer on camera as short-form content (TikTok, Reels, YouTube Shorts, or any off-the-cuff video), plus 5 hook options and text overlays. Use whenever the user asks for "content ideas", "what should I talk about", "give me a question to answer", "prompt me", "short-form ideas", "what's trending I can speak to", "I need content inspiration", or says /content-prompt. Always trigger when the user wants something to riff on for a quick video — even a casual "give me something to talk about" or "what should my next video be about".
---

# Content Prompt Generator

**The purpose of these videos:** help the user tell true stories from their own life and experience that build authenticity, nurture the audience, and share hard-won wisdom. A trending conversation is the *entry point* — the user's real story is the *content*. Not news commentary. Not generic advice. Their real experience, surfaced by a question worth answering.

**Funnel level: REACH.** Cold-audience discovery pieces. One value hit, one follow CTA. No hard offer, no links.

## Personalization
This skill works in *your* voice, drawing on *your* story and audience. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your niche, audience, offer, and a couple of real moments from your journey — I'll create it).
- The story seed for every prompt must come from something the user actually lived. If the profile's Proof/Transformation is thin, ask them for one real moment (a mistake, a turning point, a surprising result) and save it back to the profile.
- Never invent facts, results, or stories about the user — use only what's in the profile, or ask.

---

## Step 1: Load Context

Read `~/.claude/brand-profile.md`. Extract:
- **Audience + Main-pain** — who you're talking to and what they're stuck on
- **Transformation + Proof** — the real moments in the user's journey you can draw a story from
- **Tone + Words-to-avoid** — how it should sound

What you're looking for: a moment in the user's story that maps directly onto what their audience is going through right now.

---

## Step 2: Pick a Category + Find the Live Tension

**Randomly select one of the four category types below**, adapted to the user's niche. Vary across runs — don't always default to the same one.

- **Category A — Visibility / Personal Brand:** the invisible expert who can't get traction despite real skill. Story territory: posting and quitting, an audience milestone, building a system vs. grinding, the moment something clicked.
- **Category B — Making Money:** the person with a skill who can't convert it to consistent income. Story territory: pricing confidence, the first client, the gap between "I built it" and "someone paid me for it," selling without a big audience.
- **Category C — New Tool / What Just Dropped:** the early adopter who wants to stay ahead. Story territory: the user's real first-hand experience testing a new tool in their field — what surprised them, what broke, what actually worked vs. the demo.
- **Category D — Systems / Doing More With Less:** the operator drowning in manual work. Story territory: replacing manual hours with a system, the moment they stopped doing it by hand, the workflow that changed everything.

**Optional — find live tension:** if the user wants timeliness, run 1-2 web searches for an active debate or fresh release in their niche (e.g. `"[user's field] [common frustration]" reddit 2026`, or `"[new tool in their field]" honest review 2026`). You're not looking for news — you're looking for **active friction the user has personally lived through**.

The question to ask: *is there a moment in the user's story — a decision, a mistake they corrected, a belief they had to unlearn — that speaks directly to this tension?* If yes, that's the prompt. If not, pick a different tension that does connect to a real experience.

---

## Step 3: Find the Story Seed

Before picking the question, identify the **specific experience in the user's life** the video would draw from. It must be real — something they lived, from the profile, not something invented.

Story categories to draw from:
- A mistake they made and what it cost
- A moment they almost quit or pivoted
- A belief they held that turned out wrong
- A result that surprised them (better or worse than expected)
- Something a client said that reframed how they work
- A decision that felt scary but paid off
- Something they did differently than everyone else — and why

The story seed is the heart of the video. The question is just the door that opens it.

---

## Step 4: Lock the Question

Frame a question that:
- The audience is silently asking but doesn't know how to articulate
- Opens the door to the user's specific story (not generic advice)
- Creates a gap: the viewer assumes one thing, the user's answer flips it
- Feels like a TikTok opening line — punchy, not academic

Best openers: "Is...", "Why...", "What if...", "Does...", "Are you..."

---

## Step 5: Generate 5 Hooks + Text Overlays

Map the question to a core desire (Money / Time / Health / Status), then generate one hook per variation:

1. **About Me** — "I [did X] and here's what happened"
2. **If I** — "If I were starting over, I would [Y]"
3. **To You** — "If you're [doing X], you're [missing Y]"
4. **Can You** — "Is it possible to [X] without [Y]?"
5. **He/She Just Did** — "[Someone] just [did X]. Here's what they figured out."

For each hook:
- Fifth-grade reading level — short, no jargon
- Must include: Subject + Action + Objective at minimum
- Written in the user's Tone, respecting Words-to-avoid

**For each hook, also write a text overlay.**

The spoken hook and text overlay play simultaneously — the viewer hears one while reading the other. They must each stand alone AND say something different. The overlay is never a caption, label, or summary of the spoken hook.

**Write the spoken hook first.** Complete standalone hook — works with zero visual context.
**Write the text overlay second.** 2–6 words. Goal: intrigue, not description. Three categories that work:
- **Paradox** — sounds wrong or contradictory: "She was right." / "I fired all three." / "It cost me $20."
- **Social proof gap** — implies others knew something first: "78K people knew this before me."
- **Confession** — creates tension: "I almost didn't post this." / "Agency quote: $5,000."

**Text overlays that don't work:** descriptive labels, tool names, preachy statements, anything that repeats or summarizes the spoken hook.

**Good pair (simultaneous — each stands alone, together they create contrast):**
- Spoken: "I posted for 3 months, got nothing, and quit. Twice. Here's what I was actually doing wrong."
- Text: "I almost deleted the account." ← confession that adds tension without explaining the spoken hook

---

## Step 6: Output

Use exactly this format:

---

**The Question:**
[1-2 sentences. Punchy. The door that opens the user's story.]

**The Story Seed:**
[2-3 sentences. The specific real experience from the user's life this video draws from. Name the moment, the decision, the mistake, or the shift — not the lesson, the *event*.]

**Why now:**
[1 sentence. What live conversation makes this timely. Omit if not tied to a trend.]

**The so what:**
[2 sentences. What belief shifts or decision unlocks for the viewer. Grounded in a real audience outcome — specific, not vague.]

---

**5 Hooks:**

1. **[About Me]** — "[hook]"
   *Text overlay: "[2–6 words — paradox / social proof gap / confession]"*

2. **[If I]** — "[hook]"
   *Text overlay: "[2–6 words]"*

3. **[To You]** — "[hook]"
   *Text overlay: "[2–6 words]"*

4. **[Can You]** — "[hook]"
   *Text overlay: "[2–6 words]"*

5. **[He/She Just Did]** — "[hook]"
   *Text overlay: "[2–6 words]"*

**Use hook #[X].** [One sentence — why this hook, citing audience fit.]

---

**The CTA:**
[One sentence. Follow only. What they just got → what they keep getting. No offer, no link.]

---

The user hits record, not a menu. The story seed is the content. The question is the entry point. The hook is the first line. The CTA is the last.
