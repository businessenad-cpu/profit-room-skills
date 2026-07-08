---
name: outlines
description: "Generate full YouTube video outlines — hook, structured body with talking points, visual aid callouts, source citations, time budgets, and production notes. Trigger on phrases like 'outline this video', 'write an outline for', 'structure this video', 'create a video outline', 'help me outline', or any request to plan or structure a YouTube video for recording."
allowed-tools: Bash, Read, Write
user-invocable: true
metadata:
  argument-hint: "/outlines [topic or angle from /ideation]"
---

# YouTube Video Outline Generator

Generate recording-ready video outlines with open loop tracking, list-within-list retention structure, and 5th grade language enforcement. Outputs a filmable outline in your voice.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

Fields this skill uses: **Tone** + **Words-to-avoid** (voice), **Audience** + **Main-pain** (talking-point language), **Proof/wins** (the story anchor — never invent one), **Offer** + **Default-CTA** (the close).

## When This Skill Activates

**Activate when the user wants to:**
- Structure a video for recording
- Turn research or an idea brief into a filmable outline
- Create a full video plan with talking points
- Organize raw notes into a video format

**Example triggers:**
- "Outline this video about RAG concepts"
- "Turn this research into a video outline"
- "Write the outline for tomorrow's video"
- `/outlines` or `/outlines <topic>`

---

## Step 0 — Load Intelligence

**A — Brand voice:**
From the brand profile, extract the user's tone, words to avoid, and sentence-length preference. Apply silently to every line of spoken content generated.

**B — Audience language:**
Use the brand profile's **Audience** and **Main-pain** fields. Every talking point that names a pain should use the audience's own words, not a paraphrase. If you have a saved swipe file of real audience phrases (testimonials, comments, call notes), pull from it verbatim where possible.

**C — Proof anchor (required):**
Every outline must have one story anchor. Use only real, cite-able facts from the brand profile's **Proof/wins** field — never invent a result. Pick the strongest match before building:
- Transformation arc (highest trust) — before + shift + after
- Verbatim testimonial (second) — use exact quote
- The user's own build/result (always available)

**How to apply:**
- Seed talking points with real audience language — if someone said it, use that phrase
- Pick the proof anchor first, build the section it anchors around it
- When the outline runs long: cut the section least connected to an audience pain point

---

## LOOP TRACKER — Required for Every Outline

Open loops are the retention mechanism for talking head content. They replace what b-roll and graphics do visually.

**Rules:**
1. Every loop opened must be closed — no exceptions
2. Maximum 2 loops open at once. A third loop cannot open until one closes.
3. The most important payoff goes last — sequence loops by weight, lightest first
4. Secondary loops (opened inside a section) must close before the section ends or explicitly hand off to the next section

**Notation:**
- `→ LOOP OPEN [name]: "[the exact promise made to the viewer]"` — when a loop is opened
- `✓ LOOP CLOSE [name]` — when it's resolved
- `→→ SECONDARY LOOP [name]` — a loop opened inside another section (must close within that section or hand off explicitly)

**At outline completion, run a loop audit:**
List every `→ LOOP OPEN` in order. Confirm every one has a corresponding `✓ LOOP CLOSE`. If any loop is open at the end, the outline is not complete. Resolve or explicitly remove the loop before delivering.

**Loop audit format (append at end of outline):**
```
## Loop Audit
- [loop name]: OPEN at [section] → CLOSED at [section] ✓
- [loop name]: OPEN at [section] → CLOSED at [section] ✓
```

---

## LANGUAGE RULES — Apply to Every Line of Spoken Content

**The standard:** 5th grade reading level. Short sentences. One idea per sentence.

**Apply the brand voice filter after every section:**
- Short sentences. Under 15 words preferred.
- Opinion first — lead with the point, not the setup
- No hedge words: "might," "could," "perhaps," "maybe," "potentially"
- No fluff openers: "In today's world," "As we all know," "Great question"
- No em dashes — use a comma or period
- No "solopreneur"
- No long unbroken paragraphs in spoken sections — line breaks do work
- Use specifics and numbers, not vague claims: "$86K" not "a lot of money," "10 conversations" not "some research"
- Define any technical term immediately after you use it — never assume

**Self-check before finalizing any spoken section:**
Read it out loud. If it sounds like a blog post, rewrite it. If it sounds like something you would say to a client or on a call, it's right.

---

## LIST-WITHIN-LIST RETENTION SYSTEM

For talking head and strategy content, the outline structure IS the retention mechanism. No graphics means no visual anchor — the list structure gives the viewer something to track instead.

