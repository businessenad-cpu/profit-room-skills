---
name: yt-titles
description: Generate high-performing YouTube title ideas from your video content, cross-referenced with your own channel's recent top-performing videos and competitor titles. Use this skill whenever the user wants YouTube title suggestions, asks "what should I title this video", "give me title ideas", "title options for my video about...", "help me name this video", brainstorming video titles, or any request involving YouTube title generation or optimization.
---

# YouTube Title Generator

Generate YouTube title options by analyzing what's already working on your channel and applying those patterns to new content.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

This skill needs your **YouTube channel** (a `@handle` or channel URL). If it's not in your brand profile's social handles, ask once and save it back.

## Requirements
- `yt-dlp` on PATH (`pip install yt-dlp`) for pulling channel + competitor data. If it's missing, I'll tell you the one command to add it.

## Workflow

### Step 1: Pull your channel performance data

```bash
python3 ~/.claude/skills/yt-titles/scripts/channel_performance.py --channel @yourhandle --months 3 --count 30
```

Use the channel handle from your brand profile (or set the `CHANNEL` env var once so you can drop the flag). Returns recent videos sorted by views with views/day, engagement ratio, and like ratio.

If you have no channel yet, skip this step and lean on competitor analysis (Step 3) plus the title principles below.

---

### Step 2: Analyze title patterns

From the top 10 performers, identify:
- **Hooks**: Opening words that pull people in ("I built...", "Stop...", "How I...")
- **Structure**: Format patterns ("Hook + specific outcome", "Number + result")
- **Length**: What character count range works
- **Specificity signals**: Tools by name, time frames, dollar amounts, results
- **Emotional triggers**: Curiosity gaps, contrarian takes, urgency

Also note bottom performers — what to avoid.

### Step 3: Scout competition

```bash
python3 ~/.claude/skills/yt-search/scripts/search.py <topic keywords> --count 10 --months 3
```

Avoid duplicating existing titles, find angles competitors missed, identify high-performing framings.

### Step 4: Generate titles

**10-15 options in three tiers:**

**Tier 1 — High Confidence (3-5)**
Follow proven patterns. Safe bets.

**Tier 2 — Calculated Risks (3-5)**
Remix successful patterns with competitor angles. Higher ceiling.

**Tier 3 — Swing for the Fences (3-5)**
Contrarian angles, pattern breaks, untested formats. Testing these is how channels grow.

Each title gets a one-line note: what pattern it's based on and why it works for this content.

### Title principles

- **Front-load the hook** — first 3-5 words determine if someone reads the rest
- **Specific > vague** — "I Automated My Entire Business in 4 Hours" beats "How to Use AI for Business"
- **Keep it under 60 characters** — longer titles truncate on mobile
- **Avoid clickbait that can't deliver** — respect the audience's intelligence
- **Match search intent when relevant** — but don't force SEO at the expense of CTR
- **Title Case** reads better in YouTube's UI
- **Honor your brand-profile words-to-avoid** — never use phrasing the user has asked you to avoid

### What NOT to do
- No generic filler: "Ultimate Guide", "Everything You Need to Know"
- Don't start with the channel name
- One emoji maximum (if any)
- No brackets like [FULL GUIDE] or [2026] — they waste character space

### Thumbnail text principles

2-5 words max. Creates a curiosity gap WITH the title — never restates it.
- **The test**: if the thumbnail text could be a subtitle of the title, it's wrong. It should add new information the title withholds.
- Thumbnail text answers a question the title *raises* — or reveals the *how/what* the title teases
- ALL CAPS reads better on thumbnails at small sizes
- Emotion/reaction words work: "WAIT WHAT", "GAME OVER", "IT'S FREE"
- Concrete numbers: "$0/month", "10 MINUTES", "7 SKILLS"

## Output format

```
## Your Top Performers (last 3 months)
[Brief summary — top 5 with views and what title patterns stand out]

## Competitor Landscape
[What's already out there, what angles are open]

## Title Options

### Tier 1 — High Confidence
1. **Title Here**
   Based on: [pattern] — [why it works]

### Tier 2 — Calculated Risks
...

### Tier 3 — Swing for the Fences
...

## Thumbnail Text Options

### For: "[Title 1]"
1. **[2-3 WORDS]** — [why this works with the title]
```

After presenting, ask if the user wants to refine any direction or generate variations on a specific title.
