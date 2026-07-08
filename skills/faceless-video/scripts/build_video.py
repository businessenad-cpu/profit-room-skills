#!/usr/bin/env python3
"""
Stage 4 of the faceless-video skill: stitch the per-timestamp images + the voiceover
into one MP4 with FFmpeg.

Each image is held on screen from the moment its phrase begins until the next phrase
begins (the first image covers the lead-in from 0:00; the last image holds to the end
of the audio, including any trailing silence). The voiceover is muxed in underneath.

Timing comes from the millisecond-precision phrase SRT (`<audio>.phrases.srt`), NOT the
second-rounded .txt — several phrases can share a whole-second timestamp and would
otherwise collapse to zero duration. Images are matched to cues IN ORDER (the NN_ prefix
guarantees script order), so cue 1 -> first image, cue 2 -> second image, and so on.

Usage:
  python3 build_video.py --images <folder> --audio <file.m4a>
  python3 build_video.py --images <folder> --audio <file> --srt <phrases.srt> --out <out.mp4>
  python3 build_video.py --images <folder> --audio <file> --size 1920x1080 --fps 30 --bg 0xF2EAD6

Requires ffmpeg + ffprobe on PATH.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

IMG_RE = re.compile(r"\.(png|jpg|jpeg|webp)$", re.I)
SRT_TIME = re.compile(r"(\d\d):(\d\d):(\d\d)[,\.](\d{1,3})\s*-->")


def die(msg: str) -> None:
    sys.exit(f"build_video: {msg}")


def list_images(folder: Path):
    imgs = sorted(p for p in folder.iterdir() if p.is_file() and IMG_RE.search(p.name))
    if not imgs:
        die(f"no images (png/jpg/webp) found in {folder}")
    return imgs


def srt_starts(srt_path: Path):
    """Return the start time (seconds) of every cue, in order."""
    starts = []
    for line in srt_path.read_text(encoding="utf-8").splitlines():
        m = SRT_TIME.search(line)
        if m:
            h, mi, s, ms = m.groups()
            ms = ms.ljust(3, "0")  # 1.66 -> 1.660
            starts.append(int(h) * 3600 + int(mi) * 60 + int(s) + int(ms) / 1000.0)
    if not starts:
        die(f"no timecodes parsed from {srt_path}")
    return starts


def audio_duration(audio: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(audio)],
        capture_output=True, text=True,
    )
    try:
        return float(out.stdout.strip())
    except ValueError:
        die(f"could not read audio duration from {audio} ({out.stderr.strip()})")


def resolve_srt(audio: Path, explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit).expanduser()
        if not p.is_file():
            die(f"--srt not found: {p}")
        return p
    for cand in (audio.with_suffix("").name + ".phrases.srt",
                 audio.with_suffix("").name + ".srt"):
        p = audio.parent / cand
        if p.is_file():
            return p
    die(f"no phrases SRT found next to {audio}. Run Stage 2 with --phrase, or pass --srt.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Stitch per-timestamp images + voiceover into an MP4.")
    ap.add_argument("--images", required=True, help="Folder of NN_*.png images (sorted in script order).")
    ap.add_argument("--audio", required=True, help="Voiceover audio file.")
    ap.add_argument("--srt", default=None, help="Phrase SRT for timing (default: <audio>.phrases.srt beside the audio).")
    ap.add_argument("--out", default=None, help="Output MP4 (default: <images>/<audio-stem>.mp4).")
    ap.add_argument("--size", default="1920x1080", help="Output WxH (default 1920x1080).")
    ap.add_argument("--fps", type=int, default=30, help="Output frame rate (default 30).")
    ap.add_argument("--bg", default="0xF2EAD6", help="Pad color for any letterbox bars (default cream).")
    ap.add_argument("--crf", type=int, default=18, help="x264 CRF quality (default 18; lower = higher quality).")
    args = ap.parse_args()

    images_dir = Path(args.images).expanduser()
    audio = Path(args.audio).expanduser()
    if not images_dir.is_dir():
        die(f"images folder not found: {images_dir}")
    if not audio.is_file():
        die(f"audio not found: {audio}")
    try:
        W, H = (int(x) for x in args.size.lower().split("x"))
    except ValueError:
        die(f"bad --size {args.size!r}; expected like 1920x1080")

    images = list_images(images_dir)
    srt = resolve_srt(audio, args.srt)
    starts = srt_starts(srt)
    dur = audio_duration(audio)
    out = Path(args.out).expanduser() if args.out else images_dir / (audio.with_suffix("").name + ".mp4")

    n = min(len(images), len(starts))
    if len(images) != len(starts):
        print(f"build_video: WARNING — {len(images)} images vs {len(starts)} cues; "
              f"using the first {n} of each (check Stage 2/3 stayed in sync).", file=sys.stderr)
    images, starts = images[:n], starts[:n]

    # appear[0] = 0 (cover the lead-in); appear[i>=1] = phrase start; last holds to audio end.
    appear = [0.0] + starts[1:]
    durations = []
    for i in range(n):
        end = appear[i + 1] if i + 1 < n else dur
        d = round(end - appear[i], 3)
        if d <= 0:
            print(f"build_video: WARNING — non-positive duration for image {i+1}; clamping to 0.05s.", file=sys.stderr)
            d = 0.05
        durations.append(d)

    # Build the concat-demuxer list. The last image is repeated once because the demuxer
    # ignores the final `duration` directive unless another file entry follows it.
    lines = []
    for img, d in zip(images, durations):
        lines.append(f"file '{img.resolve()}'")
        lines.append(f"duration {d}")
    lines.append(f"file '{images[-1].resolve()}'")

    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write("\n".join(lines) + "\n")
        concat_path = f.name

    vf = (f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
          f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color={args.bg},"
          f"fps={args.fps},format=yuv420p")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_path,
        "-i", str(audio),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "medium", "-crf", str(args.crf),
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart",
        str(out),
    ]

    print(f"Images: {n}  ·  Audio: {dur:.2f}s  ·  Timing: {srt.name}", file=sys.stderr)
    print(f"Rendering -> {out}", file=sys.stderr)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    os.unlink(concat_path)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr[-3000:])
        die("ffmpeg failed (see output above).")

    print(f"Done: {out}")
    print(f"  {n} images · {dur:.2f}s · {W}x{H} @ {args.fps}fps", file=sys.stderr)


if __name__ == "__main__":
    main()
