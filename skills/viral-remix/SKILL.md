---
name: viral-remix
description: >
  Turn any viral video URL into AI-generated remix clips that recreate its exact
  beats, camera moves, and visual style. Watches the source video frame-by-frame
  (via the /watch skill), breaks it into precise timestamped beats — character
  action, camera movement (pan/zoom/dolly/cut), pacing, visual style — then
  writes and renders one Higgsfield Seedance 2.0 timestamped prompt per
  15-second window, using the original frames as direct references, and
  stitches the renders into one finished remix video. Fully autonomous: one
  video URL in, a finished 9:16 720p remix out — no check-ins. Trigger on
  /viral-remix, "remix this video", "recreate this viral video", "turn this
  into an AI video", "make an AI version of this clip", or a pasted video URL
  plus "remix this" / "recreate this" / "make this go viral for me". NOT for
  turning a product photo into an ad (use ad-studio / saas-ad-studio) and NOT
  for a text-only breakdown of what makes a video work without rendering
  anything (use viral-format-miner).
argument-hint: "<video URL or local path>"
allowed-tools: Bash, Read, Write
---

# Viral Remix — watch a video, rebuild it beat-for-beat with AI

You take one viral video and produce a direct AI visual recreation of it: same beats, same
camera moves, same pacing, same look — regenerated as Higgsfield Seedance 2.0 clips. This is
**recreation, not recasting** — no new subject/brand/product is introduced. The extracted
frames from the source video ARE the references fed into every render.

Fully autonomous. One input (a video URL or local path), no check-ins. Output is a finished
`remix-final.mp4` plus every intermediate artifact (beats, visual DNA, prompts, per-window clips)
so the breakdown is inspectable even if the user only wants the video.

## Requirements

- **A "watch a video" capability** — download the source and extract frames + transcript. If a
  `/watch` skill/plugin is installed, use it (it wraps this whole pipeline). Otherwise do it
  directly: `yt-dlp` to download the video, `ffmpeg` to extract frames, and captions or local
  Whisper for the transcript (no API key needed for local Whisper).
- **Higgsfield** for the render (image/video gen), model `seedance_2_0`. Either the Higgsfield MCP
  (`generate_video` — tool name prefixed per your install) **or** the public `higgsfield` CLI
  works; the CLI commands below are the reference path.
- **ffmpeg + ffprobe + yt-dlp** on `$PATH`.
- **Graceful fallback:** if none of a `/watch` skill, `yt-dlp`, or Higgsfield is available, tell
  the user what to install (`pip install yt-dlp`, add the Higgsfield MCP or install the CLI) and
  stop rather than guessing. No key is ever embedded here.

## Tooling

- **Watch the source** — prefer an installed `/watch` skill's script; it downloads with `yt-dlp`,
  extracts auto-scaled frames with `ffmpeg`, and pulls the transcript from captions (or local
  Whisper). If you have it, resolve its script path once per run and shell out to it (don't
  reimplement frame extraction). If you don't have it, run `yt-dlp` + `ffmpeg` + Whisper directly
  with the same inputs/outputs the steps below assume. Transcript quality doesn't gate rendering —
  frames are the primary signal, transcript is a secondary cue for pacing/voice beats. The command
  examples below assume a `watch.py` on `$WATCH_DIR/scripts/`; substitute your own extraction if
  the skill isn't installed.
- **Render** — the `higgsfield` CLI (install via the official Higgsfield CLI install script if
  missing) or the Higgsfield MCP. Model: `seedance_2_0`. Always pass `--wait` so the command
  blocks and prints the result URL — never the two-step `create` → `wait` pattern.
- **Assemble** — `ffmpeg` (installed) to concat per-window clips into one final video.

## Pipeline

### 1. Preflight
Confirm `ffmpeg`, `ffprobe`, `yt-dlp`, and `higgsfield` (or the Higgsfield MCP) are all
available. For the CLI, `higgsfield account status` should succeed — if it says session expired,
ask the user to run `higgsfield auth login`. If an installed `/watch` skill provides a `watch.py`,
resolve its path once per run and run its `setup.py --check`; on non-zero exit follow its
remediation (install `ffmpeg`/`yt-dlp`; local Whisper needs no key):
```bash
# resolve an installed /watch script if present, else fall back to yt-dlp + ffmpeg directly
WATCH_PY=$(find "$HOME/.claude" -name "watch.py" -path "*watch*" 2>/dev/null | sort -V | tail -1)
[ -n "$WATCH_PY" ] && WATCH_DIR=$(dirname "$(dirname "$WATCH_PY")")
```

Slugify the source (title or filename) and create the output tree (default under the current
working directory; adjust to wherever the user wants output):
```
./viral-remix/<video-slug>/{frames/, clips/}
```

### 2. Probe the full video
```bash
python3 "$WATCH_DIR/scripts/watch.py" "<source>"
```
This gives duration, title, native aspect ratio, and the full timestamped transcript in one
light pass. Note the total duration — it drives segmentation.

### 3. Segment into 15-second windows
`N = ceil(duration / 15)`. Windows are `[0,15), [15,30), ...` with the last window shorter if
duration isn't a multiple of 15.

**Why windows exist at all:** Seedance 2.0 can stitch multiple beats/cuts *inside* one render via
a timestamped multi-shot prompt (see Step 7) — but it has a **hard 15-second ceiling per render**.
It cannot span past that in a single call, no matter how the prompt is written. Windowing isn't a
stylistic choice, it's working around that ceiling: each window is exactly what fits in one
Seedance call. A source video ≤15s needs only one window — one render, done, no stitching later.

