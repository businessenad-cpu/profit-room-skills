#!/usr/bin/env python3
"""One-time setup: opens Gumroad login in a real browser window.
Log in manually (handles CAPTCHA, Google OAuth, 2FA, anything).
Once you're on the dashboard, press Enter here and the session is saved.

Run once:
  python3 gumroad-save-session.py

After this, gumroad-publish.py uses the saved session automatically.
The session file is written next to the skill and is gitignored — it is never committed.
No credentials are stored in this script.
"""

import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Run: pip install playwright && playwright install chromium")
    raise SystemExit(1)

# Written into the skill folder; matches gumroad-publish.py and is gitignored.
cookies_path = Path(__file__).resolve().parent.parent / ".gumroad-session.json"

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://gumroad.com/login")
    print("\nBrowser is open. Log in manually (Google, email/password, 2FA — whatever you normally use).")
    print("Once you're on the Gumroad dashboard, come back here and press Enter.")
    input("\n> Press Enter when logged in: ")

    # Verify we're actually logged in
    if "login" in page.url:
        print("Still on login page — make sure you're on the dashboard first.")
        input("> Press Enter again when ready: ")

    context.storage_state(path=str(cookies_path))
    print(f"\nSession saved to: {cookies_path}")
    print("You won't need to log in again. Run gumroad-publish.py normally now.")

    browser.close()
