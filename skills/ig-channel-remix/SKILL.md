---
name: ig-channel-remix
description: >
  Mine any Instagram channel's viral format and render new videos in that format with a
  creative twist. Watches the account's top 10 most-viewed reels, focusing on the first 3
  seconds of each (style, camera, realistic vs. cartoonish, the specific action taking place),
  synthesizes the recurring mechanics into a reusable Format DNA saved to a per-channel library
  (so future runs can recall it or generate more variations without re-mining), then applies a
  twist to the premise while keeping the proven camera/pacing/action mechanics intact (e.g. a
  cute-animal-rescue format becomes a mythological-creature-rescue format; a roller-coaster POV
  becomes a fantasy-world POV) and renders finished remix videos scene-for-scene with Higgsfield
  Seedance 2.0 in 15-second, 9:16, 720p clips, stitching multiple clips together for longer
  source videos. Trigger on /ig-channel-remix, "remix this Instagram channel", "reverse engineer
  this account's viral format", "steal and twist @handle's format", "what's this channel's
  formula and can we put a spin on it", "make more variations of @handle's format", or a pasted
  IG handle/profile URL plus "remix this channel" / "find their format and twist it". NOT for a
  single video 1:1 recreation with no discovery or twist and NOT for text-only hook/caption
  structure analysis.
argument-hint: "<instagram handle or profile URL>"
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# IG Channel Remix — mine a channel's viral format, twist it, render new videos

Point this at one Instagram account. It finds the account's top 10 most-viewed reels, watches
each one's opening 3 seconds frame-by-frame, distills what's actually working mechanically
(style / camera / realism / action), saves that Format DNA to a reusable per-channel library,
then helps pick a creative twist that keeps those mechanics fixed while changing the premise —
and renders finished remix videos scene-for-scene with Higgsfield Seedance 2.0. The
deliverable is video, not a spec document.

## Requirements

- **`yt-dlp`** + **`ffmpeg`/`ffprobe`** on PATH — download reels and extract frames.
- **`python3`** with `requests` (and optionally `browser_cookie3`) — the discovery script.
- **Instagram access** — the discovery script needs a logged-in IG session. It reads your own
  browser session cookies via `browser_cookie3`, OR you can set `IG_SESSIONID` (your account's
  `sessionid` cookie) in the environment. Never commit a cookie/session value. If IG access
  isn't available, the skill falls back to any IG-reels MCP tool you have configured (e.g. a
  vidIQ-style `ig_profile_reels` tool), at reduced reel counts.
- **Higgsfield** — the `higgsfield` CLI on PATH (`higgsfield account status` should succeed; run
  `higgsfield auth login` if the session expired). Video renders always use `seedance_2_0`.
- **A video-watching tool is optional.** If you have a "watch"-style skill/plugin available it
  can stand in for the yt-dlp + ffmpeg frame-extraction steps below; otherwise the inline
  commands are fully self-contained.

## Tooling

- **Discovery** — `scripts/fetch_top_reels.py` in this skill's directory. Pulls the account's
  real per-post `play_count` via Instagram's private API using a logged-in IG session (browser
  cookies via `browser_cookie3`, or the `IG_SESSIONID` env var), ranks by views, returns the
  top 10 reels. This is the validated method — do not reimplement IG scraping ad hoc.
- **Watch (download + frames)** — download each reel once with `yt-dlp`, then pull frames for
  any time window with `ffmpeg`:
  ```bash
  # download the reel once (add --cookies-from-browser chrome for private/age-gated reels)
  yt-dlp -o "frames/reel_<NN>/source.%(ext)s" "<reel url>"
  # extract frames for a [start,end] window at 2fps, scaled to 1024px wide
  ffmpeg -ss <start> -to <end> -i frames/reel_<NN>/source.mp4 \
    -vf "fps=2,scale=1024:-1" "frames/reel_<NN>/window_<MM>/frame_%03d.png"
  ```
  (If you have a dedicated video-watching skill/tool, you can use it instead of these two
  commands — it produces the same thing: frames for a time window, plus an optional caption
  transcript.)
- **Render** — the `higgsfield` CLI. **Video model is always `seedance_2_0`** — never substitute
  another video model. Use `nano_banana_2` only for hero reference stills if the twist needs a
  new subject. Always pass `--wait` so the command blocks and prints the result.
- **Assemble** — `ffmpeg` to concat multi-window renders.
- **Library** — `~/.claude/skills/ig-channel-remix/library/<handle>/`, this skill's persistent
  memory of what it found and chose for each channel (see Library section below). If the skill
  is installed elsewhere, adjust that path to this skill's own directory.