**Rules:**
- **Outer list:** 3–5 items max. The viewer holds this count in their head. Name the count upfront ("three mistakes," "five questions").
- **Inner list:** 2–3 items per outer item. Never go deeper than two levels.
- **Name every item** before explaining it. One word or short phrase. Then expand.
- **Each outer item needs one concrete example** — a real person, a specific number, a named situation. Not hypothetical.
- **Transitions between outer items must either close a loop or open a new one** — never just "okay, moving on to number two."

**Transition templates:**
- Close + open: "So that's [item 1]. But here's the thing — even people who fix [item 1] still run into [item 2] because..."
- Secondary loop open: "Before I show you [item 2], there's something you need to understand about [related concept] — and it changes everything."
- Escalation: "If [item 1] is the obvious mistake, [item 3] is the one that actually ends businesses."

---

---

## Input

The user provides one or more of:
- **Topic or idea brief** — from `/ideation` or described verbally
- **Research notes** — brain dumps, pasted research, or files
- **Hook** — from `/hooks` (optional — will generate one if not provided)
- **Target length** — how long the video should be (default: 12-18 minutes)

## Workflow

### Step 1 — Determine Video Format

Classify the video structure based on the content:

**Talking Head / Strategy** — no screenshare, no build on camera. Narrative carries attention. Use for coaching insights, frameworks, business strategy, personal brand lessons.
- Structure: Hook (5-beat intro) → Story anchor → Outer list (3–5 mistakes/steps/truths) → Framework (named, with inner list) → Close (loop payoff) → CTA
- Retention mechanism: open loops + list-within-list (replaces graphics)
- Each outer item: Name it → Example (real person or real number) → Inner list (2–3 beats) → Transition that opens or closes a loop
- No section longer than 3 minutes without a new list item or loop event
- Story anchor goes in section 1, before the list — it's the proof that makes the list credible
- The framework section (near the end) gives the viewer something actionable — a named system, a set of questions, a decision filter

**Concept/Educational** — explaining ideas with escalating depth
- Structure: Hook → Concept 1 → Concept 2 → ... → Big Picture Closer
- Per concept: core idea (one-liner) → explanation → analogy → source

**Level-Based** — progressive mastery/identity arc
- Structure: Hook → Level 1 → Level 2 → ... → Master Level
- Per level: what it is → the shift → demos → key mantra → transition

**Tool/Product Demo** — showing how something works
- Structure: Hook → Problem/Context → Tool Intro → Demo → Honest Limitations → CTA
- Heavy on screen recording, light on talking head

**Contrarian/Opinion** — challenging conventional wisdom
- Structure: Hook (contrarian claim) → Evidence → Counter-arguments → Resolution → Implications
- Needs strong authority right after the claim

**Case Study** — documenting a specific result or process
- Structure: Hook (result reveal) → Context → Process → Results → Lessons → CTA
- Heavy on demos and proof

**Listicle** — curated collection
- Structure: Hook → Item 1 → Item 2 → ... → Best/Most Important Last
- Per item: what it is → why it matters → demo moment → who it's for

**Head-to-Head** — comparing two approaches
- Structure: Hook → Contender A → Contender B → Direct Comparison → Verdict

