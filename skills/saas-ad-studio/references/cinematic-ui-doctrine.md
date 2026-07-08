# Cinematic UI Doctrine

The house style for SaaS/UI ads. This is the look that top AI tools (Anthropic, Linear, Vercel,
Raycast, Arc) and the best SaaS launch reels use right now. Apply it unless the user asks for
something else.

## The look in one breath

> Pitch-black canvas. A single accent color. The real product UI revealed in locked, static
> frames — one feature per beat — with slow, expensive camera moves, fine grain, a soft volumetric
> glow in the accent color, and minimal on-screen type. It feels like a film about software, not a
> screen recording.

## Non-negotiables

1. **Pitch black** — background `#0A0A0A`-ish, never pure flat black, never white/light unless the
   product itself is a light-mode brand (then use *its* darkest surface as the canvas).
2. **One accent** — the single extracted accent hex. It appears as: button/active states already in
   the UI, a thin glow, a pulse on the key moment, the logo. Never introduce a second hue.
3. **Locked frames** — the camera moves; the UI does not redraw. See the no-morph rule below.
4. **One idea per beat** — each shot says exactly one thing. Reveal one feature, one number, one
   claim.
5. **Generous negative space** — the UI sits small-ish in a large dark frame. Let it breathe.
6. **Restraint** — no whoosh transitions, no lens flares stacked five deep, no neon vomit. Quiet
   confidence reads as expensive.

## The no-morph rule (most important)

Video models destroy UI text. Defend against it:

- The **real screenshot is the start frame.** Motion is camera + light only.
- Keep the UI on a **flat, fronto-parallel plane** — don't bend it onto curved surfaces or extreme
  perspective; that's where morphing starts.
- Prefer **low motion**. A 3% push-in that holds the UI crisp beats a dramatic move that smears it.
- Need the UI to "change"? **Hard-cut between two real screenshots**, never animate the change.
- End every Seedance prompt with the guardrail:
  > *"Interface stays perfectly sharp and static; do not warp, morph, distort, or re-render any UI
  > text, icons, charts, or layout. Only the camera and light move."*

## Camera vocabulary (pick ONE per shot)

- **Slow push-in** — 2–5% dolly toward the screen. The default. Calm, premium.
- **Slow pull-back** — reveal the UI emerging from black. Great for openers.
- **Lateral drift / parallax** — UI on a near plane, particles/glow on a far plane, 1–2% sideways.
- **Rack focus** — start soft, settle sharp on the UI (or pull focus from UI to logo).
- **Rise / descend** — gentle vertical move down a long dashboard or up a pricing column.
- **Locked + light** — camera dead still; only an accent glow sweeps or a value pulses.

## Shot archetypes (mix these across the arc)

- **UI-in-the-void** — the screenshot floats centered in dark volumetric space, soft accent glow
  behind it, faint grain. The workhorse shot.
- **Device-held** — the screen composited into a floating laptop/phone with realistic edge light
  and a subtle reflection. Use sparingly (1–2 per ad).
- **Flat hero push-in** — the raw screenshot, edge-to-edge or matted, slow push. Zero morph risk
  (no regeneration). Use when the screen is gorgeous on its own.
- **Detail crop** — a tight push on ONE component (a button, a status pill, a number) to sell a
  single feature.
- **Atmosphere / brand** — no UI: drifting particles, light streaks, the mark forming. Bridges
  beats and opens/closes.
- **Logo lock** — the final hold: logo + tagline on black, accent glow, dead still 2–3s.

## The 4-act arc (scale to duration)

| Act | Beat | Typical content |
|-----|------|-----------------|
| 1 | **Hook** | Cold open from black → one bold line of text, or the problem stated visually |
| 2 | **Problem** | The old way (chaos: tabs, spreadsheets, generic tools) — brief, tension |
| 3 | **Reveal** | The product. 2–5 feature beats, one real screen each, accent pulses on each |
| 4 | **Payoff + lock** | The outcome (a number, a calm dashboard) → logo lock + tagline + CTA |

A single Seedance render can hold **multiple internal cuts** via a timestamped prompt (five shots
inside one 15s clip). Plan in *shots*, then pack them into 15s timestamped renders:

- **15s:** one render, ~3–5 timestamped shots — hook, 2–3 feature reveals, logo lock.
- **30s:** two 15s renders (~3–5 shots each), concatenated.
- **60s:** ~four 15s renders, concatenated — more feature beats + atmosphere bridges.

## On-screen text

- One short line per beat (≤6 words). Verb-first, benefit-led. Pull real nouns/numbers from the UI.
- Inter / Inter-class, tight tracking, high weight for the key word, the accent color for emphasis
  only.