## Fixed render spec (non-negotiable)

- **Model:** `seedance_2_0`, always.
- **Aspect ratio:** `9:16`, always — regardless of the source reel's native aspect ratio.
- **Resolution:** `720p`, always.
- **Clip length: exactly 15 seconds per render.** This is Seedance 2.0's per-call ceiling, and
  we render every window at that ceiling rather than at the source's raw sub-15s remainder
  where avoidable — each clip should read as a full, deliberate 15-second scene, not a
  truncated fragment.
- **Multi-shot via timestamps, not multiple renders, within one clip:** each 15s clip's prompt
  is bracket-timecoded with as many internal shots/cuts as the source reel actually has in
  that window (e.g. `[00:00-00:04]`, `[00:04-00:09]`, `[00:09-00:15]`) — Seedance handles the
  internal cuts natively from one prompt.
- **Multiple clips only when the source exceeds 15 seconds:** `N = ceil(source_duration / 15)`
  windows, each its own independent 15s Seedance render, stitched together afterward with
  `ffmpeg`. A source reel ≤15s is one clip, no stitching.
- **Any living subject must read as alive, not a static prop.** If the twisted (or original)
  subject is a person, animal, or mythical/fantastical creature, every render prompt must
  explicitly call for visible autonomic motion — blinking, breathing/chest movement, natural
  weight shifts, head turns, eye tracking/darting toward action or camera — never a stiff,
  frozen, or mannequin-like pose. This applies doubly to invented subjects (griffins, kelpies,
  etc.) since there's no real-world footage to fall back on for that liveliness — it has to be
  in the prompt.

## Library — recall past mining, generate more variations without re-mining

Every mined channel gets a persistent folder:
```
~/.claude/skills/ig-channel-remix/library/<handle>/
├── meta.json          # last_mined (ISO date), reel_count, source ("cookie" | "mcp_fallback")
├── reels.json          # the top-10 (or fewer) reels mined, with play_count/url/caption
├── analysis.md          # per-reel opening-3s breakdown
├── format-dna.md         # synthesized reusable format spec
├── frames/               # opening 0-3s frames per reel (small, persisted)
└── twists-log.md          # one entry per render run: date, twist used, video count, output path
```
Plus one index: `~/.claude/skills/ig-channel-remix/library/index.json` — a flat map of
`handle → {last_mined, reel_count}` for a fast existence check without globbing.

### Step 0 — check the library before doing anything else
Before Discovery, check whether `library/<handle>/format-dna.md` already exists.
- **If it exists:** tell the user when it was last mined and how many reels it covered, then
  `AskUserQuestion`: reuse the saved Format DNA (skip straight to the twist step) vs. re-mine
  fresh (pull the current top 10 and re-watch, e.g. if the channel has posted a lot since).
  Reusing is the natural path for "make more variations of @handle" requests.
- **If reusing:** load `reels.json`/`analysis.md`/`format-dna.md`/`frames/` straight from the
  library, skip Discovery/Watch/Analysis/Synthesis entirely, and jump to the twist step. Read
  `twists-log.md` first and avoid proposing a twist already tried in a recent entry unless the
  user explicitly asks to repeat/iterate on one.
- **If re-mining:** run the full pipeline and overwrite `meta.json`/`reels.json`/`analysis.md`/
  `format-dna.md`/`frames/` in the library — but only *append* to `twists-log.md`, never
  truncate it; past render history stays recoverable.
- **If no library entry exists:** run the full pipeline as normal and create the library entry
  at the end (see Step 11).

## Pipeline

### 1. Preflight
Confirm `ffmpeg`, `ffprobe`, `yt-dlp`, `python3`, and `higgsfield` are on `$PATH`
(`higgsfield account status` should succeed — if session expired, ask the user to run
`higgsfield auth login`). Slugify the handle and create the output tree:
```
~/Desktop/ig-channel-remix/<handle>/{frames/, refs/, clips/}
```

### 2. Discovery — top 10 by real views
Skip this step entirely if Step 0 chose to reuse the library.
```bash
python3 ~/.claude/skills/ig-channel-remix/scripts/fetch_top_reels.py --handle "<handle>" \
  --top 10 --out reels.json
```
If this exits non-zero (no IG session, private account, API shape change), fall back to any
IG-reels MCP tool you have configured (e.g. a vidIQ-style `ig_profile_reels`, typically capped
around 6 reels, popularity-within-recent-activity, no pagination). Note the fallback and the
reduced count in the final report and in `meta.json`'s `source` field — do not block the run
over it.

