# Higgsfield MCP — tool & model contract

**All tools are prefixed per your Higgsfield MCP install** —
`mcp__<server>__generate_image`, `mcp__<server>__generate_video`, etc. Check your connected MCP
list for the exact server prefix and use those names. No key is embedded here.

## Models we use

### `gpt_image_2` (images / hero frames)
- Params: `quality` (`low|medium|high`, use **high**), `resolution` (`1k|2k|4k`, use **2k**, **4k**
  for a hero/logo frame).
- `aspect_ratios`: `1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3`.
- Reference media: a **single `image` role** only (pass the screenshot to composite).
- Strong at text rendering & editing — that's why it's our frame model.
- ⚠️ There is **no** `gpt-image-2-pro/banana/nano` in this MCP — that was the CLI naming. Control
  quality with the `quality`/`resolution` params instead.

### `seedance_2_0` (video / animation)
- `duration`: **4–15 s per clip** (hard cap → multi-shot ads are always stitched).
- `aspect_ratios`: `auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16`.
- `resolution`: `480p, 720p, 1080p, 4k` (4k only with `mode:std`); `mode`: `std|fast`. Default is
  **720p** — pin `resolution:"1080p"` for a premium master (confirmed via `get_cost` preflight).
- `genre` hint: `auto|action|horror|comedy|noir|drama|epic` (use `auto` or `drama`).
- `generate_audio` (bool, default **true**): **set `false` on UI shots** — we score in post.
- Reference roles: `image, start_image, end_image, video, audio`. We use **`start_image`** = the
  hero frame, plus extra **`image`** refs. Multiple `image` refs + a **timestamped prompt** let ONE
  15s render contain several cuts (pattern below). `kling3_0_turbo` is a fast single-start-frame
  fallback if Seedance is unavailable.

### Audio / music — IMPORTANT (verified)
- There is **NO usable standalone music model** here. `sonilo_music`, `mirelo` (SFX), `inworld` TTS are all **game-pipeline-only** and refuse standalone use; `generate_audio` is **TTS-only** (`text2speech_v2_*`).
- Music + SFX come from the **video models' native audio**: `generate_audio: true` (Seedance / Seedance Mini), `sound:'on'` (Kling 2.6/3.0), or Veo 3.1 / Cinema Studio — describe the score in an `Audio: …` line in the prompt.
- **Best for a cohesive score: ONE single timestamped 15s render with `generate_audio:true`** — Seedance scores the whole clip natively. Per-shot stitching gives choppy audio. Otherwise mux a real / royalty-free track (see `assembly.md`). You cannot QA audio by ear in this harness — surface it to the user to judge.

## The media rule (read this twice)

`medias[].value` must be a **media_id or a prior job_id — NEVER an https:// URL.**

- **Hosted URL** (logo URL, a screenshot you uploaded somewhere): call `media_import_url(url)` →
  returns a `media_id` → pass that as `value`.
- **Local file** (a screenshot on disk in `screens/`): call `media_upload(filename, content_type)`
  → it returns presigned `upload_url`(s) → `PUT` the bytes (or run the returned curl) →
  `media_confirm` → use the returned `media_id`.
- **Chaining a prior generation** (frame → video): pass that generation's **`job_id`** directly as
  the `start_image` value; no re-upload needed.

## Call shapes

Image (composite a screenshot into a hero frame):
```
generate_image(params:{
  model: "gpt_image_2",
  prompt: "<hero-frame prompt> … <Visual DNA lines>",
  medias: [{ role: "image", value: "<screenshot media_id>" }],
  aspect_ratio: "<intake>",
  quality: "high",
  resolution: "2k",
  count: 1
})
```

Video (animate a hero frame, locked):
```
generate_video(params:{
  model: "seedance_2_0",
  prompt: "<locked-frame camera prompt> … <Visual DNA> … <no-morph guardrail>",
  medias: [{ role: "start_image", value: "<frame job_id or media_id>" }],
  duration: <4-15>,
  aspect_ratio: "<intake>",
  resolution: "1080p",          // default is 720p — pin 1080p for a premium master
  generate_audio: false,
  count: 1
})
```

## Timestamped multi-shot — many cuts in ONE 15s render (preferred)

Reuse a single `generate_video` call but pass **several `image` references** and a **timecoded
prompt**. One 15s clip then contains ~3–5 cuts — fewer renders, native cuts, one cohesive grade.
This is how `ad-studio` renders its 15s ad.

```
generate_video(params:{
  model: "seedance_2_0",
  prompt: "A 15s sequence of hard cuts. 00:00–00:03 cold open … 00:03–00:07 cut to screen (ref 1) … "
        + "00:07–00:11 cut to screen (ref 2) … 00:11–00:15 logo lock. <Visual DNA> <no-morph guardrail>",
  medias: [
    { role: "start_image", value: "<frame 1 — the crispest / most important screen>" },
    { role: "image",       value: "<frame 2>" },
    { role: "image",       value: "<frame 3>" }   // cap ~9 references
  ],
  duration: 15,
  aspect_ratio: "<intake>",
  resolution: "1080p",
  generate_audio: false
})
```

**Tradeoff:** only `start_image` is pixel-exact at frame 1; cuts to the other refs are
model-generated, so reserve the timestamped clip for cinematic beats and isolate any
razor-sharp-UI beat as its own `start_image` shot. For 30/60s ads, render 2–4 of these 15s
segments and concat them in assembly.

## Polling, displaying, downloading

1. `generate_*` returns a job (id + status). If it isn't already terminal, poll
   `show_generations` (lists recent jobs/status) or `job_display(id)` until status is
   `completed`/terminal.
2. Grab the result **CDN URL** from the completed job.
3. Download to disk with Bash:
   ```bash
   curl -L -o shots/01.mp4 "<result_url>"      # videos → shots/
   curl -L -o frames/01.png "<result_url>"     # images → frames/  (if you need the file locally)
   ```
4. `job_display(id)` renders a result inline for the user / brief.html.

## Parallelism, retries, cost

- **Frames (Phase 3):** fire all `generate_image` calls in one batch; **bind each job to its frame
  filename** (completion order is not submission order). Eyeball each as it lands; re-render any
  that break brand/UI fidelity — **max 2 retries**, then keep best and flag it.
- **Videos (Phase 4):** submit in **batches of ~4** (concurrency ceiling), poll each batch to
  terminal before the next. One informed retry per broken shot (tighten/lower the motion), then
  move on — never loop endlessly.
- **Preflight cost:** add `get_cost: true` to a `generate_*` call to get the credit cost **without
  submitting any job**. Do this before a large video batch if the user is watching spend.
- **Upscale:** `upscale_video(<job_id/url>)` for a final 4K master if asked.

## Gotchas (all hit on real runs)

- **Preset interception:** a cinematic prompt (e.g. "dark room/studio") may return a
  `preset_recommendation` notice **instead of submitting**. To run your literal prompt, resubmit
  with `declined_preset_id: "<id from the notice>"` inside `params`.
- **Polling:** `show_generations` lags — completed jobs take a while to appear and it can omit very
  recent ones. Poll a **specific job with `job_display(id)`**: it reliably returns `status` plus the
  result `rawUrl` to download.
- **Audio:** no standalone music model — see the Audio note above; use video-model `generate_audio`.
- Seedance occasionally trips a content filter on certain words — re-prompt neutrally and resubmit.
- Confirm a model's current params with `models_explore action:get model_id:<id>` before the first
  render in a session — catalogs change.