- Lower-third or centered, generous margin. Fade in ~6 frames, hold, fade out. Never crowd the UI.

---

## Prompt templates

### GPT Image 2 — UI-in-the-void hero frame (screenshot as `image` reference)

```
A single software interface screen floating centered in a vast pitch-black studio void.
The interface is shown flat and perfectly sharp, fronto-parallel, undistorted. A soft
volumetric glow in <ACCENT_HEX> rises behind it; faint film grain; deep shadow falloff
to pure black at the edges. Cinematic product photography, shallow depth, premium and
quiet. Massive negative space. <VISUAL_DNA_LINES>
```
Params: `quality: high`, `resolution: 2k`, `aspect_ratio: <intake>`, one `image` reference = the
screenshot. (Do NOT ask the model to redraw UI contents — it should treat the screenshot as a flat
plane it lights and frames.)

### GPT Image 2 — device-held frame

```
A floating <laptop|phone> in a pitch-black void, screen displaying the provided interface
exactly and sharply. Realistic thin edge light in <ACCENT_HEX>, subtle screen reflection,
soft glow, fine grain. Centered, lots of dark negative space. Cinematic, premium, restrained.
<VISUAL_DNA_LINES>
```

### GPT Image 2 — logo lock / atmosphere (text-to-image, no reference)

```
<LOGO/WORDMARK or abstract mark> centered on pure pitch black, a soft <ACCENT_HEX> glow
behind it, drifting fine particles, faint grain, deep cinematic vignette. Minimal, confident,
expensive. <VISUAL_DNA_LINES>
```

### Seedance 2.0 — animate a UI hero frame (locked frame)

```
Slow <PUSH-IN ~3% | LATERAL DRIFT ~1.5% | RACK FOCUS>. The camera moves; everything else holds.
A faint <ACCENT_HEX> glow breathes once. Subtle film grain, premium cinematic atmosphere, calm
pacing. Interface stays perfectly sharp and static; do not warp, morph, distort, or re-render
any UI text, icons, charts, or layout. Only the camera and light move. <VISUAL_DNA_LINES>
```
Params: `model: seedance_2_0`, `medias:[{role:"start_image", value:<frame id>}]`,
`duration: <4–15>`, `aspect_ratio:<intake>`, `generate_audio: false`.

### Seedance 2.0 — atmosphere / logo-lock motion

```
Drifting particles and a slow-breathing <ACCENT_HEX> glow on pure black; the mark holds dead
center, rock steady. Extremely slow, minimal, premium. <VISUAL_DNA_LINES>
```

### Seedance 2.0 — timestamped multi-shot in ONE 15s clip (the workhorse)

Pack several cuts into a single render. Pass the beat's hero frames as `image` references (the most
important real screenshot can also be the `start_image`), then write the prompt as timecoded blocks:

```
A single continuous 15-second cinematic sequence of hard cuts. Pitch-black throughout, one accent.
00:00–00:03 — cold open: <ACCENT_HEX> glow blooms from black, clear space for a title line.
00:03–00:07 — cut to the dashboard screen (ref 1): slow 3% push-in, accent pulses once.
00:07–00:10 — cut to the inbox screen (ref 2): gentle lateral drift.
00:10–00:13 — cut to the detail screen (ref 3): rack focus settles sharp.
00:13–00:15 — logo lock: the mark holds dead center on black, glow breathes.
Each interface stays perfectly sharp and static within its shot; do not warp, morph, or re-render
any UI text, icons, or layout — only the camera and light move, between and within cuts. <VISUAL_DNA_LINES>
```
Params: `medias` = the beat's frames as `role:"image"` (key screen as `role:"start_image"`), cap
~9 refs, `duration:15`, `resolution:"1080p"`, `generate_audio:false`. Tradeoff: only the
`start_image` is pixel-exact — reserve razor-sharp-UI beats for their own `start_image` shot.

## The Visual DNA block (built in Phase 2, pasted verbatim into every prompt)

Six lines, locked once, never paraphrased:

```
1. Palette: pitch-black canvas (#0A0A0A), single accent <ACCENT_HEX>, light text <TEXT_HEX>.
2. Type: <product font or Inter-class>, tight tracking, high contrast in weight.
3. Texture: fine film grain, soft volumetric glow, deep vignette, clean shadow falloff to black.
4. Camera: slow, deliberate, expensive; minimal movement; nothing whips.
5. Mood: quiet confidence — Anthropic / Linear / Vercel design DNA.
6. Guardrail: UI is a flat, sharp, static plane — never warp or re-render interface text/layout.
```
