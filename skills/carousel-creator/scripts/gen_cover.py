#!/usr/bin/env python3
"""
Generate a photo cover image for a carousel via the Higgsfield CLI.

The image is designed with strong negative space so a headline can be
overlaid on top of it by the renderer (render_solid.py sets it as
`cover_image_path` on slide 1).

Usage:
    python3 gen_cover.py                 # pick a context-appropriate/random prompt
    python3 gen_cover.py <prompt_key>    # use a specific prompt from the library
    python3 gen_cover.py --list          # print available prompt keys (no API needed)

On success the ONLY thing printed to stdout is the saved image path, so the
skill can capture it directly:  cover_path=$(python3 gen_cover.py)

Optional brand art:
    Set env BRAND_LOGO (or BRAND_MASCOT) to an image path and it will be passed
    to Higgsfield as a --image reference. If unset, the cover is generated with
    no reference. Prompts themselves are brand-neutral.

Graceful failure:
    If the `higgsfield` CLI is not installed, a clear message is printed to
    STDERR and the script exits 1 (no traceback).
"""

import os
import re
import sys
import random
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

# --- Prompt library: brand-neutral scenes with strong negative space for text ---
PROMPTS = {
    "desk_workspace": (
        "4:5. Cinematic photo of a modern minimal desk workspace — laptop, "
        "notebook, coffee, warm morning light through a window. Shot from a low "
        "angle, shallow depth of field, moody and premium. Large clean negative "
        "space in the upper third for text overlay. No people, no logos, no text."
    ),
    "abstract_hero": (
        "4:5. Abstract hero background — soft gradient light, subtle geometric "
        "shapes and depth, cinematic color grading, premium editorial feel. "
        "Generous empty negative space in the center for a headline. "
        "No people, no logos, no text."
    ),
    "city_rooftop": (
        "4:5. Cinematic wide shot of a city rooftop at golden hour, skyline in "
        "soft focus behind, warm dramatic light, aspirational and calm. Large "
        "negative space in the upper portion for text overlay. No people in "
        "focus, no logos, no text."
    ),
    "cafe_lifestyle": (
        "4:5. Warm lifestyle photo inside a bright cafe — a table by the window, "
        "coffee and an open laptop, soft daylight, shallow depth of field, "
        "inviting and premium. Clean negative space in the lower third for text. "
        "No faces, no logos, no text."
    ),
    "beach_aspirational": (
        "4:5. Aspirational coastal scene — calm ocean horizon at sunrise, soft "
        "pastel sky, wide open composition, cinematic and serene. Vast negative "
        "space across the sky for a headline. No people, no logos, no text."
    ),
    "hand_object_hero": (
        "4:5. Close-up cinematic photo of a hand holding a small everyday object "
        "against a clean softly-blurred background, dramatic single-source light, "
        "shallow depth of field, premium product-hero feel. Negative space around "
        "the object for text. No faces, no logos, no text."
    ),
}

# Keys that suit dev/AI/tooling topics vs lifestyle/aspirational — used when no key given.
_DEV_KEYS = ["desk_workspace", "abstract_hero", "hand_object_hero"]


def _find_higgsfield():
    """Locate the higgsfield CLI, or return None."""
    exe = shutil.which("higgsfield")
    if exe:
        return exe
    fallback = Path.home() / ".npm-global" / "bin" / "higgsfield"
    if fallback.exists():
        return str(fallback)
    return None


def _brand_reference():
    """Return a brand art path from env if it exists, else None."""
    for var in ("BRAND_LOGO", "BRAND_MASCOT"):
        val = os.environ.get(var)
        if val and Path(os.path.expanduser(val)).exists():
            return os.path.expanduser(val)
    return None


def _output_dir():
    """output/cover_options at the skill root (parent of scripts/)."""
    root = os.environ.get("CAROUSEL_ROOT")
    base = Path(root) if root else Path(__file__).resolve().parent.parent
    out = base / "output" / "cover_options"
    out.mkdir(parents=True, exist_ok=True)
    return out


def _extract_url(text):
    """Return the last http(s) URL found in text, or None."""
    urls = re.findall(r"https?://[^\s'\"]+", text)
    return urls[-1] if urls else None


def generate_cover(prompt_key=None):
    """Generate a cover image and return the saved local path (str)."""
    exe = _find_higgsfield()
    if not exe:
        sys.stderr.write(
            "ERROR: the 'higgsfield' CLI was not found. Install/authenticate it "
            "(npm i -g higgsfield) or use the alternating-solid render path "
            "(render_solid.py), which needs no image generation.\n"
        )
        sys.exit(1)

    if prompt_key and prompt_key not in PROMPTS:
        sys.stderr.write(
            f"ERROR: unknown prompt key '{prompt_key}'. "
            f"Available: {', '.join(PROMPTS)}\n"
        )
        sys.exit(1)

    if not prompt_key:
        prompt_key = random.choice(_DEV_KEYS)

    prompt = PROMPTS[prompt_key]
    ref = _brand_reference()

    cmd = [exe, "generate", "create", "nano_banana_2",
           "--aspect_ratio", "4:5", "--prompt", prompt, "--wait"]
    if ref:
        cmd += ["--image", ref]
        sys.stderr.write(f"[gen_cover] using brand reference: {ref}\n")

    sys.stderr.write(f"[gen_cover] generating cover '{prompt_key}'...\n")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"ERROR: higgsfield invocation failed: {e}\n")
        sys.exit(1)

    combined = (proc.stdout or "") + "\n" + (proc.stderr or "")
    url = _extract_url(combined)
    if not url:
        sys.stderr.write(
            "ERROR: no image URL returned by higgsfield.\n"
            f"--- output ---\n{combined[-1500:]}\n"
        )
        sys.exit(1)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = _output_dir() / f"cover_{prompt_key}_{ts}.jpg"
    dl = subprocess.run(["curl", "-fsSL", url, "-o", str(out_path)],
                        capture_output=True, text=True)
    if dl.returncode != 0 or not out_path.exists():
        sys.stderr.write(f"ERROR: failed to download cover from {url}\n{dl.stderr}\n")
        sys.exit(1)

    # ONLY the path goes to stdout.
    print(str(out_path))
    return str(out_path)


def main():
    args = sys.argv[1:]
    if args and args[0] in ("--list", "-l"):
        for key in PROMPTS:
            print(key)
        return
    if args and args[0] in ("--help", "-h"):
        print(__doc__)
        return
    key = args[0] if args else None
    generate_cover(key)


if __name__ == "__main__":
    main()
