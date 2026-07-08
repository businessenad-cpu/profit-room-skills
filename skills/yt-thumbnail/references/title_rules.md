# YouTube Thumbnail Copy Rules

## The One Rule
Describe what the viewer will **feel after watching** — not what the video contains.
- "SKILLS 2.0" = what it is ❌
- "YOU'VE BEEN DOING IT WRONG" = how they'll feel ✅

## Hard Limits
- **Max 5 words** — non-negotiable
- **Two weights**: small/light for context word, LARGE/HEAVY for the power word
- **One accent color** on the tension word only
- **Never**: How To, Tutorial, Tips, Guide, Introduction
- **ALL CAPS** reads better at small sizes

## Three Structures (pick one, never mix)
1. **The Accusation** — YOU'RE [doing something wrong] → pairs with smirk/challenge expression
2. **The Verdict** — [Thing] is [strong judgment] → short, declarative, forces click to understand
3. **The Displacement** — [Old thing] → [New thing] or I REPLACED [X] → before/after or replacement story

---

## Important: Thumbnail Copy vs YouTube Titles

These are two different things — never mix them:

- **YouTube title** = single sentence, Title Case, no slashes, under 60 chars. Parentheticals allowed and common: `I Grew 14,000 LinkedIn Followers in 90 Days (Using Claude)`
- **Thumbnail copy** = 2-5 words ALL CAPS on the image, slash = line break between Line 1 and Line 2. Never a full sentence.

The slash `/` in examples below = thumbnail line break. It does NOT appear in YouTube titles.

---

## The One-Two Punch Rule

**Thumbnail is the first read** — catches the eye at scroll speed. Pure emotion or reaction, no context needed.
**Title is the second read** — viewer pauses, reads it. Earns the click by answering the question the thumbnail raised, or raising a new one the video answers.

The test:
- If the thumbnail alone tells the whole story → title is redundant
- If the title alone does everything → thumbnail isn't working
- Best pairs: thumbnail creates the **feeling**, title provides the **frame**

Always generate thumbnail copy and YouTube title as a matched pair. Examples:
- Thumbnail: `10X IN 90 DAYS` → Title: `I Got 14,000 LinkedIn Followers in 90 Days Using Claude` *(what's the 10x? → followers, here's the tool)*
- Thumbnail: `+12,847 followers` (notification, no overlay) → Title: `Claude Grew My LinkedIn While I Slept` *(number hooks, title explains the angle)*
- Thumbnail: `THIS SH*T WORKS` → Title: `The 4-Level Claude System That Actually Grows LinkedIn` *(social proof bait → here's the specific thing)*

**Never repeat a word from the thumbnail copy in the title.** They should each add new information.

---

## Title Angles (YouTube titles — full sentences)

| Angle | Structure | Example |
|-------|-----------|---------|
| **Proof** | Specific result + timeframe + tool | "I Got 14,000 LinkedIn Followers in 90 Days Using Claude" |
| **Contrarian** | Challenges a belief the viewer holds | "LinkedIn Growth Has Nothing to Do With Posting More" |
| **Curiosity** | Creates a question, withholds the answer | "Claude Let Me Grow LinkedIn Without Creating Content" |
| **Direct/Clear** | States exactly what it is — specific enough to earn the click | "The 4 Levels of Claude for LinkedIn" |
| **Free** | Something valuable, available for free | "The Free Claude System That Grows LinkedIn on Autopilot" |
| **Confession** | Embarrassing admission that reframes the viewer's situation | "I Wasted a Year on LinkedIn Before I Found This" |
| **Kill the Subscription** | Ditching a paid tool for something better | "I Cancelled LinkedIn Premium and Used Claude Instead" |
| **Insider** | What experts actually do vs what they say | "What LinkedIn's Top Creators Actually Use" |
| **Formula** | Tool + tool = specific result | "Claude + LinkedIn = 14,000 Followers in 90 Days" |
| **Warning** | Stakes-driven, consequence of inaction | "The Reason Your LinkedIn Will Never Grow" |
| **Displacement** | Old approach replaced by new one | "Why I Stopped Posting on LinkedIn (And What I Do Instead)" |
| **Parenthetical** | Main hook + clarifying reveal in parens | "I Grew 14,000 LinkedIn Followers in 90 Days (It's Free)" |

---

## Thumbnail Copy Formats (image overlays — ALL CAPS, slash = line break)

| Format | Structure | Example |
|--------|-----------|---------|
| **Emotion + CTA** ⭐ | [REACTION WORD] / [ACTION] | "HLY SHT / TRY THIS" |
| **Kill the Subscription** ⭐ | I QUIT [TOOL] / [WEAPON] | "I QUIT PREMIUM / 1 SKILL" |
| **Stop/Start** ⭐ | STOP [BAD THING] / DO [GOOD THING] | "STOP POSTING / USE LEVELS" |
| **Number Drop** | [NUMBER] / [WHAT IT IS] | "14,000 / FOLLOWERS" |
| **Social Proof** | [BLUNT ENDORSEMENT] | "THIS SH*T WORKS" |
| **Feature Name Only** | /command or TOOL NAME | "/linkedin" or "4 LEVELS" |
| **The Formula** | [TOOL] + [TOOL] = [RESULT] | "CLAUDE + LINKEDIN = 10X" |
| **The Insider** | WHAT [AUTHORITY] ACTUALLY [DO] | "WHAT PROS ACTUALLY USE" |
| **The Upgrade** | [OLD] → [NEW] | "POSTING → SYSTEM" |
| **Stakes + Warning** | WARNING / [THING] | "WARNING / READ THIS" |

## Top 3 for your Niche (what's converting now)
1. **Kill the Subscription** — audience has paid tools they resent
2. **Stop/Start** — creates urgency + clear contrast
3. **Emotion + CTA** — title does the informational heavy lifting, thumbnail creates urgency

## Typography Anti-Repetition Rule
When specifying multi-line text in a prompt, explicitly state:
- The exact line order (Line 1: X, Line 2: Y)
- "Appears ONCE only — do not repeat any line elsewhere in the image"
- Gemini will duplicate lines if given any ambiguity (e.g. "above or below") — always specify exact position

## Two-Weight Typography Rule (for prompt building)
In the prompt, always specify:
- The "power word" (1-2 words) = large, heavy, accent color (orange by default — see exception below)
- The "context words" = smaller, lighter weight, white
- Example: `"10X" large orange accent, "IN 90 DAYS" smaller white text`

## Accent Color Rule — Three-Way System
The accent color on the power word signals its emotional charge. Default palette is terracotta/burnt orange — so the accent must contrast against it:

| Signal | Color | Hex | Examples |
|--------|-------|-----|---------|
| **Negative / warning** | Bright red | `#E0201A` | WRONG, BROKEN, DON'T, STOP, QUIT, NEVER, DEAD, FAILED |
| **Positive outcome / money** | Bright green | `#22C55E` | 10X, $10K, PROFIT, FREE, WIN, GREW, +12K |
| **Neutral / energy** | Orange (default) | `#F0764A` | FASTER, SYSTEM, FILES, LEVELS, EVERYTHING |

Rules:
- If the power word involves a dollar amount, follower count, or multiplier → green
- If the power word signals something bad, broken, or to avoid → red
- Everything else → orange
- Never use orange as the accent when the background is already orange/terracotta — it will disappear
