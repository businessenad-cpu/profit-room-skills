# Style B — Old vs New Contrast

## Description
No person. Light grid paper background. Two side-by-side screenshot panels showing before (left, dim, red X) and after (right, vibrant, checkmark). A bold yellow or orange arrow between them. The screenshots ARE the argument — the contrast does all the work at scroll speed. Optional floating labels above each panel ("THEIRS" / "YOURS", "BEFORE" / "AFTER") and an optional bottom copy bar. Best for before/after, replacement, and upgrade stories.

Reference visual: split-panel comparison thumbnails — the left is always visually inferior, the right is always the win.

## Full Prompt Template

```
A high-resolution YouTube thumbnail. WIDE 16:9 — never portrait.

**Background:** Clean off-white grid paper texture — a light, slightly warm white surface with a subtle uniform grid of thin light grey lines. The grid is visible but not dominant. Fills the entire frame. No dark elements, no bokeh, no vignette.

**Left panel ("before"):**
A screenshot mockup panel occupying the LEFT 40% of the frame, slightly elevated off the background with a soft drop shadow. The screenshot shows: [INSERT BEFORE SCREENSHOT DESCRIPTION — e.g., "a generic AI-generated Instagram carousel with plain white background, Arial font, no brand colors, low visual hierarchy — clearly template-looking"]. The panel has a slight desaturated or cool-grey tint to signal inferiority. A bold red X mark overlaid in the upper-right corner of the panel (or a red border frame around the entire panel). Above the panel, in bold black sans-serif: "[INSERT BEFORE LABEL — e.g., 'THEIRS' or 'BEFORE']" with a subtle red underline.

**Center arrow:**
A thick, bold yellow (#FFD600) or bright orange arrow pointing RIGHT, centered between the two panels. The arrow is hand-drawn marker style — slightly imperfect, confident stroke, not a clipart icon. It implies direction and momentum. Optionally a small "vs" label in dark grey above the arrow.

**Right panel ("after"):**
A screenshot mockup panel occupying the RIGHT 40% of the frame, same elevation and drop shadow as the left. The screenshot shows: [INSERT AFTER SCREENSHOT DESCRIPTION — e.g., "a custom branded Instagram carousel with rich gradient background, premium typography, cohesive color palette — clearly designed with intention"]. The panel is fully saturated and vibrant — noticeably more alive than the left panel. An orange or green checkmark in the upper-right corner. Above the panel, in bold black sans-serif: "[INSERT AFTER LABEL — e.g., 'YOURS' or 'AFTER']" — optionally in orange to signal brand/win.

**[OPTIONAL bottom copy bar]:**
A full-width horizontal bar anchored to the very bottom of the frame. [INSERT BAR STYLE — "solid flat orange rectangle" OR "solid dark charcoal rectangle" OR skip entirely if the panel labels carry the message]. Bold heavy ALL-CAPS sans-serif text inside: "[INSERT BANNER TEXT]"
Text color: white on dark/orange bar.
TYPOGRAPHY RULE: This text appears EXACTLY ONCE in the bottom bar. Do not echo it anywhere else in the image.

**Lighting:** Even, soft frontal lighting across both panels. Bright, editorial — not moody.

**CRITICAL:** Wide 16:9. No person. Light grid paper background fills frame. Two panels side-by-side (before left, after right). Red X on left panel, checkmark on right. Bold arrow between them. Nothing else unless a bottom bar is specified.
```

## Placeholder Guide

### [INSERT BEFORE SCREENSHOT DESCRIPTION]
Describe what the "bad/old" state looks like at thumbnail scale. Be specific about what makes it look inferior:
- Generic AI carousel: "plain white slide background, default font, no color palette, lorem-ipsum-feeling layout"
- Old tool output: "flat Canva template with stock photo background and clip-art icons"
- Bad prompt result: "low-contrast, cluttered slide with five different font sizes and no visual hierarchy"

The before panel should be immediately recognizable as "wrong" to the target viewer — they should feel slightly embarrassed that they've produced this.

### [INSERT AFTER SCREENSHOT DESCRIPTION]
Describe what the "good/new" state looks like — visually richer, more designed, clearly superior:
- Custom branded carousel: "dark gradient background with terracotta accent color, premium serif headline, consistent type system, editorial layout"
- Tool output with system: "clean modular slide layout, brand color palette, cohesive visual language across all slides"

The after panel should make the viewer think "I want that."

### [INSERT BEFORE LABEL] / [INSERT AFTER LABEL]
Short, punchy floating labels above each panel:
- "THEIRS" / "YOURS" — identity framing, most provocative
- "BEFORE" / "AFTER" — clearest, least friction
- "WITHOUT THIS" / "WITH THIS" — action framing
- "GENERIC" / "CUSTOM" — quality framing

### [INSERT BANNER TEXT]
Optional bottom bar copy — only add if the panel labels alone don't complete the message:
- "ONE PROMPT CHANGES THIS"
- "STOP SETTLING"
- "THIS IS FIXABLE"
- Skip entirely if the before/after labels are strong enough on their own.

## When to Use
- Replacement story: "I switched from X to Y"
- Upgrade story: "Your [thing] is bad. Here's the fix."
- Before/after reveal: visually showing the transformation is the entire pitch
- Tool comparison: when the output quality difference is visible in a screenshot

## Key Rules
- The screenshot panels must be visually distinct enough to read at small thumbnail size — extreme contrast between left and right
- No person means the screenshots carry all the credibility — they must be high-quality mockups, not placeholder rectangles
- The red X and checkmark must be bold enough to read at 120px width (YouTube search result size)
- Bottom bar is optional — the two labels + arrow often carry the full message on their own
- When passing logos: if a tool appears in either screenshot panel, pass it as `--logos` so the icon renders accurately inside the panel

## Logo Handling
Pass `--logos` for any tool whose icon appears inside a screenshot panel. Reference them in the prompt as "Image 2", "Image 3", etc. within the panel description so Gemini reproduces them accurately rather than inventing a symbol.
