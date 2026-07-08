"""
Render an "alternating solid" Instagram carousel from a JSON spec — no image
generation, no API keys, fully offline (PIL only).

Usage:
    python3 render_solid.py <carousel_spec.json>

Reads a spec with a `slides` list. Each slide supports these fields:
    number, type, headline, body, accent_phrase,
    bg_mode        : "dark" | "light" | "cover" | "gradient" | "light_pop"
    show_logo      : bool  — draws your logo/wordmark lockup top-left
    step_label     : str   — small uppercase label above the headline
    topic_label    : str   — accent-colored category label above the headline
    stat_value     : str   — renders a big-number stat slide (with stat_label)
    stat_label     : str
    cta_button     : str   — orange pill button (CTA slides)
    show_bookmark  : bool  — bookmark icon top-left (encourage saves)
    github_card    : dict  — {owner,name,description,language,language_color,stars}
    bottom_summary : str   — bold one-liner + arrow just above the progress bar
    image_path     : str   — local image embedded as a rounded card
    image_position : "top" | "center" | "bottom" (default bottom)
    dark_card_text : str   — key insight rendered on a dark floating card
    cover_image_path : str — full-bleed photo cover with dark overlay + white text

Output:
    output/slides/slide_XX.jpg + output/slides/manifest.json   (LOCAL ONLY)

Branding is user-supplied and optional:
    env BRAND_LOGO   path to a logo image (used for the show_logo lockup)
    env BRAND_NAME   wordmark text if you have no logo image (default "YOUR BRAND")
"""

import os
import re
import sys
import json
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)

# --- Canvas ---
W, H = 1080, 1350
MARGIN = 90

# --- Palette ---
BG_DARK = (10, 10, 10)       # #0A0A0A
BG_LIGHT = (26, 26, 26)      # #1A1A1A
BG_COVER = (20, 20, 20)      # #141414
CREAM = (232, 220, 196)      # #E8DCC4
CHARCOAL = (28, 27, 23)      # #1C1B17
WHITE = (245, 240, 232)      # #F5F0E8
GREEN = (0, 255, 0)          # #00FF00
ORANGE = (255, 102, 0)       # #FF6600

# --- Fonts (system fonts, graceful fallback to PIL default) ---
_BOLD_PATHS = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
    "arialbd.ttf",
]
_REG_PATHS = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
    "arial.ttf",
]


def _font(bold=True, size=48):
    for path in (_BOLD_PATHS if bold else _REG_PATHS):
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def _theme(bg_mode):
    """Return (bg_kind, text_color, accent_color, is_light)."""
    if bg_mode == "light_pop":
        return ("light_pop", CHARCOAL, ORANGE, True)
    if bg_mode == "gradient":
        return ("gradient", WHITE, ORANGE, False)
    if bg_mode == "light":
        return ("light", WHITE, GREEN, False)
    if bg_mode == "cover":
        return ("cover", WHITE, GREEN, False)
    return ("dark", WHITE, GREEN, False)


def _make_background(bg_kind):
    if bg_kind == "light_pop":
        img = Image.new("RGB", (W, H), CREAM)
        d = ImageDraw.Draw(img)
        # faint grid texture
        grid = tuple(min(c + 10, 255) for c in CREAM)
        for x in range(0, W, 60):
            d.line([(x, 0), (x, H)], fill=grid, width=1)
        for y in range(0, H, 60):
            d.line([(0, y), (W, y)], fill=grid, width=1)
        return img
    if bg_kind == "gradient":
        img = Image.new("RGB", (W, H))
        d = ImageDraw.Draw(img)
        for y in range(H):
            t = y / H
            c = tuple(int(10 + (28 - 10) * t) for _ in range(3))
            d.line([(0, y), (W, y)], fill=c)
        return img
    color = {"light": BG_LIGHT, "cover": BG_COVER}.get(bg_kind, BG_DARK)
    return Image.new("RGB", (W, H), color)


def _clean(text):
    """Strip italic and accent markers."""
    return re.sub(r"\*", "", re.sub(r"\{/?green\}", "", text or ""))


