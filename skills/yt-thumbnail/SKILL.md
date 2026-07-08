---
name: yt-thumbnail
description: "Generate high-CTR 16:9 4K YouTube thumbnails from a video transcript using Gemini image generation and your own reference photo. Auto-selects the 3 best thumbnail styles for the video (framework totem, old-vs-new split, dual-hold tool comparison, sleeping-notification proof, word provocation, logo crown, and more), writes a matched YouTube title + thumbnail copy for each, then renders them. Use when the user says /yt-thumbnail, 'generate a thumbnail', 'make a thumbnail for this video', or pastes a transcript and wants thumbnail options."
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
metadata:
  argument-hint: "video transcript (paste inline), or YouTube URL"
  user-invocable: true
---

# YouTube Thumbnail Generator

Generate high-impact 4K 16:9 YouTube thumbnails from a video transcript using Gemini image generation. Most styles place *you* (from your reference photo) in the frame, so the thumbnails look like your channel.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

This skill also needs a **reference photo** of the person who appears in the thumbnails. If the brand profile has no "reference photo path" saved, ask for one and save it back. The face styles will not render without it.

## Requirements
- **Google GenAI API key** in `GOOGLE_API_KEY` (environment variable or a `.env` file in the working directory). If not set, I'll tell you to add it.
- Python packages: `google-genai`, `pillow`, `python-dotenv`, `requests`. Install with `pip install google-genai pillow python-dotenv requests`.
- For a YouTube-URL input: `youtube-transcript-api` (`pip install youtube-transcript-api`).
- **Style B** (old-vs-new) can auto-source screenshots via Playwright — optional (`pip install playwright && playwright install chromium`); if absent it falls back to a generated panel.

## Config (environment variables)
Set these once (in your shell profile or a `.env` file):
- `YT_THUMBNAIL_REFERENCE` — path to your face/reference photo (this is your brand-profile "reference photo path").
- `YT_THUMBNAIL_LOGOS_DIR` — a folder of tool/company logo PNGs (used so logos reproduce accurately). Optional.
- `YT_THUMBNAIL_MODEL` — image model id (default `gemini-3.1-flash-image-preview`).

---

## Workflow

1. **Parse transcript** — extract core theme, steps/framework, tools mentioned, key metrics
2. **Map logos** — match tools to available logo files (if a logos folder is set)
3. **Select 3 styles** — score transcript signals, pick top 3 (see Auto-Style Selection)
4. **Generate paired titles** — one YouTube title + one thumbnail copy per style, each a different angle
5. **Build prompts** — read each style's template from `references/`, fill placeholders
6. **Generate thumbnails** — run Gemini for all 3 styles in parallel
7. **Present results** — show all 3 images with style name, thumbnail copy, and paired YouTube title

---

## Step 1: Parse Transcript

Extract:
- **Core theme** (1 sentence)
- **Key steps or concepts** (become totem level labels for A/H styles)
- **Tools and companies** mentioned (match to logos)
- **Key metrics** (follower counts, revenue figures, time — used in F-style notification and proof-angle titles). Pull these from the transcript; for a channel-level credibility number fall back to your brand-profile Proof field.
- **Emotional angle** (what does the viewer want to feel — ahead, capable, passive income, informed?)
- **Proof point ranking** — explicitly rank every credibility signal by specificity. A non-round number beats a round one. A timeframe beats a vague claim. A named tool beats a category. The #1 proof point from this list must anchor at least one thumbnail's copy — regardless of which style gets selected.

If the user provides a YouTube URL instead of a transcript:
```bash
pip install -q youtube-transcript-api 2>/dev/null
python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
import re
video_id = re.search(r'(?:v=|youtu\.be/)([^&\n?#]+)', 'VIDEO_URL').group(1)
transcript = YouTubeTranscriptApi.get_transcript(video_id)
print(' '.join([t['text'] for t in transcript]))
"
```

---

## Step 2: Map Logos

If you have set a logos folder:
```bash
ls "$YT_THUMBNAIL_LOGOS_DIR"
```

Note which tools have matching logo files. If no file exists, describe the tool by its visual identity (color, letter, icon shape) in the prompt instead.

---

## Step 3: Select 3 Styles

**Default behavior:** Auto-select — do NOT ask the user to choose.

Score signals from the transcript:

