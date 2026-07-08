---
name: faceless-video
description: "Four-stage pipeline for faceless educational YouTube video essays — the documentary-narrator style where one everyday thing is revealed to hide a profound story (the Zenn / 'What did ancient humans do at night?' format). STAGE 1: from any topic, research REAL named studies/dates/institutions/stats first, then write a second-person voiceover script (curiosity-gap hook, three evidence pillars, rhetorical re-hook, bookend ending) — clean script only. STAGE 2: after the user records the voiceover, find the new audio file in the folder and transcribe it with local Whisper into a timestamped (and per-phrase) transcript (+ SRT/VTT). STAGE 3: generate one illustrative image per timestamp via Higgsfield GPT Image 2 (16:9), in a consistent hand-drawn style, saved to a single ordered folder. STAGE 4: stitch the images + voiceover into a finished MP4 with FFmpeg, each image held over its phrase's time range. Use whenever the user gives a topic and wants a faceless/documentary/Zenn/RealLifeLore-style video essay, voiceover or narration script, says 'write me a script about [topic]', /faceless-video — OR when they've recorded the voiceover and want it transcribed/timestamped/captioned — OR when they want images/visuals/B-roll generated for each timestamp — OR when they want the images and audio stitched/assembled/rendered into the final video of this kind."
allowed-tools: Read, Write, WebSearch, WebFetch, Bash, Glob, Grep
user-invocable: true
metadata:
  argument-hint: "/faceless-video [a topic, e.g. 'why we dream' or 'the history of the color blue']"
---

# Faceless Video Essay Script Writer

Turn any topic into a finished, teleprompter-ready voiceover script for a **faceless educational video essay** — the style where a mundane, everyday thing is slowly revealed to hide a profound story about who we are. No host on camera, no screenshare. A narrator and B-roll. Think the channel *Zenn*, or the lineage of RealLifeLore / Johnny Harris / Primal Space.

The single source video this format is modeled on: *"What Did Ancient Humans Do at Night?"* — 8:32, 7.6M views. A full annotated teardown lives in `references/anatomy.md`. **Read that file before writing your first script** — it is the reference the rest of this skill compresses.

## Requirements

Each stage has its own dependency; you only need the ones for the stage you're running.

- **Stage 1 (script):** web search only (`WebSearch`/`WebFetch`, or any search MCP such as `firecrawl_search`). No install.
- **Stage 2 (transcribe):** local **Whisper** — `pip install -U openai-whisper` (no API key; runs on-device). `ffmpeg` on PATH is used by Whisper to read audio. If Whisper isn't available, any transcription tool that emits SRT/word timings works — the rest of the pipeline just needs a `<name>.phrases.srt`.
- **Stage 3 (images):** an image generator. This skill is written for **Higgsfield → GPT Image 2** via MCP, but any 16:9 image model works — keep one consistent style across the set and save files as `NN_MM-SS.png`. Never hardcode an API key; use whatever image tool/MCP is configured in the environment.
- **Stage 4 (stitch):** `ffmpeg` + `ffprobe` on PATH.

The scripts assume this skill is installed at `~/.claude/skills/faceless-video/`. If you installed it elsewhere, adjust the `python3 <path>/scripts/...` commands accordingly.

## What makes this format work (the why)

This style converts a small, familiar observation into an existential reveal. It keeps a viewer for 8+ minutes by doing three things relentlessly:

1. **It makes the abstract personal.** Everything is "you" and "your ancestors," never "people in general." The viewer is implicated in their own life.
2. **It earns trust with specificity.** Every claim is anchored to a *real* named researcher + year + institution + a hard number. Specificity reads as authority; vagueness reads as filler.
3. **It withholds and pays off.** It opens a curiosity gap (a question), then keeps the answer just out of reach, dripping evidence until a final reframe lands as a small revelation.

If a script you write feels generic, it is almost always failing #2 (no real specifics) or #1 (drifted into the third person).

## The two stages

This skill runs in four stages with a human recording step between 1 and 2. **Do not try to do them all in one pass.**

- **Stage 1 — Write the script.** Research → write → deliver the clean voiceover script. Then **stop and wait** for the user to record it.
- **Stage 2 — Transcribe the recording.** Once the user says the audio is recorded, find the new audio file and produce a timestamped (and per-phrase) transcript.
- **Stage 3 — Generate images.** Turn the per-phrase transcript into one illustrative image per timestamp (Higgsfield GPT Image 2, 16:9), saved to a single ordered folder. Runs when the user asks for the images/visuals.
- **Stage 4 — Stitch the video.** Assemble the images + voiceover into a finished MP4 with FFmpeg, each image held over its phrase's time range. Runs when the user asks to stitch/assemble/render the final video.

