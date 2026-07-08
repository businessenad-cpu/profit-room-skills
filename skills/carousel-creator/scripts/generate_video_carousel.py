"""
Generate a branded Instagram video carousel from a JSON spec.

Takes existing video clips, applies branded text overlays using FFmpeg,
and saves processed MP4s locally, ready to hand off to your scheduler.

Usage:
    python3 generate_video_carousel.py <path/to/video_carousel_spec.json>

Requirements:
    - ffmpeg (brew install ffmpeg)
    - pip install Pillow

Optional env:
    CAROUSEL_ROOT   root for output/ (default: skill root)
    BROLL_DIR       folder to resolve bare clip filenames from (default ./b-roll/videos)
"""

import sys
import os
import io
import json
import re
import tempfile
import subprocess
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)

# --- Path setup ---
if os.environ.get("CAROUSEL_ROOT"):
    CAROUSEL_ROOT = Path(os.environ["CAROUSEL_ROOT"])
else:
    CAROUSEL_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_DIR = CAROUSEL_ROOT / "output" / "video_slides"

# --- B-roll library (default source for bare clip_path filenames) ---
BROLL_DIR = Path(os.path.expanduser(os.environ.get("BROLL_DIR", "./b-roll/videos")))

# --- Brand Constants (same as generate_carousel.py) ---
TEXT_COLOR = (245, 240, 232)    # #F5F0E8 warm white
ACCENT_COLOR = (0, 255, 0)      # #00FF00 neon green

# --- Font loading ---
_FONT_PATHS_BOLD = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
]
_FONT_PATHS_REGULAR = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
]