**Parallel List / Dead-vs-Alive** — the most viral format in 2025-2026. Opens with a bold contrarian claim, runs two opposing numbered lists (what's broken vs. what works), bridges them with a pivot sentence, and closes with a reframe + action question.
- Structure: Hook (contrarian claim) → Why It's Dead (numbered list) → Rapid Recap Bridge → Pivot Question → What Works (numbered list, parallel structure) → Reframe Closer → CTA
- Per dead-list item: **[Name]** → what it is (one line) → why it's cooked now (one line)
- Per works-list item: **[Name]** → what it is (one line) → why it wins now (one line) → the mechanic or example
- Best for: "X is dead," "Stop doing X," "Here's what actually works," "The old way vs. the new way"
- Signature move: every list item uses the *same sentence structure* — the repetition is the rhythm

### Step 2 — Build the Outline

**For Talking Head / Strategy format, use this template:**

**Output format:**
- **INTRO: fully scripted, word for word.** This is the one section you read exactly. Short sentences. Every sentence earns the next. Ends with "So focus in. Close all your open tabs." then either "Let's build." (tool/build videos) or "Let's get to it." (strategy videos).
- **All other sections: mix of sentences and bullets.** Key points that need to land exactly — write as a sentence. Supporting details, examples, and lists — write as bullets. Never full paragraphs. Never pure bullets. The sentences are the anchors. The bullets are what he can riff on.

```markdown
# [Video Title]

**Length:** [X-Y min] | **Anchor:** [Story or proof point]

---

## INTRO — Scripted

Write this word for word. Every sentence earns the next. Read it out loud — if it sounds like a blog post, rewrite it. Target: ~120 words, ~50 seconds.

**BEAT 1 — HOOK**
One sentence. Plants a question the viewer has to answer — does NOT answer it.
Best pattern: "Most [audience] never [desired outcome] — but it's not because [the obvious reason they'd assume]."
This opens the "then why?" loop and keeps them watching for the answer.
- Must pay off the video title directly
- Conversational language only — "awesome" not "sufficient," "wrong order" not "sequencing problem"
- No jargon, no hedging
- Do NOT cushion the hook — no "I know that sounds backwards" after it. Let it land.

**BEAT 2 — CREDIBILITY + RETENTION TEASE**
Establish authority and open the main content loop in the same breath. One or two sentences.
Pattern: "I've coached over 2,000 AI builders, and there are [N] mistakes almost every one of them is making. The [last] one is the one that ends the business."
- Credibility number first, loop tease second
- Never a bio paragraph — one number, one sentence

**BEAT 3 — STAKES**
Answer the hook's question now. Name the exact behavior — no vague pronouns ("this," "it").
Pattern: "If you've been [doing X] and still [don't have result], it's probably not because [false assumption]. You're simply [plain language diagnosis]."
- If the hook already said something, do not repeat it — cut the redundant line
- Plain language: "doing things in the wrong order" not "sequencing problem"

**BEAT 4 — OLD RULE / NEW RULE (optional — use for strategy/mindset videos)**
The reframe that earns screenshots. Pattern:
"The old rule was: [belief they were taught]. That rule is dead. There's only one thing that matters now — [the new truth]. You have to [the counterintuitive action]."
Use when the video challenges a widely held belief. Skip when the video is tactical.

**BEAT 5 — DREAM OUTCOME PROMISE**
The guaranteed result with a time or effort qualifier. Pattern:
"By the end of this video you'll have [the one fix / exact framework] — and it will do more for your business than [what they're currently wasting time on]. All it takes is [number] [simple deliverable] that [specific qualifier — time, result, or action]."
- "Five questions that tell you within 24 hours" is stronger than "five simple questions" — the qualifier makes it feel real
- The deliverable should sound small and achievable — the contrast with the big promise is the hook
- Never promise a framework or a system — promise a result or a decision

**FIXED CLOSE — always verbatim:**
So focus in. Close all your open tabs.
[End: "Let's get to it." for strategy/framework videos. "Let's build." for tool/build videos.]

---

**Reference intro (use as the quality bar):**

Most AI builders never get a client — but it's not because what they're building isn't awesome.

I've coached over 2,000 AI builders, and there are three mistakes almost every one of them is making. The third one is the one that ends the business.

If you've been building for months and still don't have clients, it's probably not because your tool isn't good enough. You're simply doing things in the wrong order.

The old rule was: build something great and everyone will want it. That rule is dead. There's only one thing that matters now — distribution. You have to put the cart before the horse.

By the end of this video you'll have the one fix every AI builder should make — and it will do more for your business than the next six months of building alone. All it takes is five questions that tell you within 24 hours if your idea is worth building.

So focus in. Close all your open tabs.

Let's get to it.

---

## [Story Section Title]

[Story told in short punchy lines. Real situation, real detail.]

[Bridge — connects the specific lesson of the story to the audience's situation. Not a general restatement of the topic. The bridge should land on the exact insight the story demonstrated — then show how the audience is making the same mistake in their context. Example: story lesson = "never asked what success looked like" → bridge = "Most AI builders do exactly this. They think they know what the market wants. They never ask."]

---

## [List Section Title] — name the count upfront

**[Item 1]**
[What it is.]
[Why it happens or what it costs.]
[Real example — named person or specific number.]
[Transition to item 2.]

**[Item 2]**
[What it is.]
[The behavior — use exact ICP language.]
[Real example.]
[Transition — escalate toward the payoff item.]

**[Item N] — the one nobody talks about**
[What it is.]
[The proof — real numbers or real story.]
[The reframe — what to do instead.]

---

## [Framework Section Title]

[Name the framework. One line.]

[Why this fixes everything above.]

1. [Question or action]
2. [Question or action]
3. [Question or action]
4. [Question or action]
5. [Question or action]

[What you're listening for — one concrete signal.]

[Smallest possible first action.]

---

## CLOSE

[One sentence reframe — recontextualizes the whole video.]

[Your one-sentence CTA from the brand profile — name who it's for + the outcome your offer delivers, then point to your offer.] Link's in the description.

---

*Internal checklist — runs before delivery, never shown:*
- *Every loop opened closes*
- *Every list item has a real example*
- *Hook creates intrigue, not just empathy*
- *Dream outcome promise includes less time or less effort*
- *5th grade language — short sentences, no hedging, no em dashes*
- *CTA uses verbatim offer*
```

---

**For all other formats (Concept/Educational, Level-Based, Tool Demo, Contrarian, Case Study, Listicle, Head-to-Head, Parallel List), use this template:**

```markdown
# [Video Title] — Video Outline

- **Date:** YYYY-MM-DD
- **Target publish:** YYYY-MM-DD
- **Format:** [Format type]
- **Target length:** [X-Y minutes]

---

## Hook (~30-90 seconds)

[If hook provided from /hooks, insert with Three Hook Alignment]

[If no hook, generate one:]
- **Desire mapping:** [Core Desire] → [Proxy Desire]
- **Spoken hook:** "[The actual words]"
- **Visual hook:** [What's on screen]
- **Text overlay:** "[The text]"

---

## [Section 1 Title] (~X minutes)

**The core idea:** [One sentence — what the viewer should understand]

**Talking points:**
- [Specific point with data/example]
- [Specific point with data/example]
- [Transition to next section]

**Visual aid:** → [excalidraw or screen recording description]

**Demo:** [What to show on screen, if applicable]

**Source:** [Citation with URL]

---

## [Section 2 Title] (~X minutes)
[Same structure...]

---

## Outro / CTA (~30-60 seconds)

**Recap:** [One-line per section — rapid fire]

**CTA:** [Subscribe, comment, or your offer/community link from the brand profile]

---

## Production Notes

### Competitive Landscape
- [Creator] — [Video title] ([X views]) — [How ours differs]

### Title Ideas
1. [Option 1]
2. [Option 2]
3. [Option 3]

### Thumbnail Moments
- [Section where a good thumbnail frame could come from]

### Honest Limitations
- [What the video doesn't cover or where advice breaks down]

### Total Estimated Length: [X minutes]
```

---

#### Parallel List / Dead-vs-Alive — Full Template

When this format is selected, use this structure exactly:

```markdown
# [Video Title] — Video Outline

- **Date:** YYYY-MM-DD
- **Format:** Parallel List / Dead-vs-Alive
- **Target length:** [X-Y minutes]

---

## Hook (~60-90 seconds)

**Contrarian claim (spoken):** "[X] is dead in 2026."
**Why they should believe you:** [One sentence — what makes you credible on this topic, from your Proof/Credentials]
**Curiosity plant:** "And by the end of this video, you'll know exactly [specific outcome]."

**Visual hook:** [What's on screen in the first 2 seconds]
**Text overlay:** "[The claim in 5 words or fewer]"

---

## Why [X] Is Dead — The Problem List (~3-5 minutes)

**Setup line (spoken):** "Here's what changed. / Here's why it's not working."

### Problem [#1]: [Name — 2-4 words]
- **What it is:** [One sentence]
- **Why it's cooked now:** [One sentence — the 2026-specific reason]
- **The consequence:** [What happens to people who keep doing this]

### Problem [#2]: [Name — 2-4 words]
- **What it is:** [One sentence]
- **Why it's cooked now:** [One sentence]
- **The consequence:** [What happens]

### Problem [#3]: [Name — 2-4 words]
- **What it is:** [One sentence]
- **Why it's cooked now:** [One sentence]
- **The consequence:** [What happens]

[Add more as needed — 4-6 items is the sweet spot. Every item must follow the exact same structure.]

**Rapid Recap Bridge (spoken):**
> "So to recap — the [dead/broken/wrong] things are: [item 1], [item 2], [item 3], [item 4]. If your [X] has any of these, that's why it's not working."

---

## [Intrigue Pivot — the most important sentence in the video]

**Pivot question or statement (spoken, one line):**
> "So what's the fix?" / "So what actually works in 2026?" / "Here's the truth." / "Now here's where it gets interesting."

**Bridge (1-2 sentences):** [Short reframe before the second list — flip the narrative]

---

## What Actually Works — The Solution List (~4-6 minutes)

**Setup line (spoken):** "Here's what [works / wins / prints money] in 2026."

### [#1]: [Name — parallel structure to Problem list]
- **What it is:** [One sentence — mirrors the problem list format]
- **Why it wins now:** [One sentence — the 2026-specific reason]
- **The mechanic:** [How to actually do it — one concrete example or demo moment]

### [#2]: [Name]
- **What it is:** [One sentence]
- **Why it wins now:** [One sentence]
- **The mechanic:** [How to do it]

### [#3]: [Name]
- **What it is:** [One sentence]
- **Why it wins now:** [One sentence]
- **The mechanic:** [How to do it]

[Match the count from the problem list — same number of items feels intentional]

---

## Reframe Closer (~60-90 seconds)

**The reframe (spoken):**
> "[X] isn't dead. [Weak version of X] is dead. [Strong version / the right version] is [unstoppable / printing money / the only thing that works]."

**Action question (one question that makes them audit their own situation):**
> "So here's what I want you to do. Take your [X] and ask yourself: [Question 1]? [Question 2]? [Question 3]? If you can answer those, you're not dead. You might be about to [result]."

---

## CTA (~20-30 seconds)

**Comment CTA (creates engagement data):** "Comment [KEYWORD] below and I'll send you [the thing]."
**Next video tease (optional):** "[One-line tease of the natural next video in this topic arc]"

---

## Production Notes

### Why This Works
- The parallel structure (same sentence rhythm per item) creates a momentum effect — viewers feel the list building
- The recap bridge is a retention spike — it signals "we're about to turn the corner"
- The reframe closer lands because it distinguishes the real insight from the clickbait claim

### Intrigue Transition Library
Use these word-for-word or as templates for section pivots:
- "So what's the fix? Here's the truth."
- "Now let's talk about the stuff [audience] keeps doing that's not working — and why."
- "If that's what's broken, here's what's not."
- "Here's the part most people get wrong."
- "Now — if [X] is dead, what's alive? This."
- "So before I show you what works, you need to understand why most people never get there."
- "That's the problem. Here's the pattern that solves it."

### Parallel Item Rhythm Check
Every item in both lists should follow the same spoken rhythm. Read them aloud. If one sounds different from the others, rewrite it. The rhythm IS the format.

### Title Ideas
1. "[X] Is Dead in 2026 (Here's What Works)"
2. "Stop Doing [X] — Do This Instead"
3. "The [X] Problem Nobody's Talking About"

### Thumbnail Moments
- Reaction shot at the contrarian hook claim
- The pivot question (text on screen, strong expression)
- One item from the solution list with the result visible

### Total Estimated Length: [X minutes]
```

---

### Step 3 — Apply Narrative Principles

Apply the Kallaway dopamine ladder:

1. **Stimulation** — the hook (visual stun gun, first 1-2 seconds)
2. **Captivation** — plant the core curiosity question early
3. **Anticipation** — build toward the key reveal (don't give the best insight first)
4. **Validation** — deliver the payoff (must be non-obvious)
5. **Affection** — honest limitations, personal experience (likability)
6. **Revelation** — big-picture closer that reframes everything

**Curiosity loops per section:**
- Each section opens a mini-loop (question/tension) and closes it
- Best sections close one loop while opening the next

**Fifth-grade reading level for spoken content.** Short sentences. Common words. Define technical terms immediately.

### Step 4 — Time Budget

- **Hook:** 30-90 seconds (never longer)
- **Individual section:** 2-4 minutes each
- **Demo segments:** 3-7 minutes
- **Outro:** 30-60 seconds

If outline runs long, cut the weakest section rather than rushing everything.

### Step 5 — Competitive Check

```bash
python3 ~/.claude/skills/yt-search/scripts/search.py <topic> --count 10 --months 3
```

Add 2-3 entries to Production Notes.

### Step 6 — Save

Save to `~/content/YYYY-MM-DD-<slug>-outline.md`.

## Key Principles

- **Outlines are for speaking, not reading.** Every talking point is something you would say to a client or on a call. If it sounds like a blog post, rewrite it.
- **Every loop opened must close.** Run the loop audit before delivering. An unclosed loop is a broken promise to the viewer.
- **Lists give the viewer something to track.** Name the count upfront. Every item gets named before it gets explained. The structure is the retention mechanism.
- **Language is 5th grade.** Short sentences. One idea per sentence. Numbers not adjectives. No hedging.
- **Every section needs a real anchor.** Real person, real number, real situation. No hypotheticals.
- **Every section earns its spot.** If it doesn't advance a loop or advance the list, cut it.
- **The proof anchor goes first.** Story before the list. It makes everything that follows credible.
- **CTA is always the verbatim offer.** Use the user's **Default-CTA** and **Offer** from the brand profile — lead with the outcome, point to the product. Never a lead magnet as the primary close.
- **Honest limitations build trust.** At least one "here's where this breaks down" or "this only works if..." per video.
