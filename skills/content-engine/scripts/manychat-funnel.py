#!/usr/bin/env python3
"""
Generic ManyChat comment-to-DM funnel creator.

Duplicates a ManyChat template flow, renames it, and fills in your keyword,
opening DM, delivery DM, follow-up DM, and up to two link buttons. Opens a
visible browser — log in with your ManyChat account when prompted (a persistent
profile means you only log in once).

All values are passed as flags — nothing is hardcoded.

Env vars:
  MANYCHAT_ACCOUNT_ID   your ManyChat account/page id (the "fbNNNNNNN" segment
                        in your ManyChat CMS URL). Required.

Usage:
  python3 manychat-funnel.py \
    --keyword MANGO \
    --flow-name "MANGO - My Free Guide - 01/01/2026" \
    --opening-dm "Want the free guide? Tap below 👇" \
    --opening-btn "Send me the link" \
    --link-dm "Here you go 👇" \
    --link1-label "Watch the video" \
    --link1-url "https://www.youtube.com/watch?v=VIDEO_ID" \
    --link2-label "Free guide" \
    --link2-url "https://YOUR-SUBDOMAIN.gumroad.com/l/xxxx" \
    --followup-dm "Did you grab it? Link's still above 👆" \
    --template-name "LEADMAGNET TEMPLATE"

--link2-* is optional (omit both for a single-link funnel, e.g. discussion videos).
"""
import argparse
import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

# Persistent browser profile — log in once, future runs are automatic.
# Matches the .gitignore "**/.chrome-profile/" rule so it is never committed.
PROFILE_DIR = Path(__file__).resolve().parent.parent / ".chrome-profile"


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--keyword", required=True)
    p.add_argument("--flow-name", required=True)
    p.add_argument("--opening-dm", required=True)
    p.add_argument("--opening-btn", default="Send me the link")
    p.add_argument("--link-dm", default="Here you go 👇")
    p.add_argument("--link1-label", required=True)
    p.add_argument("--link1-url", required=True)
    p.add_argument("--link2-label", default=None)
    p.add_argument("--link2-url", default=None)
    p.add_argument("--followup-dm", default="Did you grab it? Link's still above 👆")
    p.add_argument("--template-name", default="LEADMAGNET TEMPLATE",
                   help="Name of the ManyChat flow to duplicate as the starting point")
    return p.parse_args()


def wait_for_captcha(page):
    """If a CAPTCHA appeared, wait for the user to solve it."""
    if "confirm you are human" in page.content().lower() or "captcha" in page.url.lower():
        print("\n⚠  CAPTCHA detected — please solve it in the browser window.")
        print("   Waiting up to 2 minutes...\n")
        try:
            page.wait_for_function(
                "() => !document.body.innerText.toLowerCase().includes('confirm you are human')",
                timeout=120000
            )
            time.sleep(2)
            print("✓ CAPTCHA solved.\n")
        except Exception:
            print("⚠  CAPTCHA wait timed out — continuing anyway.")


def wait_for_login(page):
    """Watch the browser — user logs in visually, we detect when they're done."""
    if "/signin" in page.url or "/login" in page.url or "accounts.google" in page.url:
        print("\n⚠  Sign in to ManyChat in the browser window. Waiting up to 5 minutes...")
        try:
            page.wait_for_function(
                "() => !window.location.href.includes('/signin') && "
                "!window.location.href.includes('/login') && "
                "!window.location.href.includes('accounts.google')",
                timeout=300000
            )
            time.sleep(2)
            print("✓ Logged in.\n")
        except Exception:
            print("✗ Login timed out.")
            return False
    return True


def ensure_on_flows(page):
    """If ManyChat redirected to sign-in, watch the browser and wait for re-login."""
    if "/signin" in page.url or "/login" in page.url or "accounts.google" in page.url:
        print("\n⚠  ManyChat kicked you out — log back in via the browser window. Waiting...")
        try:
            page.wait_for_function(
                "() => !window.location.href.includes('/signin') && "
                "!window.location.href.includes('/login') && "
                "!window.location.href.includes('accounts.google')",
                timeout=300000
            )
            time.sleep(2)
            print("✓ Back in. Resuming...\n")
        except Exception:
            print("✗ Re-auth timed out.")
            return False
    return True


