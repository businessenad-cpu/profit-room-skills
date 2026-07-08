# Assembly — music, on-screen text, stitching

Phase 5. Turns the rendered shots in `shots/` into `ad-final.mp4`. ffmpeg 8.x is installed.

## 1. Audio / music

**There is no standalone music generator in this MCP** (`sonilo_music`/`mirelo`/`inworld` are
game-pipeline-only; `generate_audio` is TTS-only). Two real paths:

1. **Native audio (preferred):** render the video with `generate_audio:true` (Seedance) + an
   `Audio: …` line in the prompt — a single 15s timestamped render scores the whole clip in one
   pass. Pull it out separately if needed: `ffmpeg -i shot.mp4 -vn -c:a aac native.m4a`.
2. **A real track:** user-provided, or a clearly-licensed royalty-free instrumental → `music.m4a`,
   muxed below.

You can't hear audio in-harness — surface it for the user to judge. Keep `music-prompt.txt` as the
brief either way.

**Music prompt shape** — instrumental only, match the arc:
```
Instrumental cinematic synth score, pitch-black-mood, restrained and premium. 0–Xs: sparse low
pulse and rising pad (hook). mid: a clean arpeggio enters as the product reveals build. peak:
confident, warm swell on the payoff. last 2–3s: resolve to a single held note under the logo lock.
No vocals, no lyrics. Tempo calm. Reference: Anthropic / Linear / Vercel launch-film scoring.
```

**Fallbacks** (if `sonilo_music` is gated — its catalog note says "game pipeline only"):
1. A licensed local track the user provides (drop into the folder, point ffmpeg at it).
2. ElevenLabs music if available in the workspace.
3. Seedance's native `generate_audio: true` on ONE atmosphere shot to capture an ambient bed, then
   loop/extend it under the cut (last resort — thinner than a real score).

## 2. Normalize shots before concat (do this first)

Clips can differ in fps/size/codec; normalize so concat is clean. For each `shots/NN.mp4`:

```bash
ffmpeg -i shots/01.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,fps=24,format=yuv420p" -c:v libx264 -crf 18 -an norm/01.mp4
```
(Swap `1920:1080` for `1080:1920` on 9:16, `1440:1440` on 1:1. `-an` drops Seedance audio — we
score in post.)

## 3. On-screen text (burn per-beat copy)

Use `drawtext`. Provide a font file — install Inter, or fall back to a clean system font
(`/System/Library/Fonts/HelveticaNeue.ttc` or `/Library/Fonts/Arial.ttf` on macOS). One line per
beat, fade in/out, accent color on the key word:

```bash
ffmpeg -i norm/03.mp4 -vf "drawtext=fontfile=<INTER.ttf>:text='Reply rate, doubled':\
fontcolor=white:fontsize=54:x=(w-text_w)/2:y=h-180:\
alpha='if(lt(t,0.25),t/0.25,if(lt(t,2.5),1,(3-t)/0.5))'" -c:v libx264 -crf 18 -an txt/03.mp4
```
For an accent-colored keyword, layer a second `drawtext` with `fontcolor=<ACCENT_HEX>` positioned
for just that word. Keep text ≤6 words, generous margins, never over the busiest UI region.

> Prefer pre-rendered text cards (transparent PNGs) over drawtext when the typography needs to be
> precise — make them with `gpt_image_2` or a quick HTML→screenshot, then `overlay` them.

## 4. Concat (hard cuts) + optional dissolves

> Skip this whole step if the ad is a **single 15s timestamped render** — its cuts already live
> inside the clip. Go straight to §5 (mux music). Concat is only for multi-segment 30/60s ads.

**Hard cuts** — concat demuxer (fast, lossless-ish). Build `list.txt`:
```
file 'txt/01.mp4'
file 'txt/02.mp4'
file 'txt/03.mp4'
```
```bash
ffmpeg -f concat -safe 0 -i list.txt -c:v libx264 -crf 18 -pix_fmt yuv420p video-silent.mp4
```

**A soft dissolve between two beats** (use sparingly, ~8 frames) — `xfade`:
```bash
ffmpeg -i txt/02.mp4 -i txt/03.mp4 -filter_complex \
"[0][1]xfade=transition=fade:duration=0.33:offset=<clip2_start-0.33>" -c:v libx264 -crf 18 dissolve.mp4
```

## 5. Mux music (from ad-studio, proven)

Music only:
```bash
ffmpeg -i video-silent.mp4 -i music.m4a -map 0:v:0 -map 1:a:0 \
  -c:v copy -c:a aac -b:a 192k -shortest ad-final.mp4
```

Music + a low ambience bed (only if a shot had usable diegetic audio):
```bash
ffmpeg -i video-silent.mp4 -i music.m4a -filter_complex \
"[0:a]volume=0.12[amb];[1:a]volume=1.0[mus];[amb][mus]amix=inputs=2:duration=shortest:dropout_transition=0:normalize=0[a]" \
  -map 0:v:0 -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest ad-final.mp4
```

## 6. Optional voiceover (only if chosen at intake)

Generate the line, then duck music under it:
```
generate_audio(params:{ model:"text2speech_v2_elevenlabs", voice_type:"preset", voice_id:"<id>",
  prompt:"<the VO line>" })   # → vo.m4a
```
```bash
ffmpeg -i video-silent.mp4 -i music.m4a -i vo.m4a -filter_complex \
"[1:a]volume=0.35[mus];[2:a]volume=1.0[vo];[mus][vo]amix=inputs=2:duration=longest:normalize=0[a]" \
  -map 0:v:0 -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest ad-final.mp4
```

## 7. Verify the master

```bash
ffprobe -v error -show_entries stream=codec_type,width,height,duration -of default=nk=1:nw=1 ad-final.mp4
```
Confirm exactly 1 video + 1 audio stream, the right dimensions, and the duration matches the brief.
Optional 4K master: `upscale_video(<ad-final job/url>)`.

## Scope: website + Higgsfield + ffmpeg only

No Remotion, no external editors. Every pixel comes from the audited **website** (screenshots) and
**Higgsfield** (hero frames, video, music); **ffmpeg** only concatenates segments, burns on-screen
text, and muxes audio. Keep the whole pipeline inside those three tools. If the typography needs to
be more precise than `drawtext`, pre-render text cards as transparent PNGs with `gpt_image_2` and
`overlay` them — still all Higgsfield + ffmpeg.