### 4. Watch each window densely
For each window, call `/watch`'s script in focused mode for frame-accurate density:
```bash
python3 "$WATCH_DIR/scripts/watch.py" "<source>" --start <window_start> --end <window_end> \
  --resolution 1024 --out-dir "$PWD/frames/window_<NN>"
```
`--resolution 1024` (not the 512 default) so on-screen text/detail is legible in the extracted
stills. These frames are the actual visual content of that 15-second slice of the source
video — in Step 8 they get passed straight into Seedance as `--start-image`/`--image`
references, so the render is generated *from* real footage rather than hallucinated from the
prompt text alone. Read every frame path returned, plus the window's transcript slice.

### 5. Beat extraction → `beats.md`
For each window, write sub-timestamped beats grounded in what you actually saw in the frames —
never invent action that isn't visible:
- **Character action** — what the subject physically does, moment to moment
- **Camera movement** — static / pan / tilt / zoom / dolly / handheld / hard cut, and direction
- **Pacing** — cut frequency, holds vs. rapid cuts
- **On-screen text or style cues** — captions, graphics, filters, color grade notes
- Cite the source frame path for each beat

### 6. Visual DNA → `dna.md`
Synthesize ONE cross-window style summary from all the frames: color grade, lighting quality,
lens feel (wide/telephoto, depth of field), edit rhythm, mood, any recurring visual motif. This
is the consistency anchor appended to every render prompt so windows don't visually drift from
each other.

### 7. Prompt generation → `prompts.md`
One Seedance 2.0 prompt per window, bracket-timecoded relative to the window (always starting at
`00:00`, since each window renders as its own independent clip):
```
[00:00-00:03] <camera move> — <character action>
[00:03-00:07] <camera move> — <character action>
...
<Visual DNA line — color grade / lighting / lens / mood, kept identical across every window>
Recreate the visual style and motion exactly as shown in the reference frames; do not invent
new elements, subjects, or text not present in the references.
```
Keep each bracket line to camera motion + action only — the reference frames carry the actual
look, the prompt just tells the model how to move between them.

### 8. Render
One Seedance call per window. Within that single call, the bracket-timecoded prompt from Step 7
handles every internal cut/camera-move for that window's beats — Seedance does that stitching
natively. What Seedance can't do is carry that render past 15 seconds or across windows, which is
exactly why Step 9 exists.

Per window:
```bash
higgsfield generate create seedance_2_0 \
  --prompt "<window's timestamped prompt>" \
  --start-image "frames/window_<NN>/<first frame>" \
  --image "frames/window_<NN>/<second frame>" \
  --image "frames/window_<NN>/<third frame>" \
  ... \
  --duration <window_length_seconds> \
  --aspect_ratio 9:16 \
  --resolution 720p \
  --wait --json
```
**Fixed output spec: 9:16 / 720p**, regardless of the source video's native aspect ratio or
resolution. Cap references at ~9 per window (Seedance's documented limit) — if a window has more
frames than that, pick the 9 most representative (start, end, and evenly spaced between).
Download each result to `clips/<NN>.mp4`, binding strictly by window index — never by completion
order, since renders can finish out of order.

If a window's render clearly breaks (subject warps unrecognizably, motion is incoherent), retry
that window once with a tighter/simpler prompt. Don't loop indefinitely — after one retry, keep
the best result and note the issue in the final report.

### 9. Assemble
This step only stitches **between** windows — the boundary Seedance can't cross on its own (Step
8). It does nothing *within* a window; that stitching already happened inside each render.

If there's only one window (source ≤15s), skip concat entirely — just copy `clips/01.mp4` to
`remix-final.mp4`. Otherwise, concat all window clips in order:
```bash
ffmpeg -f concat -safe 0 -i <(for f in clips/*.mp4; do echo "file '$PWD/$f'"; done) \
  -c copy remix-final.mp4
```
If codecs/params mismatch and `-c copy` fails, re-encode instead (`-c:v libx264 -c:a aac`).

### 10. Report → `report.md`
Summarize: total beats extracted, number of windows, any window that needed a retry or fell back
to a best-effort render, and links to every artifact. Print the final output tree and the path to
`remix-final.mp4`.

## Output folder (per run)

```
viral-remix/<video-slug>/
├── beats.md          # per-window timestamped beats: action, camera, pacing, style cues
├── dna.md             # cross-window Visual DNA — the consistency line in every prompt
├── prompts.md         # one bracket-timecoded Seedance 2.0 prompt per window
├── frames/
│   └── window_01/, window_02/, ...   # dense frame extraction per 15s window
├── clips/
│   └── 01.mp4, 02.mp4, ...           # rendered Seedance clips, one per window
├── remix-final.mp4    # ffmpeg-concatenated finished remix
└── report.md          # beat count, retries/flags, links to every artifact
```

## Rules

- **Never invent action, subjects, or text not visible in the extracted frames.** The whole
  point is fidelity to the source — if a beat isn't visible in a frame, don't write it.
- **9:16 / 720p is fixed**, not inferred from the source's aspect ratio.
- **No check-ins, no casting step.** This skill runs start to finish on one video URL/path and
  reports at the end — it does not ask the user to approve concepts, storyboards, or a subject.
- **Bind renders by window index, not completion order.**
- If the source video is very long (multiple minutes), still segment into 15s windows across the
  whole thing rather than truncating — warn the user up front if this means a large number of
  renders (and therefore credits), but proceed unless they say otherwise.
