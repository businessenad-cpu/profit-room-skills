---
name: youtube-clipping-agent
description: >
  Clips ranked compilation videos (e.g., "Top 50 NBA Dunks", "Top 20 Movie Scenes") into individual
  vertical 9:16 clips with smart cropping and lower-third rank/title overlays.
  Identifies each ranked item via AI transcript analysis, clips them out, reformats to vertical
  with face-aware cropping, and adds text overlays showing rank and description.
  Keywords: ranked video, compilation, top 10, clips, vertical video, shorts, reels, smart crop
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
model: claude-sonnet-4-6
---

# YouTube Ranked Compilation Clipping Agent

Automatically clip ranked compilation videos into individual vertical (9:16) clips with smart cropping and text overlays.

## Phase 0: Get Video URL

**If the user provided a YouTube URL** → skip to Phase 1.

**If the user provided a search query (no URL):**

```bash
python3 -m yt_dlp "ytsearch10:<query>" \
  --flat-playlist --dump-json 2>/dev/null
```

Parse the JSON lines and filter to videos where:
- `duration` is between 180 and 1800 seconds (3–20 min)
- `live_status` is not `"is_live"`

From the filtered results, display the top 5 as a numbered list:
```
1. [Title] — [Channel] — [duration as M:SS] — [view count]
   https://youtube.com/watch?v=<id>
2. ...
```

Use AskUserQuestion to ask the user to pick one (or type a different query). Then proceed with that URL.

---

## Phase 1: Environment Check

Verify all required tools are installed before proceeding.

```bash
python3 -m yt_dlp --version
ffmpeg -version
python3 --version
python3 -c "import cv2; print('opencv', cv2.__version__)"
python3 -c "import yt_dlp; print('yt-dlp ok')"
```

**Note**: Use `python3 -m yt_dlp` not `yt-dlp` directly — the module is installed via pip but may not be on PATH.

If any dependency is missing, provide the appropriate install commands and **stop execution**. Do not proceed until all dependencies are confirmed working.

## Phase 2: Download Video + Transcript

- Ask the user for a YouTube URL (or accept one from the invocation arguments).

### 2a. Get Transcript (VTT subtitles)

Pull the video's captions with yt-dlp and parse them — no API or MCP needed:

```bash
cd ~/.claude/skills/youtube-clipping-agent && python3 scripts/download_video.py <url>
python3 scripts/analyze_subtitles.py <subtitle_path>
```

This returns the transcript text and timestamps. If you have another transcript source available (any MCP or tool that returns clean YouTube transcript text), you can use it instead — the rest of the pipeline only needs the transcript text plus the video title.

### 2b. Download Video

**IMPORTANT**: YouTube blocks most formats with 403 errors due to SABR streaming. Always use the `android` player client to bypass this:

```bash
python3 -m yt_dlp \
  --extractor-args "youtube:player_client=android" \
  -f "best[height<=720]" \
  -o "/tmp/VIDEO_ID.%(ext)s" \
  "<url>"
```

- Do NOT use the `download_video.py` script for the video itself (it uses the default client which gets 403).
- After download, copy the file to `~/.claude/skills/youtube-clipping-agent/VIDEO_ID.mp4`.
- Show the user: title, duration, and file size.

### 2c. Extract YouTube Metadata (Chapters + Title)

Always fetch the full video metadata JSON immediately after getting the URL:

```bash
python3 -m yt_dlp -j "<url>" 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('TITLE:', d.get('title'))
print('CHAPTERS:')
for c in (d.get('chapters') or []):
    print(f\"  {c['start_time']}s - {c['end_time']}s: {c['title']}\")
"
```

**Chapter titles**: If the video has YouTube chapters, use them as the primary source of segment boundaries AND clip titles (see Phase 3). Chapter titles are already human-curated and should be preferred over transcript analysis.

