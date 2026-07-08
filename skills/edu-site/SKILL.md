---
name: edu-site
description: Turn a GitHub repo URL or a research topic into a complete single-page riso-print educational website that makes a technical subject instantly graspable for a non-technical reader. Use when the user says /edu-site, "make an explainer site for this repo", "turn this topic into a teaching page", "build an educational landing page about X", or pastes a GitHub URL and wants it explained visually. Handles research, plain-English translation, 6 generated infographics, and a finished HTML page.
---

# Edu-Site Generator

Turn a GitHub repo URL or a research topic into a complete riso-print editorial education site — a single-page explainer that makes a technical subject instantly graspable for a non-technical reader.

**Invocation:** `/edu-site [github-url or topic description]`

**Output:** A complete single-file HTML saved to `~/Desktop/[topic-slug]/index.html` plus generated infographics in the same folder.

---

## Step 1 — Research

**If given a GitHub URL:**
Use WebFetch or firecrawl to read:
- The repo README (the core explanation)
- The About/description field (one-line summary)
- Stars, forks, release version (social proof numbers for the hero)
- Key file structure (tells you what kind of thing it is)
- Any linked docs site

Extract: what it does, what problem it solves, what's new/notable about it, who built it and why that matters.

**If given a topic/prompt:**
Use WebSearch to understand:
- What is this thing actually? (not marketing — the real mechanics)
- Who built it and why they're credible
- What problem it solves and what existed before
- Why it matters right now (timing signal)
- 2-3 concrete examples a non-developer can grasp

---

## Step 2 — Audience Translation

The audience is **non-developers who use AI tools** — smart, business-minded people building brands and businesses with AI, but not technical. If a brand profile exists at `~/.claude/brand-profile.md`, use its Audience field to tune this; otherwise assume this general non-technical builder.

**Before writing a single word, translate every concept through this filter:**

| Raw technical fact | Audience translation |
|---|---|
| "native binary compilation" | "runs 100x faster than existing tools" |
| "typed error returns" | "when it breaks, it fixes itself and tries again" |
| "capability-based permissions" | "you see exactly what it can access before it runs" |
| "structured JSON output" | "AI reads the result perfectly — no guessing" |
| "WebAssembly target" | "runs anywhere, no setup required" |

Translation rules:
- Never use developer jargon without immediately translating it
- Always answer "so what does that mean for me?" explicitly
- Connect to tools they already use — Claude Code skills, AI agents, everyday apps
- Frame everything as outcomes and time saved, not technical specs
- Use numbers when possible: "100x faster", "thousands of calls", "2ms vs 200ms"

---

## Step 2.5 — Copy Voice

Every word on this site must pass these rules. Apply them before writing any section content.

**Reading level: 5th grade.** If a 10-year-old couldn't understand a sentence, rewrite it. Short words. Short sentences. One idea at a time.

**WITFM first.** Every bullet, heading, and card answers "what's in it for me?" before anything else. Lead with the outcome, not the explanation. Wrong: "Ruflo uses a modular agent architecture." Right: "Your AI agents work together without breaking."

**Opinion before explanation.** State the point first, then support it. Never bury the lead. Wrong: "There are several factors that make this worth watching." Right: "This changes how AI agents communicate. Here's why."

**One job per section. No redundancy.** Each section covers one angle and one angle only. If two sections say the same thing, cut the weaker one. The narrative arc is: credibility → what it is → why it matters now → how it works → the problem → the fix → the stakes → the signal. Don't revisit a point once it's made.

**Bullet copy rules:**
- Max 2 sentences per bullet
- Lead with the outcome or the problem — never with "this tool..."
- No em dashes anywhere, ever
- No parenthetical asides — if it needs a note, write a second sentence
- Concrete and specific beats vague and general: "saves 3 hours" beats "saves time"

**Heading rules:**
- Ask a question or make a claim — not a label
- "Why your AI keeps breaking" beats "The Problem"
- Max 8 words
- Sentence case for headings, ALL CAPS for Anton display type only

**What to avoid:**
- Technical acronyms without explanation (API, JSON, CLI, SDK)
- "Leverages," "enables," "facilitates," "utilizes" — use plain verbs
- Passive voice: "is built" "was designed" — say who did what
- Double adjectives: "powerful, flexible framework" — pick one or use neither
- Any summary of what the previous section said

