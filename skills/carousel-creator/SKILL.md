---
name: carousel-creator
description: "Create high-impact Instagram carousel posts with branded slides. Use when: (1) user says /carousel or 'create a carousel', (2) user provides a topic, YouTube transcript, or lead magnet and wants it turned into a carousel, (3) user wants branded carousel slides for Instagram, (4) user has existing video clips and wants a video carousel with branded text overlays, (5) user says 'top repos this week/month' or 'trending GitHub repos' or provides a github.com repo URL. Handles: content writing, GitHub trending/repo analysis, image generation, text overlay rendering, video overlay burning via FFmpeg, and final slide output."
allowed-tools: Bash, Read, Write, Edit, WebSearch, WebFetch, Glob, Grep, Task
metadata:
  argument-hint: "topic, YouTube transcript, lead magnet reference, GitHub repo URL, or 'top repos this week'"
  user-invocable: true
---

# Carousel Creator

Create branded Instagram carousel posts from topics, YouTube transcripts, lead magnets, or GitHub repos.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

The profile supplies: your **tone/voice**, your **offer** (what you sell or your community), your **default CTA**, your **booking/link** destination, and your **proof** (a real win or number you can stand behind). Wherever this skill says "your offer", "your CTA", or "your proof", pull it from the profile — never hardcode.

## Requirements
- **Higgsfield CLI or MCP** — for photo covers (`gen_cover.py`) and the RISO/editorial render path. Graceful fallback: the default **alternating-solid** renderer (`render_solid.py`) needs **no API** and works fully offline.
- **ffmpeg** — video-carousel mode only (`brew install ffmpeg`).
- **Playwright MCP** — optional, for GitHub repo screenshots.
- **Pillow** — `pip install Pillow` (all rendering).

Never embed an API key in the repo. Higgsfield reads its own credentials from your shell/`~/` environment.

## Workflow
1. **Parse input** — identify source type and extract content
2. **Select style** — solid (default), photo overlay, RISO, or video
3. **Select framework** — choose a carousel blueprint
4. **Write slides** — slide-by-slide copy in your voice
5. **Generate the carousel JSON** — structured spec for the renderer
6. **Render slides** — run the appropriate renderer
7. **Publish / hand off** — slides saved locally; you post or schedule them

## Step 1: Parse Input

Determine input type:
- **Topic/idea** — short phrase → research with WebSearch first
- **YouTube URL** — fetch transcript (below), then analyze
- **Pasted transcript** — extract key insights, story, framework
- **Lead magnet** — the carousel promotes an existing free asset
- **GitHub trending / repo URL** — see `references/github-mode.md`

### YouTube Transcript Extraction
```bash
pip install -q youtube-transcript-api 2>/dev/null
python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
t = YouTubeTranscriptApi.get_transcript('VIDEO_ID')
print(' '.join(x['text'] for x in t))
"
```
No API key needed. If captions are disabled, ask the user to paste the transcript.

### Content Analysis (for transcripts)
Extract before writing slides:
1. **Main thesis** — one big idea, one sentence
2. **2-3 distinct angles** — each a standalone teaching moment
3. **3-6 quotable moments per angle** — short, punchy phrases
4. **Audience pain point** — what problem this solves
5. **Emotional hook per angle** — the tension or feeling

**Present angles to the user for approval before writing slides.**

### CTA mode
- **GitHub / lead-magnet carousel** → CTA = "Comment [KEYWORD] and I'll DM you [the thing]". Pick a random, memorable, unrelated keyword (e.g. `WAFFLE`, `TORCH`, `SUMMIT`) — never a topic word. If you use a comment-to-DM tool, check that keyword isn't already live in it.
- **Everything else** → CTA = your default CTA / offer (from the brand profile). "Link in bio" on the slide; the URL goes in the caption only.

Display before writing:
```
Carousel: {summary}
Style: {solid / photo / riso / video}
Framework: {chosen framework}
CTA: {your offer  OR  lead_magnet — KEYWORD}
Slides: {count}
Est. cost: $0.00 (solid) or ~${count * 0.13} (photo)
```
If `--count N` is set, generate N independent copy sets (different hook + framework each), present all for approval, then render.

## Step 2: Select Style

| Style | Renderer | Cost | Best for |
|-------|----------|------|----------|
| **Alternating solid** (default) | `scripts/render_solid.py` | $0.00 | How-tos, step-by-steps, informational, quick turnaround |
| **Photo overlay** | `scripts/generate_carousel.py` | ~$0.13/slide | Storytelling, personal brand, emotional impact |
| **RISO / editorial poster** | Higgsfield `nano_banana_2` | ~$0.03/slide | Brand-forward print aesthetic — see `references/riso-mode.md` |
| **Video clips** | `scripts/generate_video_carousel.py` | $0.00 | You have existing footage — burns branded overlay per clip |

**Default to alternating solid** for educational content. Use photo overlay for storytelling, RISO when asked for "poster/editorial/riso" style, video when the user supplies clips.

