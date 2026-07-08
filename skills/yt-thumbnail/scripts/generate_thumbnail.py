"""
Generate a YouTube thumbnail using the Google GenAI SDK.

Usage:
    python3 generate_thumbnail.py --prompt-file /path/to/prompt.txt --output /path/to/out.jpg
    python3 generate_thumbnail.py --prompt "..." --output /path/to/out.jpg --logos Claude LinkedIn

Your reference photo is always the first image in contents.
Pass --logos to inject additional brand logo references for accurate reproduction.
Outputs native 16:9 at 4K resolution via the SDK's response_format config.

Configure via environment variables (or a .env file in the current directory):
    GOOGLE_API_KEY            — required, your Google GenAI API key
    YT_THUMBNAIL_REFERENCE    — path to your face/reference photo (default ~/thumbnail-reference.png)
    YT_THUMBNAIL_LOGOS_DIR    — folder of tool/company logo PNGs (default ~/thumbnail-logos)
    YT_THUMBNAIL_MODEL        — image model id (default gemini-3.1-flash-image-preview)
"""

import argparse, os, sys
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
from google import genai
from google.genai import types

REFERENCE_IMAGE = Path(os.path.expanduser(os.getenv("YT_THUMBNAIL_REFERENCE", "~/thumbnail-reference.png")))
LOGOS_DIR = Path(os.path.expanduser(os.getenv("YT_THUMBNAIL_LOGOS_DIR", "~/thumbnail-logos")))
MODEL = os.getenv("YT_THUMBNAIL_MODEL", "gemini-3.1-flash-image-preview")


def load_api_key():
    # Loads a local .env if present (searches the current directory upward), then the environment.
    load_dotenv(override=True)
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        sys.exit("ERROR: GOOGLE_API_KEY not set. Add it to your environment or a .env file.")
    return key


def resolve_logo(name: str) -> Path | None:
    """Find a logo file — exact stem match wins over partial."""
    needle = name.lower().replace(" ", "").replace("-", "").replace("_", "")
    exact = partial = None
    for logo in sorted(LOGOS_DIR.glob("*.png")):
        stem = logo.stem.lower().replace(" ", "").replace("-", "").replace("_", "")
        if stem == needle:
            exact = logo
            break
        if (needle in stem or stem in needle) and partial is None:
            partial = logo
    return exact or partial


def generate(prompt: str, output_path: Path, api_key: str, logo_names: list[str], ref_images: list[str] | None = None):
    client = genai.Client(api_key=api_key)

    # All images go first, then a single text prompt referencing them by number.
    # Gemini reliably reproduces multi-image references when called out as "Image 1", "Image 2" etc.
    images = []
    image_labels = []

    # Image 1: your reference photo (always first)
    if not REFERENCE_IMAGE.exists():
        sys.exit(
            f"ERROR: reference photo not found at {REFERENCE_IMAGE}. "
            "Set YT_THUMBNAIL_REFERENCE to your face/reference photo path."
        )
    images.append(Image.open(REFERENCE_IMAGE))
    image_labels.append(
        "Image 1 is the reference photo of the person to portray. "
        "Match this exact likeness — hair, facial hair, eyewear, and clothing."
    )

    # Images 2+: logo references
    for name in logo_names:
        path = resolve_logo(name)
        if path:
            images.append(Image.open(path))
            idx = len(images)
            image_labels.append(
                f"Image {idx} is the '{name}' logo. "
                f"Reproduce this exact logo mark on the corresponding element in the thumbnail — "
                f"copy it precisely, do not invent or substitute a different symbol."
            )
            print(f"Image {idx}: {path.name}", file=sys.stderr)
        else:
            print(f"WARNING: No logo file found for '{name}' — relying on prompt description only", file=sys.stderr)

    # Additional arbitrary reference images (e.g. a real dashboard screenshot to reproduce inside an app window)
    for ref in (ref_images or []):
        p = Path(ref)
        if p.exists():
            images.append(Image.open(p))
            idx = len(images)
            image_labels.append(
                f"Image {idx} is a reference screenshot/interface. "
                f"Reproduce its layout, colors, and on-screen text as faithfully as possible where the prompt calls for it."
            )
            print(f"Image {idx}: {p.name}", file=sys.stderr)
        else:
            print(f"WARNING: ref image not found: {ref}", file=sys.stderr)

    # Single unified prompt: image index descriptions first, then instructions
    reference_block = "\n".join(image_labels)
    full_prompt = f"{reference_block}\n\nTHUMBNAIL INSTRUCTIONS:\n{prompt}"

    contents = images + [full_prompt]

    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio="16:9",
                image_size="4K",
            ),
        ),
    )

    # Extract and save the image
    for part in response.parts:
        img = part.as_image() if hasattr(part, "as_image") else None
        if img:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(str(output_path))
            print(f"Saved: {output_path}")
            return output_path

    # Fallback: check for inline_data in raw parts
    for part in response.parts:
        if hasattr(part, "inline_data") and part.inline_data:
            import base64
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(part.inline_data.data))
            print(f"Saved: {output_path}")
            return output_path
        if part.text:
            print(f"Model text: {part.text}", file=sys.stderr)

    sys.exit("ERROR: No image in response. Check prompt or API quota.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", help="Prompt text directly")
    parser.add_argument("--prompt-file", help="Path to file containing the prompt")
    parser.add_argument("--output", required=True, help="Output image path (.jpg or .png)")
    parser.add_argument("--logos", nargs="*", default=[],
                        help="Logo names to inject as references (e.g. Claude LinkedIn Notion)")
    parser.add_argument("--ref-image", nargs="*", default=[], dest="ref_images",
                        help="Arbitrary reference image paths to inject (e.g. a dashboard screenshot)")
    args = parser.parse_args()

    if args.prompt_file:
        prompt = Path(args.prompt_file).read_text()
    elif args.prompt:
        prompt = args.prompt
    else:
        sys.exit("ERROR: Provide --prompt or --prompt-file")

    api_key = load_api_key()
    output_path = Path(args.output)
    generate(prompt, output_path, api_key, args.logos or [], args.ref_images or [])


if __name__ == "__main__":
    main()
