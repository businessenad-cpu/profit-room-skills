"""
Generate a branded Instagram carousel from a JSON spec.

Reads a carousel_spec.json, generates images via the image backend
(Higgsfield / nano_banana_2), applies branded text overlays, and saves the
final slides locally.

Usage:
    python3 generate_carousel.py <path/to/carousel_spec.json>

Optional env:
    CAROUSEL_ROOT   root for output/ and the image library (default: skill root)
    BRAND_FACE / BRAND_PORTRAIT   path to a portrait image used as the reference
                                  for `character` shots (e.g. the CTA slide).
                                  If unset, character shots generate with no ref.
"""

import sys
import os
import io
import json
import time
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Same-dir import of the shippable image backend.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from image_backend import generate_image, upload_reference

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    print("ERROR: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)

# --- Brand Constants ---
BACKGROUND_COLOR = (10, 10, 10)       # #0A0A0A
TEXT_COLOR = (245, 240, 232)           # #F5F0E8 warm white
ACCENT_COLOR = (0, 255, 0)            # #00FF00 neon green
OVERLAY_BG = (0, 0, 0, 178)           # black at 70% opacity
SHADOW_COLOR = (0, 0, 0, 200)

# --- Reference image for character shots (optional, user-supplied) ---
def _brand_face():
    """Return a portrait reference path from env if it exists, else None."""
    for var in ("BRAND_FACE", "BRAND_PORTRAIT"):
        val = os.environ.get(var)
        if val and Path(os.path.expanduser(val)).exists():
            return os.path.expanduser(val)
    return None


# --- Directories ---
if os.environ.get("CAROUSEL_ROOT"):
    CAROUSEL_ROOT = Path(os.environ["CAROUSEL_ROOT"])
else:
    CAROUSEL_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = CAROUSEL_ROOT / "output" / "slides"
LIBRARY_DIR = CAROUSEL_ROOT / "Reference"
LIBRARY_INDEX = LIBRARY_DIR / "library.json"

# --- Font loading ---
_FONT_PATHS_BOLD = [
    os.path.expanduser("~/Library/Fonts/Gotham-Ultra.otf"),
    os.path.expanduser("~/Library/Fonts/Gotham-Black.otf"),
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
]
_FONT_PATHS_REGULAR = [
    os.path.expanduser("~/Library/Fonts/Gotham-Bold.otf"),
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
]


def _load_library_index():
    """Load the library index, or return empty dict if it doesn't exist."""
    if LIBRARY_INDEX.exists():
        with open(LIBRARY_INDEX) as f:
            return json.load(f)
    return {"images": []}


def _save_library_index(index):
    """Save library index."""
    LIBRARY_INDEX.parent.mkdir(parents=True, exist_ok=True)
    with open(LIBRARY_INDEX, "w") as f:
        json.dump(index, f, indent=2)


def _save_to_library(raw_bytes, shot_type, tags=None, prompt=""):
    """
    Save a raw (no overlay) image to the library for future reuse.

    Args:
        raw_bytes: raw image bytes
        shot_type: "character", "establishing", or "detail"
        tags: optional list of descriptive tags
        prompt: the prompt used to generate the image

    Returns:
        str: relative path within Reference/ (e.g., "establishing/arch_001.jpg")
    """
    subdir = LIBRARY_DIR / shot_type
    subdir.mkdir(parents=True, exist_ok=True)

    # Find next available filename
    existing = list(subdir.glob("*.jpg"))
    idx = len(existing) + 1
    filename = f"{shot_type}_{idx:03d}.jpg"
    filepath = subdir / filename

    # Save raw image
    img = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
    img.save(str(filepath), quality=95)

    # Update library index
    index = _load_library_index()
    entry = {
        "path": f"{shot_type}/{filename}",
        "shot_type": shot_type,
        "tags": tags or [],
        "prompt": prompt[:200],
    }
    index["images"].append(entry)
    _save_library_index(index)

    rel_path = f"{shot_type}/{filename}"
    print(f"  [library] Saved raw image: {rel_path}")
    return rel_path


def _load_library_image(rel_path):
    """Load a raw image from the library. Returns bytes or None."""
    full_path = LIBRARY_DIR / rel_path
    if full_path.exists():
        with open(full_path, "rb") as f:
            return f.read()
    print(f"  [library] WARNING: {rel_path} not found")
    return None


def _load_font(bold=True, size=48):
    paths = _FONT_PATHS_BOLD if bold else _FONT_PATHS_REGULAR
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def _wrap_text(text, font, max_width, draw):
    """Word-wrap text to fit within max_width pixels. Respects explicit \\n breaks."""
    lines = []
    for segment in text.split("\n"):
        words = segment.split()
        if not words:
            lines.append("")
            continue
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
    """
    Parse text with {green}...{/green} markers.
    Returns list of (text, is_green) tuples.
    """
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


def _draw_text_with_green(draw, x, y, text, font, default_color=TEXT_COLOR):
    """Draw text with {green}...{/green} segments highlighted."""
    segments = _parse_green_segments(text)
    cursor_x = x
    for segment_text, is_green in segments:
        color = ACCENT_COLOR if is_green else default_color
        draw.text((cursor_x, y), segment_text, font=font, fill=color)
        bbox = draw.textbbox((0, 0), segment_text, font=font)
        cursor_x += bbox[2] - bbox[0]


def _render_slide(slide, img_bytes):
    """
    Render branded text overlay onto a generated image.

    Args:
        slide: dict with headline, body, green_accent, type
        img_bytes: raw image bytes from generation

    Returns:
        PIL Image (RGBA)
    """
    img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    w, h = img.size

    # Apply semi-transparent dark overlay
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    # Gradient overlay — heavier at top for text legibility, light at bottom to show image
    for y_pos in range(h):
        opacity = int(170 - (y_pos / h) * 120)  # 170 at top, 50 at bottom
        opacity = max(40, min(170, opacity))
        overlay_draw.line([(0, y_pos), (w, y_pos)], fill=(0, 0, 0, opacity))

    img = Image.alpha_composite(img, overlay)

    # --- Text rendering ---
    draw = ImageDraw.Draw(img)
    margin_left = int(w * 0.08)
    margin_right = int(w * 0.08)
    max_text_width = w - margin_left - margin_right

    headline = slide.get("headline", "")
    body = slide.get("body", "")
    green_accent = slide.get("green_accent", "")

    # Headline font sizing
    headline_size = min(96, max(56, int(w * 0.075)))
    headline_font = _load_font(bold=True, size=headline_size)
    body_size = min(48, max(28, int(w * 0.035)))
    body_font = _load_font(bold=False, size=body_size)

    # Layout: headline starts in upper-left
    y_cursor = int(h * 0.15)

    # Draw headline (ALL CAPS)
    if headline:
        headline_upper = headline.upper()
        # Strip green markers for wrapping calculation
        clean_headline = re.sub(r'\{/?green\}', '', headline_upper)
        wrapped = _wrap_text(clean_headline, headline_font, max_text_width, draw)

        # Re-apply green markers for rendering
        for line in wrapped:
            # Shadow
            draw.text((margin_left + 3, y_cursor + 3), re.sub(r'\{/?green\}', '', line),
                      font=headline_font, fill=(0, 0, 0, 180))
            # If green_accent is in this line, render with green
            if green_accent and green_accent.upper() in line.upper():
                line_with_green = line.replace(
                    green_accent.upper(),
                    f"{{green}}{green_accent.upper()}{{/green}}"
                )
                _draw_text_with_green(draw, margin_left, y_cursor,
                                     line_with_green, headline_font)
            else:
                draw.text((margin_left, y_cursor), line,
                         font=headline_font, fill=TEXT_COLOR)
            y_cursor += int(headline_size * 1.2)

    # Spacing between headline and body
    y_cursor += int(body_size * 0.8)

    # Draw body
    if body:
        body_lines = body.split("\n")
        for body_line in body_lines:
            if not body_line.strip():
                y_cursor += int(body_size * 0.6)
                continue

            clean_line = re.sub(r'\{/?green\}', '', body_line)
            wrapped = _wrap_text(clean_line, body_font, max_text_width, draw)
            for wline in wrapped:
                # Shadow
                draw.text((margin_left + 2, y_cursor + 2),
                         re.sub(r'\{/?green\}', '', wline),
                         font=body_font, fill=(0, 0, 0, 150))
                # Check for green accent
                if green_accent and green_accent.lower() in wline.lower():
                    # Case-insensitive replacement
                    idx = wline.lower().find(green_accent.lower())
                    original_text = wline[idx:idx + len(green_accent)]
                    line_with_green = (
                        wline[:idx] +
                        f"{{green}}{original_text}{{/green}}" +
                        wline[idx + len(green_accent):]
                    )
                    _draw_text_with_green(draw, margin_left, y_cursor,
                                        line_with_green, body_font)
                else:
                    draw.text((margin_left, y_cursor), wline,
                             font=body_font, fill=TEXT_COLOR)
                y_cursor += int(body_size * 1.4)

    return img


def _generate_single_slide(idx, slide, total, gen_offset=0):
    """
    Generate (or pull from library) image and apply overlay for a single slide.

    Args:
        idx: index for staggering (only among slides that need generation)
        slide: slide spec dict
        total: total slides in carousel
        gen_offset: stagger offset for parallel generation timing
    """
    import requests

    num = slide["number"]
    shot_type = slide.get("shot_type", "establishing")
    prompt = slide.get("image_prompt") or ""
    library_image = slide.get("library_image")
    label = f"slide_{num:02d}"
    raw_bytes = None
    raw_url = None
    from_library = False

    try:
        # --- Option A: Pull from library ---
        if library_image:
            print(f"  [{num}/{total}] Loading from library: {library_image}")
            raw_bytes = _load_library_image(library_image)
            if raw_bytes:
                from_library = True
            else:
                print(f"  [{num}/{total}] Library image not found, generating instead...")

        # --- Option B: Generate new image ---
        if raw_bytes is None:
            if not prompt:
                raise Exception("No image_prompt and no valid library_image")

            # Stagger for rate limiting
            time.sleep(gen_offset * 2.0)

            print(f"  [{num}/{total}] Generating ({shot_type})...")

            # Use an optional user-supplied portrait reference for character shots.
            face = _brand_face()
            ref_paths = [face] if (shot_type == "character" and face) else None

            raw_url = generate_image(
                prompt=prompt,
                reference_paths=ref_paths,
                aspect_ratio="4:5",
            )
            if not raw_url:
                raise Exception("No result URL returned")

            # Download raw image
            resp = requests.get(raw_url, timeout=60)
            resp.raise_for_status()
            raw_bytes = resp.content

            # Save raw (no overlay) to library for future reuse
            tags = [t for t in slide.get("headline", "").lower().split() if len(t) > 3][:5]
            _save_to_library(raw_bytes, shot_type, tags=tags, prompt=prompt)

        # --- Apply branded overlay ---
        composited = _render_slide(slide, raw_bytes)

        # Save composited slide locally
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        local_path = OUTPUT_DIR / f"{label}.jpg"
        composited.convert("RGB").save(str(local_path), quality=95)

        # Upload composited version
        hosted_url = upload_reference(str(local_path))

        source = "library" if from_library else "generated"
        print(f"  [done] Slide {num} ({source}) -> {hosted_url[:60]}...")
        return {
            "number": num,
            "label": label,
            "raw_url": raw_url,
            "final_url": hosted_url,
            "local_path": str(local_path),
            "from_library": from_library,
            "status": "success",
        }
    except Exception as e:
        print(f"  [FAIL] Slide {num}: {e}")
        return {
            "number": num,
            "label": label,
            "from_library": False,
            "status": f"error: {e}",
        }


def generate_carousel(spec_path):
    """Main entry point — generate all slides from a carousel spec JSON."""
    with open(spec_path) as f:
        spec = json.load(f)

    title = spec.get("title", "Untitled Carousel")
    slides = spec.get("slides", [])
    total = len(slides)

    # Separate library pulls from new generations
    library_slides = [s for s in slides if s.get("library_image")]
    gen_slides = [s for s in slides if not s.get("library_image")]
    gen_cost = len(gen_slides) * 0.13

    print(f"\n{'=' * 60}")
    print(f"  Carousel: {title}")
    print(f"  Slides: {total} ({len(library_slides)} from library, {len(gen_slides)} new)")
    print(f"  Model: Nano Banana Pro")
    print(f"  Estimated cost: ${gen_cost:.2f}")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"{'=' * 60}\n")

    # Build generation order: library slides get idx=None (no stagger needed),
    # gen slides get sequential gen_offset for staggering
    slide_gen_offsets = {}
    gen_counter = 0
    for i, slide in enumerate(slides):
        if slide.get("library_image"):
            slide_gen_offsets[i] = 0  # no stagger for library
        else:
            slide_gen_offsets[i] = gen_counter
            gen_counter += 1

    # Generate in parallel with staggered starts (only gen slides stagger)
    max_workers = min(max(len(gen_slides), 1), 5)
    results_map = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                _generate_single_slide, i, slide, total,
                gen_offset=slide_gen_offsets[i]
            ): i
            for i, slide in enumerate(slides)
        }
        for future in as_completed(futures):
            idx = futures[future]
            results_map[idx] = future.result()

    # Collect in order
    results = [results_map[i] for i in range(total)]

    # Summary
    succeeded = sum(1 for r in results if r["status"] == "success")
    from_lib = sum(1 for r in results if r.get("from_library"))
    generated = succeeded - from_lib
    print(f"\n{'=' * 60}")
    print(f"  CAROUSEL COMPLETE: {succeeded}/{total} slides")
    print(f"  ({from_lib} from library, {generated} newly generated)")
    print(f"{'=' * 60}")
    for r in results:
        status = "OK" if r["status"] == "success" else "FAIL"
        source = " [lib]" if r.get("from_library") else ""
        print(f"  [{status}] Slide {r['number']}{source}: {r.get('label', '?')}")
        if r.get("final_url"):
            print(f"         {r['final_url']}")
    print(f"\n  Actual cost: ${generated * 0.13:.2f}")
    print(f"  Raw images saved to library for reuse")
    print(f"{'=' * 60}\n")

    # Save results manifest
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = OUTPUT_DIR / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump({"title": title, "slides": results}, f, indent=2)
    print(f"  Manifest saved: {manifest_path}")

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate_carousel.py <carousel_spec.json>")
        sys.exit(1)
    generate_carousel(sys.argv[1])
