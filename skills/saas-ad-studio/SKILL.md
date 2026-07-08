---
name: saas-ad-studio
description: >
  Turn a SaaS website, web app, or product URL into a high-quality cinematic ad
  that features the REAL product UI — the pitch-black "Anthropic / Linear / Vercel"
  look: one accent color, locked-frame scene-by-scene UI reveals built from real
  screenshots, scored with music + on-screen text (optional voiceover). Full
  pipeline: live audit (Playwright screenshots + CSS brand tokens) → brand DNA →
  concept + 4-act arc → cinematic hero frames (GPT Image 2) → locked-frame
  animation (Higgsfield Seedance 2.0) → music + ffmpeg assembly → organized output
  folder + a living brief.html. Two check-ins (concept+look, then storyboard);
  everything else is autonomous. Trigger on /saas-ad-studio, "make an ad for my
  SaaS", "turn my website/app/landing page into a video ad", "cinematic product
  ad", "UI ad", "app demo ad", "promo video for my software/tool". NOT for
  physical hold-in-hand products (use ad-studio) and NOT for UGC / talking-head /
  avatar-presenter ads.
argument-hint: "[product URL] [optional: login creds, aspect ratio, duration, brand colors]"
---

# SaaS Ad Studio — cinematic UI ads from a URL

You turn a live SaaS product into a short, premium, **UI-forward** cinematic ad. The look is
the current AI-tool standard: **pitch-black canvas, a single accent color, real product
screenshots revealed scene-by-scene in locked frames**, scored with music and clean on-screen
text. No talking heads, no avatars, no stock footage — the product's own interface is the hero.

This skill is the SaaS/UI sibling of `ad-studio` (which is for physical products). It reuses
that skill's living-`brief.html`, "Visual DNA" prompt discipline, and ffmpeg assembly, driven by
the **Higgsfield MCP** motion engine.

## The one rule that makes or breaks this: DO NOT let the UI morph

AI video models warp text and UI when asked to animate an interface. The entire technique here
is built to avoid that:

- The **real screenshot is the first frame.** Motion comes from the *camera and light*, never
  from the model redrawing the UI.
- Allowed motion on a UI shot: slow push-in, gentle parallax/drift (1–2%), rack focus, a glint
  of light, the accent color pulsing, a soft reveal from black. **No whip pans, no UI elements
  re-animating, no morphing menus, no cursors that retype text.**
- If a feature needs to "do something," show it as a **hard cut between two real screenshots**,
  not as in-frame animation.
- Every Seedance prompt ends with the guardrail line: *"Interface stays perfectly sharp and
  static; do not warp, morph, or re-render any UI text, icons, or layout."*

Read `references/cinematic-ui-doctrine.md` before writing any prompt. It has the camera
vocabulary, the shot archetypes, and copy-paste prompt templates.

## Requirements

- **Higgsfield MCP** — the motion/image engine (`generate_image`, `generate_video`,
  `models_explore`, `media_import_url`, `media_upload`, `media_confirm`, `job_display`,
  `show_generations`, `upscale_video`). Tool names are prefixed per your install
  (`mcp__<server>__generate_image`, etc.) — check your connected MCP list for the exact prefix and
  use those names. Requires a Higgsfield account with credits. No key is embedded here.
- **Playwright MCP** (`mcp__playwright__browser_*`) — for the live UI audit / screenshots.
  Firecrawl `firecrawl_scrape` is the no-login fallback.
- **ffmpeg** (installed locally) — assembly, on-screen text, muxing.
- **Graceful fallback:** if the Higgsfield MCP isn't connected, tell the user to add it (or fall
  back to any image/video-gen MCP that exposes equivalent `generate_image`/`generate_video`
  tools); if Playwright isn't available, use Firecrawl for screenshots + copy and note the limit.

## Tooling (use these exact tool names)
- **Image model:** `gpt_image_2` — params `quality: high`, `resolution: 2k|4k`, one `image`
  reference role.
- **Video model:** `seedance_2_0` — `duration` 4–15s **per clip**, set `generate_audio: false`
  on UI shots (we score in post), roles include `start_image`.
- **Audio/music:** no standalone music model exists here — use the **video model's native audio**
  (`generate_audio:true` on Seedance), best captured on a **single 15s timestamped render** that
  scores the whole clip. Royalty-free/track fallback in `references/assembly.md`. You can't QA audio
  by ear in-harness — surface it for the user to judge.
- **Audit:** Playwright MCP (`mcp__playwright__browser_*`). Firecrawl `firecrawl_scrape` fallback.
- **Assembly:** `ffmpeg` (installed). See `references/assembly.md`.
- **Full tool/param contract, polling, downloading, and `get_cost` preflight:**
  `references/higgsfield-tools.md` — read it before the first generation call.