**Alternating solid** uses bold type on dark backgrounds (`#0A0A0A` / `#1A1A1A` / `#141414`) with a green accent, plus a warm-cream **light_pop** mode (`#E8DCC4` bg, charcoal text, orange accent). No image generation. See `references/brand-style.md`.

**GitHub source carousels**: solid body slides + a **photo cover** via `gen_cover.py`. See `references/github-mode.md`.

## Step 3: Select Framework
Read `references/carousel-frameworks.md` for slide-by-slide blueprints. Choose ONE:

| Framework | Best for |
|-----------|----------|
| Checklist / Audit | Actionable lists, "X things you need" |
| Myth vs Fact | Challenging beliefs, contrarian takes |
| Before / After (Reframe) | Transformations, "generic vs specific" |
| Step-by-step | How-to guides, processes, systems |
| Teardown | Analyzing what works, case studies |

## Step 4: Write Slides

### Hook first (always)
Lock the slide-1 hook before anything else. Start from your saved hooks if you have a swipe file, or write a fresh one.

**Formula: mechanism + outcome in one line.** The mechanism is the tool or system; the outcome is the result or tension. Both must be on slide 1.
- Bad: "Your AI marketing team starts here" — no mechanism, no outcome
- Bad: "One command" — mechanism only
- Good: "I went from 3 hours per post to 60 seconds with one command" — transformation + mechanism

The hook names the result and the tool that delivers it. It is not a teaser or a mystery. If the hook is weak, the carousel is dead — fix it before writing body slides.

### Length
Write **5-10 slides**: minimum 5 (cover + 3 body + CTA), sweet spot 7-8, max 10. Every slide earns its place or gets cut. Never pad.

### Narrative first — one big idea per slide (non-negotiable)
A carousel is a STORY, not a deck. Write the narrative spine first: the single sentence each slide adds. Each slide carries ONE big idea that only makes sense after the slide before it. If you can shuffle the slides without breaking the flow, rewrite.

**Every reader should feel themselves LEVELING UP** — each slide gives a sharper diagnosis, a hidden cause, a move, a system. By the final value slide they should feel a distinct **unlock**: "oh, THAT'S what was stopping me."

**Two failure modes to avoid:**
- **Restating** — two slides saying the same thing. Cut one.
- **List soup** — every slide a bullet list. Only ONE slide may be a list: the System slide. Every other slide is one concrete idea in prose.

Be clear and concrete. Tie it to money and stakes, not vague abstractions.

**Default narrative spine (adapt, keep the escalation):**
1. **Hook** — one sentence, under 12 words. Mechanism + outcome/tension.
2. **The real problem** — concrete, money-tied. The misdiagnosis.
3. **Why it fails** — the mechanism of the pain; make them feel the cost.
4. **The turn** — what you did instead. Lead with a hard result/number when you have one.
5. **The System** — the ONE allowed list. Numbered steps of the real build.
6. **The payoff / seed** — relate the system to THE READER's own situation; make the gap visible without selling.
7. **CTA** — hard CTA based on mode.

For shorter carousels merge adjacent beats, but never merge problem and payoff, and never duplicate a beat.

**Self-check before rendering:** read the slides as one paragraph. Does each line need the one before it? Anything repeat? More than one list? If yes, rewrite.

### Writing rules
- 6th-grade reading level — clarity, not complexity
- Specific > generic — name the real outcome, tool, and number
- Speak from experience, not at people; short lines, one thought per line
- **Double line break (`\n\n`) between every sentence** in body copy
- **Vary vocabulary across slides** — don't repeat the same core noun on every slide
- **Every claim must make literal sense** — read each line cold, fix logic
- **Proof slides: use an in-copy connector** for action→result (e.g. "I GAVE CLAUDE MY LIST = 1,154 REAL LEADS"). Keep the swipe arrow isolated bottom-right.
- Mark ONE key phrase per slide for accent: `{green}phrase{/green}` (photo) or the `accent_phrase` field (solid)
- Wrap italic lines in `*...*`
- Use emoji (👉) instead of unicode arrows
- **Numbered lists are for the System slide ONLY**
- **Max 4-5 body lines per slide** — split dense content into another slide

### Copy rules
- Follow the **brand voice** from your profile.
- **Use only real proof** — pull your proof/number from the profile; never invent a follower count, revenue figure, or member count.
- **CTA slide** → "Link in bio" (offer mode) or "Comment [KEYWORD]" (lead-magnet mode). Never put a raw URL on the slide; URL goes in the caption.
- Pick ONE CTA line / tagline from your profile that fits the carousel's topic.

## Step 5: Generate Carousel JSON