**Stage 1 output:** the clean voiceover script only — no section headers, no timestamps, no B-roll notes, no titles — just the flowing narration, written to be read aloud. Short, spoken sentences and fragments. Default length **~1,500–1,800 words (≈8–10 min)** unless the user asks otherwise. Save it to a file and show it in the response.

(Section labels like "HOOK" below are for *your* construction process. Strip them from the final script.)

---

## Stage 1 — Write the script

### Step 1 — Find the spine

Before researching, decide the three load-bearing creative choices. Everything else hangs off these.

- **The question (your title).** Reframe the topic as one counterintuitive question about everyday life. Not "The history of sleep" → but *"Why do you wake up at 3am?"* The question should make the viewer realize they've never actually thought about something they do constantly.
- **The everyday entry point.** The mundane action or assumption the viewer takes for granted, that you'll open on. (Source video: flipping a light switch.)
- **The contrast type (this decides your hook and your third pillar).** Two kinds of topic, and they flex the structure differently:
  - **Lost-over-history** (e.g. darkness, two-phase sleep, walking everywhere). The shocking contrast is *we used to live the opposite way and gave it up.* The hook pivot is "But for 99.9% of human history, that didn't exist," and Pillar 3 is naturally the "how we lost it / what it costs us" turn.
  - **Hidden-in-plain-sight** (e.g. why we dream, what gut bacteria do, why we cry). The thing was never lost — it happens to you constantly and you've just never examined it. The hook contrast is *hidden scale or strangeness* ("you'll spend six years of your life doing this and then delete the evidence"), NOT a historical-loss claim — forcing "for most of history this didn't exist" here would be factually false. Pillar 3 becomes the deepest mechanism or the highest-stakes "what it really means" reveal instead of a loss.
  Pick the type now; the four-beat hook shape below is constant, but which contrast you use is not.
- **The bookend object.** One concrete image you open on and return to in the final line. It's the emotional anchor. (Source video: the light switch — "we traded all of that for a light switch.") Pick this now so the whole script can aim at it.

### Step 2 — Research real evidence (do this *before* writing — it shapes the structure)

The credibility of this format is built entirely on real, checkable facts. **Research first, write second** — and let the research decide your three pillars, not the other way around. If you pick three pillars from imagination and then go hunting for studies to fit them, you will be tempted to fabricate. Instead, find the strongest real evidence that exists, then build pillars around it.

Use your web search tools (`WebSearch` / `WebFetch`, or any search MCP available such as `firecrawl_search`) to gather, for the topic:

