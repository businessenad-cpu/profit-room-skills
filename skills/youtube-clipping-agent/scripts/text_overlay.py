#!/usr/bin/env python3
"""Build FFmpeg filter strings for text overlays."""

import argparse
import os


IMPACT_FONT = "/System/Library/Fonts/Supplemental/Impact.ttf"
DIN_FONT    = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
FALLBACK    = "/System/Library/Fonts/Helvetica.ttc"


def _font(path: str) -> str:
    return path if os.path.exists(path) else FALLBACK


def escape_drawtext(text: str) -> str:
    """Escape special characters for FFmpeg drawtext filter.

    NOTE: text values are wrapped in single quotes in the filter string
    (text='...'). FFmpeg's filter parser does NOT allow escaping single
    quotes inside single-quoted values — there is no valid escape sequence.
    Replace ' with the Unicode right single quotation mark (U+2019) which
    is visually identical but not special to the parser.
    """
    text = text.replace("\\", "\\\\")
    text = text.replace(":", "\\:")
    text = text.replace("'", "\u2019")   # ' → ' (visually identical, parser-safe)
    text = text.replace(";", "\\;")
    return text


def get_drawtext_filter(rank: int, title: str, subtitle: str = "",
                        duration: float = 6.0) -> str:
    """Top-third overlay for individual clips.

    Hardcoded pixels for 1080x1920 output (avoids FFmpeg `h=` shadowing `h*N` expressions).

    Layout (left-anchored compact card, top third, text 30% smaller than original):
      Box     : x=0, y=40, w=400, h=193  (top third)
      Text centered within box: x = 200 - text_w/2
      Rank    : Impact y=60,  fontsize=84  (gold,  20px from box top)
      Title   : DIN    y=152, fontsize=30  (white, 8px below rank)
      Subtitle: DIN    y=188, fontsize=25  (white, 6px below title)
      → padding = 20px top & bottom
    """
    impact = _font(IMPACT_FONT)
    din    = _font(DIN_FONT)

    # Compact rectangle, flush left (x=0), 400w x 193h, top third of frame.
    # Text block (84+8+30+6+25=153px) + 20px padding top & bottom = 193px box height.
    #   Rank    : Impact y=60,  fontsize=84  (gold)
    #   Title   : DIN    y=152, fontsize=30  (white, 8px below rank)
    #   Subtitle: DIN    y=188, fontsize=25  (white, 6px below title)
    parts = [
        "drawbox=x=0:y=40:w=400:h=193:color=black@0.85:t=fill",
        f"drawtext=fontfile={impact}:text='{escape_drawtext(f'#{rank}')}':fontcolor=#FFD700"
        f":fontsize=84:x=200-text_w/2:y=60",
        f"drawtext=fontfile={din}:text='{escape_drawtext(title)}':fontcolor=white"
        f":fontsize=30:x=200-text_w/2:y=152",
    ]
    if subtitle:
        parts.append(
            f"drawtext=fontfile={din}:text='{escape_drawtext(subtitle)}':fontcolor=white"
            f":fontsize=25:x=200-text_w/2:y=188"
        )
    return ",".join(parts)


def get_intro_overlay_filter(top_line: str, *body_lines: str) -> str:
    """Left-aligned stacked title card, no background box.

    Matches the style: large Impact text stacked top-to-bottom on the left,
    top_line in gold, body_lines in white, black border for readability.

    Hardcoded pixels for 1080x1920.

    Layout (fontsize=160, line_height=175):
      top_line  : y=70  (gold, Impact 160px)
      body_line1: y=245 (white, Impact 160px)
      body_line2: y=420
      body_line3: y=595
      body_line4: y=770
      x=30 (left-anchored)
    """
    impact = _font(IMPACT_FONT)
    fontsize = 160
    line_height = 175
    border = "borderw=5:bordercolor=black@0.9"

    # Vertically center the text block in the 1920px frame
    n_lines = 1 + len(body_lines)
    text_block_height = fontsize + (n_lines - 1) * line_height
    y_start = (1920 - text_block_height) // 2

    # Center each line horizontally on the 1080px frame
    x = "(w-text_w)/2"

    parts = [
        f"drawtext=fontfile={impact}:text='{escape_drawtext(top_line.upper())}'"
        f":fontcolor=#FFD700:fontsize={fontsize}:x={x}:y={y_start}:{border}",
    ]
    for i, line in enumerate(body_lines):
        y = y_start + (i + 1) * line_height
        parts.append(
            f"drawtext=fontfile={impact}:text='{escape_drawtext(line.upper())}'"
            f":fontcolor=white:fontsize={fontsize}:x={x}:y={y}:{border}"
        )
    return ",".join(parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("rank", type=int)
    parser.add_argument("title", type=str)
    parser.add_argument("--duration", type=float, default=6.0)
    args = parser.parse_args()
    print(get_drawtext_filter(args.rank, args.title, args.duration))


if __name__ == "__main__":
    main()
