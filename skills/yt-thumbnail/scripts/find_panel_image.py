"""
Find or generate a representative image for a Style B panel.

Priority:
  1. Company logo file (exact or fuzzy match)
  2. Playwright screenshot of the tool's website
  3. Gemini-generated representative image

Usage:
    python3 find_panel_image.py --tool "n8n" --context "complex automation workflow" --output /tmp/old_panel.jpg
    python3 find_panel_image.py --tool "Claude Code" --context "AI coding assistant" --output /tmp/new_panel.jpg
"""

import argparse, base64, json, os, re, sys, time
import requests
from pathlib import Path
from dotenv import load_dotenv

LOGOS_DIR = Path(os.path.expanduser(os.getenv("YT_THUMBNAIL_LOGOS_DIR", "~/thumbnail-logos")))
MODEL = os.getenv("YT_THUMBNAIL_MODEL", "gemini-3.1-flash-image-preview")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

TOOL_URLS = {
    "n8n": "https://n8n.io",
    "make": "https://make.com",
    "zapier": "https://zapier.com",
    "notion": "https://notion.so",
    "airtable": "https://airtable.com",
    "claude": "https://claude.ai",
    "chatgpt": "https://chat.openai.com",
    "gemini": "https://gemini.google.com",
    "elevenlabs": "https://elevenlabs.io",
    "firecrawl": "https://firecrawl.dev",
    "apify": "https://apify.com",
    "reddit": "https://reddit.com",
    "linkedin": "https://linkedin.com",
    "instagram": "https://instagram.com",
}


def load_api_key():
    # Loads a local .env if present (searches the current directory upward), then the environment.
    load_dotenv(override=True)
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        sys.exit("ERROR: GOOGLE_API_KEY not set. Add it to your environment or a .env file.")
    return key


def find_logo(tool_name: str) -> Path | None:
    """Fuzzy match tool name to a logo file."""
    name = tool_name.lower().replace(" ", "").replace("-", "").replace("_", "")
    for logo in LOGOS_DIR.glob("*.png"):
        stem = logo.stem.lower().replace(" ", "").replace("-", "").replace("_", "")
        if name in stem or stem in name:
            print(f"Logo match: {logo.name}", file=sys.stderr)
            return logo
    return None


def screenshot_website(tool_name: str, output_path: Path) -> bool:
    """Try to screenshot the tool's website via Playwright MCP (if available)."""
    url = None
    name_lower = tool_name.lower()
    for key, val in TOOL_URLS.items():
        if key in name_lower or name_lower in key:
            url = val
            break

    if not url:
        print(f"No URL known for '{tool_name}', skipping screenshot", file=sys.stderr)
        return False

    # Try to use playwright via subprocess if available
    script = f"""
import asyncio
try:
    from playwright.async_api import async_playwright
    async def run():
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={{"width": 1280, "height": 720}})
            await page.goto("{url}", wait_until="networkidle", timeout=15000)
            await page.screenshot(path="{output_path}", full_page=False)
            await browser.close()
            return True
    result = asyncio.run(run())
    print("screenshot_ok")
except Exception as e:
    print(f"screenshot_failed: {{e}}")
"""
    import subprocess
    result = subprocess.run(["python3", "-c", script],
                            capture_output=True, text=True, timeout=30)
    if "screenshot_ok" in result.stdout and Path(output_path).exists():
        print(f"Screenshot saved: {output_path}", file=sys.stderr)
        return True
    print(f"Playwright unavailable: {result.stdout.strip()}", file=sys.stderr)
    return False


def generate_representative(tool_name: str, context: str, output_path: Path, api_key: str) -> bool:
    """Generate a representative image with Gemini."""
    prompt = (
        f"A clean, professional screenshot-style image representing '{tool_name}'. "
        f"Context: {context}. "
        f"Style: realistic UI mockup or interface screenshot, dark or light theme appropriate for the tool, "
        f"showing the tool in action. No text overlays or labels. High resolution, 16:9 landscape format. "
        f"Make it immediately recognizable as '{tool_name}'."
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }

    print(f"Generating image for '{tool_name}'...", file=sys.stderr)
    r = requests.post(API_URL,
                      headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
                      json=payload, timeout=120)

    if r.status_code != 200:
        print(f"Gemini error {r.status_code}: {r.text[:200]}", file=sys.stderr)
        return False

    for candidate in r.json().get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "inlineData" in part:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(base64.b64decode(part["inlineData"]["data"]))
                print(f"Generated: {output_path}", file=sys.stderr)
                return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", required=True, help="Tool or concept name (e.g. 'n8n', 'Claude Code')")
    parser.add_argument("--context", default="", help="Brief description for image generation fallback")
    parser.add_argument("--output", required=True, help="Output image path")
    parser.add_argument("--force-generate", action="store_true", help="Skip logo/screenshot, always generate")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    if not args.force_generate:
        # 1. Try logo
        logo = find_logo(args.tool)
        if logo:
            import shutil
            shutil.copy(logo, output)
            print(str(output))
            return

        # 2. Try screenshot
        if screenshot_website(args.tool, output):
            print(str(output))
            return

    # 3. Generate with Gemini
    api_key = load_api_key()
    if generate_representative(args.tool, args.context, output, api_key):
        print(str(output))
        return

    sys.exit(f"ERROR: Could not find or generate image for '{args.tool}'")


if __name__ == "__main__":
    main()
