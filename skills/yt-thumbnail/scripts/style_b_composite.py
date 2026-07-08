"""
Style B — Old vs New Contrast Thumbnail
Composites a split-panel before/after YouTube thumbnail at 3840x2160 (4K 16:9).

Usage:
    python3 style_b_composite.py \
        --old-label "OLD WAY" \
        --new-label "NEW WAY" \
        --old-image /path/to/old_panel.jpg \
        --new-image /path/to/new_panel.jpg \
        --output /path/to/thumbnail_b.jpg
"""

import argparse, math, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 3840, 2160
PANEL_MARGIN = 80
PANEL_GAP = 160
BADGE_H = 240
BADGE_RADIUS = 55
BORDER = 16
FONT_BADGE = 240         # Impact / heavy font size
FONT_ARROW = 360         # arrow symbol fallback
ARROW_COLOR = (255, 210, 0)
RED = (220, 30, 30)
GREEN = (30, 200, 60)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRID_COLOR = (200, 200, 200)
BG_COLOR = (238, 238, 238)


# ── helpers ──────────────────────────────────────────────────────────────────

def draw_grid(draw, w, h, spacing=80):
    for x in range(0, w, spacing):
        draw.line([(x, 0), (x, h)], fill=GRID_COLOR, width=2)
    for y in range(0, h, spacing):
        draw.line([(0, y), (w, y)], fill=GRID_COLOR, width=2)


def rounded_rect(draw, xy, radius, fill, outline=None, outline_width=0):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill,
                            outline=outline, width=outline_width)