**Max clips per video**: Never produce more than 10 clips per output video. If the source has more than 10 ranked items (e.g. a Top 20), split into two separate Top 10 videos:
- Video A: items #20–#11, renumbered #10→#1 (with "TOP 10 PART 1" intro)
- Video B: items #10–#1, renumbered #10→#1 (with "TOP 10 PART 2" intro, or "THE BEST 10" etc.)
Each video gets its own output directory, intro montage, and FINAL concat.

**Intro title reformat**: Take the raw YouTube title and reformat it for the intro card using these rules:
- Prefix with "TOP N" where N = the actual number of clips being produced (use the count from the title if chapters match, otherwise use the real chapter count — e.g. title says "10" but only 7 chapters → use "TOP 7"; cap at 10 per video)
- Make the subject/action more punchy and social-media friendly
- Keep it short enough to fit ~4 words per line on a vertical frame
- Examples:
  - "Jeff Hardy's 10 most jaw-dropping dives" → "TOP 10 | JEFF HARDY'S | MOST INSANE | DIVES"
  - "Top 50 NBA Dunks of All Time" → "TOP 50 | NBA | DUNKS | OF ALL TIME"
  - "10 Heaviest Wrestlers" → "TOP 10 | HEAVIEST | WRESTLERS | OF ALL TIME"
- Each pipe-separated word/phrase becomes one stacked line in `get_intro_overlay_filter`
- First arg is always "TOP N" (gold), remaining args are white body lines

## Phase 3: AI Analysis

This is the core phase where Claude identifies each ranked item with timestamps and titles.

