---
name: yt-description
description: "Generate a high-converting YouTube description from a transcript with timestamps. Trigger on phrases like 'write a description for this video', 'generate a YouTube description', 'turn this transcript into a description', 'write the description', or any request to create a YouTube video description from a transcript or outline."
allowed-tools: Bash, Read, Write
user-invocable: true
metadata:
  argument-hint: "/yt-description [paste transcript or provide file path]"
---

# YouTube Description Generator

Generate a high-converting YouTube description from a transcript with timestamps. Produces a description that serves both the algorithm (SEO) and the viewer (hook + navigation + CTA).

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

Fields this skill uses: **Tone** and **Words-to-avoid** (applied to every line), **Offer** + **Booking/checkout link** + **Default-CTA** (for the CTA block).

## When This Skill Activates

**Activate when the user wants to:**
- Write a description for a video they just recorded or outlined
- Turn a transcript into a publishable description
- Get chapters auto-generated from a timestamped transcript

**Example triggers:**
- "Write a description for this video"
- "Generate a YouTube description from this transcript"
- "Turn this transcript into a description"
- `/yt-description` followed by a transcript or file path

---

## Step 0 — Load Voice

From the brand profile, extract the user's tone, words to avoid, and sentence-length preference. Apply them to every line of the description.

---

## Step 1 — Parse the Transcript

**If a file path is provided:** read the file.
**If the transcript is pasted inline:** use it directly.

From the transcript, extract:
1. **Core promise** — what transformation or result does the viewer get? (This drives the hook.)
2. **Primary topic keywords** — 3-5 words/phrases a person would search to find this video. Look for: tool names, problem names, outcome phrases, method names.
3. **Chapter moments** — identify 4-8 distinct topic shifts or sections. A chapter break happens when:
   - The speaker transitions to a new concept, step, or framework
   - There's a natural "okay so now..." or "let's talk about..." signal
   - A new list item or mistake begins
   - The story section starts or ends

---

## Step 2 — Name the Chapters

For each chapter moment identified in Step 1:

**Naming rules:**
- Default to **search-intent format** when the section covers a distinct method, concept, or how-to: "How to validate your offer in 24 hours"
- Use **label format** for intro/outro and transitional moments: "The mistake that ends businesses", "My first month: $35.14"
- Keep chapter names under 60 characters
- No generic names ("Introduction", "Part 1", "Conclusion") — every name should tell the viewer what they're about to learn or hear
- Write chapter names at 5th grade reading level — no jargon unless it's a search term

**Output format:**
```
0:00 - [Chapter name]
1:45 - [Chapter name]
...
```

---

## Step 3 — Write the Description

Output the description in this exact order:

---

### BLOCK 1 — Hook (shows before "show more")

2 lines max. This is the only thing most viewers read before clicking away or reading more.

**Rules:**
- Line 1: restate the core promise as a pain or problem the viewer already feels. Do NOT restate the title verbatim.
- Line 2: name what they'll walk away with — a specific result, method, or decision.
- No fluff openers ("In this video...", "Welcome to...", "Hey guys...")
- Pain-first, not topic-first
- 5th grade reading level
- No em dashes

**Example:**
```
Most builders spend months building and never get a single client. Here's the one fix that changes that, and it takes less than 24 hours.
```

---

### BLOCK 2 — Chapters

Paste the chapter list from Step 2.

---

### BLOCK 3 — CTA

One sentence. One link. No more. Use the user's **Offer**, **Default-CTA**, and **Booking/checkout link** from the brand profile. If those are blank, ask once (or omit the CTA rather than invent one).

**Template (fill from the brand profile):**
```
[One sentence naming who it's for + the outcome your offer delivers].
👉 [your booking/checkout link]
```

Do not add social links, newsletter links, or secondary CTAs. One destination.

---

### BLOCK 4 — SEO Paragraph

2-3 sentences. Weaves in the primary keywords from Step 1 naturally. Written as if explaining the video to someone who hasn't watched it — not a keyword dump.

**Rules:**
- Front-load the most searchable phrase in sentence 1
- Read like a human wrote it, not a keyword tool
- No hashtags in this block (hashtags go at the very end if used at all)
- 5th grade reading level

**Example:**
```
This video covers the three biggest mistakes builders make before landing their first client, including why building before validating is the single fastest way to waste six months. The Mom Test framework and five validation questions are the fix.
```

---

### BLOCK 5 — Hashtags (optional)

3-5 max. Only include if they're actually relevant search terms — not vanity tags.
Format: `#AIAutomation #ClaudeAI #PersonalBrand`

Place at the very bottom, after everything else.

---

## Output Format

Deliver the complete description as a single clean block, ready to paste into YouTube Studio. No section headers in the output — just the text.

Then below the description, show:
```
---
CHAPTER NAMES USED:
[list all chapters with timestamps]

PRIMARY KEYWORDS EXTRACTED:
[list the 3-5 keywords identified]
```

This lets you review the logic without it appearing in the final description.

---

## Quality Checks Before Delivering

- [ ] Hook does not repeat the title verbatim
- [ ] Hook is pain-first, not topic-first
- [ ] Every chapter name is specific (no "Introduction", "Part 1")
- [ ] At least half of chapter names use search-intent format
- [ ] CTA is exactly one link
- [ ] SEO paragraph reads like a human wrote it
- [ ] No em dashes anywhere
- [ ] No hedging language ("might", "could", "perhaps")
- [ ] No fluff openers
- [ ] Honors the brand-profile words-to-avoid
- [ ] Total description is under 5,000 characters (YouTube limit)
