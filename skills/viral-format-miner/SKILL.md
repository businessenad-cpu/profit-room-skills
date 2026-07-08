---
name: viral-format-miner
description: "Turn a viral video FORMAT into new shootable content, two ways: REMIX one proven video into the user's own niche, or REVERSE-ENGINEER the repeating pattern across a batch of outlier videos into a reusable format brief plus 3 new concepts. Always ends with a script/shot list ready to shoot or generate. Trigger on /viral-format-miner, 'remix this video', 'steal this format', 'find the pattern across these viral videos', 'mine this niche for a format', or 'turn these outliers into a video concept'."
allowed-tools: Bash, Read, Write, WebSearch, WebFetch, mcp__claude_ai_vidIQ_for_Claude__vidiq_outliers, mcp__claude_ai_vidIQ_for_Claude__vidiq_breakout_channels, mcp__claude_ai_vidIQ_for_Claude__vidiq_channel_stats, mcp__claude_ai_vidIQ_for_Claude__vidiq_similar_channels, mcp__claude_ai_vidIQ_for_Claude__vidiq_ig_outlier_reels_search, mcp__claude_ai_vidIQ_for_Claude__vidiq_video_transcript, mcp__claude_ai_vidIQ_for_Claude__vidiq_video_watch, mcp__claude_ai_vidIQ_for_Claude__vidiq_channel_videos
metadata:
  argument-hint: "/viral-format-miner [niche] [remix|reverse-engineer]"
---

# Viral Format Miner

This is a FORMAT-recreation skill, not a topic-ideation skill. It finds a proven STRUCTURE (hook type,
pacing, visual style, payoff) and rebuilds new content on top of it, either from one reference video or
from the repeating pattern across a batch of outliers.

## Personalization
This skill rebuilds proven formats for *your* niche. Before running, load the brand profile at
`~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your niche and audience).
- Default target niche = the user's own (from the profile) unless they name a specific client or niche.
- Never invent view counts, subscriber counts, or results — pull them live via vidIQ or ask the user to
  paste them.

## Requirements
- **vidIQ MCP** (optional but recommended) — powers the live outlier/breakout/transcript pulls in Mode 2
  and video lookups in Mode 1. If it's not connected, I'll fall back to WebSearch/WebFetch and ask you to
  paste the transcript or video results directly. I'll tell you exactly what's missing when it matters.

Two modes. Ask which one if it isn't clear from the request, plus the target niche.

---

## Mode 1 — REMIX (one video → one rebuild)

**Input needed:** one reference video. The user pastes its transcript/description, names it (title +
channel), or gives a URL.

### Step 1 — Get the source material
- If pasted: use as-is.
- If named/URL only: try `vidiq_video_transcript` or `vidiq_video_watch` first. Fall back to
  WebFetch/WebSearch if it's not a YouTube video vidIQ can resolve (e.g. an Instagram Reel — describe
  what's visible from search results and ask the user to paste the caption/hook if a transcript isn't
  available).

### Step 2 — Deconstruct the structure
Extract these five things from the source, not the topic itself:
1. **Hook type** — what happens in the first 3 seconds (cold-open result, contrast statement, visual
   shock, question, POV drop-in)
2. **Pacing** — average shot length, cut frequency, where it slows down vs. speeds up
3. **Visual style** — cinematic/AI-generated, talking head, screen recording, b-roll heavy, on-screen
   text density
4. **Payoff structure** — where and how the hook's promise gets paid off (twist at the end, escalating
   reveals, single big reveal)
5. **Length + beat count** — total runtime and how many distinct beats/shots it breaks into

### Step 3 — Rebuild for the user's niche
Keep the five structural elements identical. Swap every piece of content: the subject, the visuals, the
specific words. Write a one-line mapping table before the rebuild:

```
| Original beat | What it did | Your swap |
```

### Step 4 — Output: shootable script/shot list
Go straight to the **Output Format** below.

---

## Mode 2 — REVERSE-ENGINEER (batch of outliers → new pattern → 3 concepts)

**Input needed:** a batch of videos in the niche. Either the user pastes vidIQ outlier/breakout results,
or the skill pulls them live.

### Step 1 — Get the batch (live pull if the user hasn't pasted results)
Run in parallel, scoped to the niche:
- `vidiq_breakout_channels` — channels currently spiking in the niche
- `vidiq_outliers` — individual videos outperforming their channel norm
- `vidiq_similar_channels` — if the user names one breakout channel, find its peers to widen the sample
- `vidiq_channel_stats` — confirm scale on any channel worth citing as proof
- `vidiq_ig_outlier_reels_search` — if the niche lives on Instagram/Reels instead of YouTube

Pull at least 6-10 videos across 2-3+ channels. A pattern from one channel is a style, not a format —
the whole point of this mode is cross-channel repetition. (Example of the kind of proof to cite: a
channel jumping from ~44K to ~89K subs and 21M to 41M views in a month off 16 videos — real numbers,
pulled live, never invented.)

### Step 2 — Extract the repeating pattern
For each video note: hook type, pacing, visual style, payoff structure (same five-part lens as Mode 1,
skip length if not visible). Then look ACROSS all of them and answer:
- Which hook type shows up in 3+ of them? (that's the format's hook, not any single video's hook)
- What's the shared pacing signature? (fast-cut cinematic, slow single-take reveal, etc.)
- What's the shared visual style? (AI-generated cinematic shorts, real footage, screen recording, etc.)
- What's the shared payoff structure?
- What's different from video to video? (this tells you what's actually variable — the part you get to
  make original)

Do not just list the batch. The deliverable is the DISTILLED, reusable pattern.

### Step 2b — Format Brief (output this before the concepts)

```
### FORMAT BRIEF: [name the format in one line]