---

## Step 3 — Generate the Content Outline

Fill in this 9-section structure. Every section has a defined job — don't skip or merge them. Each section covers one angle exactly once. Never repeat a point made in a previous section.

```
SECTION: WHO IS [COMPANY/CREATOR]
Job: Establish credibility. Make the reader think "okay, this person/company is worth listening to."
Content: 3 bullets — what they've built that matters, their track record, one proof point
Copy tone: Matter-of-fact. Name the things they've shipped. No hype.
Format: bullets with company logo if available

SECTION: INTRO — [THEY JUST LAUNCHED X]
Job: Name the thing and give the 30-second pitch. First impression.
Content:
  - Big Anton headline: "THEY JUST LAUNCHED [NAME]."
  - Subhead: plain English — what type of tool + who it's for (one line)
  - Screenshot of the real thing (GitHub page, product, etc.)
  - 1 bullet: one sentence, what it does in plain language
  - 4 VALUE PROP CARDS — the key outcomes, not the features. "Your agents stop breaking" not "modular protocol design."
  - 1 closing bullet: why this matters right now, specific to the viewer
Copy tone: Direct. Outcome-first. No technical description in any card.

SECTION 01: THE HOOK
Job: Make the reader feel the timing. Why is this a signal worth paying attention to right now?
Content: 3 bullets — what makes this notable, why now, why most people haven't seen it yet
Closer: Pullout quote — a one-liner that reframes the whole thing. Historical analogy or bold claim.
Copy tone: Confident. Slightly urgent. This is the "lean in" moment. Don't repeat the intro.

SECTION 02: WHAT [X] ACTUALLY IS
Job: Explain the mechanics — once, clearly, connected to something they already know.
Content:
  - Heading: a plain-English label for what this thing is (not the brand name)
  - Image: system diagram infographic
  - 3 bullets: how it works — plain English, connected to familiar tools they use
  - Image: tools/skills connection infographic
Copy tone: Calm and clear. Teacher voice. No assumptions about what they know.
Do NOT: repeat the "why it matters" pitch from the Intro or Hook.

SECTION 03: THE PROBLEM WITH [CURRENT SITUATION]
Job: Make them feel the pain of the before-state. The itch before the scratch.
Content:
  - Heading: name the failure mode directly. "When [X breaks], [consequence]."
  - Image: before/after or diagnostic infographic
  - 4 bullets: specific failures of the current approach — each one a felt frustration
Copy tone: Empathetic and honest. Name real problems. No vague "challenges."
Do NOT: describe the solution here — that's the next section.

SECTION 04: HOW [X] SOLVES THIS
Job: The payoff. One solution per problem from Section 03.
Content:
  - Heading: "[X] fixes this. Here's how."
  - 3 bullets: one per solution, concrete, specific, plain language
Copy tone: Confident. Direct. The reader should feel relief.
Do NOT: introduce new problems or re-explain what the tool is.

SECTION 05: THE [FUTURE/SCALE] STAKES
Job: Zoom out. This isn't just useful today — missing it will cost them tomorrow.
Content:
  - Heading: contrast now vs. then ("Right now you're watching. In [year], you'll be behind.")
  - Stat block: a before/after number that makes the scale tangible
  - 5-6 bullets: what changes at scale — keep each to one sentence
  - Image: scale infographic
Copy tone: Stakes-driven. Not fear-mongering — logical consequence.
Do NOT: repeat the solution mechanics. Focus on what happens at scale.

SECTION 06: THE SIGNAL
Job: What does this launch actually mean? What are they betting on?
Content:
  - Heading: "[Company] doesn't build things without a reason."
  - 5-6 bullets: read the market signal, what this bets on, what it means for the viewer specifically
  - Image: signal/bet infographic
Copy tone: Analytical. Like a smart friend reading between the lines.
Do NOT: summarize earlier sections. This is new information — the strategic read.

CLOSING CALLOUT
Job: The one thing to remember. Single screenshot-worthy statement.
Content: 3 short lines, centered, stacked. Final line all-caps + large + accent color.
Formula: "[What they're doing now] is the foundation. [This] is the ceiling. [IDENTITY STATEMENT.]"
Examples: "YOU ARE EARLY." / "YOU'RE ALREADY HERE." / "THE WINDOW IS OPEN."
Copy tone: Bold. Earned. Don't qualify it.
```

