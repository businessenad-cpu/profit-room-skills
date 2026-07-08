# RISO / Editorial Poster Mode

A print-first, editorial "concept poster" carousel rendered slide-by-slide by Higgsfield `nano_banana_2` from per-slide text prompts. **No JSON spec** — skip the renderer scripts and use the workflow below. Best when you want a brand-forward, stands-out-in-feed aesthetic. Follow the **Narrative First** spine from SKILL.md Step 4 — the cream/orange fields just alternate for rhythm, they don't dictate content.

## Design system
- Two-ink logic: orange `#E96A3C`, warm paper/cream `#E8DCC4`, charcoal `#1C1B17`
- Display type: heavy condensed (Anton-style), UPPERCASE
- Meta labels: mono caps, small, wide tracking
- Heavy riso grain on every surface. No gradients. Print-first.

Adjust these tokens to your own brand palette if you have one in your profile; the two-ink + grain structure is what makes it read as "riso".

## Optional brand art
Any logo or mascot is **optional and user-supplied** — this skill ships no logo art. If you have one, set env `BRAND_LOGO` to its path (or add a `Logo-path` field to your brand profile) and pass it as a `--image` reference on the cover slide so `nano_banana_2` renders the real art instead of hallucinating one. If you don't, generate covers with no reference — the type-driven cover works on its own. Never bundle a third party's logo or trademark into the repo; point `BRAND_LOGO` at your own file.

## Workflow

**1. Confirm Higgsfield is available:**
```bash
higgsfield account status
```

**2. Write per-slide prompts** using the templates below, filling `[BRACKETED]` fields from the transcript/topic.

**3. Submit all slides in parallel, each writing to its OWN zero-padded file.** This is the fix for out-of-order carousels: with background `&`, stdout interleaves and you can't tell which job ID belongs to which slide. Redirect each job to `jobs/NN.out` so slide index → job ID is locked by filename, never by completion order.
```bash
SLUG=YYYY-MM-DD-topic
mkdir -p ~/content/$SLUG/jobs ~/content/$SLUG/slides
JOBDIR=~/content/$SLUG/jobs
# Optional brand art on the cover only — your own logo, if you have one:
LOGO="${BRAND_LOGO:-}"

# Cover → pass your brand art as a reference if you set BRAND_LOGO; otherwise drop --image.
if [ -n "$LOGO" ]; then IMG=(--image "$LOGO"); else IMG=(); fi
higgsfield generate create nano_banana_2 --aspect_ratio "4:5" "${IMG[@]}" --prompt '[SLIDE_1_COVER_PROMPT]' > "$JOBDIR/01.out" 2>&1 &
# Body slides → no --image (keep them clean type fields).
higgsfield generate create nano_banana_2 --aspect_ratio "4:5" --prompt '[SLIDE_2_PROMPT]' > "$JOBDIR/02.out" 2>&1 &
# ... 03, 04, 05 ... one per slide.
wait
```

**4. Extract the job ID per slide from its file, then wait per slide** (safe because the index lives in the filename):
```bash
for f in "$JOBDIR"/*.out; do
  n=$(basename "$f" .out)
  JOB_ID=$(grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' "$f" | head -1)
  higgsfield generate wait "$JOB_ID" 2>&1 | grep -oE 'https?://[^ ]+' | tail -1 > "$JOBDIR/$n.url"
done
```
(Simpler alternative: add `--wait` to each create call in step 3 and grep the URL straight out of each `NN.out`.)

**5. Download in numeric order:**
```bash
for u in "$JOBDIR"/*.url; do
  n=$(basename "$u" .url)
  curl -fsSL "$(cat "$u")" -o ~/content/$SLUG/slides/slide-$n.jpg
done
```
`slides/slide-01.jpg … slide-NN.jpg` are now guaranteed in carousel order. Then hand off to your scheduler (see SKILL.md Step 7).

## Slide prompt templates
Fill `[BRACKETED]` fields. Alternate cover Variant A/B across carousels for variety.

**Cover — Variant A (orange top / cream bottom):**
```
Editorial riso-print poster cover. Horizontal split: top 60% solid orange (#E96A3C), bottom 40% warm cream (#E8DCC4). Subtle crosshatch grid texture on both. On the orange top: large bold condensed uppercase cream (#E8DCC4) type, left-aligned — hook "[HOOK]" then smaller cream subline "[SUBLINE]". Single graphic element centered on the cream section straddling the split: [a simple icon or your logo]. Bottom-right: bold right-pointing arrow in charcoal. Heavy riso grain. No gradients. No badge/pill/other elements. Print-first riso aesthetic.
```