def dismiss_overlays(page):
    """Remove Braze in-app message overlays and any ManyChat interstitial popups."""
    page.evaluate("""
        () => {
            document.querySelectorAll('.ab-iam-root, .ab-in-app-message').forEach(el => el.remove());
            const btns = Array.from(document.querySelectorAll('button'));
            const dismiss = btns.find(b =>
                b.textContent.includes("Maybe Later") ||
                b.textContent.includes("Yes, That") ||
                b.textContent.includes("Dismiss") ||
                b.textContent.includes("Got it")
            );
            if (dismiss) dismiss.click();
        }
    """)
    time.sleep(0.5)


def set_react_value(page, index, value):
    """Set value on a React-controlled input by its index among inputs/textareas."""
    page.evaluate(f"""
        () => {{
            function setVal(el, value) {{
                const proto = el.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
                Object.getOwnPropertyDescriptor(proto, 'value').set.call(el, value);
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            const inputs = Array.from(document.querySelectorAll('input, textarea'));
            if (inputs[{index}]) setVal(inputs[{index}], {repr(value)});
        }}
    """)


def find_row_js(text):
    """JS snippet: find a CMS/automation row by its visible text and open its menu."""
    return """
        () => {
            function findRowByText(text) {
                for (const article of document.querySelectorAll('article')) {
                    const h = article.querySelector('h1');
                    if (h && h.textContent.includes(text)) return article;
                }
                for (const el of document.querySelectorAll('*')) {
                    if (el.children.length === 0 && el.textContent.trim().includes(text)) {
                        let node = el.parentElement;
                        for (let i = 0; i < 8; i++) {
                            if (!node) break;
                            if (node.querySelectorAll('button').length > 0) return node;
                            node = node.parentElement;
                        }
                    }
                }
                return null;
            }
            const row = findRowByText(%s);
            if (row) {
                row.scrollIntoView({ behavior: 'instant', block: 'center' });
                row.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
                row.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
                const btns = row.querySelectorAll('button');
                if (btns.length) btns[btns.length - 1].click();
            }
        }
    """ % repr(text)