---

## Step 4 — Generate Infographics

Use Higgsfield CLI to generate 6 riso-print infographics. Make sure the Higgsfield CLI is installed and authenticated first (see Requirements at the bottom). If your API key lives in an env file, source it before running, e.g. `set -a && source ~/.env && set +a`.

Submit all 6 jobs in parallel (background), then wait for each individually:

```bash
JOB1=$(higgsfield generate create nano_banana_2 --aspect_ratio "16:9" --prompt '[PROMPT_1]' 2>&1 | tail -1)
JOB2=$(higgsfield generate create nano_banana_2 --aspect_ratio "16:9" --prompt '[PROMPT_2]' 2>&1 | tail -1)
JOB3=$(higgsfield generate create nano_banana_2 --aspect_ratio "16:9" --prompt '[PROMPT_3]' 2>&1 | tail -1)
JOB4=$(higgsfield generate create nano_banana_2 --aspect_ratio "16:9" --prompt '[PROMPT_4]' 2>&1 | tail -1)
JOB5=$(higgsfield generate create nano_banana_2 --aspect_ratio "16:9" --prompt '[PROMPT_5]' 2>&1 | tail -1)
JOB6=$(higgsfield generate create nano_banana_2 --aspect_ratio "16:9" --prompt '[PROMPT_6]' 2>&1 | tail -1)

URL1=$(higgsfield generate wait $JOB1 2>&1 | tail -1)
URL2=$(higgsfield generate wait $JOB2 2>&1 | tail -1)
URL3=$(higgsfield generate wait $JOB3 2>&1 | tail -1)
URL4=$(higgsfield generate wait $JOB4 2>&1 | tail -1)
URL5=$(higgsfield generate wait $JOB5 2>&1 | tail -1)
URL6=$(higgsfield generate wait $JOB6 2>&1 | tail -1)

curl -L "$URL1" -o ~/Desktop/[slug]/01_hook.png
curl -L "$URL2" -o ~/Desktop/[slug]/02_system.png
curl -L "$URL3" -o ~/Desktop/[slug]/03_skills.png
curl -L "$URL4" -o ~/Desktop/[slug]/04_problem.png
curl -L "$URL5" -o ~/Desktop/[slug]/05_scale.png
curl -L "$URL6" -o ~/Desktop/[slug]/06_signal.png
```

### Infographic design rules

Apply the same principles as the copy — before writing any prompt.

**One job per image.** Each infographic visualizes exactly one idea. If you could describe two infographics with the same sentence, redesign one of them.

**Value at a glance.** A viewer should understand the point in under 3 seconds without reading the surrounding page copy. The image must stand alone.

**No redundancy across the set.** The 6 images tell a visual arc: announcement → what it is → who it connects to → the problem → the stakes → the signal. Each image picks up where the last one left off. Never repeat a visual concept already shown in an adjacent image.

**Max 5 elements per image.** A headline, 2-3 supporting elements, and one dominant visual anchor (big number, arrow, split field, or grid). More than 5 and nothing reads.

**One dominant layout per image.** Either a split field, a big number, a before/after, or a grid. Never combine two layout patterns in the same image.

**Specificity beats generality.** Replace placeholder labels with real content from the research. "115K clones in 14 days" beats "key stats." Real numbers are always more persuasive than generic labels.

**Anti-redundancy check — run before submitting prompts:**
- Does 01 introduce something that 02 re-introduces? Cut the overlap from 02.
- Does 04 (before/after) show the same pain as 03 (tools)? Redesign one.
- Does 06 (signal) summarize what 05 (stakes) already showed? Make 06 forward-looking instead.

---

### Prompts by infographic

