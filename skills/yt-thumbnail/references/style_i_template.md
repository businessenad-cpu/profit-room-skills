# Style I — Logo Crown (Social Proof Arc)

## Description
your face centered or slightly off-center. AI/tool logos arc around their head like a crown — a semicircle of recognizable app icons above and around them. A bold paint-stroke or solid banner at the bottom with blunt endorsement copy. Slightly skeptical or knowing expression. The logo arc IS the argument: "all these tools, and this is the one."

Reference format: a blunt one-line banner endorsement with a row of recognizable tool logos arcing above the person.

## Full Prompt Template

```
A photorealistic, cinematic, high-resolution YouTube thumbnail. WIDE 16:9 — never portrait.

**Person:** Use Image 1 for exact likeness — match the person's hair, facial hair, glasses, and clothing from your reference photo. Centered or slightly left-of-center. Chest-up. Slightly skeptical, knowing expression — one eyebrow slightly raised, hint of a smirk. Not a big grin — the expression says "I know something you don't." Fills ~55% of frame height.

**Logo crown (arcing above and around their head):**
A semicircular arc of [INSERT N] large, clean, recognizable app icon tiles floating above them — arranged in a gentle arc from their left shoulder, over their head, to their right shoulder. Each icon is a rounded-square tile, equally sized, evenly spaced. From left to right:
[INSERT LOGO LIST — e.g., "ChatGPT green swirl icon, Make purple icon, N8N orange icon, Claude orange terracotta face (from Image 2), LinkedIn blue 'in' (from Image 3), Obsidian purple crystal, Reddit orange alien"]
The icons float slightly, with subtle drop shadows. They are recognizable and clean — not glowing, just clear and present.

**Bottom banner:**
A full-width horizontal banner anchored at the very bottom of the frame. [INSERT BANNER STYLE — "rough red paint-stroke" (grunge/artistic feel) OR "solid flat orange rectangle" (cleaner, your brand) OR "solid white rectangle"]. Bold heavy ALL-CAPS sans-serif text inside: "[INSERT BANNER TEXT]".
Text color: white on red/orange banner, OR black on white banner.
Default to red paint-stroke unless orange fits the brand moment better.

**Background:** Two valid options based on content type:
- **Dark charcoal/navy** — use for AI automation, passive income, outcomes content
- **Light grid paper / whiteboard** (light editorial reference) — white or off-white gridded paper texture. Use for educational, framework, or "how to" content. Person cut out against light background. Creates high-contrast editorial feel.

**Logo arrangement:** Two valid options:
- **Arc above head** — logos in a semicircle from shoulder to shoulder, floating above. Best when all logos are similar size/weight.
- **Horizontal flanking** — logos spread across the frame at chest level, flanking the person on both sides (editorial flanking format). Best when logos are diverse sizes or when you want a more editorial layout.

**Lighting:** Even warm studio lighting on face. Slight rim light catching the edges of the logo icons. Clean catchlights in eyes.

**CRITICAL:** Wide 16:9. Face center. Logo arc above. Bottom banner with copy. Nothing else.
```

## Placeholder Guide

### [INSERT LOGO LIST]
List 5-8 tool logos in arc order (left to right). Always include Claude (from reference image) if Claude is the focus tool. Mix familiar (ChatGPT, LinkedIn) with lesser-known tools to create "insider knowledge" feeling.

For Claude/AI automation content:
> ChatGPT, Make, N8N, Claude (Image 2), LinkedIn (Image 3), Obsidian, Reddit

For LinkedIn-specific:
> Claude (Image 2), LinkedIn (Image 3), Reddit, Obsidian, Firecrawl, Zapier

### [INSERT BANNER TEXT]
Blunt, endorsement-style. The paint-stroke banner demands short, punchy copy:
- "THIS SH*T WORKS"
- "USE ALL OF THESE"
- "I TESTED THEM ALL"
- "THE ONLY STACK YOU NEED"
- "THESE REPLACED MY TEAM"

### [INSERT BANNER STYLE]
- **Red paint-stroke** — most aggressive, grunge/artistic feel
- **Solid flat orange** — cleaner, matches your brand color, more polished
- **Solid white** — cleanest, works if text is black, highest contrast

## When to Use
- Tool roundup / comparison videos
- "My AI stack" or "tools I use" content
- Any video showcasing multiple tools working together
- Works well with: The Formula title format, Social Proof Badge format

## Logo Handling
Pass `--logos Claude LinkedIn N8N` (or whatever tools are in the arc). The most prominent logo in the arc should be the most prominent one passed as a reference.