def _wrap(text, font, max_w, draw):
    lines = []
    for segment in text.split("\n"):
        words = segment.split()
        if not words:
            lines.append("")
            continue
        cur = ""
        for word in words:
            test = f"{cur} {word}".strip()
            if draw.textlength(test, font=font) <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def _draw_line(draw, x, y, line, font, color, accent_phrase, accent_color):
    """Draw a line, highlighting accent_phrase (case-insensitive) in accent_color."""
    if accent_phrase and accent_phrase.lower() in line.lower():
        idx = line.lower().find(accent_phrase.lower())
        before, match, after = line[:idx], line[idx:idx + len(accent_phrase)], line[idx + len(accent_phrase):]
        cx = x
        for seg, col in ((before, color), (match, accent_color), (after, color)):
            if seg:
                draw.text((cx, y), seg, font=font, fill=col)
                cx += draw.textlength(seg, font=font)
    else:
        draw.text((x, y), line, font=font, fill=color)


def _draw_text_block(draw, x, y, text, font, color, accent_phrase, accent_color,
                     max_w, line_gap=1.4, para_gap=0.6):
    lh = int(font.size * line_gap)
    for raw in text.split("\n"):
        if not raw.strip():
            y += int(font.size * para_gap)
            continue
        for line in _wrap(_clean(raw), font, max_w, draw):
            _draw_line(draw, x, y, line, font, color, accent_phrase, accent_color)
            y += lh
    return y


# ---------- decorative elements ----------

def _draw_logo(img, draw, x, y, is_light):
    """Draw the user's logo (env BRAND_LOGO) or a text wordmark (env BRAND_NAME)."""
    logo_path = os.environ.get("BRAND_LOGO")
    if logo_path and Path(os.path.expanduser(logo_path)).exists():
        try:
            logo = Image.open(os.path.expanduser(logo_path)).convert("RGBA")
            target_h = 56
            ratio = target_h / logo.height
            logo = logo.resize((int(logo.width * ratio), target_h))
            img.paste(logo, (x, y), logo)
            return
        except Exception:  # noqa: BLE001
            pass
    name = os.environ.get("BRAND_NAME", "YOUR BRAND").upper()
    color = CHARCOAL if is_light else WHITE
    draw.text((x, y), name, font=_font(True, 34), fill=color)


def _draw_bookmark(draw, x, y):
    """Small orange bookmark icon."""
    w, h = 34, 46
    draw.polygon([(x, y), (x + w, y), (x + w, y + h),
                  (x + w // 2, y + h - 16), (x, y + h)], fill=ORANGE)


def _draw_progress(draw, number, total, is_last, accent):
    """Progress bar + counter + swipe chevron (chevron omitted on last slide)."""
    bar_y = H - 70
    bar_x0, bar_x1 = MARGIN, W - MARGIN
    track = (90, 90, 90)
    draw.line([(bar_x0, bar_y), (bar_x1, bar_y)], fill=track, width=6)
    frac = max(0.0, min(1.0, number / max(total, 1)))
    fill_x = bar_x0 + int((bar_x1 - bar_x0) * frac)
    draw.line([(bar_x0, bar_y), (fill_x, bar_y)], fill=accent, width=6)
    draw.text((bar_x0, bar_y - 40), f"{number}/{total}", font=_font(True, 26), fill=track)
    if not is_last:
        cx, cy = W - MARGIN - 20, bar_y - 30
        draw.line([(cx, cy - 14), (cx + 16, cy), (cx, cy + 14)], fill=accent, width=6)


def _fit_cover(im, w, h):
    """Resize + center-crop an image to exactly (w, h)."""
    ratio = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * ratio) + 1, int(im.height * ratio) + 1))
    left = (im.width - w) // 2
    top = (im.height - h) // 2
    return im.crop((left, top, left + w, top + h))


def _rounded(im, radius=32):
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.size[0], im.size[1]], radius, fill=255)
    im.putalpha(mask)
    return im


# ---------- slide renderers ----------

