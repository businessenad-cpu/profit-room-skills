---
name: infographic
description: "Generate hand-drawn educational infographic images from any topic using Google Gemini image generation. Use this skill whenever the user says /infographic, 'create an infographic', 'visualize this', 'make a diagram', 'explain this visually', 'create visuals for', 'I need graphics for', 'illustrate this concept', 'drill into this', 'go deeper on', or wants to turn a topic, system, or process into educational visual graphics. Always trigger when the user wants something explained visually — even if they don't say 'infographic'."
---

# Infographic Creator

## Requirements

Image generation runs through Google Gemini via `scripts/generate_image.py`, which needs a Google AI (Gemini) API key. The script reads it from the environment — set `GOOGLE_API_KEY` (or `GEMINI_API_KEY`) before running (e.g. `export GOOGLE_API_KEY=...`, or add it to your shell profile / Claude Code settings `env`). Get a free key at https://aistudio.google.com/apikey. If the key isn't set, the script errors and I'll tell you exactly what to add. The Python deps install with `pip install google-genai Pillow`.

Turn any concept into a two-level visual explainer series:
- **Level 1 — Overview:** 3–5 broad diagrams that tell the full story of the topic
- **Level 2 — Drill-down:** For any Level 1 diagram, generate one deeper diagram per component — each with internal callout annotations showing what's happening inside

**Style target:** Dark charcoal background, rough sketch ink lines, white and warm accent colors, handwritten text throughout. Warm, approachable, human — like a smart teacher drew it on a dark sketchpad.

---

## Two-Level Structure

### Level 1: Overview Run
The default. Generate 3–5 diagrams that cover the full topic at a high level. Each diagram should be understandable on its own but also work as part of a set.

After showing the Level 1 set, always offer:
> "Want to drill deeper into any of these? I can generate a Level 2 set for [diagram title] — one diagram per component with internal callouts."

### Level 2: Drill-Down Run
Triggered when the user says "drill into [X]", "go deeper on [X]", or picks a specific Level 1 diagram to expand.

For the chosen diagram:
1. Identify its **3–4 sub-components** (e.g. if the overview shows "4 Phases", drill into each phase individually)
2. Generate one diagram per sub-component
3. Each diagram shows the sub-component's **internal workings** using callout annotations — arrows pointing to specific elements with labels explaining what they are and what they do
4. Keep the **same character design** across all Level 2 diagrams for consistency (lock the character description in every prompt)

**Level 2 prompt addition:**
```
DRILL-DOWN diagram for [COMPONENT NAME] — [TITLE]. Large central scene showing [CHARACTER] actively [DOING THE ACTION]. Multiple hand-drawn callout arrows pointing outward from different parts of the scene, each with a handwritten label describing what that element does: "[action]", "[detail]", "[outcome]". Feels like a zoomed-in explanation of one piece of a larger system.
```

---

## Step 1: Identify Visual Moments

For **Level 1**, identify 3–5 overview moments — narrative arc first:

| Type | When to use |
|------|-------------|
| **Before / After** | Problem → solution, chaos vs order |
| **Flow / Process** | Sequential steps with labeled transitions |
| **Transformation** | Multi-panel story showing change over time |
| **Components / Anatomy** | What a system is made of |
| **Loop / Cycle** | Repeating systems, feedback loops |
| **Timeline** | Phases or milestones over time |

For each moment: title, type, key elements (3–6), layout, color (red = problem, amber = process, green = solution).

Present plan then proceed immediately:
```
Visual moments:
1. [Title] — [type] — [elements] — [color]
2. ...
Generating now.
```

---

## Step 2: Write Prompts

**Always include this style base:**
```
hand-drawn educational diagram, dark charcoal background, rough sketch ink line quality, slightly imperfect hand-drawn lines, all text in handwritten chalk lettering style, warm off-white sketch lines, subtle paper texture, friendly and approachable
```

**Color palette — use purposefully:**
- **Warm red** — problem state, chaos, the "before"
- **Amber/gold** — process, action, the "during"
- **Green** — clean output, solution, the "after"

**Always add:**
- **Labeled arrows** — label every connector with an action verb (`fires →`, `consolidates →`, `results in →`)
- **Handwritten text** — ALL labels, titles, captions look hand-lettered, slightly imperfect
- **Contrasting panel moods** — problem panels dense/chaotic, solution panels open/calm
- **A character** — include a simple sketch robot or figure for warmth; keep description identical across all diagrams in a set for consistency

**Consistent robot character description (use this exact wording every time):**
```
cute hand-drawn robot character, round head, simple antenna, small glowing chest panel, friendly expression, rough sketch ink style
```

**Full prompt template:**
```
hand-drawn educational diagram, dark charcoal background, rough sketch ink line quality, slightly imperfect hand-drawn lines, all text in handwritten chalk lettering style, warm off-white lines, friendly — [DIAGRAM TYPE]: [TITLE]. [PANEL/SCENE DESCRIPTIONS with color-coded borders]. [LABELED ARROWS]. [CHARACTER if relevant — use consistent description]. [BOTTOM CAPTION in handwritten font]. Spacious layout, breathing room.
```

