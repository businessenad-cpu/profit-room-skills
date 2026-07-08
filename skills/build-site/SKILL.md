---
name: build-site
description: Build a $10k-class animated website for the user's brand. Interviews them, picks a scroll style, designs to a strict set of design laws, generates or sources bespoke hero media, and ships a single premium animated landing page, product site, or portfolio. Use when the user wants a high-end animated site, a scroll-scrub product page, or a portfolio that looks expensive.
---

# Build Site

You are building the user a premium animated website that looks like it cost $10,000. The quality comes from two things working together: a strict set of **design laws** (the quality floor) wrapped around a **unique config and unique assets** (what makes it theirs). You never lower the floor; you make the site specific.

## Personalization

This skill builds a site in *your* brand voice and look. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

## The one idea

Every great site here = **the design laws (the quality floor) + a unique config + unique assets (the customization).** The look is guaranteed by obeying the laws; you make it specific with the brand's palette, copy, and bespoke renders. Read both references before you start:
- `references/design-laws.md` — palette, type, copy, and layout laws. Obey them.
- `references/scroll-catalog.md` — the seven scroll styles (A–G), the render laws, and the frame-sequence technique that makes scrubbing feel premium.

## Flow

### 1. Interview (keep it to 4 questions)
- What is the product or brand, in one line?
- Who is it for, and what should they *feel*?
- What is the one thing they should remember?
- Do you want bespoke AI-generated media, or should we use stock/placeholder media for now?

Do not over-ask. Pull what you can from the brand profile, infer the rest, and propose.

### 2. Pick the scroll style
Read `references/scroll-catalog.md`. Match the product to a style — do not default to one:
- **A Ambient loop** — a single hero object that just looks beautiful (spirits, fragrance, a watch). No scroll effect.
- **B Scroll-scrub** — a material or product that transforms/rotates as you scroll (most products, textures).
- **C Cursor-spotlight** — something that hides in the dark and is revealed (lighting, a car, anything dramatic).
- **D Horizontal pan-lock** — a place or a lineup you move sideways through (a workshop, a coast, a collection).
- **E Exploded** — a built object worth taking apart (a watch, earbuds, a camera, anything mechanical).
- **F Push-through** — a space you fly into (architecture, an experience, an interface).
- **G Scrollytelling** — a process worth watching unfold (coffee, forging, making anything).

State your pick and why in one line.

### 3. Design the config (this IS the design work)
Decide every design choice up front, obeying `references/design-laws.md`:
- **Palette**: OKLCH only, never `#000`/`#fff`, one committed accent. Choose a theme from a one-sentence scene, not from the category.
- **Type**: a distinctive display face + a clean grotesk body. Real hierarchy (≥1.25 scale ratio).
- **Copy**: tight, specific, no filler. **No em dashes.** Headlines short.
- **Captions** (3 short beats): 3–5 words each, one accent word each.
- Keep the asset budget: the spine uses **2 videos + 3 images, each exactly once.** Never add more slots; never reuse an asset. That restraint is what keeps it clean.

### 4. Write the render prompts (or plan placeholders)
Following the render laws in `references/scroll-catalog.md`:
- **2 videos**: `hero` (the header move) + `middle` (a *different* second video that matches the hero's light and palette — a sibling prompt, not the same shot).
- **3 images**: a product/context shot, a macro, and a hero still.
- Lock the camera, constant velocity, motion blur off. For any scroll-scrubbed style, **render long and export a WebP/PNG frame sequence** — that is what makes scrubbing feel premium.

### 5. Build the page
Build a single self-contained site using free, open-source libraries (pull from a CDN or npm):
- **GSAP + ScrollTrigger** for pin + scrub.
- **Lenis** for smooth inertia scrolling.
- A **canvas flipbook** driven by scroll progress for any frame-sequence hero (Style B–G).
- **SplitType** for caption choreography.

Follow the canonical section spine in `references/scroll-catalog.md` (hero → thesis → feature pairs → gallery band → second moment → editorial rows → CTA → footer). Enforce the universal legibility rules (dark halo behind hero text, translucent content sections over a slow mesh-gradient background, a seam gradient so hero footage fades into content).

- **With generated media**: use your available image/video generation (see Requirements) to render the 2 videos + 3 images from the prompts, chop scroll videos into a frame sequence with ffmpeg, and wire them in.
- **Without**: drop in tasteful placeholders (a solid brand-tinted plate or a simple CSS loop) into the exact same slots so the structure and motion are correct, and mark each slot so the user can swap real media in later.

Serve the folder locally and open the page. Show the user.

### 6. Iterate by conversation
This is the whole point. The user says it, you change the design:
- "Make it darker / warmer" → edit the palette (no re-render).
- "Shorter headline / different copy" → edit copy (no re-render).
- "Use the exploded style" → change the style + rewrite the hero render prompt, re-render the hero only.
- "Swap the product shot" → rewrite one image prompt, re-render that one image.
Only re-render the asset that changed. Copy and palette edits never need a render.

## Hard rules (do not break)
- 2 videos + 3 images, each used once. No gallery grids, no reused frames as filler.
- No em dashes in copy. No `#000`/`#fff`. One accent.
- Scroll-scrubbed heroes ship as a **frame sequence**, never a raw scrubbed `<mp4>` (raw video stutters on backward scrub).
- The footer credit line is the brand's own (from the brand profile), not anyone else's.
- If a render's START and END drift into a different object (exploded/transform styles), fall back to a loop — consistency over spectacle.

## Requirements
- **A modern browser + a local static server** (e.g. `npx serve`) to preview. Always available.
- **ffmpeg** — to chop rendered videos into scroll frame sequences. If missing, tell the user to install it, or fall back to ambient-loop (Style A) which needs no frames.
- **Image/video generation (optional)** — for bespoke hero media. Use whatever generator you have access to (e.g. an MCP image/video tool or a CLI). If none is available, build the full structure with placeholders and tell the user exactly which slots to fill.
- No API keys are embedded in this skill. If a generator needs a key, source it yourself before running.

## Result
A site indistinguishable in quality from a top awwwards build, but unmistakably the user's: their brand, their product, their words, their bespoke renders.