**01 — Hook Announcement:**
```
Editorial riso-print infographic poster. 16:9. Left 60% solid orange (#E96A3C) field, right 40% warm cream (#E8DCC4). Massive Anton heavy condensed headline "[TOPIC NAME]" in cream uppercase spanning both fields, bleeding left edge. Below on orange: "[COMPANY]" in small cream JetBrains Mono caps. Right panel: 3 bullet points in charcoal mono caps showing key signals, each preceded by "//". Charcoal bottom strip full-bleed: "[ONE-LINE HOOK — what this changes for a non-technical builder]" in cream mono caps. Metadata bottom left orange panel: "NO. 01 / [DATE]" in tiny cream mono caps. Heavy grain texture. No gradients. Orange, cream, charcoal only. Print-first riso aesthetic.
```

**02 — What X Is (System Diagram):**
```
Editorial riso-print infographic poster. 16:9. Full warm cream (#E8DCC4) background. Orange (#E96A3C) header bar full-bleed: "WHAT [X] ACTUALLY IS" in large Anton cream uppercase. Below: two charcoal-bordered boxes side by side. Left box header "INPUT" with icon of scattered notes/text. Center: large orange right-pointing arrow. Right box header "OUTPUT" with icon of clean organized result. Labels underneath each box in JetBrains Mono charcoal caps. Bottom: one plain-English sentence in charcoal body text explaining what it does. Heavy grain texture. No gradients. Orange, cream, charcoal. Print-first riso aesthetic.
```

**03 — Skills/Tools Connection:**
```
Editorial riso-print infographic poster. 16:9. Solid orange (#E96A3C) background. "ALREADY IN THIS WORLD" in large Anton cream (#E8DCC4) uppercase top-left, bleeding off left edge. Below: 4-5 cream boxes with charcoal borders arranged in a horizontal row, each labeled with a skill/tool name in JetBrains Mono charcoal caps, connected by cream arrows. Bottom cream strip: short mono caps explanation. Heavy grain texture. No gradients. Cream and charcoal on orange. Print-first riso aesthetic.
```

**04 — Before/After Problem:**
```
Editorial riso-print infographic poster. 16:9. Left half cream (#E8DCC4) background, right half orange (#E96A3C). Left panel header "BEFORE" in Anton charcoal uppercase: 3 X-marked lines in charcoal mono caps showing the broken state, dense layout. Right panel header "AFTER" in Anton cream uppercase: 3 checkmark lines in cream mono caps showing the fixed state, open layout. Bold charcoal vertical dividing line center. Heavy grain texture. No gradients. Two-ink riso aesthetic.
```

**05 — Scale / Stakes:**
```
Editorial riso-print infographic poster. 16:9. Warm cream (#E8DCC4) background. Orange header bar: "THE SCALE PROBLEM" in Anton cream uppercase. Center: massive Anton charcoal number "[SMALL NUM]" on left, large orange right-pointing arrow, massive Anton orange number "[BIG NUM]" on right. Below: two-column comparison table — "TODAY" vs "[YEAR]" — each with 3 bullet points in JetBrains Mono charcoal caps. Charcoal bottom strip: scale label in cream mono caps. Heavy grain texture. No gradients. Print-first riso aesthetic.
```

**06 — The Signal:**
```
Editorial riso-print infographic poster. 16:9. Solid orange (#E96A3C) background. "THE SIGNAL" in massive Anton cream (#E8DCC4) uppercase bleeding off top edge. Below: 2x2 grid of cream boxes with charcoal borders. Each box: short charcoal Anton label + 1-sentence Inter body in charcoal. Bottom charcoal strip full-bleed: "WHAT THIS MEANS FOR YOU" in cream JetBrains Mono caps. Heavy grain texture. No gradients. Cream and charcoal on orange. Print-first riso aesthetic.
```

Fill in `[TOPIC NAME]`, `[COMPANY]`, `[X]`, numbers, and date from the actual research before generating.

Save all as `01_[slug].png` through `06_[slug].png` in `~/Desktop/[topic-slug]/`.

---

## Step 5 — Build the HTML

Copy the base template `template.html` (shipped alongside this skill) to the output folder.

Fill in every `<!-- SLOT: ... -->` comment with the generated content following the template structure.

