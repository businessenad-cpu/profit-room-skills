#!/usr/bin/env python3
"""
Transcribe a recorded voiceover with local Whisper and emit a timestamped transcript.

Stage 2 of the faceless-video skill: after the user records their VO, point this at
the recording (or the folder containing it) and it produces:
  - <stem>.timestamped.txt   ->  "[MM:SS] line of narration"  (segment level, default)
  - <stem>.srt  and  <stem>.vtt                                (for editors / captions)

With --phrase it ALSO breaks the transcript into short per-phrase chunks (split on the
natural comma/period beats, using word-level timing) and writes:
  - <stem>.phrases.txt       ->  "[MM:SS] short phrase"
  - <stem>.phrases.srt / .vtt -> phrase-level captions (great for burned-in subtitles)

Uses OpenAI Whisper running locally — no API key required.

Usage:
  python3 transcribe.py <audio-file>            # transcribe a specific file
  python3 transcribe.py <folder>                # auto-pick the NEWEST audio file in folder
  python3 transcribe.py <path> --phrase         # per-phrase chunks (comma/period beats)
  python3 transcribe.py <path> --phrase --max-words 5 --gap 0.5   # tune phrase size
  python3 transcribe.py <path> --model small    # override model (default: turbo)
  python3 transcribe.py <path> --words          # raw word-level timestamps -> .words.tsv

Cached models on this machine: turbo (large-v3-turbo, best), small, base (fastest).
"""
import argparse
import os
import sys
from pathlib import Path

AUDIO_EXTS = {
    ".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".opus",
    ".mp4", ".mov", ".m4v", ".webm", ".mkv", ".caf", ".aiff",
}
SKIP_SUFFIXES = (".timestamped.txt", ".phrases.txt", ".srt", ".vtt", ".words.tsv")

# A phrase ends after a word whose trailing punctuation closes a clause.
PHRASE_END_PUNCT = set(",.!?;:—–…")


def fmt_ts(seconds: float) -> str:
    seconds = max(0, int(round(seconds)))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def fmt_srt(seconds: float) -> str:
    if seconds < 0:
        seconds = 0
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def fmt_vtt(seconds: float) -> str:
    return fmt_srt(seconds).replace(",", ".")