def load_font(size):
    candidates = [
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        "/Library/Fonts/Impact.ttf",
        "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default(size=size)


def draw_badge(draw, text, color, cx, cy, w_hint=None):
    font = load_font(FONT_BADGE)
    bbox = font.getbbox(text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 120, 40
    bw = tw + pad_x * 2
    bh = th + pad_y * 2
    x0 = cx - bw // 2
    y0 = cy - bh // 2
    x1 = x0 + bw
    y1 = y0 + bh
    # shadow
    rounded_rect(draw, (x0 + 14, y0 + 14, x1 + 14, y1 + 14), BADGE_RADIUS,
                 fill=(0, 0, 0, 120))
    # badge
    rounded_rect(draw, (x0, y0, x1, y1), BADGE_RADIUS, fill=color,
                 outline=BLACK, outline_width=BORDER)
    # text (white + thick black stroke)
    tx = cx - tw // 2 - bbox[0]
    ty = cy - th // 2 - bbox[1]
    for ox, oy in [(-8, -8), (8, -8), (-8, 8), (8, 8),
                   (0, -10), (0, 10), (-10, 0), (10, 0)]:
        draw.text((tx + ox, ty + oy), text, font=font, fill=BLACK)
    draw.text((tx, ty), text, font=font, fill=WHITE)


def draw_red_x(draw, x0, y0, x1, y1, thickness=36):
    pad = 60
    for i in range(-thickness // 2, thickness // 2 + 1):
        draw.line([(x0 + pad + i, y0 + pad), (x1 - pad + i, y1 - pad)],
                  fill=RED, width=6)
        draw.line([(x0 + pad, y0 + pad + i), (x1 - pad, y1 - pad + i)],
                  fill=RED, width=6)
        draw.line([(x1 - pad + i, y0 + pad), (x0 + pad + i, y1 - pad)],
                  fill=RED, width=6)
        draw.line([(x1 - pad, y0 + pad + i), (x0 + pad, y1 - pad + i)],
                  fill=RED, width=6)


def draw_swoosh_arrow(img, draw, cx, cy, width=520, height=380):
    """Draw a fat 3D-style yellow curved arrow pointing right."""
    # Approximate with a thick bezier-ish arc + arrowhead using polygon
    # Arrow body: thick curved band
    pts_top = []
    pts_bot = []
    steps = 60
    thickness = 130

    # Curve: arc from left-up to right-down, like a swoosh
    for i in range(steps + 1):
        t = i / steps
        # parametric curve
        x = cx - width // 2 + int(t * width)
        y = cy - int(math.sin(t * math.pi) * (height * 0.45)) + int((t - 0.5) * height * 0.5)
        # normal vector (perpendicular to tangent)
        if i < steps:
            t2 = (i + 1) / steps
            nx = cx - width // 2 + int(t2 * width)
            ny = cy - int(math.sin(t2 * math.pi) * (height * 0.45)) + int((t2 - 0.5) * height * 0.5)
            dx = nx - x
            dy = ny - y
            length = math.sqrt(dx*dx + dy*dy) or 1
            nx_norm = -dy / length
            ny_norm = dx / length
        pts_top.append((int(x + nx_norm * thickness // 2), int(y + ny_norm * thickness // 2)))
        pts_bot.append((int(x - nx_norm * thickness // 2), int(y - ny_norm * thickness // 2)))

    body_pts = pts_top + list(reversed(pts_bot))

    # shadow
    shadow_pts = [(p[0] + 18, p[1] + 18) for p in body_pts]
    draw.polygon(shadow_pts, fill=(0, 0, 0, 100))
    # body
    draw.polygon(body_pts, fill=ARROW_COLOR, outline=(180, 150, 0), width=6)

    # arrowhead triangle at the end
    tip = pts_top[-1]
    tail_top = pts_top[int(steps * 0.75)]
    tail_bot = pts_bot[int(steps * 0.75)]
    head_pts = [
        (tip[0] + 100, (tip[1] + pts_bot[-1][1]) // 2),
        (tail_top[0], tail_top[1] - 80),
        (tail_bot[0], tail_bot[1] + 80),
    ]
    draw.polygon([(p[0]+18, p[1]+18) for p in head_pts], fill=(0, 0, 0, 100))
    draw.polygon(head_pts, fill=ARROW_COLOR, outline=(180, 150, 0), width=6)


def fit_image_into(panel_img, box_w, box_h):
    """Resize image to fill box, center-crop."""
    src_w, src_h = panel_img.size
    scale = max(box_w / src_w, box_h / src_h)
    new_w = int(src_w * scale)
    new_h = int(src_h * scale)
    panel_img = panel_img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - box_w) // 2
    top = (new_h - box_h) // 2
    return panel_img.crop((left, top, left + box_w, top + box_h))


# ── main ─────────────────────────────────────────────────────────────────────

def compose(old_label, new_label, old_image_path, new_image_path, output_path):
    canvas = Image.new("RGBA", (W, H), (*BG_COLOR, 255))
    draw = ImageDraw.Draw(canvas, "RGBA")

    draw_grid(draw, W, H, spacing=int(H * 0.037))

    # Layout
    badge_top = int(H * 0.04)
    badge_cy = badge_top + BADGE_H // 2
    panel_top = badge_top + BADGE_H + 60
    panel_bot = H - PANEL_MARGIN
    panel_h = panel_bot - panel_top

    panel_w = (W - PANEL_MARGIN * 2 - PANEL_GAP) // 2
    left_x0 = PANEL_MARGIN
    left_x1 = left_x0 + panel_w
    right_x0 = left_x1 + PANEL_GAP
    right_x1 = right_x0 + panel_w

    left_cx = (left_x0 + left_x1) // 2
    right_cx = (right_x0 + right_x1) // 2

    # ── Old panel ──
    old_img = Image.open(old_image_path).convert("RGBA")
    old_filled = fit_image_into(old_img.convert("RGB"), panel_w - BORDER * 2, panel_h - BORDER * 2)
    rounded_rect(draw, (left_x0, panel_top, left_x1, panel_bot), 40,
                 fill=BLACK, outline=BLACK, outline_width=BORDER)
    canvas.paste(old_filled.convert("RGBA"),
                 (left_x0 + BORDER, panel_top + BORDER))

    # Red X over old panel
    draw_red_x(draw, left_x0, panel_top, left_x1, panel_bot, thickness=52)

    # ── New panel ──
    new_img = Image.open(new_image_path).convert("RGBA")
    new_filled = fit_image_into(new_img.convert("RGB"), panel_w - BORDER * 2, panel_h - BORDER * 2)
    rounded_rect(draw, (right_x0, panel_top, right_x1, panel_bot), 40,
                 fill=BLACK, outline=BLACK, outline_width=BORDER)
    canvas.paste(new_filled.convert("RGBA"),
                 (right_x0 + BORDER, panel_top + BORDER))

    # ── Badges ──
    draw_badge(draw, old_label.upper(), RED, left_cx, badge_cy)
    draw_badge(draw, new_label.upper(), GREEN, right_cx, badge_cy)

    # ── Swoosh arrow ──
    arrow_cx = W // 2
    arrow_cy = panel_top + panel_h // 2 - 60
    draw_swoosh_arrow(canvas, draw, arrow_cx, arrow_cy, width=560, height=420)

    # Flatten to RGB and save
    final = canvas.convert("RGB")
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final.save(output_path, quality=95)
    print(f"Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--old-label", default="OLD", help="Label for left/bad panel")
    parser.add_argument("--new-label", default="NEW", help="Label for right/good panel")
    parser.add_argument("--old-image", required=True, help="Image for the old/left panel")
    parser.add_argument("--new-image", required=True, help="Image for the new/right panel")
    parser.add_argument("--output", required=True, help="Output path (.jpg)")
    args = parser.parse_args()

    compose(args.old_label, args.new_label, args.old_image, args.new_image, args.output)


if __name__ == "__main__":
    main()