**Repo link:** If the subject has a GitHub repo, add the `↗` link directly beneath the screenshot image in the INTRO section (see template slot). Format: `// GITHUB.COM/ORG/REPO ↗`. If no repo, remove the anchor entirely.
**Hero stats:** Use 3 real proof points — all must build credibility. Good options: GitHub stars, launch date, forks, downloads, contributors, company track record stat. Avoid vanity metrics (commit count, version number) that mean nothing to a non-developer audience.
**Title:** `[TOPIC] // [CREATOR] // [YEAR]`

**Screenshare legibility:** This site is often presented on screen. Never use `--ink-paper-shadow` (#C9BDA0) for primary readable text. Use `--ink-charcoal` on light surfaces, `--ink-paper` on dark surfaces.

---

## Aesthetic Reference

The full aesthetic is defined in the shipped `template.html`. The RISO-print tokens below are the canonical spec. Key rules if you ever write custom HTML:

**Colors:**
- `--ink-orange: #E96A3C` — primary warm. Hero fields, accent lines, hover states.
- `--ink-paper: #E8DCC4` — cream substrate. Page background, hero text.
- `--ink-charcoal: #1C1B17` — structural ink. Body text, borders, dark blocks.
- `--ink-bone: #F2E9D6` — secondary paper. Card backgrounds.
- `--ink-paper-shadow: #C9BDA0` — aged paper. Muted labels, dividers.
- `--ink-orange-soft: #F4A584` — halftone tint. Subtle accents only.
- `--ink-amber: #F0B24A` — highlight only. Use sparingly as punctuation.

**Fonts:** Anton (display, all-caps) + JetBrains Mono (all labels, meta, chapter numbers) + Inter (body copy)

**Component vocabulary:**
- Hero: full orange field, Anton display title, grain overlay, right-edge ticker strip
- Chapter labels: `01 / SECTION NAME` in JetBrains Mono orange + charcoal rule
- Bullets: `//` prefix in orange, slide-right + sweep-line on hover
- Cards: 2×2 grid, bone background, orange top sweep on hover
- Statement blocks: charcoal background, `OUTPUT` label in orange, cream Anton text
- Pullout quotes: orange left border, Inter body
- Stats: giant Anton number, orange `→` arrow, mono label
- Images: 2px charcoal border, no decorative corners
- Section connectors: static charcoal vertical line between sections

**Print aesthetic rules:**
- Grain overlay on body (SVG turbulence, 0.12 opacity, multiply blend)
- Never pure white or pure black — use paper and ink tokens only
- Orange fields get cream text; cream fields get charcoal text
- 70/25/5: dominant ink ~70%, paper ~25%, detail marks ~5%

**Screenshare legibility:** This site is often presented on screen. On cream backgrounds, body text uses `--ink-charcoal` at full opacity. On charcoal blocks, use `--ink-paper`. Never use a muted color for primary readable text.

---

## Step 5.5 — Editorial Review Pass (REQUIRED before output)

After the HTML is written, run this review before opening the browser. This is not optional. Catching these issues after the fact wastes a full editing session.

### Redundancy audit

Read every section heading and first sentence in sequence. Ask: does this section teach something the reader doesn't already know from the previous one?

**Patterns that always indicate redundancy:**
- INTRO cards define the thing → Section 02 defines the thing again → cut the definitions from one. Cards should be labels/teasers only (3-5 words). Full definitions belong in one place.
- Problem section references what each model/tool does → Definition section explains what each model/tool does → merge them into one section: pain first, table second.
- The same anchor stat appears more than once (e.g. "90% of your work" used in 4 bullets). Pick the one place it lands hardest. Cut the rest.
- A pullout restates the heading it sits under. If you can summarize both in one sentence, cut the pullout or rewrite it to add new information.

**Merge test:** If two adjacent sections could be summarized with the same sentence, merge them. Use the pain/problem as the opener, the definition/solution as the closer. One dark section, one flow.

### Feature discipline (REQUIRED — run before writing any section after the Intro)

Each specific feature of the product gets exactly ONE home on the page. After you've placed a feature, it may appear in passing (≤5 words) elsewhere but never gets another full bullet or explanation.

**The rule:**
- If a feature has an INTRO card → that card is its home. Every other section may name it once in a list but never elaborate again.
- If a feature appears in Section 03 (Problem) as a full bullet → it may not also have a full bullet in Section 04 (Solution). Map them 1:1, not 1:2.
- If a feature appears in Section 02 as a bullet → it may not re-appear as a dedicated bullet in 05 or 06.

**Before writing each section, run this check:**
1. List every feature you plan to mention in that section.
2. For each one, ask: where did I already give this a full explanation?
3. If it already has a home, cut it to a passing reference or cut it entirely.
4. If it has no home yet, this section can be its home.

**Example of the failure pattern to avoid:**
- Email has a dedicated INTRO card → Section 02 bullet 1 mentions email → Section 03 has a full problem bullet about email → Section 04 has a full solution bullet about email → Section 05 lists email in two bullets → Section 06 mentions email drafts. That is 7 mentions. The card is the home. Everything else is noise.

**Diversity check:** After writing all sections, list every feature mentioned. If any one feature appears more than 3 times total (including its home), cut the excess. If any major feature of the product has 0 mentions, add it — the site should be comprehensive, not a deep-dive on one capability at the expense of others.

### Jargon audit

Scan for any term a non-developer might not know on first read. Flag it. For each flagged term:
- Is it translated inline? ("agent" → "a sequence of steps your AI runs on its own")
- Is the stat meaningful without context? ("84% score" = meaningless; "4x fewer mistakes" = clear)
- Does the technical name actually need to appear, or can you just use the plain-language version?

**Terms that always need translation:**
- benchmark → "a test where..."
- agent / agentic → "a task your AI runs on its own, step by step"
- parallel / concurrent → "multiple tasks at the same time"
- tokens → "words processed" or just omit
- API, CLI, SDK → translate or cut entirely for non-developer audience
- "runs without you" → too vague. Say what that means: "works through 20+ steps without you reviewing each one"

### WIIFM audit

Read every bullet and card body. The payoff — why the reader should care — must appear in the first sentence, not the last. If the bullet explains what something is before saying why it matters, flip the order.

**Self-congratulatory lines to cut immediately:**
- "There's been no guide like this — until now."
- "This is the first time anyone has..."
- Any closer that compliments the site itself rather than giving the reader something

### Hover legibility check

Dark sections (`section--dark`) flip bullet backgrounds to cream on hover. The text color must also switch to charcoal. Verify `.section--dark .bullets li:hover` includes `color: var(--ink-charcoal)`.

### Color legibility check

`--ink-paper-shadow` (#C9BDA0) must never be used for body text or labels on cream backgrounds. Replace with `color: var(--ink-charcoal); opacity: 0.5` for muted labels, or full charcoal for readable copy.

### Hero stats size check

Hero stat numbers (the 3 proof points at the bottom of the hero) must be large enough to read as display elements — minimum 72px, same Anton font as the title. Stat labels use the meta font at minimum 13px. Small stats in the hero look broken; if they feel like fine print, double the size.

---

## Audience Value Checklist

Before finalizing, verify every section answers one of these:

- **"Why does this exist?"** — Section: WHO IS + INTRO
- **"What is it actually?"** — Section: WHAT X IS or merged PROBLEM + GUIDE
- **"Why is what I have now broken?"** — Section: THE PROBLEM
- **"How does this fix it?"** — Section: THE SOLUTION
- **"Why does it matter at scale?"** — Section: THE STAKES
- **"What should I do with this information?"** — Section: THE SIGNAL + CLOSING

If any of these questions isn't answered, the site is incomplete.

**Copy quality check — run on every bullet:**
1. Does it answer "what's in it for me" in the first 5 words?
2. Is it under 2 sentences?
3. Would a non-technical person understand it immediately?
4. Does it have a specific outcome, number, or named tool — not vague language?

If any answer is no, rewrite before moving on.

---

## Output

Save to: `~/Desktop/[topic-slug]/index.html`

Open in browser to verify before reporting complete.

---

## Requirements

- **Higgsfield CLI** — used to generate the 6 riso-print infographics (`higgsfield generate ...`). Install and authenticate it per Higgsfield's docs. If it isn't available, tell the user what to install, or skip the infographics and leave labeled image slots in the HTML so they can drop images in later.
- **WebFetch / web search** — to research the repo or topic. Built in.
- No API keys are embedded in this skill. If your Higgsfield key lives in an env file, source it yourself before running.