- **3 "evidence pillars."** Each pillar needs at least one *real* anchor: a **named researcher or source + a year + an institution or journal + a hard number or specific finding.** (Source video's anchors: Wonderwerk Cave ~1M yrs; Polly Wiesner, PNAS, 2014, "81% of night talk was stories"; Roger Ekirch, 2001, "500+ references, first & second sleep"; Thomas Wehr, NIMH, 1992, the darkness experiment; Edison, 1879.)
- **Hard numbers to use as hooks:** percentages, spans of years, counts, distances, durations. The format leans on them constantly (99.9%, 300,000 years, 30 feet, 14 hours).
- **One texture detail per pillar** — an etymology, an origin, a vivid concrete image (e.g. "curfew" = French *couvre-feu*, "cover fire"). These make it feel researched and human.

**The anti-fabrication rule (non-negotiable, and here's why):** this skill is for scripts people publish. A fabricated study — a plausible-sounding name, year, and stat that doesn't exist — is the one failure that can destroy the creator's credibility and isn't recoverable. So: **only state a named study, statistic, date, or quote if your research actually surfaced it.** If you can't verify a fact, either find a different real fact or phrase the point without a fake citation. When you're confident in the gist but not the exact figure, write the gist and don't invent a number. Keep a short source list for yourself (not in the final script) so the user can fact-check.

If the topic is genuinely opinion/concept-based and has little hard evidence, tell the user — this format may be the wrong fit, or you'll lean on real history/etymology/documented examples instead of studies.

### Step 3 — Build the structure

Assemble the script in this order. The detailed beat-by-beat anatomy and a phrase bank are in `references/anatomy.md`.

1. **HOOK (~70 words, 4 beats):** (a) second-person present-tense mundane action the viewer will do; (b) the **contrast pivot** — for a *lost-over-history* topic: "But for [huge % / time span], that didn't exist" + a shock stat; for a *hidden-in-plain-sight* topic: a shocking hidden-scale or strangeness stat about a thing happening to them right now ("you'll do this every night and spend six years of your life on it"); (c) a vivid concrete detail that drives the scale home (the old reality, or the strange truth they never noticed); (d) the title asked as an open question. The four beats — mundane → contrast → stakes → question — are fixed; the *kind* of contrast is whatever is actually true for the topic. Never bend a topic into a false historical-loss claim to fit the template.
2. **PROMISE (1 line):** "The answer changes everything we think we know about [noun 1], [noun 2], and [noun 3]." The three nouns are your three pillars — name them here so the body feels foretold.
3. **THREE PILLARS (~2 min each):** each pillar follows the same internal skeleton — *transition in → provocation → real named study → mechanism (how/why) → reframe → thesis line.* Order them so the stakes climb. Pillar 2 is strongest with two studies: one that discovered the idea, one that confirms it. Pillar 3 carries the heaviest payoff — for a *lost-over-history* topic make it the "how we lost it / what it costs us" turn; for a *hidden-in-plain-sight* topic make it the deepest mechanism or the highest-stakes "what this really means about you" reveal. Either way, end the body on the most profound point, not the smallest.
4. **RE-HOOK (rhetorical question stack):** take something the viewer personally experiences and recast it. "We call it [modern label] and treat it like a problem. But what if it isn't a malfunction — what if it's [the thing we lost] reasserting itself?" This is the emotional peak.
5. **OUTRO (poetic recap + bookend):** callback the opening number, give a 3-beat poetic recap of the pillars, then land the final line on the **exact bookend object** from Step 1 + a quiet "and most of us never even knew."

### Step 4 — Write it in the voice

Hold these while drafting (full rules in `references/anatomy.md`):

- **Second person, always.** "You," "your body," "your ancestors." Never drift to "people" or "humans in general."
- **The reframe sentence is the engine.** Short, two beats: *"This wasn't insomnia. This was normal."* Use one at the close of each pillar.
- **Spoken, not written.** Short sentences. Fragments are good. Read it aloud in your head; if it doesn't sound like a person talking over footage, cut it down.
- **Numbers stay concrete and front-loaded.** "For 99.9% of human history" beats "for almost all of history."
- **One idea per video.** Everything serves the single question in the title. Kill tangents that don't.

### Step 5 — Quality pass before delivering

Check, and fix if any fail:

- [ ] Does the opening image return in the final line? (Bookend closed.)
- [ ] Are all three pillars anchored to *real, researched* names/years/institutions/stats — nothing invented?
- [ ] Is it in second person throughout, with no third-person drift?
- [ ] Is there a sharp reframe sentence landing each pillar?
- [ ] Does the promise line's three nouns match the three pillars?
- [ ] Is it the right length and does it read aloud cleanly as voiceover?
- [ ] Have you stripped all section labels from the final delivered script?

Then deliver the clean script (file + in response), and offer the user the short source list you kept so they can verify the facts.

### Step 6 — Hand off and STOP

After delivering the script, the human records the voiceover — that's a step only they can do, so **do not continue to Stage 2 yet.** Tell the user plainly:

> "Record your voiceover and save the file into the same folder as the script (`<that folder>`). Tell me when it's done and I'll transcribe it with timestamps."

Note the folder you saved the script in — Stage 2 looks there for the new recording. Then end the turn and wait. Do not poll or guess that audio exists; wait for the user to say it's recorded.

---

## Stage 2 — Transcribe the recorded voiceover

Trigger this when the user signals the recording exists — e.g. "audio's recorded," "I recorded the VO," "the voiceover is done," "transcribe it," "add timestamps." Transcription runs on **local Whisper** (no API key needed; the `turbo` model is already cached on this machine).

### Step 1 — Find the audio

The recording should be in the folder where you saved the Stage 1 script. If you know that folder, use it. If you don't (e.g. a fresh session), ask the user which folder the recording is in, or for the file path.

The bundled transcriber auto-selects the **newest** audio/video file in a folder, so you usually just point it at the folder. If several recent recordings could match (retakes), show the user the filename it picked and confirm before continuing.

### Step 2 — Run the transcriber

Run the bundled script (it handles model loading, timestamping, and output files):

```bash
python3 ~/.claude/skills/faceless-video/scripts/transcribe.py "<folder-or-audio-file>"
```

It writes three files next to the audio and echoes the transcript to stdout:
- `<name>.timestamped.txt` — the main deliverable, `[MM:SS] line of narration` per segment
- `<name>.srt` and `<name>.vtt` — for video editors / burning captions

Useful flags:
- `--phrase` — also break the transcript into short **per-phrase** chunks (split on the natural comma/period/pause beats), writing `<name>.phrases.txt` + phrase-level `<name>.phrases.srt`/`.vtt`. This is what you want for burned-in captions or fine B-roll/motion timing. Tune chunk size with `--max-words N` (default 12; use 5–6 for tighter caption chunks) and `--gap SECONDS` (pause that forces a split, default 0.65).
- `--model small` (or `base`) — faster, slightly less accurate; default is `turbo` (best, already cached)
- `--words` — emit raw word-level timestamps to `<name>.words.tsv` (for karaoke-style per-word timing)

### Step 3 — Deliver

Show the user the `[MM:SS]` timestamped transcript in the response and the saved file paths. Mention the `.srt`/`.vtt` are ready for their editor. If they want it mapped to the script's structural beats (hook / pillar 1–3 / outro), you can label the segments using the Stage 1 script — offer it, don't assume.

**If no audio is found:** tell the user which folder you searched and ask them to drop the recording there or give the path. Don't fabricate a transcript.

---

## Stage 3 — Generate one image per timestamp

Trigger this when the user wants visuals — e.g. "generate the images," "make the b-roll," "one image per timestamp," "illustrate the script." It turns the **per-phrase** transcript into a folder of images, **one per timestamped line**, each a simple visual explanation of exactly what the narrator says at that moment — generated with Higgsfield GPT Image 2 (16:9) in one consistent illustration style.

The full procedure, the locked default art style, and the per-line prompt recipe live in **`references/images.md` — read it before generating.** The essentials:

- **One image per `[MM:SS]` line** in `<name>.phrases.txt`. Each prompt = a simple CONTENT visual of that line + the locked STYLE block + an `Avoid:` clause (GPT Image 2 has no negative-prompt field).
- **Model:** `gpt_image_2`, `aspect_ratio:"16:9"`, `resolution:"1k"`, `quality:"medium"`. Load `generate_image` + `show_generations` via ToolSearch first.
- **Concurrency cap is 8 jobs** — submit in batches of ≤8, poll `show_generations` for `results.rawUrl`, `curl` each into the folder, resubmit any that hit the rate limit.
- **Save to one folder**, filenames `NN_MM-SS.png` — the zero-padded sequence prefix makes them sort in **script order regardless of render-finish order**, and uniquely names lines that share a timestamp.
- **Write `manifest.md`** in the folder (file ↔ timestamp ↔ line ↔ visual) as the hand-off for editing/motion.

Each image must illustrate its line's story/emotion/idea — never a random image — and the whole set must share one style and palette.

---

## Stage 4 — Stitch the final video

Trigger this when the user wants the finished video — e.g. "stitch it together," "assemble the video," "render the final cut," "put it all together." It combines the Stage 3 images and the Stage 2 voiceover into one MP4 with FFmpeg: each image is held from the moment its phrase begins until the next phrase begins, with the voiceover muxed underneath.

Use the bundled script — it handles the timing math and the FFmpeg command:

```bash
python3 ~/.claude/skills/faceless-video/scripts/build_video.py \
  --images "<images-folder>" \
  --audio  "<voiceover-file>"
```

What it does and why it's built this way:
- **Timing comes from the millisecond-precision `<audio>.phrases.srt`**, not the second-rounded `.txt` — phrases that share a whole-second timestamp (common in fast lines) would otherwise collapse to zero duration. The script auto-finds the SRT beside the audio.
- **Images map to cues in order** (the `NN_` prefix guarantees script order): cue 1 → first image, and so on. The **first image covers the lead-in from 0:00**, and the **last image holds to the end of the audio** (including trailing silence/breath).
- Output defaults to `<images-folder>/<audio-stem>.mp4` — 1920×1080, 30fps, H.264 + AAC, faststart. Override with `--out`, `--size`, `--fps`, `--bg` (letterbox pad color, default cream), `--crf`.
- After rendering, **spot-check sync**: the script prints duration; optionally pull a frame or two (`ffmpeg -ss <t> -i out.mp4 -frames:v 1 frame.png`) to confirm the right image lands on the right line, then tell the user the output path.

Requires `ffmpeg`/`ffprobe` on PATH. If a phrase SRT is missing, re-run Stage 2 with `--phrase` first (the video timing depends on it).

---

## Reference

- `references/anatomy.md` — full annotated teardown of the model video (every beat with timestamps), the transition phrase bank, the fill-in template, and the complete style rules. Read it before writing.
- `scripts/transcribe.py` — Stage 2 transcriber. Local Whisper → `[MM:SS]` timestamped transcript + SRT/VTT, and per-phrase chunks with `--phrase`. Auto-finds the newest recording in a folder. No API key required.
- `references/images.md` — Stage 3 image generation: the locked art style, the per-line prompt recipe, model settings, the 8-job concurrency handling, and the file-naming/manifest rules. Read before generating images.
- `scripts/build_video.py` — Stage 4 assembler. FFmpeg-stitches the ordered images + voiceover into a finished MP4, each image held over its phrase's time range (timing from the phrase SRT). Auto-finds images, audio's SRT, and output path.