def _render_cover_photo(slide):
    """Full-bleed photo cover with dark overlay + white text."""
    path = os.path.expanduser(slide["cover_image_path"])
    base = Image.open(path).convert("RGB")
    base = _fit_cover(base, W, H).convert("RGBA")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 150))
    img = Image.alpha_composite(base, overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    y = int(H * 0.14)
    topic = slide.get("topic_label")
    if slide.get("show_bookmark"):
        _draw_bookmark(draw, MARGIN, y)
        if topic:
            draw.text((MARGIN + 50, y + 8), topic.upper(), font=_font(True, 30), fill=WHITE)
        y += 80
    elif topic:
        draw.text((MARGIN, y), topic.upper(), font=_font(True, 30), fill=ORANGE)
        y += 60
    headline = slide.get("headline", "")
    hfont = _font(True, 92)
    y = max(y, int(H * 0.55))
    _draw_text_block(draw, MARGIN, y, headline, hfont, WHITE,
                     slide.get("accent_phrase"), ORANGE, W - 2 * MARGIN, line_gap=1.05)
    return img


def _render_stat(slide, text_color, accent):
    img = _make_background(_theme(slide.get("bg_mode", "dark"))[0])
    draw = ImageDraw.Draw(img)
    value = slide.get("stat_value", "")
    label = slide.get("stat_label", "")
    vfont = _font(True, 220)
    vw = draw.textlength(value, font=vfont)
    draw.text(((W - vw) / 2, H * 0.30), value, font=vfont, fill=accent)
    if label:
        lfont = _font(True, 46)
        lw = draw.textlength(label.upper(), font=lfont)
        draw.text(((W - lw) / 2, H * 0.30 + 240), label.upper(), font=lfont, fill=text_color)
    return img


def _render_github_card(img, draw, card, y, is_light):
    """White floating GitHub-style repo card."""
    x0, x1 = MARGIN, W - MARGIN
    card_h = 230
    ImageDraw.Draw(img).rounded_rectangle([x0, y, x1, y + card_h], 24, fill=(255, 255, 255))
    tx, ty = x0 + 36, y + 30
    owner = card.get("owner", "")
    name = card.get("name", "")
    draw.text((tx, ty), f"{owner}/", font=_font(False, 34), fill=(80, 80, 80))
    ow = draw.textlength(f"{owner}/", font=_font(False, 34))
    draw.text((tx + ow, ty), name, font=_font(True, 34), fill=(20, 20, 20))
    desc = card.get("description", "")
    if desc:
        for i, line in enumerate(_wrap(desc, _font(False, 28), x1 - x0 - 72, draw)[:2]):
            draw.text((tx, ty + 56 + i * 36), line, font=_font(False, 28), fill=(60, 60, 60))
    ly = y + card_h - 52
    lang = card.get("language")
    if lang:
        col = card.get("language_color", "#3572A5")
        try:
            rgb = tuple(int(col.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
        except Exception:  # noqa: BLE001
            rgb = (120, 120, 120)
        draw.ellipse([tx, ly + 6, tx + 18, ly + 24], fill=rgb)
        draw.text((tx + 28, ly), lang, font=_font(False, 26), fill=(60, 60, 60))
    stars = card.get("stars")
    if stars:
        draw.text((tx + 220, ly), f"* {stars}", font=_font(False, 26), fill=(60, 60, 60))
    return y + card_h + 30


def _render_standard(slide):
    bg_kind, text_color, accent, is_light = _theme(slide.get("bg_mode", "dark"))
    img = _make_background(bg_kind)
    draw = ImageDraw.Draw(img)

    y = int(H * 0.10)

    # top-left icons
    if slide.get("show_bookmark"):
        _draw_bookmark(draw, MARGIN, y)
    if slide.get("show_logo"):
        _draw_logo(img, draw, MARGIN + (60 if slide.get("show_bookmark") else 0), y, is_light)
    if slide.get("show_logo") or slide.get("show_bookmark"):
        y += 90

    # labels
    if slide.get("step_label"):
        draw.text((MARGIN, y), slide["step_label"].upper(), font=_font(True, 34), fill=accent)
        y += 56
    if slide.get("topic_label"):
        draw.text((MARGIN, y), slide["topic_label"].upper(), font=_font(True, 32), fill=accent)
        y += 56

    # headline
    headline = slide.get("headline", "")
    if headline:
        hsize = 96 if is_light else 88
        hfont = _font(True, hsize)
        text = headline if is_light else headline.upper()
        y = _draw_text_block(draw, MARGIN, y, text, hfont, text_color,
                             slide.get("accent_phrase"), accent, W - 2 * MARGIN, line_gap=1.05)
        y += 40

    # github card
    if slide.get("github_card"):
        y = _render_github_card(img, draw, slide["github_card"], y, is_light)

    # embedded image card
    if slide.get("image_path"):
        p = os.path.expanduser(slide["image_path"])
        if Path(p).exists():
            try:
                card_w = W - 2 * MARGIN
                card_h = 520
                im = _fit_cover(Image.open(p).convert("RGB"), card_w, card_h).convert("RGBA")
                im = _rounded(im, 28)
                pos = slide.get("image_position", "bottom")
                iy = {"top": y, "center": int(H * 0.35)}.get(pos, H - 700)
                img.paste(im, (MARGIN, iy), im)
                y = max(y, iy + card_h + 20)
            except Exception:  # noqa: BLE001
                pass

    # dark floating insight card (light_pop)
    if slide.get("dark_card_text"):
        card_w = W - 2 * MARGIN
        cy = int(H * 0.40)
        card_h = 300
        ImageDraw.Draw(img).rounded_rectangle([MARGIN, cy, MARGIN + card_w, cy + card_h], 28, fill=CHARCOAL)
        _draw_text_block(draw, MARGIN + 40, cy + 40, slide["dark_card_text"],
                         _font(True, 50), CREAM, slide.get("accent_phrase"), ORANGE,
                         card_w - 80, line_gap=1.25)

    # body
    body = slide.get("body", "")
    if body:
        y = _draw_text_block(draw, MARGIN, y + 10, body, _font(False, 42), text_color,
                             slide.get("accent_phrase"), accent, W - 2 * MARGIN)

    # cta pill button
    if slide.get("cta_button"):
        label = slide["cta_button"].upper()
        bfont = _font(True, 40)
        tw = draw.textlength(label, font=bfont)
        pad_x, pad_h = 50, 84
        by = y + 40
        bx1 = MARGIN + tw + pad_x * 2
        draw.rounded_rectangle([MARGIN, by, bx1, by + pad_h], pad_h // 2, fill=ORANGE)
        draw.text((MARGIN + pad_x, by + (pad_h - bfont.size) / 2 - 4), label, font=bfont, fill=WHITE)

    # bottom summary
    if slide.get("bottom_summary"):
        sfont = _font(True, 40)
        sy = H - 150
        draw.text((MARGIN, sy), ">", font=sfont, fill=ORANGE)
        _draw_text_block(draw, MARGIN + 40, sy, slide["bottom_summary"], sfont,
                         text_color, slide.get("accent_phrase"), accent, W - 2 * MARGIN - 40,
                         line_gap=1.15)

    return img, text_color, accent


def render_slide(slide, total):
    number = slide.get("number", 1)
    is_last = number >= total

    if slide.get("cover_image_path") and Path(os.path.expanduser(slide["cover_image_path"])).exists():
        img = _render_cover_photo(slide)
        accent = ORANGE
    elif slide.get("stat_value"):
        _, text_color, accent, _ = _theme(slide.get("bg_mode", "dark"))
        img = _render_stat(slide, text_color, accent)
    else:
        img, _text_color, accent = _render_standard(slide)

    draw = ImageDraw.Draw(img)
    _draw_progress(draw, number, total, is_last, accent)
    return img


def render_carousel(spec_path):
    with open(spec_path) as f:
        spec = json.load(f)

    title = spec.get("title", "Untitled Carousel")
    slides = spec.get("slides", [])
    total = len(slides)

    root = os.environ.get("CAROUSEL_ROOT")
    base = Path(root) if root else Path(__file__).resolve().parent.parent
    out_dir = base / "output" / "slides"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'=' * 60}")
    print(f"  Carousel: {title}")
    print(f"  Slides: {total}   Output: {out_dir}")
    print(f"{'=' * 60}\n")

    results = []
    for slide in slides:
        num = slide.get("number", len(results) + 1)
        label = f"slide_{num:02d}"
        try:
            img = render_slide(slide, total)
            path = out_dir / f"{label}.jpg"
            img.convert("RGB").save(str(path), quality=95)
            print(f"  [OK] {label} ({slide.get('bg_mode', 'dark')})")
            results.append({"number": num, "label": label,
                            "local_path": str(path), "status": "success"})
        except Exception as e:  # noqa: BLE001
            print(f"  [FAIL] {label}: {e}")
            results.append({"number": num, "label": label, "status": f"error: {e}"})

    manifest = out_dir / "manifest.json"
    with open(manifest, "w") as f:
        json.dump({"title": title, "slides": results}, f, indent=2)

    ok = sum(1 for r in results if r["status"] == "success")
    print(f"\n  DONE: {ok}/{total} slides -> {out_dir}")
    print(f"  Manifest: {manifest}\n")
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 render_solid.py <carousel_spec.json>")
        sys.exit(1)
    render_carousel(sys.argv[1])