### Solid / photo spec
Save to `output/carousel_spec.json`:
```json
{
  "title": "Internal reference title",
  "style": "alternating_solid",
  "cta_mode": "offer",
  "cta_keyword": null,
  "cta_offer": null,
  "slides": [
    { "number": 1, "bg_mode": "dark",  "headline": "HOOK IN CAPS", "body": "", "accent_phrase": "KEY WORD" },
    { "number": 2, "bg_mode": "light", "headline": "SLIDE HEADLINE", "body": "Line one.\n\nLine two.", "accent_phrase": "phrase" },
    { "number": 7, "bg_mode": "gradient", "show_logo": true, "headline": "WANT THE SYSTEM?", "body": "Link in bio.", "cta_button": "Get it" }
  ]
}
```
- For photo overlay, use `shot_type` + `image_prompt` (generate, ~$0.13) or `library_image` (reuse, free) per slide, and `{green}...{/green}` accent markers. See `references/brand-style.md`.
- For `cta_mode: "lead_magnet"`, set `cta_keyword` and `cta_offer`.
- Full field list for the solid renderer (bg modes, `stat_value`, `cta_button`, `show_bookmark`, `github_card`, `bottom_summary`, `image_path`, `dark_card_text`, `cover_image_path`, `topic_label`, `step_label`): see `references/brand-style.md` and `references/github-mode.md`.

### Video carousel spec
Save to `output/video_carousel_spec.json`. Use `clip_path` (bare filename resolved from `BROLL_DIR`, or an absolute path):
```json
{
  "title": "…", "cta_mode": "offer",
  "slides": [
    { "number": 1, "type": "cover", "clip_path": "clip1.mp4", "headline": "HOOK", "body": "One-line payoff", "green_accent": "key phrase" }
  ]
}
```
- `body` is required on every slide (a one-line overlay looks thin). Headline ALL CAPS, one `green_accent` per slide. Audio is stripped; pre-trim clips.

## Step 6: Render Slides

Scripts live in `scripts/`. Output goes to `output/`. Set `CAROUSEL_ROOT` if you run from elsewhere (defaults to the skill root).

### Alternating solid (default, $0.00, offline)
```bash
cd <skill>/scripts
python3 render_solid.py ../output/carousel_spec.json
```
Progress bar + swipe chevron are automatic (last slide gets no chevron). Slides save to `output/slides/slide_XX.jpg` + `manifest.json`. To draw your logo lockup on `show_logo` slides, set `BRAND_LOGO` (image path) or `BRAND_NAME` (wordmark text).

### Photo overlay (~$0.13/slide)
Show the cost estimate first (only slides needing new generation count). Then:
```bash
CAROUSEL_ROOT="<skill>" python3 scripts/generate_carousel.py output/carousel_spec.json
```
Generates images via the Higgsfield backend, applies branded overlays, saves raw images to a local library for reuse, and writes final slides to `output/slides/`. For a `character` (CTA face) shot, set `BRAND_FACE` or `BRAND_PORTRAIT` to a portrait image path — if unset, the shot generates with no reference.

### Video clips ($0.00, needs ffmpeg)
```bash
BROLL_DIR="./b-roll/videos" python3 scripts/generate_video_carousel.py output/video_carousel_spec.json
```
Burns a gradient + branded text overlay (0.9 brightness + vignette + drop shadow) onto each clip. Saves silent MP4s to `output/video_slides/` + `manifest.json`.

### RISO / editorial poster
No JSON — slides are rendered individually by Higgsfield `nano_banana_2` from per-slide prompts. See `references/riso-mode.md` for the full workflow, prompt templates, and the parallel-render-order pattern.

## Step 7: Publish / Hand Off

Rendering is **local only** — nothing is uploaded automatically.

1. **Show results** — list `output/slides/` (or `output/video_slides/`) in order, total cost, and ask: regenerate any slides? adjust copy? ready to post?
2. **Write the caption** — no hashtags unless requested; expand on the content, conversational, in your voice.
   - Lead-magnet mode: open with "Comment [KEYWORD] and I'll send it to you."
   - Offer mode: soft close at the very end — one line about your offer + "Link in bio." Use only real proof from your profile.
3. **Post or schedule** — upload the slides in `output/slides/` to your Instagram scheduler (Meta, Later, Buffer, or similar) or post manually. Slides are numbered `slide_01…slide_NN` so carousel order is preserved.
4. **Lead magnet?** — if you use a comment-to-DM keyword, set that keyword and its DM copy up in your comment-to-DM automation tool. The keyword lives in the caption, not on the slide.

## Flags
| Flag | Default | What it does |
|------|---------|-------------|
| `--count N` | 1 | Generate N carousels on one topic, each a different hook + framework; all presented before rendering |
| `--slides N` | auto (5-10) | Target a specific slide count |
| `--cta "text"` | your default CTA | Custom CTA text for the final slide |

## Reference Files
- **references/brand-style.md** — colors, typography, solid-renderer fields, image-prompt templates
- **references/carousel-frameworks.md** — slide-by-slide framework blueprints
- **references/github-mode.md** — trending-repos + single-repo teardown carousels
- **references/riso-mode.md** — editorial/RISO poster render workflow
