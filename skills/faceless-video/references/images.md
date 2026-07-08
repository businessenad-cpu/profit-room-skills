# Stage 3 — Generate one doodle image per timestamp

Turn the phrase-level transcript from Stage 2 into a folder of images: **one image per timestamped line**, each a simple visual explanation of exactly what the narrator says at that moment. Images are generated with **Higgsfield → GPT Image 2** and saved locally, ordered by a sequence prefix.

## Inputs
- `<name>.phrases.txt` from Stage 2 — each `[MM:SS] line` becomes one image. If the user wants fewer/sparser images, use the segment-level `<name>.timestamped.txt` instead; default to the phrase file when they ask for "one image per timestamp."

## Model settings (fixed)
- Tool: `generate_image` (Higgsfield MCP). First load schemas via ToolSearch: `generate_image`, `show_generations`.
- `model: "gpt_image_2"`, `aspect_ratio: "16:9"`, `resolution: "1k"`, `quality: "medium"` (~2 credits/image; preflight with `get_cost:true` if the count is large).
- GPT Image 2 has **no negative-prompt field** — fold the "avoid" list into the prompt text as an `Avoid: …` clause.

## The per-line prompt recipe
For each line, write: **`CONTENT. ` + the locked STYLE block + the AVOID clause.**

- **CONTENT** = a simple visual that illustrates *this specific line*. One subject, literal where the line is concrete ("running" → a figure running), a clean metaphor where it's abstract ("And then," → a sweeping arrow; "most of it is already gone" → an almost-empty thought bubble). It must make sense with the story, the emotion, and the idea — never a random image. Keep it to one short sentence, generous negative space, single focal subject.
- Keep the SAME style + palette on every image so the set feels like one hand. Vary only the CONTENT.

### Locked default STYLE block (the "house" doodle style)
> Hand-drawn marker doodle illustration, simple childlike whiteboard-explainer sketch style. Thick uneven black felt-tip outlines with visible hand wobble, flat solid color fills, no gradients. Flat limited palette: cream/white background, charcoal black linework, flat gray, navy-blue, mustard yellow, muted orange accents only. Generous negative space, loose imperfect lines, marker-on-paper texture, 2D flat vector-doodle, casual and playful.

### AVOID clause (guardrails)
> Avoid: photorealism, realistic, 3D render, gradients, soft shadows, depth of field, glossy, hyperdetailed, clean vector, ruler-straight lines, anime, watercolor, oil painting, busy background, many colors, neon, glow, drop shadow.

This doodle style is the default. If the user supplies a different style block for a project, swap the STYLE + AVOID text and keep everything else identical.

## Workflow

1. **Parse** `<name>.phrases.txt` into ordered tuples `(seq, MM-SS, line)`, seq starting at 01, zero-padded. The seq prefix is what guarantees the folder sorts in **script order regardless of which render finishes first**, and it uniquely names lines that share a timestamp (e.g. two `0:13` lines → `08_00-13.png`, `09_00-13.png`).
2. **Make the output folder**, a single directory, e.g. `<project>/images/<slug>/`.
3. **Submit in batches.** The plan caps at **8 concurrent jobs** — submit ≤8 `generate_image` calls, then poll. Each returns a job `id` with `status:"pending"`; record `id → NN_MM-SS.png`. If a call returns a rate-limit error, just resubmit it once a slot frees up (don't skip it).
4. **Poll** `show_generations(type:"image", size:30)`. Completed items expose `results.rawUrl` (a PNG). Match by `id`.
5. **Download** each completed `rawUrl` with `curl -s -o "NN_MM-SS.png" "<rawUrl>"` into the folder.
6. **Repeat** 3–5 until every line has a file. Verify count and that each is 16:9 (`file *.png`).
7. **Write `manifest.md`** in the folder: a table of `file | timestamp | narration line | visual`. This is what the editor (and the next stage) reads to place each image on the timeline.

## Quality checks before finishing
- One image per line — count matches the phrase file (mind duplicate timestamps).
- Every image visibly illustrates its line, not a generic scene.
- Consistent style/palette across the whole set.
- All files present, valid PNG, 16:9, named `NN_MM-SS.png`, sorting in script order.
- Spot-read a few images (open them) to confirm content + style before declaring done.

## Notes
- Higgsfield returns hosted URLs; `curl` is how they become local files. Don't pass `https://` URLs back into `medias[]` — that's only for reference-image inputs (not used here).
- If the user wants the set as motion/video later, this ordered folder + `manifest.md` is the hand-off (timestamps drive each image's on-screen moment).