### 3. Watch each reel's opening 3 seconds
Skip if reusing the library. Per reel in `reels.json`, download it once and pull the first 3s
of frames:
```bash
yt-dlp -o "frames/reel_<NN>/source.%(ext)s" "<reel url>"   # add --cookies-from-browser chrome if needed
ffmpeg -ss 0 -to 3 -i frames/reel_<NN>/source.mp4 -vf "fps=3,scale=1024:-1" \
  "frames/reel_<NN>/frame_%03d.png"
```
Read every extracted frame plus (optionally) the reel's caption for the 0-3s idea. If a reel
fails to download (deleted, private), skip it and note it in the final report — don't let one
bad reel block the run.

### 4. Per-reel analysis → `analysis.md`
Skip if reusing the library. Grounded strictly in what's visible in the frames — never invent.
For each reel record:
- **Style** — POV selfie, static tripod talking-head, screen recording, b-roll montage,
  whiteboard/hand demo, meme-text-over-clip, etc.
- **Camera** — phone front/back cam, DSLR/mirrorless, screen capture, drone, action cam, or
  AI-generated (no real camera involved).
- **Realism** — live-action photoreal vs. animated/cartoon/illustrated/AI-stylized.
- **Action** — one concrete line: what physically happens in frame 0–3s.
- Secondary cues: aspect ratio, on-screen text/hook overlay present at 0s, cut count within
  the first 3s, first spoken/caption line.

### 5. Synthesize → `format-dna.md`
Skip if reusing the library. Cross-reel pattern synthesis with frequency counts, e.g.:
- "8/10: static front-facing phone camera, no tripod visible"
- "10/10: live-action, zero cartoon/animated openers"
- "7/10: subject already mid-action at frame 0, no wind-up"

This is the mechanical spec that must survive the twist untouched: camera/framing, opening-
beat structure, realism level, pacing. Write it as instructions, not just observations — this
is what Step 9's render prompts pull from.

### 6. Twist concepts — check-in
Generate 3 twist directions that hold every `format-dna.md` mechanic fixed but swap the
subject/premise into something novel. The move is: keep the camera, framing, pacing, and
realism level identical; change what/who is on screen and what they're doing thematically.
Examples: cute-animal-rescue → mythological-creature-rescue (same handheld rescue-footage
camera, same rescue action, same live-action realism, subject is now a griffin/kelpie/etc.);
roller-coaster POV → fantasy-world POV (same GoPro-style mounted camera and motion, same
photoreal-vs-stylized call as the source, setting becomes a fantasy realm).

Check `twists-log.md` (if the library entry already existed) and skip twists already tried
recently unless the user asks to repeat one. Use `AskUserQuestion` to present the 3 concepts
plus a "my own idea" option, and confirm how many remix videos to render (default 3). This is
the one required check-in — the twist materially changes the output and render credits are
real money.

### 7. Reference stills (only if needed)
If the twisted subject has no usable real-world reference (a mythological creature, an
invented setting), generate hero reference stills first:
```bash
higgsfield generate create nano_banana_2 --prompt "<twisted subject, consistent with
format-dna's realism level>" --aspect_ratio 9:16 --resolution 1k --wait --json
```
Save to `refs/`. If the twist keeps a real-world subject (e.g. fantasy *styling* of a real POV
format), skip this — lean on the source frames' camera/motion plus prompt text only.

### 8. Full-video beat extraction for the reels being rendered → `beats.md`
The opening-3s frames from Step 3 are enough to define the Format DNA, but reproducing a reel
**scene-for-scene** needs the whole video's beat structure, not just its opening. For only the
source reels selected for rendering (the confirmed count from Step 6 — not all 10):

1. Probe duration: `ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 frames/reel_<NN>/source.mp4`.
2. Compute windows: `N = ceil(duration / 15)`, windows `[0,15), [15,30), ...`, last window
   shorter only if duration isn't a multiple of 15.
3. Dense frames per window:
   ```bash
   ffmpeg -ss <window_start> -to <window_end> -i frames/reel_<NN>/source.mp4 \
     -vf "fps=2,scale=1024:-1" "frames/reel_<NN>/window_<MM>/frame_%03d.png"
   ```
4. Per window, write sub-timestamped beats grounded in the actual frames — character action,
   camera movement (static/pan/tilt/zoom/dolly/handheld/cut) and direction, cut frequency,
   on-screen text/style cues. This is the shot list the render prompt in Step 9 rewrites with
   the twisted subject — the shot *count and timing* stay the source's, only the subject/action
   content changes per the twist.