def _load_font(bold=True, size=48):
    paths = _FONT_PATHS_BOLD if bold else _FONT_PATHS_REGULAR
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def _wrap_text(text, font, max_width, draw):
    """Word-wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines


def _parse_green_segments(text):
    """Parse text with {green}...{/green} markers."""
    pattern = r'\{green\}(.*?)\{/green\}'
    segments = []
    last_end = 0
    for match in re.finditer(pattern, text):
        if match.start() > last_end:
            segments.append((text[last_end:match.start()], False))
        segments.append((match.group(1), True))
        last_end = match.end()
    if last_end < len(text):
        segments.append((text[last_end:], False))
    return segments if segments else [(text, False)]


def _get_emoji_font(size):
    """Load Apple Color Emoji font for emoji rendering."""
    try:
        return ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", size)
    except (OSError, IOError):
        return None


def _has_emoji(text):
    """Check if text contains emoji characters."""
    import unicodedata
    for ch in text:
        if unicodedata.category(ch).startswith(('So', 'Sk')) or ord(ch) > 0x1F000:
            return True
    return False


def _split_emoji(text):
    """Split text into segments of (text, is_emoji)."""
    import unicodedata
    segments = []
    current = ""
    current_is_emoji = False
    for ch in text:
        is_emoji = unicodedata.category(ch).startswith(('So', 'Sk')) or ord(ch) > 0x1F000
        if is_emoji != current_is_emoji and current:
            segments.append((current, current_is_emoji))
            current = ""
        current += ch
        current_is_emoji = is_emoji
    if current:
        segments.append((current, current_is_emoji))
    return segments


def _draw_segment(draw, x, y, text, font, color, size):
    """Draw text with emoji fallback support."""
    if not _has_emoji(text):
        draw.text((x, y), text, font=font, fill=color)
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0]
    emoji_font = _get_emoji_font(size)
    segments = _split_emoji(text)
    cx = x
    for seg_text, is_emoji in segments:
        seg_text = seg_text.strip() if is_emoji else seg_text
        if is_emoji and emoji_font:
            draw.text((cx, y), seg_text, font=emoji_font, fill=color, embedded_color=True)
            bbox = draw.textbbox((0, 0), seg_text, font=emoji_font)
        else:
            draw.text((cx, y), seg_text, font=font, fill=color)
            bbox = draw.textbbox((0, 0), seg_text, font=font)
        cx += bbox[2] - bbox[0] + (4 if is_emoji else 0)
    return cx - x


def _draw_text_with_green(draw, x, y, text, font, default_color=TEXT_COLOR, size=None):
    """Draw text with {green}...{/green} segments highlighted in neon green, with emoji support."""
    if size is None:
        size = font.size if hasattr(font, 'size') else 48
    segments = _parse_green_segments(text)
    cursor_x = x
    for segment_text, is_green in segments:
        color = ACCENT_COLOR if is_green else default_color
        cursor_x += _draw_segment(draw, cursor_x, y, segment_text, font, color, size)


def _get_video_dimensions(clip_path):
    """Get video width and height by parsing ffmpeg -i stderr output."""
    result = subprocess.run(
        ['ffmpeg', '-i', str(clip_path)],
        capture_output=True, text=True
        # ffmpeg exits non-zero when given no output — that's expected here
    )
    # Dimensions appear in lines like: "Stream ... Video: h264, yuv420p, 1080x1920 ..."
    for line in result.stderr.split('\n'):
        if 'Video:' in line:
            match = re.search(r'(\d{2,5})x(\d{2,5})', line)
            if match:
                return int(match.group(1)), int(match.group(2))
    raise ValueError(f"Could not parse video dimensions from: {clip_path}")


def _create_text_overlay(slide, width, height):
    """
    Create a transparent RGBA overlay image with gradient darkening + branded text.

    Same visual style as _render_slide in generate_carousel.py, but on a
    transparent background so FFmpeg can composite it onto the video.
    """
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    margin_left = int(width * 0.15)
    margin_right = int(width * 0.15)
    max_text_width = width - margin_left - margin_right

    headline = slide.get("headline", "")
    body = slide.get("body", "")
    green_accent = slide.get("green_accent", "")
    step_label = slide.get("step_label", "")  # e.g. "STEP 2" — renders in green above headline

    headline_size = min(88, max(52, int(width * 0.07)))
    headline_font = _load_font(bold=True, size=headline_size)
    body_size = min(56, max(40, int(width * 0.055)))
    body_font = _load_font(bold=False, size=body_size)
    step_size = int(headline_size * 0.65)
    step_font = _load_font(bold=True, size=step_size)

    def _shadow(x, y, text, font):
        """Multi-layer drop shadow for text readability on bright footage."""
        for dx, dy, alpha in [(4, 4, 80), (3, 3, 110), (2, 2, 140), (1, 1, 160)]:
            _draw_segment(draw, x + dx, y + dy, text, font, (0, 0, 0, alpha), 12)

    # --- Render step_label (green, above headline) ---
    y_cursor = int(height * 0.30)
    if step_label:
        clean_step = step_label.upper()
        _shadow(margin_left, y_cursor, clean_step, step_font)
        _draw_segment(draw, margin_left, y_cursor, clean_step, step_font, ACCENT_COLOR, step_size)
        y_cursor += int(step_size * 1.4)

    # --- Render headline ---
    if headline:
        clean_headline = re.sub(r'\{/?green\}', '', headline).upper()
        # Detect numbered skill prefix like "01. BRAND VOICE" — render number bigger + green
        number_match = re.match(r'^(\d+\.)\s*(.*)', clean_headline)
        if number_match:
            number_part = number_match.group(1)   # e.g. "01."
            skill_name  = number_match.group(2)   # e.g. "BRAND VOICE"
            number_size = int(headline_size * 1.5)
            number_font = _load_font(bold=True, size=number_size)
            _shadow(margin_left, y_cursor, number_part, number_font)
            _draw_segment(draw, margin_left, y_cursor, number_part, number_font, ACCENT_COLOR, number_size)
            y_cursor += int(number_size * 1.05)
            wrapped = _wrap_text(skill_name, headline_font, max_text_width, draw)
            for line in wrapped:
                _shadow(margin_left, y_cursor, line, headline_font)
                _draw_segment(draw, margin_left, y_cursor, line, headline_font, TEXT_COLOR, headline_size)
                y_cursor += int(headline_size * 1.2)
        else:
            # Multi-line headline support — split on \n first, then word-wrap each part
            raw_h_lines = clean_headline.split("\n")
            for raw_line in raw_h_lines:
                if not raw_line.strip():
                    y_cursor += int(headline_size * 0.5)
                    continue
                wrapped = _wrap_text(raw_line, headline_font, max_text_width, draw)
                for line in wrapped:
                    _shadow(margin_left, y_cursor, line, headline_font)
                    if green_accent and green_accent.upper() in line:
                        line_with_green = line.replace(
                            green_accent.upper(),
                            f"{{green}}{green_accent.upper()}{{/green}}"
                        )
                        _draw_text_with_green(draw, margin_left, y_cursor, line_with_green, headline_font, size=headline_size)
                    else:
                        _draw_segment(draw, margin_left, y_cursor, line, headline_font, TEXT_COLOR, headline_size)
                    y_cursor += int(headline_size * 1.2)

    # --- Render body ---
    y_cursor += int(body_size * 0.8)
    if body:
        for body_line in body.split("\n"):
            if not body_line.strip():
                y_cursor += int(body_size * 0.6)
                continue
            clean_line = re.sub(r'\{/?green\}|\*', '', body_line)
            wrapped = _wrap_text(clean_line, body_font, max_text_width, draw)
            for wline in wrapped:
                _shadow(margin_left, y_cursor, wline, body_font)
                if green_accent and green_accent.lower() in wline.lower():
                    idx = wline.lower().find(green_accent.lower())
                    original_text = wline[idx:idx + len(green_accent)]
                    line_with_green = (
                        wline[:idx] +
                        f"{{green}}{original_text}{{/green}}" +
                        wline[idx + len(green_accent):]
                    )
                    _draw_text_with_green(draw, margin_left, y_cursor, line_with_green, body_font, size=body_size)
                else:
                    _draw_segment(draw, margin_left, y_cursor, wline, body_font, TEXT_COLOR, body_size)
                y_cursor += int(body_size * 1.4)

    return overlay


def _burn_overlay(clip_path, overlay_img, output_path, brightness=0.75):
    """
    Composite a transparent PNG overlay onto a video clip using FFmpeg.

    Args:
        brightness: multiply video RGB by this value before overlaying text (0.5 = 50% brightness)
    """
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        overlay_img.save(tmp.name, 'PNG')
        overlay_path = tmp.name

    # Vignette darkens edges, keeps centre bright. Then composite text overlay.
    if brightness < 1.0:
        dim = f'lutrgb=r=val*{brightness}:g=val*{brightness}:b=val*{brightness}'
        filter_complex = f'[0:v]{dim}[dim];[dim]vignette=angle=PI/4[vig];[vig][1:v]overlay=0:0'
    else:
        filter_complex = '[0:v]vignette=angle=PI/4[vig];[vig][1:v]overlay=0:0'

    try:
        result = subprocess.run([
            'ffmpeg', '-y',
            '-i', str(clip_path),
            '-i', overlay_path,
            '-filter_complex', filter_complex,
            '-an',           # strip audio — carousels play silent
            '-preset', 'fast',
            '-movflags', '+faststart',
            str(output_path)
        ], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg failed:\n{result.stderr[-500:]}")
    finally:
        os.unlink(overlay_path)


def _resolve_clip_path(clip_path_str):
    """
    Resolve a clip path. If it's just a filename (no directory), look in BROLL_DIR.
    Absolute paths are used as-is.
    """
    p = Path(clip_path_str)
    if p.is_absolute():
        return p
    # Bare filename — resolve from B-roll library
    candidate = BROLL_DIR / p.name
    if candidate.exists():
        return candidate
    raise FileNotFoundError(f"Clip '{clip_path_str}' not found (checked {candidate})")


def _process_slide(slide, total):
    """Apply branded text overlay to a video clip and save the result."""
    num = slide['number']
    clip_path = _resolve_clip_path(slide['clip_path'])
    label = f"slide_{num:02d}"

    if not clip_path.exists():
        raise FileNotFoundError(f"Clip not found: {clip_path}")

    print(f"  [{num}/{total}] Getting dimensions: {clip_path.name}")
    width, height = _get_video_dimensions(clip_path)

    print(f"  [{num}/{total}] Creating text overlay ({width}x{height})...")
    overlay = _create_text_overlay(slide, width, height)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{label}.mp4"

    print(f"  [{num}/{total}] Burning overlay with FFmpeg...")
    _burn_overlay(clip_path, overlay, output_path)

    size_mb = output_path.stat().st_size / 1_000_000
    print(f"  [done] Slide {num} -> {output_path.name} ({size_mb:.1f} MB)")

    return {
        "number": num,
        "label": label,
        "clip_path": str(clip_path),
        "local_path": str(output_path),
        "size_mb": round(size_mb, 1),
        "status": "success",
    }


def generate_video_carousel(spec_path):
    """Main entry point — process all video slides from a carousel spec JSON."""
    with open(spec_path) as f:
        spec = json.load(f)

    title = spec.get("title", "Untitled Video Carousel")
    slides = spec.get("slides", [])
    total = len(slides)

    print(f"\n{'=' * 60}")
    print(f"  Video Carousel: {title}")
    print(f"  Slides: {total}")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"{'=' * 60}\n")

    results = []
    for slide in slides:
        try:
            result = _process_slide(slide, total)
            results.append(result)
        except Exception as e:
            num = slide.get("number", "?")
            print(f"  [FAIL] Slide {num}: {e}")
            results.append({
                "number": num,
                "label": f"slide_{num:02d}" if isinstance(num, int) else "slide_??",
                "status": f"error: {e}",
            })

    succeeded = sum(1 for r in results if r["status"] == "success")
    total_mb = sum(r.get("size_mb", 0) for r in results)

    print(f"\n{'=' * 60}")
    print(f"  VIDEO CAROUSEL COMPLETE: {succeeded}/{total} slides")
    print(f"  Total size: {total_mb:.1f} MB")
    print(f"{'=' * 60}")
    for r in results:
        status = "OK" if r["status"] == "success" else "FAIL"
        size = f" ({r['size_mb']} MB)" if r.get("size_mb") else ""
        print(f"  [{status}] Slide {r['number']}: {r.get('label', '?')}{size}")
        if r.get("local_path"):
            print(f"         {r['local_path']}")
    print(f"{'=' * 60}\n")

    # Save manifest with local paths (upload/publish is a separate hand-off step)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = OUTPUT_DIR / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump({"title": title, "slides": results}, f, indent=2)
    print(f"  Manifest saved: {manifest_path}")

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate_video_carousel.py <video_carousel_spec.json>")
        sys.exit(1)
    generate_video_carousel(sys.argv[1])