**Source priority** (use whichever is available, in this order):
1. **YouTube chapters** (from 2c) — preferred when available. Chapter `start_time` and `title` are already the segment boundary and clip title. Assign rank numbers in order of appearance (first chapter = #10 counting down, or #1 counting up — match the video's own ordering).
2. **Transcript** (VTT subtitles) — fall back when chapters are missing or incomplete.

### 3a. Chapter-based analysis (when chapters available)

Convert each YouTube chapter into a clip entry. The chapter title becomes the overlay title — clean it up if needed (remove event names/dates if too long, keep the action phrase):

```json
[
  {"rank": 10, "title": "ENTRANCE STAGE DIVE", "subtitle": "Raw, Jan. 14, 2008", "start_seconds": 0, "end_seconds": 19, "description": "..."},
  ...
]
```

- `title`: The action/move name (Impact font overlay, max ~20 chars)
- `subtitle`: Event or date context from the chapter title (DIN font overlay, max ~25 chars)
- If the chapter title has a pipe or dash separator (e.g. `SWANTON ANYWHERE | One Night Stand 2008`), split on it: left side → title, right side → subtitle

### 3b. Transcript-based analysis (fallback)

Use the transcript from the VTT subtitle text and analyze it directly as Claude — no need to run a separate script.

**CRITICAL**: Use the following prompt to analyze the transcript:

```
Analyze this transcript from a ranked compilation video. Identify each ranked item (e.g., "Number 10", "#5", "Coming in at number 3", "And the number one spot goes to...").

For each ranked item, extract:
- rank: The ranking number
- title: A short descriptive title (max 40 chars) for the overlay
- start_time_seconds: When this segment begins (in seconds from the VTT timestamps)
- description: One sentence describing the clip content

**Clip duration**: Each clip should be 5-10 seconds max, starting ~1 second before the rank is announced.
So end_time = start_time + 8 (seconds).

Look for these patterns:
- Explicit numbering: "number 10", "number nine", "#5", "at number 3"
- Countdown language: "coming in at", "taking the X spot", "and at X"
- Transition phrases: "next up", "moving on to", "and finally"
- Superlative language for #1: "the greatest", "number one", "the top spot", "and the winner"

IMPORTANT:
- The video may count UP (1 to N) or DOWN (N to 1) - detect which pattern is used
- start_time is the segment boundary only — clip start will be set to peak_frame - 0.5s in Phase 3c
- Each clip should be 5-10 seconds long (not the full segment)

Output as JSON array with times in seconds:
[
  {"rank": 10, "title": "...", "start_seconds": 12, "end_seconds": 20, "description": "..."},
  ...
]
```

To get timestamps, also run the subtitle extraction script on the VTT file to see `[HH:MM:SS.mmm]` markers:

```bash
python3 scripts/analyze_subtitles.py <subtitle_path>
```

Parse the VTT file directly for exact timing of keyword matches (rank announcements).

- After generating the JSON, save it to a temp file and validate:

```bash
python3 scripts/detect_ranked_items.py <temp_json>
```

- Show any warnings to the user.

### 3c. Frame Sampling for Peak Action — Process Segments Sequentially

**IMPORTANT**: Process segments one at a time. Extract all frames at **320×240 thumbnail size** — this reduces token cost ~20x vs full resolution while still giving enough detail to identify peak action. Read **1 frame per tool call** (never batch multiple image reads in one message).

**For each segment, follow this loop:**

**Step 1 — Initial sample (3 frames at 320×240):**
```bash
mkdir -p /tmp/frames_segN
# Sample at 33%, 50%, 67% through the segment — always scale to 320x240
ffmpeg -y -ss <T_33> -t 0.1 -i <video> -vframes 1 -vf scale=320:240 /tmp/frames_segN/a_33pct.jpg 2>/dev/null
ffmpeg -y -ss <T_50> -t 0.1 -i <video> -vframes 1 -vf scale=320:240 /tmp/frames_segN/b_50pct.jpg 2>/dev/null
ffmpeg -y -ss <T_67> -t 0.1 -i <video> -vframes 1 -vf scale=320:240 /tmp/frames_segN/c_67pct.jpg 2>/dev/null
```

**Step 2 — Read 1 frame at a time, decide after each:**
- Read a_33pct.jpg → if clear peak action found → skip to Step 5
- Read b_50pct.jpg → if clear peak action found → skip to Step 5
- Read c_67pct.jpg → pick the best of what you've seen, or go to Step 3 if all aftermath

**Step 3 — 1s interval scan (only if all 3 initial frames are aftermath):**
Narrow the scan range based on what you saw. Read **1 frame at a time**.

```bash
for t in $(seq <RANGE_START> 1 <RANGE_END>); do ffmpeg -y -ss $t -t 0.1 -i <video> -vframes 1 -vf scale=320:240 /tmp/frames_segN/scan_${t}s.jpg 2>/dev/null; done
```

**Step 4 — Fine pass (optional — only if Step 3 still leaves a 2s+ ambiguous window):**
Narrow to ±1s around candidate, 0.5s intervals (4 frames max). Read 1 frame at a time.
```bash
for t in <PEAK-1.0> <PEAK-0.5> <PEAK+0.5> <PEAK+1.0>; do
  ffmpeg -y -ss $t -t 0.1 -i <video> -vframes 1 -vf scale=320:240 /tmp/frames_segN/fine_${t}s.jpg 2>/dev/null
done
```

**Step 5 — Finalize:** Set `start_seconds = confirmed_peak - 0.5`. Clean up `/tmp/frames_segN/`. Move to next segment.

**Max frames read per segment:** 3 (initial, stop early if action found) + 4 (scan if needed) + 4 (fine pass if needed) = ~11 frames worst case, each read individually. In practice most segments resolve in 1–2 reads.

**Rules for choosing the best clip window:**

- **Target**: the frame where the move/action is MID-EXECUTION (opponent ~45° on the way down, mid-air, or at point of impact) — not before, not after.
- **Avoid**: white/black transition flashes, chapter badge still animating in, aftermath (everyone standing around or already on the mat).
- **Segment start ≠ clip start**: The chapter badge appears at the segment boundary, but the actual action often happens 2–6 seconds INTO the segment. Sample frames and find it — don't assume the right window from boundary timestamps alone.
- **Sometimes the move is gone by frame 1**: If the segment opens on pure aftermath (opponent already flat on the mat), scan further into the segment for the payoff moment — the celebration, the reveal, or the story beat that makes the clip worth watching.
- **yt-dlp chapters may be incomplete**: Videos can have more in-video chapter cards than the metadata reports. If a long metadata chapter (>20s) contains a new chapter card mid-way through, it counts as a separate clip. Always scan frames for new chapter card text to detect these hidden segments.

**Typical search strategy:**

1. Identify segment boundary from transcript/chapters (e.g. 36s–70s)
2. Extract 3 frames at 33%, 50%, 67% — all at **320×240**. Read **1 at a time**, stop as soon as you find clear action.
3. If all aftermath, narrow the scan range and do 1s interval scan — still **1 frame per read**.
4. **Fine pass** (only if still ambiguous): ±1s around candidate at 0.5s intervals (4 frames). Read **1 at a time**.
5. Set `start_seconds` to **0.5s before the confirmed peak frame**

## Phase 4: User Confirmation

Display all detected ranked items in a clear table:

```
Detected N ranked items:

#10 [00:12 - 00:20] (8s) - "Title Here"
#9  [00:45 - 00:53] (8s) - "Title Here"
...
```

Use AskUserQuestion to ask:
1. Which items to process (default: all)
2. Any title corrections

## Phase 5: Batch Processing

- Create output directory: `./ranked-clips/{sanitized_title}_{timestamp}/` (relative to project working directory)

**Choose the right processor per clip:**
- **`process_clip.py`** — default. Static crop, fast. Good for ring-level shots and close-ups where the action stays in one place.
- **`process_clip_panscan.py`** — use when the action spans the full frame width, involves aerial/wide shots, or the static crop cuts off the move (e.g. cage dives, ladder spots, outdoor scenes). Samples motion every second and animates the crop.

Same CLI interface for both:
```bash
cd ~/.claude/skills/youtube-clipping-agent && python3 scripts/process_clip.py \
  <video> <start> <end> <rank> "<title>" <output_path> --subtitle "<event/date>"
# or swap in process_clip_panscan.py for wide/moving action
```

- **Launch ALL clips simultaneously** using `run_in_background=true` — fire every clip as a separate background task in a single message, then wait for all of them with `TaskOutput` (another parallel batch).
- Continue on individual clip failures (report at end).
- Verify output by running `ls -lh` on the output directory.

**Note**: `ffprobe` is not always installed. Both scripts use `ffmpeg` for probing instead.

**Subtitle arg**: Always pass `--subtitle "<Event, Date>"` — this shows the event/date context in the lower-third overlay.

## Phase 6: Intro Montage + Final Concatenation

Build a ~3-second intro montage (0.3s flashes of each clip in countdown order) then concatenate everything into one final video.

**Always write this as a self-contained `/tmp/build_intro.py` script** and run it — never inline the FFmpeg calls as shell commands. Use subprocess list args throughout (no string interpolation).

The script needs:
- `SOURCE` — path to the raw downloaded video (`.mp4` in skill dir)
- `OUTDIR` — the output directory from Phase 5
- `clips` list — each entry has `rank`, `peak` (timestamp in raw source for the 0.3s snippet), and `file` (filename in OUTDIR). Use the peak action timestamps from Phase 3c.
- `CROP_W`, `CROP_H`, `CROP_X`, `CROP_Y` — the static crop params for the source (same as used in process_clip.py). Use center crop `(video_width - crop_w) / 2` if unknown.

```python
#!/usr/bin/env python3
import os, subprocess, sys

SKILL_DIR = os.path.expanduser("~/.claude/skills/youtube-clipping-agent")
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))
from text_overlay import get_intro_overlay_filter

SOURCE = os.path.join(SKILL_DIR, "<VIDEO_ID>.mp4")
OUTDIR = "<output_dir>"

# Clips in countdown order (N → 1) with peak timestamps from Phase 3c
clips = [
    {"rank": 10, "peak": <t>, "file": "clip_10_<name>.mp4"},
    # ... one entry per clip, highest rank first
]

CROP_W, CROP_H, CROP_X, CROP_Y = <w>, <h>, <x>, 0

# Step 1: Extract 0.3s snippets from RAW source (NOT processed clips)
snippet_files = []
for c in clips:
    snip = f"/tmp/intro_snip_{c['rank']:02d}.mp4"
    subprocess.run(["ffmpeg", "-y", "-ss", str(c["peak"]), "-t", "0.3", "-i", SOURCE,
        "-vf", f"crop={CROP_W}:{CROP_H}:{CROP_X}:{CROP_Y},scale=1080:1920",
        "-c:v", "libx264", "-crf", "23", "-preset", "ultrafast",
        "-c:a", "aac", "-b:a", "128k", snip], check=True)
    snippet_files.append(snip)

# Step 2: Build intro — concat snippets + title overlay
intro_path = os.path.join(OUTDIR, "_intro.mp4")
n = len(snippet_files)
inputs = []
for s in snippet_files:
    inputs += ["-i", s]
concat_filter = "".join(f"[{i}:v][{i}:a]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vraw][aout]"
# Each word/phrase is its own stacked line. First arg = "TOP N" (gold), rest are white.
intro_overlay = get_intro_overlay_filter("TOP N", "WORD1", "WORD2", "WORD3")
subprocess.run(["ffmpeg", "-y"] + inputs + [
    "-filter_complex", f"{concat_filter};[vraw]{intro_overlay}[vout]",
    "-map", "[vout]", "-map", "[aout]",
    "-c:v", "libx264", "-crf", "20", "-preset", "medium",
    "-c:a", "aac", "-b:a", "128k", intro_path], check=True)

# Step 3: Concat list — intro first, then clips in countdown order
concat_txt = "/tmp/build_concat.txt"
final_path = os.path.join(OUTDIR, "FINAL_<name>.mp4")
with open(concat_txt, "w") as f:
    f.write(f"file '{intro_path}'\n")
    for c in clips:
        f.write(f"file '{os.path.join(OUTDIR, c['file'])}'\n")

# Step 4: Final concat
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt,
    "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "128k",
    "-movflags", "+faststart", final_path], check=True)

# Cleanup
for s in snippet_files: os.remove(s)
os.remove(concat_txt)
print(f"✅ {final_path}  ({os.path.getsize(final_path)/1024/1024:.1f} MB)")
```

- Run with `python3 /tmp/build_intro.py`
- Clean up snippet temp files and concat.txt after final concat.

## Phase 7: Output Summary

- List all generated clips with file sizes.
- Report the final video path, size, and duration.
- Provide open command: `open "{OUTPUT_DIR}/"`
- Ask if the user wants to adjust any clips or re-process.

## Important Notes

### General
- All scripts are in `~/.claude/skills/youtube-clipping-agent/scripts/`. Always `cd` there before running (for relative imports).
- **Frame verification rate limit**: Extract frames at **320×240** (add `-vf scale=320:240` to all ffmpeg frame commands) — ~80 tokens each vs ~1,700 at full res. Read **1 frame per tool call**, never batch. Process segments sequentially. Most segments resolve in 1–2 reads.
- Output is always **1080x1920** (9:16 vertical).
- **FFmpeg commands**: Always build via Python subprocess list args — never shell string interpolation (causes quoting failures with spaces/special chars).
- **Background tasks**: Do NOT pipe (`|`) at the end of background bash commands — causes SIGPIPE, kills the process before files are written.
- **ffprobe not installed**: Use `ffmpeg -v quiet -show_entries stream=width,height -of json -i <file>` instead. Already handled in `process_clip.py`.

### Downloading
- **yt-dlp command**: Use `python3 -m yt_dlp` not `yt-dlp` (may not be on PATH).
- **YouTube 403**: Always use `--extractor-args "youtube:player_client=android"` — other clients hit SABR streaming blocks.
- **Transcript**: Use the VTT subtitles pulled by `download_video.py`. Prefer manually-uploaded captions over auto-generated ones when both exist (cleaner text).

### Clipping
- **Clip duration**: 5-10 seconds. Use 6s as default.
- **Clip start time**: Always find the peak action frame via Phase 3c sampling FIRST, then set `start = peak - 0.5s`. Never use badge/segment boundary time as the start. The move is often 2–6s into the segment — sample to find it, then cut in tight (0.5s before peak).
- **Peak action frame**: Target mid-execution (opponent 45° on the way down, mid-air, or at point of impact). If only aftermath is available, find the story payoff (celebration, reveal, winner declared).
- **Defining characteristic**: Always extract the key stat for each item (weight, score, year, etc.) and pass it as the `subtitle` arg to `get_drawtext_filter`. This is what makes the overlay informative.
- **Audio**: Include original source audio in all clips (`-c:a aac -b:a 128k`). The audio is the continuous, unedited segment from the source at the clip's timestamps. Do NOT use `-an`.
- **Smart crop verification**: After processing the first clip, check its output frame. If the crop is pulling to the far left or right edge (face detector found crowd/background), **force center crop** for all clips on that source by bypassing `detect_focal_x` and hardcoding `focal_x = video_width / 2`. Low-res sources (≤480p) and footage with large crowds are especially prone to bad face detection.
- **Chapter-based videos**: Not all compilations use explicit rank numbers. Some use chapter titles (e.g. "The Rock's Most Iconic Rock Bottoms"). Still assign sequential numbers (#10 → #1 in order of appearance). Use YouTube chapter data (from Phase 2c) as the primary source of segment boundaries and titles — always prefer chapter titles over transcript-derived titles when both are available.

### Lower-Third Overlay (clip cards)
- **Design**: Compact rectangle, flush left (`x=0`), bottom third of frame. 3-line layout: rank number (gold Impact) + name (white DIN) + defining characteristic (white DIN). Text horizontally centered within the box.
- **Current spec** (`text_overlay.py:get_drawtext_filter`):
  - Box: `x=0, y=1460, w=400, h=254` — compact rectangle, flush left
  - Rank: Impact 120px gold, `x=200-text_w/2, y=1480`
  - Name: DIN Condensed Bold 44px white, `x=200-text_w/2, y=1608`
  - Subtitle: DIN Condensed Bold 36px white, `x=200-text_w/2, y=1658`
  - Text block (120+8+44+6+36=214px) + 20px padding top & bottom = 254px box height
- **NEVER use `h*N` expressions in drawbox** — FFmpeg's `h=` parameter shadows the frame-height variable `h`, placing the box at the wrong position. Always use hardcoded pixel values (output is always 1080×1920).
- **Centering math**: `padding = (box_h - text_block_height) / 2; first_text_y = box_y + padding`
- Text overlay duration: first 4 seconds of each clip (`duration=min(clip_duration, 4.0)`).

### Intro Title Card
- **Design**: No background box. Large left-aligned Impact text stacked vertically on the footage. "TOP N" in gold, each word/phrase of the title on its own line in white. Black border for readability without a panel.
- **Current spec** (`text_overlay.py:get_intro_overlay_filter`):
  - No drawbox — text sits directly on video footage
  - `x=30` (left-anchored), Impact 160px, `line_height=175`
  - `borderw=5:bordercolor=black@0.9` on all lines
  - Top line: gold (`#FFD700`); remaining lines: white
  - **Vertically centered**: `y_start = (1920 - text_block_height) // 2` — auto-calculated for any number of lines
- **Calling convention**: Pass each word/phrase as a separate arg — `get_intro_overlay_filter("TOP 10", "NBA", "DUNKS", "OF ALL TIME")`. Each becomes its own stacked line.
- **Intro snippets**: Always extract from the RAW source video, not processed clips (processed clips have baked-in overlays that will reappear).

### Fonts
- Impact: `/System/Library/Fonts/Supplemental/Impact.ttf` — rank numbers, intro "TOP N" line
- DIN Condensed Bold: `/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf` — names, stats, intro body lines
- Fallback: `/System/Library/Fonts/Helvetica.ttc`
