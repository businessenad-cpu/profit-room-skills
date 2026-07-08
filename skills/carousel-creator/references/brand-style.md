# Carousel Style Guide

A layout, typography, and contrast system for carousel slides. It ships with a strong default palette (dark editorial + a warm "light_pop" cream mode), but **colors, logo, and CTA come from your brand profile** (`~/.claude/brand-profile.md`). Swap the hex values below for your own brand colors — the layout principles are what matter.

## Color System (default palette — override with your brand)

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Background | Near-black | `#0A0A0A` | All slide backgrounds, overlay backing |
| Primary text | Warm white | `#F5F0E8` | Headlines, body text |
| Accent | Neon green | `#00FF00` | ONE key phrase per slide — the most important concept |
| Secondary accent | Orange | `#FF6600` | Sparingly — numbers, stats, emphasis (optional) |
| Overlay backing | Black 70% | `rgba(0,0,0,0.7)` | Semi-transparent bar behind text on photo slides |

### Accent Rule

Every slide gets exactly ONE phrase highlighted in the accent color. This creates a visual throughline — as people swipe, their eye tracks the accent, which is always the core concept. Never highlight more than 3-4 words.

- **Photo overlay style**: Accent = neon green (#00FF00)
- **Alternating solid style**: Accent = neon green (#00FF00) on all slides; orange (#FF6600) on CTA slides only (button + numbers)

## Style: Alternating Solid

Bold typography on dark backgrounds. No photos, no image generation ($0.00 cost).

### Color Scheme

| Slide Mode | Background | Headline | Body | Accent |
|------------|-----------|----------|------|--------|
| `dark` | `#0A0A0A` near-black | `#F5F0E8` warm white | `#F5F0E8` warm white | `#00FF00` neon green |
| `light` | `#1A1A1A` subtle dark variant | `#F5F0E8` warm white | `#F5F0E8` warm white | `#00FF00` neon green |
| `cover` | `#141414` slightly lighter dark | `#F5F0E8` warm white | `#F5F0E8` warm white | `#00FF00` neon green |
| `gradient` | `#0A0A0A`→`#1C1C1C` subtle gradient | `#F5F0E8` warm white | `#F5F0E8` warm white | `#FF6600` orange (CTA slides) |

All slides are dark. `"light"` is a subtle dark variation, not a true light background. CTA slides use `"gradient"` bg_mode — subtle dark gradient with orange as the accent color (for buttons and numbers).

Slides alternate `dark`/`light` for body slides. First slide uses `cover`. CTA slide uses `gradient`.

### Renderer

Use `scripts/render_solid.py`. Run (from the skill root):
```bash
python3 scripts/render_solid.py output/carousel_spec.json
```

### JSON Spec Format (alternating solid)

```json
{
  "title": "Internal reference title",
  "style": "alternating_solid",
  "slides": [
    {
      "number": 1,
      "bg_mode": "dark",
      "headline": "HEADLINE\nIN CAPS",
      "body": "",
      "accent_phrase": "KEY WORD"
    }
  ]
}
```

Key differences from photo overlay spec:
- `style` field set to `"alternating_solid"`
- `bg_mode` instead of `shot_type` — alternates `"dark"` / `"light"`
- `accent_phrase` instead of `green_accent` — plain text, no `{green}` markers
- No `image_prompt`, `library_image`, `type`, or `shot_type` fields
- Headlines are ALL CAPS in the spec (renderer does not auto-capitalize)

## Typography

| Element | Font | Style | Size (at 1080x1350) |
|---------|------|-------|---------------------|
| Headline | Gotham Ultra | ALL CAPS | 88-120px (120px for cover/headline-only slides) |
| Body | Gotham Bold | Sentence case | 36-48px |
| Body italic | Gotham Bold Italic | Sentence case, italic | 36-48px |
| Accent text | Same font as context | Same style, accent color | Same as surrounding |

Font stack: Gotham Ultra/Bold/BoldIta → Arial Bold → system sans-serif.
Headline line height: 0.95x font size (tight stacking for impactful headlines).
Body line height: 1.5x font size.

### Italic Text

Wrap body lines in `*...*` markers to render in Gotham Bold Italic. Use for:
- Quoted prompts or commands (e.g., *"fix the login bug"*)
- Descriptive/explanatory annotations (e.g., *one-shot task*)
- Emphasis on key phrases

## Slide Layout Patterns

### Cover Slide (establishing/detail — text-dominant)
```
┌─────────────────────┐
│                     │
│   [DARK OVERLAY]    │
│                     │
│   HEADLINE IN       │
│   ALL CAPS          │
│   {green}KEY WORD{/green}│
│                     │
│   [Atmospheric      │
│    background]      │
│                     │
└─────────────────────┘
```
- Dark moody background — architecture, neon, shadows, textures
- Headline is the star, not the image. Text must be readable at thumbnail size.
- Only use a character shot on the cover for personal story carousels ("How I went from X to Y")

### Body Slide (text on dark photo)
```
┌─────────────────────┐
│                     │
│   HEADLINE          │
│                     │
│   Body line 1       │
│   Body line 2       │
│   {green}Accent{/green} line│
│   Body line 4       │
│                     │
│   [Photo visible    │
│    through overlay] │
└─────────────────────┘
```
- Semi-transparent black overlay over entire image
- Text left-aligned with generous left margin (~10% of width)
- Headline at top, body below with line spacing

### Text-Only Slide (no photo background)
```
┌─────────────────────┐
│  #0A0A0A solid      │
│                     │
│   HEADLINE          │
│                     │
│   Body line 1       │
│   Body line 2       │
│   {green}Accent{/green}│
│                     │
│                     │
│                     │
└─────────────────────┘
```
- Solid near-black background
- Clean, minimal, text does all the work
- Good for high-density information slides

### CTA Slide (character shot)
```
┌─────────────────────┐
│                     │
│   [DARK OVERLAY]    │
│                     │
│   CTA HEADLINE      │
│                     │
│   {green}Comment KEYWORD{/green}│
│   or                │
│   [Your offer name] │
│   Link in bio       │
│                     │
└─────────────────────┘
```
Pull the CTA line and offer name from your brand profile. Never hardcode a URL on the slide — the link lives in the caption.

## Image Prompt Templates

### Character Shot Prompts
```
4:5. [Pose description] of a man in his early 30s, [location/setting].
[Outfit — dark, casual: black t-shirt, hoodie, henley].
[Lighting — single hard light, side light, window light. Always dramatic].
[Expression — confident, focused, candid, genuine].
Cinematic, high contrast, shallow depth of field.
Negative space in [upper/center] third for text overlay.
Shot on 85mm lens. No smile unless candid moment.
```

### Establishing Shot Prompts
```
4:5. [Scene description — architecture, urban, atmospheric].
[Mood — moody, cinematic, dark tones].
[Key visual element — converging lines, reflections, neon, shadows].
No people. High contrast, teal and grey or teal and orange color grading.
Negative space in [upper/lower] portion for text overlay.
```

### Detail Shot Prompts
```
4:5. [Object/element close-up — laptop, hands, coffee, keyboard, phone].
Shallow depth of field, background softly blurred.
[Lighting — warm desk lamp, screen glow, ambient RGB].
Cinematic, intimate, real textures. Imperfection = authenticity.
Negative space in [upper/center] third for text overlay.
```

## Emoji Support

Use emoji (e.g., 👉) instead of unicode arrows or special characters — Gotham fonts don't have those glyphs. The renderer handles emoji via Apple Color Emoji font fallback. Use sparingly for visual pointing or emphasis.

## Anti-Patterns (NEVER do these)

- Pure white or bright backgrounds
- CGI, 3D renders, or world-building scenes
- Over-produced studio setups (ring lights, seamless backdrops)
- Stock photo vibes (too clean, too lit, too posed)
- More than 2-3 colors on any single slide
- Text without backing/overlay on busy images
- Multiple accents on one slide
- Unicode arrows (→, ←) — use emoji instead

## Style: Light Pop

High-contrast light mode. Stands out in a dark-dominated Instagram feed. Use when you want maximum scroll-stopping contrast, or for any carousel aimed at a broader/warmer tone.

### Color Scheme

| Role | Color | Hex |
|------|-------|-----|
| Background | Warm cream | `#E8DCC4` |
| Headline | Charcoal | `#1C1B17` |
| Body | Charcoal | `#1C1B17` |
| Accent phrase | Orange | `#FF6600` |
| Progress fill | Orange | `#FF6600` |

**Typography on light_pop:** Use Gotham Bold (not Ultra) weight. Write headlines in sentence case — not ALL CAPS. Bold italic on key phrases using `*phrase*` markers creates emphasis naturally.

Use `bg_mode: "light_pop"` in the carousel spec.

### When to use
- Cover slide on any dark carousel (light cover + dark body = cover pops in feed preview)
- Full carousel when you want to differentiate from dark-dominated feed
- Emotional/personal topics that benefit from a warmer, more approachable feel

### Anti-patterns on light slides
- Never use neon green on a light background (harsh, unreadable)
- Avoid pure white (#FFFFFF) — warm white (#F5F0E8) is softer
- Don't mix light_pop and dark slides unless it's intentional (cover = light_pop, rest = dark)

## Slide Types (Solid Renderer)

### Standard slide
Headline + body. The default. Use for explanations, insights, takeaways.

### Cover slide
Use `bg_mode: "cover"` (or "dark"/"light_pop") with an optional `topic_label` field.
- `topic_label`: small accent-colored text rendered ABOVE the headline (category/series label)
- Example: `"topic_label": "INSTAGRAM GROWTH"` renders above "YOU DON'T NEED MORE FOLLOWERS"

### Stat slide
Add `stat_value` and `stat_label` fields to any slide. Renders as a massive centered number with label.
- `stat_value`: the number/value displayed at 200px (e.g., "127K", "$4K", "10 hrs")
- `stat_label`: the context label below (e.g., "followers in 90 days", "saved per month")
- Use sparingly — 1 per carousel max. High visual impact.
- Example: `{"stat_value": "127K", "stat_label": "followers in 90 days"}`

### CTA slide with pill button
Add `cta_button` field to the final slide to render an orange pill-shaped button.
- `cta_button`: button text — pull from your brand profile's default CTA (e.g., "Get the system", "Comment SYSTEM")
- Rendered as an orange rounded pill with white uppercase text