**Example — transformation (Level 1):**
```
hand-drawn educational diagram, dark charcoal background, rough sketch ink line quality, all text in handwritten chalk lettering — TRANSFORMATION: What the Onboarding Flow Does. Three panels connected by thick hand-drawn arrows. Panel 1 red border 'New Signup': messy overlapping to-do cards, a confused customer. Arrow labeled 'flow starts →'. Panel 2 amber border 'Onboarding Flow': cute hand-drawn robot character, round head, simple antenna, small glowing chest panel, friendly expression, rough sketch ink style — guiding the customer, three rough boxes labeled 'welcome' 'setup' 'first win'. Arrow labeled 'done →'. Panel 3 green border 'Activated Customer': neat organized dashboard, checkmark, happy customer. Timeline arrow at bottom: 'Day 1' → 'Day 3' → 'Day 7'. All handwritten text.
```

**Example — drill-down (Level 2):**
```
hand-drawn educational diagram, dark charcoal background, rough sketch ink line quality, all text in handwritten chalk lettering — DRILL-DOWN: Step 1 — Welcome. Large central scene: cute hand-drawn robot character, round head, simple antenna, small glowing chest panel, friendly expression, rough sketch ink style — greeting a new customer and reading a large book labeled 'Account Profile'. Multiple hand-drawn callout arrows pointing outward: arrow pointing to book labeled 'reads what they signed up for', arrow pointing to robot's eyes labeled 'checks their goals', arrow pointing to open pages labeled 'personalizes the welcome', arrow at bottom labeled 'making them feel understood on day one'. Amber border. Handwritten title 'STEP 1: WELCOME' at top with a wave icon. Spacious, dark background.
```

---

## Step 3: Generate Images

Run all images in **parallel background tasks**.

```bash
python3 scripts/generate_image.py \
  "<full prompt>" \
  "/tmp/infographic_<slug>.png" \
  "16:9" \
  "2K"
```

- Run from the skill directory so the relative `scripts/` path resolves (or use the absolute path to `generate_image.py`).
- `<slug>` = short snake_case title (e.g. `phases_overview`, `drill_orient`)
- Default: `16:9` at `2K`
- Requires a Google Gemini API key in the environment (see Requirements above)

---

## Step 4: Return Results

```
**[Topic] — [Level 1 Overview / Level 2: Drill-down on X]**

1. **[Title]**
   ![infographic](/tmp/infographic_slug.png)
   *[One sentence: the insight this teaches]*

2. ...
```

After Level 1: offer to drill deeper on any diagram.
After Level 2: offer to drill into another component or regenerate any image.

---

## Visual Style Reference

**Use:**
- Dark charcoal background
- White + warm off-white sketch lines
- Red / amber / green as story-driven accent colors
- Rough, slightly imperfect line quality
- Handwritten text for ALL labels, titles, captions
- Labeled arrows (never silent)
- Contrasting panel density (chaotic before, calm after)
- Consistent robot character across all images in a set

**Avoid:**
- Clean flat vector / computer-perfect lines
- Silent unlabeled arrows
- Monochromatic layouts
- Clutter — max 6 elements per panel
- Typed/print fonts anywhere
- Inconsistent character appearance across a set

---

## Troubleshooting

- **Text looks typed:** Emphasize "all text handwritten chalk lettering, hand-lettered, slightly imperfect"
- **Too monochromatic:** Name border colors explicitly per panel
- **Arrows not labeled:** Add each arrow label explicitly in the prompt
- **Character looks different across images:** Use the exact same robot character description verbatim in every prompt
- **Script errors:** `pip install google-genai Pillow`
- **`TypeError: 'NoneType' object is not iterable` / no image returned:** Gemini returned `MALFORMED_FUNCTION_CALL`. Two known causes:
  1. **"callout card" in prompt** — model interprets it as a function call instruction. Always frame prompts as "hand-drawn educational diagram", never "callout card".
  2. **Slash commands are fine** — writing `/tasks`, `/memory` etc. literally in prompts does not cause this error. The root cause is always "callout card" framing or shell `&` parallelism.
- **Parallel generation failures:** Don't run multiple scripts via shell `&` loops. Use Claude Code's background task system (`run_in_background: true`) to run all images in parallel reliably.
- **Wrong model:** Only use `gemini-3.1-flash-image-preview`. Do not use older or alternative model IDs.

## Cue / Command Slides

For slides that show a screen command the creator should type (e.g. `/memory`, `/tasks`), use this framing:

```
hand-drawn educational diagram, dark charcoal background, rough sketch ink line quality, all text in handwritten chalk lettering — SCREEN CUE SLIDE: [command]. Large centered text 'forward-slash [command]' in bold handwritten lettering, warm amber glow. [Supporting label]. Dark background, minimal, high contrast.
```

The different visual styling (large centered command, amber glow) signals the cue — no label like "SWITCH TO CLAUDE CODE" needed.
