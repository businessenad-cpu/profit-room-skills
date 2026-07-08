"""
Shippable image backend for the carousel-creator skill.

Wraps the Higgsfield CLI so the rest of the skill has a stable interface and
no dependency on any private/internal image-generation modules.

Public API:
    generate_image(prompt, reference_paths=None, aspect_ratio="4:5") -> str
        Generate an image and return a URL (or local path) to it.
    upload_reference(path) -> str
        "Host" a local file. With the CLI backend there is no external host,
        so this simply returns the absolute local path. Swap this out if you
        later add a real upload target (S3, your own CDN, etc.).

Both functions import cleanly even if the `higgsfield` CLI is not installed —
they only fail (with a clear message) when actually called.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path


class ImageBackendError(RuntimeError):
    """Raised when image generation cannot be completed."""


def _find_higgsfield():
    exe = shutil.which("higgsfield")
    if exe:
        return exe
    fallback = Path.home() / ".npm-global" / "bin" / "higgsfield"
    if fallback.exists():
        return str(fallback)
    return None


def _extract_url(text):
    urls = re.findall(r"https?://[^\s'\"]+", text or "")
    return urls[-1] if urls else None


def generate_image(prompt, reference_paths=None, aspect_ratio="4:5"):
    """
    Generate an image via Higgsfield (nano_banana_2) and return its URL.

    Args:
        prompt: text prompt.
        reference_paths: optional list of local image paths passed as --image
            references (only the first is used — nano_banana_2 takes one).
        aspect_ratio: e.g. "4:5", "1:1", "16:9".

    Returns:
        str: a URL to the generated image.

    Raises:
        ImageBackendError: if the CLI is missing or generation fails.
    """
    exe = _find_higgsfield()
    if not exe:
        raise ImageBackendError(
            "the 'higgsfield' CLI was not found. Install/authenticate it "
            "(npm i -g higgsfield), or use the alternating-solid render path "
            "(render_solid.py) which needs no image generation."
        )

    cmd = [exe, "generate", "create", "nano_banana_2",
           "--aspect_ratio", aspect_ratio, "--prompt", prompt, "--wait"]
    if reference_paths:
        ref = os.path.expanduser(str(reference_paths[0]))
        if Path(ref).exists():
            cmd += ["--image", ref]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    except Exception as e:  # noqa: BLE001
        raise ImageBackendError(f"higgsfield invocation failed: {e}") from e

    combined = (proc.stdout or "") + "\n" + (proc.stderr or "")
    url = _extract_url(combined)
    if not url:
        raise ImageBackendError(
            "no image URL returned by higgsfield:\n" + combined[-1000:]
        )
    return url


def upload_reference(path):
    """
    Return a hosted URL for a local file.

    The CLI backend has no external host, so this returns the absolute local
    path. Replace the body with a real upload if you want permanent URLs.
    """
    return str(Path(os.path.expanduser(str(path))).resolve())