Seedance caps at **15s per render**, but a single render can hold **multiple internal cuts** via a
timecoded prompt — so a 15s ad is usually **one render of ~3–5 timestamped shots** (this is how
`ad-studio` renders). Longer ads chain 15s segments: a 30s ad ≈ two segments, a 60s ad ≈ four,
ffmpeg-concatenated. **Tooling is website + Higgsfield + ffmpeg only — no Remotion or other editors.**

---

## Phase 0 — Intake (one message)

Ask everything at once. Fill any blank with the default and move on; only the URL is required.

1. **Product URL** (+ login creds / a path to a staging build if the good screens are gated).
2. **Aspect ratio** — `16:9` (default; site hero / YouTube), `9:16` (Reels/TikTok/Shorts), `1:1`.
3. **Duration** — `15` / `30` (default) / `60` s.
4. **Sound** — `music + on-screen text` (default) / `+ AI voiceover` / `music only`.
5. **Brand** — paste brand colors + logo URL if known; otherwise I extract them from the live CSS.
6. **Feature focus** — the 3–6 screens/features to spotlight; otherwise I pick the hero modules.
7. **Output dir** — default `./saas-ad-studio/<product-slug>/`.

Create the output folder tree, then proceed autonomously to the first check-in.

## Phase 1 — Live audit + Brand DNA (autonomous)

Goal: real screenshots + the real brand, never invented. Follow `references/audit-playbook.md`.

- `browser_navigate` the URL; if creds were given, `browser_fill_form` / `browser_type` to log
  in. Walk every reachable key route.
- `browser_resize` to a clean capture size matched to the chosen aspect (e.g. 1920×1080 for 16:9,
  1080×1920 for 9:16), then `browser_take_screenshot` each hero screen → `screens/`.
- `browser_evaluate` to read the **live CSS tokens** off the DOM: background, surface, the single
  **accent**, text, border hexes, and font-family. This is the source of truth for the palette.
- Grab the logo (favicon/nav SVG/PNG). Note the module map and any real numbers visible in the UI
  (counts, statuses, names) — they make great on-screen text.
- No login / SPA blocks Playwright? Fall back to `firecrawl_scrape` on the marketing site for
  copy + colors, and use marketing-page hero screenshots.
- Parallelize: this is a good place to fan out subagents (one per route) if the app is large.

Write `research.md` (palette + hexes, type, voice, module map, the real numbers). Initialise
`brief.html` themed from the extracted palette — the product's own brand drives the brief.

## Phase 2 — Concept + look — ⏸ CHECK-IN 1

Present **2–3 concepts** on `brief.html` (with the captured screenshots embedded). Each concept:

- **Logline** — one sentence.
- **4-act arc** scaled to the chosen duration: **hook → problem → feature reveals → payoff +
  logo lock.** Map each beat to a *specific real screen* from `screens/`.
- **Visual signature** — how the single accent is used; the on-screen-text style.
- **Music mood** — 3–5 words.

Recommend one. After the user picks, lock two verbatim blocks into `dna.md`:

- **Concept spine** — 2–4 things that must be visibly true in every shot.
- **Visual DNA** — the exact lines appended to *every* image and video prompt: pitch-black
  canvas, accent hex, Inter-class type, grain/glow, camera language, and the no-morph guardrail.

## Phase 3 — Shot list + hero frames — ⏸ CHECK-IN 2

Decompose the arc into N shots (respect 4–15s/clip and the total duration). For each shot record:
duration, the real screen used, camera move, **UI treatment** (flat push-in / UI floating in dark
volumetric space / on a device / glass reflection), on-screen text copy, and the accent moment.
Write `shotlist.md`.

Build one **hero frame per shot**:

- **UI shots:** composite the real screenshot into the cinematic dark scene with `gpt_image_2`
  (screenshot passed as the `image` reference, `quality: high`, `resolution: 2k`), keeping the UI
  on a flat, undistorted plane — OR, for a clean straight push-in, use the raw screenshot
  directly (no regeneration = zero morph risk).
- **Brand / atmosphere / logo-lock shots:** text-to-image with `gpt_image_2`.
- Append the Visual DNA lines to every prompt.

Render frames **in parallel**, bind each job to its filename (never trust completion order),
eyeball each as it lands, re-render any that break the brand/UI (**max 2 retries**, then show best
and flag). Save to `frames/` (`01.png`…). Present the full storyboard on `brief.html` and get
approval before spending video credits.

## Phase 4 — Animate the shots (autonomous)

`models_explore get seedance_2_0` once to reconfirm params. Two render methods — prefer **A**:

**A — Single timestamped render with EVERY storyboard frame as a reference (default — strongly
preferred).** Render the whole 15s ad as ONE Seedance call: pass **all the storyboard frames as
references in narrative order** (cap ~9) — `start_image` = the opener/establishing frame,
`end_image` = the logo lock, and every middle beat (the real UI screenshots, proof cards,
comparison, community) as `image` refs. Write the prompt as **timecode blocks**, each naming the
shot's reference content + its camera move, and explicitly tell it the **UI animates** (scrolls,
glows, cursor moves, light sweeps) and must **not warp/melt/scramble text or numbers**. Set
`generate_audio:true` so the same render carries the score. This gives native animation + native
transitions between the real frames — far better than ffmpeg-stitching separate clips, and it makes
the actual product UI come alive (passing the real screenshot as the reference is what animates it).
This is how `ad-studio` renders, and it's what the user wants. Template in
`references/cinematic-ui-doctrine.md`.

**B — Isolated start_image shot (fidelity fallback).** Only when ONE beat's text must be
pixel-perfect and Seedance softened it too much in the single render — re-render just that beat from
its real screenshot as `start_image`, or overlay that one number/label with an ffmpeg text pass.
Reach for this surgically, not as the default; don't fall back to stitching the whole ad in ffmpeg.

```
generate_video(params:{
  model: "seedance_2_0",
  prompt: "<timecoded multi-shot OR single locked-frame prompt> … <Visual DNA> … <no-morph guardrail>",
  medias: [{ role: "start_image", value: "<key frame id>" }, { role: "image", value: "<frame 2>" }, …],
  duration: 15,                 // method B: the shot's own 4–15s
  aspect_ratio: "<from intake>",
  resolution: "1080p",
  generate_audio: false,
  count: 1
})
```

For a 30/60s ad, render multiple 15s timestamped segments (each its own mini-arc) and concat them
in Phase 5. Submit in batches of ~4, poll to terminal, download each to `shots/` (`01.mp4`…). Watch
each; if the UI morphs or a cut breaks, re-render that one segment once with tighter/lower motion —
don't loop endlessly. Media IDs, polling, downloading, and the multi-shot pattern are in
`references/higgsfield-tools.md`.

## Phase 5 — Music + on-screen text + assembly (autonomous)

- **Audio/music:** prefer Seedance **native audio** (`generate_audio:true`) — describe the score in
  an `Audio: …` line in the render prompt. A single 15s timestamped render scores the whole clip in
  one pass (best). No standalone music model exists; for a specific track, mux a royalty-free/user
  track per `references/assembly.md`.
- **On-screen text:** burn the per-beat copy with ffmpeg `drawtext` (Inter/Inter-class font,
  accent color for emphasis), or pre-render text cards as transparent PNGs and overlay. Keep it
  minimal — one idea per beat.
- **Optional VO** (only if chosen at intake): generate the line with `text2speech_v2_elevenlabs`,
  time it under the cut, and duck music ~-10 dB beneath it.
- **Assemble:** a single 15s timestamped render just needs text burned + music muxed; for a
  multi-segment ad, concat the 15s segments first (hard cuts + the occasional 6–10 frame dissolve),
  then text + music. Optional `upscale_video` for a 4K master.
- Output `ad-final.mp4`. The full ffmpeg command set (concat, drawtext, mux, ambience-duck) is in
  `references/assembly.md`. **Website + Higgsfield + ffmpeg only — no Remotion or other editors.**

## Phase 6 — Deliver

Finalize `brief.html`: embed `ad-final.mp4`, lock every section, add a one-line "recreate" recap.
Print the output folder tree and the final file path. Note credit spend if the user asked.

---

## Output folder (per run)

```
saas-ad-studio/<product-slug>/
├── brief.html          # living doc: research → concept → DNA → storyboard → final video
├── research.md         # palette+hexes, type, voice, module map, real numbers
├── concepts.md         # the 2–3 concepts + which was picked
├── dna.md              # Concept spine + Visual DNA (verbatim, appended to every prompt)
├── shotlist.md         # locked shots: screen, camera, UI treatment, text, duration
├── screens/            # raw captured screenshots (source of truth for the UI)
├── frames/             # cinematic hero frames 01.png …
├── shots/              # rendered clips 01.mp4 …
├── music-prompt.txt
├── music.m4a
└── ad-final.mp4
```

## Check-in protocol (only 2)

1. **Concept + look** (end of Phase 2) — pick a concept; locks the spine + Visual DNA.
2. **Storyboard** (end of Phase 3) — approve the hero frames; gates the video render spend.

Everything else runs autonomously. Show every rendered asset on `brief.html` the moment it lands
(never "rendering…" placeholders).

## Rules

- **Never invent UI.** Every screen shown must be a real screenshot from `screens/`. Every claim
  in on-screen text must trace to something actually in the product.
- **Single accent.** Use the one extracted accent hex; resist adding a second color.
- **Preflight cost** with `get_cost: true` before a big batch if the user is watching credits.
- **Match the user's language** in all on-screen text and copy.
- Default look = the doctrine. Only deviate if the user asks for a different style.
