#!/usr/bin/env python3
"""Publish an HTML guide to Gumroad as a pay-what-you-want digital product.

Usage:
  python3 gumroad-publish.py \
    --file ~/content/2026-01-01-slug/guide.html \
    --title "My Framework — Free Resource Guide" \
    --description "Step-by-step companion guide to the YouTube video." \
    --thumbnail "https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg"

Prerequisites:
  Run once to save a browser session (nothing is hardcoded):
    python3 gumroad-save-session.py

Optional env var:
  GUMROAD_SUBDOMAIN   your "<name>.gumroad.com" handle, used only to print the
                      public product URL. If unset, the URL is printed with a
                      placeholder you can swap.

Requires playwright:
  pip install playwright && playwright install chromium
"""

import argparse
import os
import ssl
import sys
import time
import urllib.request
from pathlib import Path

GUMROAD_SUBDOMAIN = os.environ.get("GUMROAD_SUBDOMAIN", "YOUR-SUBDOMAIN")


def load_env():
    """Optionally load env vars from ~/.claude/.env if present. No hardcoded paths."""
    env_path = Path.home() / ".claude" / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True, help="Path to HTML guide file to upload")
    p.add_argument("--title", required=True, help="Product title")
    p.add_argument("--description", default=None, help="Product description (plain text, use \\n for newlines)")
    p.add_argument("--description-file", default=None, help="Path to file containing product description")
    p.add_argument("--thumbnail", default=None, help="Thumbnail URL to use as cover image")
    p.add_argument("--min-price", default="0", help="Minimum price USD (default: 0)")
    p.add_argument("--suggested-price", default="9", help="Suggested price USD (default: 9)")
    p.add_argument("--headless", action="store_true", help="Run headless")
    return p.parse_args()


def download_thumbnail(url: str, dest: Path):
    """Download thumbnail image to a local file."""
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=15) as r, open(dest, "wb") as f:
            f.write(r.read())
        return True
    except Exception as e:
        print(f"Warning: Could not download thumbnail: {e}", file=sys.stderr)
        return False