**Cover — Variant B (cream top / orange bottom):**
```
Editorial riso-print poster cover. Horizontal split: top 60% warm cream (#E8DCC4), bottom 40% solid orange (#E96A3C). Subtle crosshatch grid. On the cream top: large bold condensed uppercase charcoal (#1C1B17) type, left-aligned — hook "[HOOK]" then smaller charcoal subline "[SUBLINE]". Single graphic element centered on the orange section straddling the split: [icon or logo], cream (#E8DCC4). Bottom-right: bold right-pointing arrow in cream. Heavy riso grain. No gradients. Print-first riso aesthetic.
```

**Slide 2 — Problem (cream field):**
```
Editorial riso-print poster interior slide. Full warm cream (#E8DCC4) background. Large bold charcoal (#1C1B17) condensed headline: "[PROBLEM — 4-8 words, UPPERCASE]". Short orange (#E96A3C) rule beneath. Center: 2-3 short mono-caps charcoal lines listing [pain points], each with a bold X mark. Bottom-right arrow, bottom-left slide counter "[N]/[TOTAL]" in mono caps. Heavy grain. No gradients. Print-first.
```

**Slide 3 — System (orange field):**
```
Editorial riso-print poster interior slide. Full solid orange (#E96A3C) field. Large bold cream (#E8DCC4) condensed headline: "[SYSTEM TITLE — 2-5 words, UPPERCASE]". Short cream rule. Center: numbered mono-caps cream lines "01. [STEP]" / "02. [STEP]" ... left-aligned. Bottom-right cream arrow, bottom-left counter "[N]/[TOTAL]". Heavy grain. No gradients. Print-first.
```

**Slide 4 — Insight/step (cream field):**
```
Editorial riso-print poster interior slide. Full warm cream (#E8DCC4) background. Large bold charcoal condensed headline: "[INSIGHT — 4-8 words, UPPERCASE]". Short orange rule. 2-3 short charcoal mono-caps lines with sub-points. Bottom-right arrow, bottom-left counter. Heavy grain. No gradients. Print-first.
```

**Proof / stat slide (cream field, when you have a real metric):**
```
Editorial riso-print poster interior slide. Full warm cream (#E8DCC4) background. Massive bold charcoal condensed number "[STAT — e.g. 1,154 / 80% / 12x]" filling the upper half, bleeding off the top. Below in large orange condensed: "[STAT LABEL — 3-5 words]". Short orange rule, then 2-3 charcoal mono-caps proof lines. Bottom-right arrow, bottom-left counter. Heavy grain. No gradients. Print-first.
```
Use only real numbers from your brand profile — never invent a stat.

**CTA slide (orange field, final):**
```
Editorial riso-print poster final slide. Full solid orange (#E96A3C) field. Center: three stacked cream (#E8DCC4) words in massive condensed type — "SAVE" / "SHARE" / "FOLLOW" — each with a bold cream right-pointing arrow. Below in cream mono caps: "[YOUR CTA LINE — e.g. Comment KEYWORD for the full breakdown]". Bottom strip: solid charcoal (#1C1B17) bar with "[YOUR HANDLE]" in cream mono caps. Bottom-left counter above the strip. No swipe arrow (final slide). Heavy grain. No gradients. Print-first.
```

## Structure (7 slides)
| Slide | Field | Content (ONE idea each) |
|-------|-------|-------------------------|
| 1 Cover | split | Hook + subline + icon/logo + arrow |
| 2 Real problem | cream | One concrete, money-tied sentence (the misdiagnosis). No bullets. |
| 3 Why it fails | orange | The mechanism of the pain. Prose. |
| 4 The turn | cream | What you did instead — lead with a hard number if you have one. |
| 5 The System | orange | The ONE allowed list — numbered steps. |
| 6 Payoff / seed | cream | Relate the system to the reader's own channel/offer. |
| 7 CTA | orange | SAVE / SHARE / FOLLOW + your CTA |

Never duplicate a beat (no "plan" slide AND a "system" slide) and never make a second slide a list.