def find_newest_audio(folder: Path) -> Path | None:
    candidates = [
        p for p in folder.iterdir()
        if p.is_file()
        and p.suffix.lower() in AUDIO_EXTS
        and not p.name.endswith(SKIP_SUFFIXES)
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def resolve_audio(arg: str | None) -> Path:
    target = Path(arg).expanduser() if arg else Path.cwd()
    if target.is_file():
        return target
    if target.is_dir():
        newest = find_newest_audio(target)
        if newest is None:
            sys.exit(
                f"No audio/video file found in {target}.\n"
                f"Looked for: {', '.join(sorted(AUDIO_EXTS))}.\n"
                "Record the voiceover into that folder, or pass the file path directly."
            )
        return newest
    sys.exit(f"Path not found: {target}")


def group_into_phrases(segments, max_words: int, gap: float):
    """Regroup word-level timing into short phrases.

    A phrase closes when any of these is true:
      - the current word ends with clause punctuation (, . ! ? ; : — …)
      - the next word starts after a pause >= `gap` seconds (a breath/beat)
      - the phrase has reached `max_words` words
    Falls back to the whole segment if a segment carries no word timings.
    """
    phrases = []
    buf = []  # list of (text, start, end)

    def flush():
        if not buf:
            return
        text = "".join(w[0] for w in buf).strip()
        if text:
            phrases.append({"start": buf[0][1], "end": buf[-1][2], "text": text})
        buf.clear()

    for seg in segments:
        words = seg.get("words") or []
        if not words:  # no per-word data — keep the segment whole
            flush()
            t = seg["text"].strip()
            if t:
                phrases.append({"start": seg["start"], "end": seg["end"], "text": t})
            continue
        for i, w in enumerate(words):
            buf.append((w["word"], w["start"], w["end"]))
            token = w["word"].strip()
            ends_clause = token and token[-1] in PHRASE_END_PUNCT
            next_gap = (words[i + 1]["start"] - w["end"]) if i + 1 < len(words) else 0
            if ends_clause or len(buf) >= max_words or next_gap >= gap:
                flush()
        flush()  # close at segment boundary
    return phrases


def write_caption_files(chunks, out_dir: Path, stem: str, suffix: str):
    """chunks: list of {start, end, text}. Writes <stem><suffix>.srt and .vtt."""
    srt_lines = []
    for i, c in enumerate(chunks, 1):
        srt_lines.append(str(i))
        srt_lines.append(f"{fmt_srt(c['start'])} --> {fmt_srt(c['end'])}")
        srt_lines.append(c["text"])
        srt_lines.append("")
    (out_dir / f"{stem}{suffix}.srt").write_text("\n".join(srt_lines) + "\n", encoding="utf-8")

    vtt_lines = ["WEBVTT", ""]
    for c in chunks:
        vtt_lines.append(f"{fmt_vtt(c['start'])} --> {fmt_vtt(c['end'])}")
        vtt_lines.append(c["text"])
        vtt_lines.append("")
    (out_dir / f"{stem}{suffix}.vtt").write_text("\n".join(vtt_lines) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Transcribe a voiceover with local Whisper + timestamps.")
    ap.add_argument("path", nargs="?", default=None,
                    help="Audio file, or a folder to auto-pick the newest recording from. Default: cwd.")
    ap.add_argument("--model", default="turbo",
                    help="Whisper model: turbo (default, best), small (faster), base (fastest).")
    ap.add_argument("--language", default="en", help="Spoken language (default: en).")
    ap.add_argument("--phrase", action="store_true",
                    help="Also break the transcript into short per-phrase chunks (comma/period beats).")
    ap.add_argument("--max-words", type=int, default=12,
                    help="Phrase mode: max words per chunk before forcing a split (default: 12; "
                         "phrases split mainly on commas/periods/pauses, this only catches long run-ons; "
                         "use a smaller value like 5-6 for tighter caption chunks).")
    ap.add_argument("--gap", type=float, default=0.65,
                    help="Phrase mode: pause (seconds) between words that forces a split (default: 0.65).")
    ap.add_argument("--words", action="store_true", help="Also emit raw word-level timestamps to .words.tsv.")
    args = ap.parse_args()

    try:
        import whisper
        from whisper.utils import get_writer
    except ImportError:
        sys.exit("openai-whisper is not importable from this python. Install with: pip install -U openai-whisper")

    audio = resolve_audio(args.path)
    out_dir = audio.parent
    stem = audio.stem
    need_words = args.phrase or args.words

    print(f"Audio:  {audio}", file=sys.stderr)
    print(f"Model:  {args.model}  (loading…)", file=sys.stderr)
    model = whisper.load_model(args.model)

    print("Transcribing… (this scales with clip length)", file=sys.stderr)
    result = model.transcribe(
        str(audio),
        language=args.language,
        word_timestamps=need_words,
        verbose=False,
        fp16=False,  # CPU-safe; avoids the fp16 warning on Macs
    )
    segments = result.get("segments", [])

    # --- Segment-level outputs (always) ---
    ts_path = out_dir / f"{stem}.timestamped.txt"
    seg_lines = [f"[{fmt_ts(seg['start'])}] {seg['text'].strip()}" for seg in segments]
    ts_path.write_text("\n".join(seg_lines) + "\n", encoding="utf-8")
    for fmt in ("srt", "vtt"):
        get_writer(fmt, str(out_dir))(result, str(audio),
                                      {"max_line_width": None, "max_line_count": None, "highlight_words": False})

    saved = [ts_path, out_dir / f"{stem}.srt", out_dir / f"{stem}.vtt"]

    # --- Phrase-level outputs (--phrase) ---
    phrase_lines = None
    if args.phrase:
        phrases = group_into_phrases(segments, max_words=args.max_words, gap=args.gap)
        phrase_lines = [f"[{fmt_ts(p['start'])}] {p['text']}" for p in phrases]
        ph_path = out_dir / f"{stem}.phrases.txt"
        ph_path.write_text("\n".join(phrase_lines) + "\n", encoding="utf-8")
        write_caption_files(phrases, out_dir, stem, ".phrases")
        saved += [ph_path, out_dir / f"{stem}.phrases.srt", out_dir / f"{stem}.phrases.vtt"]

    # --- Raw word-level (--words) ---
    if args.words:
        word_path = out_dir / f"{stem}.words.tsv"
        wl = ["start_s\tend_s\tword"]
        for seg in segments:
            for w in seg.get("words", []) or []:
                wl.append(f"{w['start']:.2f}\t{w['end']:.2f}\t{w['word'].strip()}")
        word_path.write_text("\n".join(wl) + "\n", encoding="utf-8")
        saved.append(word_path)

    # Echo the relevant transcript to stdout (phrase view if requested, else segment view)
    print("\n".join(phrase_lines if phrase_lines is not None else seg_lines))

    total_words = sum(len(seg["text"].split()) for seg in segments)
    duration = segments[-1]["end"] if segments else 0
    chunk_note = f"  ·  {len(phrase_lines)} phrases" if phrase_lines is not None else ""
    print(f"\n---\nLength: {fmt_ts(duration)}  ·  {total_words} words{chunk_note}  ·  model={args.model}", file=sys.stderr)
    print("Saved:\n  " + "\n  ".join(str(p) for p in saved), file=sys.stderr)


if __name__ == "__main__":
    main()