def make_square(src: Path, dest: Path) -> bool:
    """Center-crop image to square (Gumroad thumbnail requires square)."""
    try:
        from PIL import Image
        with Image.open(src) as img:
            w, h = img.size
            size = min(w, h)
            left = (w - size) // 2
            top = (h - size) // 2
            cropped = img.crop((left, top, left + size, top + size))
            cropped.save(dest, "JPEG", quality=95)
        return True
    except ImportError:
        print("Warning: Pillow not installed — run: pip install Pillow", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Warning: Could not crop thumbnail to square: {e}", file=sys.stderr)
        return False


def wait_for_upload(page, timeout=30):
    """Wait until an upload progress indicator disappears."""
    try:
        page.wait_for_selector('[aria-label*="upload"], [class*="progress"], [class*="uploading"]',
                               state="hidden", timeout=timeout * 1000)
    except Exception:
        pass
    time.sleep(1)


def main():
    load_env()
    args = parse_args()

    file_path = Path(args.file).expanduser().resolve()
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    # Resolve description
    if args.description_file:
        desc_path = Path(args.description_file).expanduser().resolve()
        if not desc_path.exists():
            print(f"Error: Description file not found: {desc_path}", file=sys.stderr)
            sys.exit(1)
        description = desc_path.read_text()
    elif args.description:
        description = args.description.replace("\\n", "\n")
    else:
        description = "Step-by-step companion guide to the YouTube video. Watch the video, follow the guide."

    cookies_path = Path(__file__).resolve().parent.parent / ".gumroad-session.json"
    if not cookies_path.exists():
        print(f"Error: No saved session. Run gumroad-save-session.py first.", file=sys.stderr)
        sys.exit(1)

    # Download thumbnail: keep 16:9 for Cover, make square crop for Thumbnail
    cover_path = None
    thumbnail_path = None
    if args.thumbnail:
        raw_path = Path("/tmp/gumroad-cover-raw.jpg")
        print(f"Downloading thumbnail...")
        if download_thumbnail(args.thumbnail, raw_path):
            cover_path = raw_path  # 16:9 for Cover section
            square_path = Path("/tmp/gumroad-thumbnail-square.jpg")
            if make_square(raw_path, square_path):
                thumbnail_path = square_path  # square for Thumbnail section
                print("Thumbnail downloaded (16:9 cover + square thumbnail).")
            else:
                print("Thumbnail downloaded (16:9 cover only — Pillow not available for square crop).")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Run: pip install playwright && playwright install chromium", file=sys.stderr)
        sys.exit(1)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=args.headless, slow_mo=200)
        context = browser.new_context(storage_state=str(cookies_path))
        page = context.new_page()

        # ── Verify session ────────────────────────────────────────────────
        print("Verifying session...")
        page.goto("https://gumroad.com/dashboard", wait_until="domcontentloaded", timeout=30000)
        time.sleep(2)
        if "login" in page.url:
            print("Error: Session expired. Run gumroad-save-session.py to refresh.", file=sys.stderr)
            sys.exit(1)
        print("Session valid.")

        # ── Step 1: Create product ────────────────────────────────────────
        print(f"Creating product: {args.title}")
        page.goto("https://gumroad.com/products/new", wait_until="domcontentloaded", timeout=30000)
        time.sleep(2)

        # Select Digital product type (may already be selected)
        digital_btn = page.locator('button:has(h4:text("Digital product"))')
        if digital_btn.count() > 0:
            digital_btn.first.click()
            time.sleep(0.5)

        # Wait for name input (no longer has placeholder — match by id pattern)
        page.wait_for_selector('input[id*="name"]', timeout=15000)

        # Fill name and price
        page.locator('input[id*="name"]').first.fill(args.title)
        price_input = page.locator('input[id*="price"]')
        if price_input.count() > 0:
            price_input.first.fill("0")
        time.sleep(0.3)

        # Click Next: Customize — wait for button to be ready
        print("Moving to customize page...")
        next_btn = page.locator('button:has-text("Next: Customize")').first
        next_btn.wait_for(state="visible", timeout=10000)
        next_btn.click()

        # SPA navigation — wait for the edit UI to appear (URL doesn't change)
        page.wait_for_selector('text=Save and continue', timeout=20000)
        time.sleep(1)

        # Extract product ID (slug) from the URL field on the edit page.
        # The URL field shows "<subdomain>.gumroad.com/l/<slug>" — slug is the short editable part.
        product_id = page.evaluate("""
            () => {
                const inputs = Array.from(document.querySelectorAll('input'));
                // The slug input is the short one (6-12 chars, no spaces, after the gumroad URL prefix)
                const slugInput = inputs.find(i =>
                    i.value && i.value.length >= 4 && i.value.length <= 20 &&
                    !i.value.includes(' ') && !i.value.includes('@') &&
                    i.id && !i.id.includes('name') && !i.id.includes('price')
                );
                return slugInput ? slugInput.value : null;
            }
        """)
        if not product_id:
            # Fallback: extract from the current URL if it changed
            product_id = page.url.split("/products/")[-1].split("/")[0] if "/products/" in page.url else "unknown"
        print(f"Product created: {product_id}  →  https://{GUMROAD_SUBDOMAIN}.gumroad.com/l/{product_id}")

        # ── Step 2: Product tab — description ────────────────────────────
        print("Adding description...")
        desc_editor = page.locator('div[aria-label="Description"]').first
        if desc_editor.is_visible():
            desc_editor.click()
            time.sleep(0.3)
            lines = description.split("\n")
            in_list = False
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue  # skip blank lines — no extra Enter presses
                if stripped == "---":
                    # Divider — always exits list first
                    if in_list:
                        page.keyboard.press("Enter")
                        in_list = False
                    page.keyboard.type("---")
                    page.keyboard.press("Enter")
                elif stripped.startswith("**") and stripped.endswith("**") and len(stripped) > 4:
                    # Bold section header — exits list, applies Cmd+B (macOS)
                    if in_list:
                        page.keyboard.press("Enter")
                        in_list = False
                    page.keyboard.press("Meta+b")
                    page.keyboard.type(stripped[2:-2])
                    page.keyboard.press("Meta+b")
                    page.keyboard.press("Enter")
                elif stripped.startswith("- "):
                    # First bullet in a new list
                    if not in_list:
                        page.keyboard.type(stripped)  # "- text" triggers list mode
                        in_list = True
                    else:
                        page.keyboard.type(stripped[2:])  # already in list, skip "- "
                    page.keyboard.press("Enter")
                else:
                    if in_list:
                        # Continuation bullet — stay in list, just type content
                        page.keyboard.type(stripped)
                        page.keyboard.press("Enter")
                    else:
                        # Regular paragraph
                        page.keyboard.type(stripped)
                        page.keyboard.press("Enter")
            time.sleep(0.3)

        # ── Step 3: Product tab — cover (16:9) + thumbnail (square) ─────────
        if cover_path and cover_path.exists():
            print("Uploading cover image (16:9)...")

            # Scroll to bottom to reveal Cover/Thumbnail sections
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1.5)

            cover_uploaded = False

            # Cover upload flow: "Upload images or videos" button → sub-menu →
            # <label role="tab"> "Computer files" → file chooser
            upload_btns = page.locator('button:has-text("Upload images or videos")').all()

            for btn in reversed(upload_btns):
                try:
                    btn.scroll_into_view_if_needed()
                    time.sleep(0.5)
                    btn.click()
                    time.sleep(1.5)

                    cf_label = page.locator('label:has-text("Computer files"), [role="tab"]:has-text("Computer files")').first
                    if cf_label.count() > 0 and cf_label.is_visible():
                        with page.expect_file_chooser(timeout=5000) as fc_info:
                            cf_label.click()
                        fc_info.value.set_files(str(cover_path))
                        time.sleep(3)
                        print("Cover image uploaded.")
                        cover_uploaded = True
                        break
                    else:
                        page.keyboard.press("Escape")
                        time.sleep(0.3)
                except Exception as e:
                    print(f"  Cover upload attempt failed: {e}")
                    page.keyboard.press("Escape")
                    time.sleep(0.3)

            if not cover_uploaded:
                print("Warning: Could not upload cover image.")

        # ── Step 3b: Product tab — thumbnail (square) ────────────────────
        if thumbnail_path and thumbnail_path.exists():
            print("Uploading thumbnail (square)...")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)

            thumb_uploaded = False

            # Debug: list all "Upload" buttons and labels with file inputs on page
            all_upload_btns = page.locator('button:has-text("Upload")').all()
            btn_texts = []
            for b in all_upload_btns:
                try:
                    btn_texts.append(b.inner_text().strip())
                except Exception:
                    pass
            print(f"  Upload buttons visible: {btn_texts}")

            # Try: find a second "Upload images or videos" button (Thumbnail section)
            # or any other button that can open a file chooser for the thumbnail
            upload_btns = page.locator('button:has-text("Upload images or videos")').all()
            for btn in reversed(upload_btns):
                try:
                    btn.scroll_into_view_if_needed()
                    time.sleep(0.5)
                    btn.click()
                    time.sleep(1.5)
                    cf_label = page.locator('label:has-text("Computer files"), [role="tab"]:has-text("Computer files")').first
                    if cf_label.count() > 0 and cf_label.is_visible():
                        with page.expect_file_chooser(timeout=5000) as fc_info:
                            cf_label.click()
                        fc_info.value.set_files(str(thumbnail_path))
                        time.sleep(3)
                        print("Thumbnail uploaded.")
                        thumb_uploaded = True
                        break
                    else:
                        page.keyboard.press("Escape")
                        time.sleep(0.3)
                except Exception as e:
                    print(f"  Thumbnail upload attempt failed: {e}")
                    page.keyboard.press("Escape")
                    time.sleep(0.3)

            if not thumb_uploaded:
                # Fallback: click any label wrapping a file input that hasn't been used
                cover_labels = page.locator('label:has(input[type="file"])').all()
                print(f"  Labels with file input: {len(cover_labels)}")
                for lbl in cover_labels:
                    try:
                        lbl_text = lbl.inner_text().strip()
                        print(f"    label text: {lbl_text!r}")
                        lbl.scroll_into_view_if_needed()
                        time.sleep(0.3)
                        with page.expect_file_chooser(timeout=5000) as fc_info:
                            lbl.click()
                        fc_info.value.set_files(str(thumbnail_path))
                        time.sleep(3)
                        print("Thumbnail uploaded (label fallback).")
                        thumb_uploaded = True
                        break
                    except Exception as e:
                        print(f"    label click failed: {e}")

            if not thumb_uploaded:
                print("Warning: Could not upload thumbnail.")

        # ── Step 4: Product tab — PWYW pricing ───────────────────────────
        print("Setting pay-what-you-want pricing...")

        # Scroll to pricing section
        page.evaluate("""() => {
            const el = document.querySelector('[id*="price-cents"], [id*="minimum"]');
            if (el) el.scrollIntoView({ block: 'center' });
        }""")
        time.sleep(0.5)

        # Find PWYW checkbox — it sits between price-cents and minimum-amount inputs
        pwyw_enabled = page.evaluate("""() => {
            const inputs = Array.from(document.querySelectorAll('input'));
            const priceIdx = inputs.findIndex(i => i.id && i.id.includes('price-cents'));
            const minIdx = inputs.findIndex(i => i.id && i.id.includes('minimum-amount'));
            if (priceIdx === -1 || minIdx === -1) return false;
            // Find checkbox between them
            for (let i = priceIdx + 1; i < minIdx; i++) {
                if (inputs[i].type === 'checkbox' && !inputs[i].checked) {
                    inputs[i].click();
                    return true;
                }
            }
            // If already checked, we're good
            for (let i = priceIdx + 1; i < minIdx; i++) {
                if (inputs[i].type === 'checkbox' && inputs[i].checked) return true;
            }
            return false;
        }""")
        time.sleep(0.5)

        if pwyw_enabled:
            print("PWYW enabled.")
            # Set minimum price via JS (input may be disabled but still writable)
            if args.min_price != "0":
                page.evaluate(f"""() => {{
                    const el = document.querySelector('[id*="minimum-amount"]');
                    if (el) {{
                        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                        nativeInputValueSetter.call(el, '{args.min_price}');
                        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    }}
                }}""")

            # Set suggested price
            suggested_input = page.locator('[id*="suggested-price-cents"]').first
            if suggested_input.is_visible():
                suggested_input.fill(args.suggested_price)
                print(f"Suggested price set to ${args.suggested_price}.")
        else:
            print("PWYW toggle not found — product stays at $0 (free). Customers can still pay more via tip.")

        # ── Step 5: Save Product tab ──────────────────────────────────────
        print("Saving product details...")
        save_btn = page.locator('button:has-text("Save and continue")').first
        if save_btn.is_visible():
            save_btn.click()
            time.sleep(3)
        else:
            # Try alternate save button text
            page.locator('button:has-text("Save changes")').first.click()
            time.sleep(3)

        # ── Step 6: Content tab — upload file ────────────────────────────
        print("Switching to Content tab...")
        page.locator('a:has-text("Content"), [role="tab"]:has-text("Content")').first.click()
        time.sleep(2)

        print(f"Uploading guide file: {file_path.name}")
        content_file_input = page.locator('input[type="file"]').first
        content_file_input.set_input_files(str(file_path))

        # Wait for upload — poll until the file name appears or spinner goes away
        print("Waiting for upload to complete...")
        for _ in range(20):
            time.sleep(1.5)
            # Check if file name appears anywhere on page
            content = page.content()
            if file_path.name in content or file_path.stem in content:
                print("Upload confirmed.")
                break
        else:
            print("Warning: Could not confirm upload completed — continuing anyway.")

        time.sleep(1)

        # ── Step 7: Publish ───────────────────────────────────────────────
        print("Publishing...")
        publish_btn = page.locator('button:has-text("Publish and continue")').first
        if publish_btn.is_visible():
            publish_btn.click()
            time.sleep(4)
        else:
            # Check if already published / try "Publish" button
            alt_publish = page.locator('button:has-text("Publish")').first
            if alt_publish.is_visible():
                alt_publish.click()
                time.sleep(4)
            else:
                print("Warning: No publish button found — product may already be published.", file=sys.stderr)

        # ── Step 8: Get public URL ────────────────────────────────────────
        public_url = f"https://{GUMROAD_SUBDOMAIN}.gumroad.com/l/{product_id}"
        print(f"\n✓ Done!")
        print(f"  Product ID:  {product_id}")
        print(f"  Public URL:  {public_url}")
        print(f"  Edit URL:    https://gumroad.com/products/{product_id}/edit")

        # Save updated session
        context.storage_state(path=str(cookies_path))
        browser.close()
        return public_url


if __name__ == "__main__":
    main()