def main():
    args = parse_args()

    account_id = os.environ.get("MANYCHAT_ACCOUNT_ID")
    if not account_id:
        print("Error: set MANYCHAT_ACCOUNT_ID (the 'fbNNNNNNN' segment from your ManyChat CMS URL).")
        raise SystemExit(1)

    flows_url = f"https://app.manychat.com/{account_id}/cms?path=/&field=modified&order=desc"

    links = [("link1", args.link1_label, args.link1_url)]
    if args.link2_label and args.link2_url:
        links.append(("link2", args.link2_label, args.link2_url))

    with sync_playwright() as p:
        PROFILE_DIR.mkdir(parents=True, exist_ok=True)
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=False,
            slow_mo=200,
        )
        page = ctx.new_page()

        # ── Step 1: Login check ─────────────────────────────────────────────
        print("Step 1: Checking login...")
        page.goto("https://app.manychat.com", wait_until="domcontentloaded", timeout=30000)
        time.sleep(2)
        if not wait_for_login(page):
            ctx.close()
            raise SystemExit(1)
        print("✓ Using persistent profile — no session save needed.")

        # ── Step 2: Navigate to Flows ───────────────────────────────────────
        print("Step 2: Navigating to Flows...")
        page.goto(flows_url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)
        wait_for_captcha(page)
        dismiss_overlays(page)

        # ── Step 3: Duplicate the template flow ────────────────────────────
        print(f"Step 3: Duplicating template '{args.template_name}'...")
        page.evaluate(find_row_js(args.template_name))
        time.sleep(1)
        page.evaluate("""
            () => {
                const dup = Array.from(document.querySelectorAll('button, li'))
                    .find(el => el.textContent.trim() === 'Duplicate');
                if (dup) dup.click();
            }
        """)
        time.sleep(3)
        wait_for_captcha(page)
        if not ensure_on_flows(page):
            ctx.close()
            raise SystemExit(1)

        # ── Step 4: Rename the new duplicate ────────────────────────────────
        print("Step 4: Renaming flow...")
        # The new duplicate appears at top with the template name (often "... copy")
        page.evaluate(find_row_js(args.template_name[:16]))
        time.sleep(1)
        page.evaluate("""
            () => {
                Array.from(document.querySelectorAll('button, li'))
                    .find(el => el.textContent.trim() === 'Rename')?.click();
            }
        """)
        time.sleep(1)
        name_input = page.locator('[data-test-id="name-input"]')
        name_input.click(click_count=3)
        name_input.fill(args.flow_name)
        time.sleep(0.5)
        page.locator('button:has-text("Rename")').last.click()
        time.sleep(2)
        print(f"  → Renamed to: {args.flow_name}")

        # ── Step 5: Open the flow editor ────────────────────────────────────
        print("Step 5: Opening flow editor...")
        flow_url = page.evaluate(f"""
            () => {{
                for (const el of document.querySelectorAll('*')) {{
                    if (el.children.length === 0 && el.textContent.trim() === {repr(args.flow_name)}) {{
                        let node = el;
                        for (let i = 0; i < 8; i++) {{
                            if (!node) break;
                            if (node.tagName === 'A' && node.href) return node.href;
                            const link = node.querySelector && node.querySelector('a[href]');
                            if (link) return link.href;
                            node = node.parentElement;
                        }}
                    }}
                }}
                return null;
            }}
        """)
        if flow_url:
            print(f"  → Navigating to: {flow_url}")
            page.goto(flow_url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(3)
        else:
            print("  → No link found — clicking the flow name to open the editor...")
            page.evaluate(f"""
                () => {{
                    for (const el of document.querySelectorAll('*')) {{
                        if (el.children.length === 0 && el.textContent.trim() === {repr(args.flow_name)}) {{
                            el.click();
                            return;
                        }}
                    }}
                }}
            """)
            time.sleep(3)

        # ── Step 6: Enter edit mode ─────────────────────────────────────────
        print("Step 6: Entering edit mode...")
        edit_btn = page.locator('button:has-text("Edit")').first
        if edit_btn.is_visible():
            edit_btn.click()
            time.sleep(2)
        dismiss_overlays(page)

        # ── Step 7: Fill keyword, opening DM, link DM body, follow-up ──────
        # NOTE: These input indices match the default "LEADMAGNET TEMPLATE" layout.
        # If you duplicate a different template, adjust the indices to match.
        print("Step 7: Filling text fields...")
        set_react_value(page, 4, args.keyword)
        time.sleep(0.3)
        set_react_value(page, 11, args.opening_dm)
        time.sleep(0.3)
        set_react_value(page, 16, args.link_dm)
        time.sleep(0.3)
        set_react_value(page, 18, args.followup_dm)
        time.sleep(0.5)

        # ── Step 8: Fill link buttons ───────────────────────────────────────
        print("Step 8: Filling link buttons...")
        try:
            page.evaluate("() => { const s = document.querySelector('._sidebar_1vex7_19'); if (s) s.scrollTop = 2000; }")
            time.sleep(1)
        except Exception:
            pass

        for label_text, new_label, new_url in links:
            try:
                page.evaluate(f"""
                    () => {{
                        const spans = Array.from(document.querySelectorAll('span.text-ellipsis'));
                        const el = spans.find(s => s.textContent.trim() === {repr(label_text)});
                        if (el) el.closest('[class*="d-flex"]').click();
                    }}
                """)
                time.sleep(1)
                modal = page.locator('[data-test-id="dm-link-modal"]')
                if modal.is_visible():
                    label_field = modal.get_by_role('textbox', name='Button label')
                    label_field.click(click_count=3)
                    label_field.fill(new_label)
                    url_field = modal.get_by_role('textbox', name='Link')
                    url_field.click(click_count=3)
                    url_field.fill(new_url)
                    page.locator('button:has-text("Save")').click()
                    time.sleep(1)
                    print(f"  → {label_text}: '{new_label}' → {new_url}")
                else:
                    print(f"  ⚠ Modal not visible for {label_text}")
            except Exception as e:
                print(f"  ⚠ Error on {label_text}: {e}")

        # ── Step 9: Save and Go Live ────────────────────────────────────────
        print("Step 9: Saving and activating...")
        dismiss_overlays(page)
        update_btn = page.locator('button:has-text("Update"), button:has-text("Save")').first
        if update_btn.is_visible():
            update_btn.click()
            time.sleep(2)

        golive_btn = page.locator('button:has-text("Go Live"), button:has-text("Activate")').first
        if golive_btn.is_visible():
            golive_btn.click()
            time.sleep(2)
            print("  ✓ Flow is LIVE")
        else:
            print("  ⚠ Go Live button not found — may already be live.")

        print(f"\n✓ Done! Flow: {args.flow_name}")
        print(f"  Keyword: {args.keyword}")
        print(f"  Test: comment '{args.keyword}' from another account on your latest post.")

        ctx.close()


if __name__ == "__main__":
    main()