### 9. Prompt + render — Seedance 2.0, one 15s clip per window
For each window from Step 8, rewrite its beats with the twisted subject/action but preserve the
shot count, timing, and camera moves exactly:

```bash
higgsfield generate create seedance_2_0 \
  --prompt "[00:00-00:04] <camera move from source beat> — <twisted action>
[00:04-00:09] <camera move from source beat> — <twisted action>
[00:09-00:15] <camera move from source beat> — <twisted action>
<realism/camera/pacing line pulled straight from format-dna.md, unchanged>
<if subject is living: natural blinking, breathing, weight shifts, and head/eye movement —
never stiff or frozen>
Recreate the camera work, shot timing, and pacing exactly; only the subject and setting are
different." \
  --start-image <original frame or generated ref> --image <...> \
  --duration 15 --aspect_ratio 9:16 --resolution 720p --wait --json
```
Cap references at ~9 per window (Seedance's documented limit) — pick the most representative
(start, end, evenly spaced between). Bind renders by source-reel/window index, never
completion order — renders finish out of order. Download to
`clips/remix_<NN>_window_<MM>.mp4` (or `clips/remix_<NN>.mp4` directly if the reel is a single
window).

If a render clearly breaks (subject warps unrecognizably, motion incoherent), retry once with
a tighter prompt, then keep the best result and flag it — don't loop indefinitely.

### 10. Assemble
Only needed for multi-window remixes (source reel >15s) — concat windows for that reel in
order:
```bash
ffmpeg -f concat -safe 0 -i <(for f in remix_<NN>_window_*.mp4; do echo "file '$PWD/$f'"; done) \
  -c copy clips/remix_<NN>.mp4
```
Re-encode (`-c:v libx264 -c:a aac`) if `-c copy` fails on codec mismatch. Single-window remixes
need no concat step — the window's render *is* `clips/remix_<NN>.mp4`.

### 11. Report + update library → `report.md`
Summarize: how many reels were sampled/ranked, any fallback used (cookie method failed → MCP
cap), any reel skipped, the chosen twist, and a link to every finished `clips/remix_*.mp4`.
Print the final output tree.

Then update the library:
- Write/overwrite `library/<handle>/meta.json`, `reels.json`, `analysis.md`, `format-dna.md`,
  and copy `frames/reel_*` (opening 0-3s only, not the full-video Step 8 frames) into
  `library/<handle>/frames/`.
- Append one entry to `library/<handle>/twists-log.md`: date, twist chosen, number of clips
  rendered, path to this run's `~/Desktop/ig-channel-remix/<handle>/` output.
- Update `library/index.json` with this handle's `last_mined`/`reel_count`.

## Output folder (per run)

```
~/Desktop/ig-channel-remix/<handle>/
├── reels.json           # top 10 (or fewer, on fallback): shortcode, play_count, caption, url
├── frames/
│   └── reel_01/, reel_02/, ...              # opening 0-3s frames (Step 3, all 10 reels)
│       └── window_01/, window_02/, ...       # full-video dense frames (Step 8, rendered reels only)
├── analysis.md           # per-reel opening-3s: style / camera / realism / action / cues
├── beats.md              # per-window scene-for-scene beats for reels being rendered
├── format-dna.md          # synthesized reusable format spec (mechanics the twist must preserve)
├── twist-concepts.md       # the 3 generated options + which one was chosen
├── refs/                  # generated hero reference stills, if the twist needed a new subject
├── clips/
│   └── remix_01.mp4, remix_02.mp4, ...   # finished 15s (or stitched multi-window) remix videos
└── report.md
```

## Rules

- **Never invent action, camera, or style not visible in the extracted frames** when writing
  `analysis.md`/`format-dna.md`/`beats.md`. Fidelity to the source format is what makes the
  twist land — only the subject/premise should change, never the underlying mechanics.
- **The twist check-in is required**, not optional — it's the one point where user judgment
  materially changes the output and where render spend begins.
- **`seedance_2_0` / 9:16 / 720p / 15-second clips are fixed**, regardless of source aspect
  ratio, duration, or resolution. Stitch with `ffmpeg` for sources >15s; never shrink the clip
  length to match a shorter source instead.
- **Bind renders by index, never completion order.**
- One retry per broken render, then move on and flag it.
- **Always save/update the library at the end of a run** (Step 11) so a later "make more
  variations" request can skip straight to the twist step.
- If the account's videos aren't format-consistent (the top 10 are a grab-bag of unrelated
  styles), say so plainly in `format-dna.md` rather than forcing a false pattern — a twist
  needs a real mechanic to preserve.