| Signal detected | Primary style | Why |
|-----------------|---------------|-----|
| Video has 3-5 named levels / steps / a framework | **H** | Most personal version of the framework visual |
| Transcript has a specific follower/revenue/metric | **F** | Notification popup = proven format, highest CTR for outcomes |
| Exactly 2 tools compared or integrated | **C** | Dual-hold is the direct "A + B" visual |
| 3+ tools mentioned prominently | **I** | Logo crown = social proof arc, "my stack" feel |
| Feature reveal / slash command | **D** | App window = curiosity + tool-specific hook |
| Opinion / strong take / identity content | **G** | Word-provocation mode, face + 2-4 words |
| Before/after / replacement story | **B** | Old vs New split panel |
| Walkthrough / explainer / multi-use-case | **E** | Whiteboard teaching energy |

**Tie-breaking:** Prefer visual diversity — never pick two styles that look similar (e.g. A + H are both totem-based, only pick one). When signals tie, pick the style with the most visual contrast vs others already selected.

**Example — "4 Levels of a Framework" (a 1,200 → 14,000 subscriber growth story):**
- Slot 1: **H** (framework with levels)
- Slot 2: **F** (+12,847 followers metric = notification format)
- Slot 3: **I** (three tool logos in an arc — visually distinct from H and F)

---

## Step 4: Generate Paired Titles

**Read `references/title_rules.md` before writing anything.**

Each style gets its own YouTube title + thumbnail copy — a matched one-two punch pair. Three styles = three different title angles. Never use the same title across variants.

The thumbnail copy catches the eye at scroll speed (emotion, no context needed). The YouTube title earns the click by answering or deepening the question the thumbnail raised. They should never repeat the same words.

**Copy decision order — proof point first, format second:**

Start from the #1 proof point identified in Step 1. Ask: which copy format makes this proof point hit hardest at scroll speed? Let that answer drive the format choice. Then check the style-to-copy table below to confirm the format fits the style — if it doesn't, pick the style that fits the format, not the other way around. Specificity always beats a vague identity hook. A non-round number in the thumbnail copy will outperform a clever phrase almost every time.

**Style-to-copy pairing:**

| Style | Thumbnail copy angle | Best thumbnail formats |
|-------|---------------------|----------------------|
| A / H (totem) | Outcome after mastering the system | Number Drop, Stop/Start, Kill the Subscription |
| C (dual-hold) | The combination creates something new | The Formula (Tool + Tool = Result), Emotion + CTA |
| F (sleeping) | No overlay text — the notification metric IS the copy | Use a specific non-round number in the notification |
| G (word) | Identity-level provocation | The Accusation, The Verdict, Command |
| I (logo crown) | Social proof endorsement | Social Proof, The Formula, blunt banner text |
| D (app window) | Feature curiosity | Feature Name Only, The Insider |
| E (whiteboard) | Teaching credibility | Number Drop, The Insider |
| B (old vs new) | Replacement story | The Displacement, Stop/Start, Kill the Subscription |

State each pairing before generating: `H [Number Drop]: thumbnail copy "NO AUDIENCE / $9,000" → title "I Made $9,000 in Digital Products (No Audience)"`

**Always pick the strongest proof point for F-style.** The notification metric is the entire message — use the highest-credibility, most specific number from the transcript (e.g. $2,547/month over $91 in a slow month).

---

## Step 5: Output Path + File Naming

**Save thumbnails in the same directory as the transcript source.**

- If the user provided a transcript file path → save in that folder
- If the user pasted the transcript inline → ask where to save before generating

**File naming:** Use the YouTube title exactly as the filename — title case, spaces, parentheses allowed. No dashes, no slugs. This lets you copy-paste the title directly from the filename.

Format: `[YouTube Title Here].jpg`

Rules: match the YouTube title exactly (Title Case), omit colons if present (macOS path separator conflict), no version suffixes needed.

---

## Step 6: Build Prompts + Generate

For each selected style, read its template from `references/style_[x]_template.md` and fill the placeholders. Then generate:

```bash
cat > /tmp/yt_thumbnail_[style]_prompt.txt << 'PROMPT'
[filled prompt]
PROMPT

python3 ~/.claude/skills/yt-thumbnail/scripts/generate_thumbnail.py \
  --prompt-file /tmp/yt_thumbnail_[style]_prompt.txt \
  --logos [Tool1] [Tool2] \
  --output "/path/to/folder/[YouTube Title Here].jpg"
```

**Logo passing rules:**
- Always pass `--logos` for any style that references a specific tool icon
- For F (sleeping notification): pass `--logos [AppName]` — the script injects the logo as Image 2, reference it in the prompt as "Image 2" without describing its appearance (let the reference do the work)
- For G (word provocation): no logos needed
- For E (whiteboard): no logos needed — any mascot is drawn, not reproduced

---

## Step 7: Scan Outputs for Typography Errors

After generating, **view each image** using the Read tool and check for:

1. **Duplicated text** — any word or line appearing more than once (Gemini hallucinates this with 2-line copy)
2. **Garbled numbers** — dollar signs split from values ("+$,8,947" instead of "+$8,947"), commas in wrong positions
3. **Missing text** — copy that was specified in the prompt but didn't render
4. **Wrong notification format** — F-style: number must be inside the notification card, not floating separately
5. **Face legibility** — your face must always be fully legible and recognizable at thumbnail size. In Riso or graphic styles, the face must remain photorealistic — do NOT apply halftone, ink filters, or 2-color treatment to the face. Only the background, clothing, and graphic elements receive the stylized treatment.

**If any issue found:** regen that thumbnail only. Add this block to the start of the prompt to suppress duplication:

```
TYPOGRAPHY RULES — READ FIRST:
- The ONLY text in this image is: [list each line exactly once]
- Each line appears EXACTLY ONCE. Do not repeat any text element anywhere in the image.
- Do not add a dollar sign before a number that already contains one (e.g. "$9K" not "$ $9K")
- Render text elements in the EXACT positions specified — do not echo them above or below
```

Regen with this block prepended, then re-scan. Repeat once more if still broken before flagging to the user.

---

## Step 8: Present Results

Show all 3 images. For each, state:
- Style name and why it was selected
- Thumbnail copy used
- Paired YouTube title

Then ask: Want to regenerate any of these, adjust copy, or try a different style?

---

## Style Reference

| ID | Style | Person | Background | Objects | Best for |
|----|-------|--------|------------|---------|----------|
| **A** | Digital Tactile Minimalism | Fully 3D modular character | Bright eggshell-white textured paper | 4-level modular totem with logo blocks | Frameworks, levels, systems |
| **H** | Hybrid | Photorealistic | Dark cinematic bokeh | Real hands holding 3D modular totem | Same as A but more personal |
| **C** | Cinematic Dual-Hold | Photorealistic | Dark cinematic bokeh | Two large glowing 3D app icons, one per hand | Tool comparisons, "A + B" |
| **D** | App Window + Face | Photorealistic, peeking right | Dark navy | Mac browser window + terminal slash command | Feature reveals, slash commands |
| **E** | Whiteboard + Face | Photorealistic, centered | Dark navy + whiteboard | Hand-drawn icons + arrows, mascot, bottom text bar | Explainers, system walkthroughs |
| **F** | Sleeping / Notification | Photorealistic, face-down asleep | Dark warm interior bokeh | Floating phone notification with logo + specific metric | Automation, passive income |
| **G** | Word Provocation | Photorealistic, extreme close-up | Dark charcoal / plain black | 2-4 words only | Opinion, identity, takes |
| **I** | Logo Crown | Photorealistic, centered | Dark charcoal / navy | Tool logos arcing above head, solid bottom banner | Tool roundups, "my stack" |
| **B** | Old vs New Contrast | No person | Light grid paper | Two split screenshot panels, red X, yellow arrow | Before/after, replacement stories |
| **J** | Grid Paper | Photorealistic, centered | Light off-white grid paper | Bold dark text directly on background, optional marker arrows | Outcome/proof, comparisons, visual diversity from dark set |
| **K** | Whiteboard Number | Photorealistic, left side | Light/natural, whiteboard right | One giant handwritten number/word on physical whiteboard | Single big proof point, credibility, teaching energy |

---

## Riso Style — Face Rule (CRITICAL)

When generating any Riso / graphic poster style thumbnail, your **face must always remain photorealistic**. Do NOT apply halftone filters, 2-color ink treatment, or any stylization to the face itself. The riso aesthetic (halftone dots, limited ink palette, paper texture, grain) applies only to: the background, clothing, body below the neck, and graphic/type elements. The face stays fully photorealistic and legible.

**Prompt pattern for Riso face:** "The face and glasses are rendered photorealistically — full color, sharp, natural skin tones. The riso/halftone treatment applies to the background, clothing, and graphic elements only. The face must be immediately recognizable at thumbnail size."

This rule applies to ALL styles — if a style produces a face that is illegible, halftoned, or over-stylized, regen with this correction added.

---

## Competitor Intelligence (proven thumbnail formulas)

**Notification / outcome formula:** Specific non-round numbers (never round), relaxed expression, one bold accent color, tool logos as social proof. The sleeping-notification thumbnail is one of the most replicable high-CTR formats for outcome/passive-income videos. Always use the strongest available metric — specificity = credibility.

**Word-provocation formula:** 2-4 words, period at end = punch, dark background only, face is the only visual. Sells identity, not outcomes. Expression must match copy tone exactly — smirk for provocation, neutral for verdict.

**Key distinction:** the notification format sells outcomes (numbers, passive income); the word format sells identity (who you become). Most channels need both depending on video type — match the style to the video's emotional angle, not just the topic.