**Proof it works:** [channel(s) + hard numbers, pulled live]
**Recurring hook type:** [pattern, not one example]
**Recurring pacing:** [pattern]
**Recurring visual style:** [pattern]
**Recurring payoff structure:** [pattern]
**What varies (your original space):** [the slot every creator fills differently — this is where your
  niche content goes]
```

### Step 3 — 3 new concepts from the pattern
Generate 3 video concepts for the target niche that follow the format brief exactly on
hook/pacing/visual style/payoff, varying only the "what varies" slot. Each concept gets a one-line
premise before the full shot list (Output Format runs once per concept, or once for whichever concept
the user picks if they want to narrow first — ask only if there are 3+ concepts and no clear favorite).

---

## Output Format (both modes end here — always shootable)

```
## [Title / working name]

**Format source:** [reference video name, OR "pattern from: Format Brief above"]
**Niche target:** [the user's own / client name]
**Runtime target:** [seconds]

### Shot List

| # | Duration | Visual (what's on screen) | Hook/VO/caption line | Notes (pacing/transition) |
|---|---|---|---|---|
| 1 | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... |

### Hook (word for word)
[The exact opening line(s), matching the source's hook type]

### Payoff (word for word or described)
[How it resolves, matching the source's payoff structure]

### Production handoff
- **Visual generation:** which style fits — cinematic AI shorts (image/video gen tools), talking-head
  (avatar or self-filmed), or screen-based (screen recording).
- **Cut/caption:** your usual editing pipeline (any editor that does captions + cuts).
- **Aspect ratio:** 9:16 default for shorts/reels unless the source is long-form.
```

## Principles

- Format, not topic. Never let this skill drift into "here's a video idea" — it must always name the
  structural beats it's preserving.
- REMIX preserves one video's structure. REVERSE-ENGINEER preserves what's PROVEN ACROSS MULTIPLE videos
  — never generalize a pattern from a single example in that mode.
- Every run ends with an actual shot list, not just a concept description, unless the user says they only
  want the Format Brief (Mode 2) or the deconstruction (Mode 1).
- Cite real numbers only when proof exists — pull them live via vidIQ or ask the user to paste them.
  Never invent view counts or sub counts.
