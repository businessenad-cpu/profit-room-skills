#!/usr/bin/env python3
"""Rank an Instagram account's reels by real view count (play_count) and return the top N.

Primary path: Instagram private API via a logged-in IG session. The session comes from EITHER
of these, in order of preference:
  1. The IG_SESSIONID environment variable — your account's `sessionid` cookie value
     (Chrome DevTools > Application > Cookies > instagram.com > sessionid). Preferred for
     headless/CI use. Never commit this value.
  2. Your local browser session cookies via `browser_cookie3` (reads whatever IG session is
     already logged in in Chrome).

No fallback is implemented here — the calling skill falls back to an IG-reels MCP tool itself
if this script exits non-zero.
"""
import argparse
import json
import os
import sys
import time

IG_APP_ID = "936619743392459"


def get_session(cookiefile=None):
    import requests

    session = requests.Session()

    sessionid = os.environ.get("IG_SESSIONID")
    if sessionid:
        # Auth via an explicitly-provided sessionid cookie (no browser needed).
        session.cookies.set("sessionid", sessionid, domain=".instagram.com")
    else:
        # Fall back to reading the logged-in IG session from the local Chrome profile.
        try:
            import browser_cookie3
        except ImportError:
            print("Installing browser_cookie3...", file=sys.stderr)
            import subprocess

            subprocess.run([sys.executable, "-m", "pip", "install", "-q", "browser_cookie3"], check=True)
            import browser_cookie3

        cj = browser_cookie3.chrome(domain_name="instagram.com")
        session.cookies.update(cj)

    session.headers.update(
        {
            "X-IG-App-ID": IG_APP_ID,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        }
    )
    return session


def get_user_id(session, handle):
    handle = handle.lstrip("@")
    r = session.get(
        f"https://www.instagram.com/api/v1/users/web_profile_info/?username={handle}",
        timeout=15,
    )
    r.raise_for_status()
    data = r.json()
    user = data.get("data", {}).get("user")
    if not user:
        raise RuntimeError(f"no profile data for @{handle} (private account, wrong handle, or logged-out session)")
    return user["id"]


def fetch_posts(session, user_id, max_pages=6):
    posts = []
    max_id = None
    for _ in range(max_pages):
        url = f"https://www.instagram.com/api/v1/feed/user/{user_id}/?count=33"
        if max_id:
            url += f"&max_id={max_id}"
        r = session.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()
        items = data.get("items", [])
        posts.extend(items)
        if not data.get("more_available") or not data.get("next_max_id"):
            break
        max_id = data["next_max_id"]
        time.sleep(0.5)
    return posts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--handle", required=True, help="Instagram handle, with or without @")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--pages", type=int, default=6, help="feed pages to sample (33 posts/page)")
    ap.add_argument("--out", default="reels.json")
    args = ap.parse_args()

    session = get_session()
    user_id = get_user_id(session, args.handle)
    posts = fetch_posts(session, user_id, max_pages=args.pages)

    reels = [p for p in posts if p.get("product_type") == "clips"]
    if not reels:
        print("no reels (product_type=clips) found in sampled posts", file=sys.stderr)
        sys.exit(1)

    def views(p):
        return p.get("play_count") or p.get("view_count") or 0

    reels.sort(key=views, reverse=True)
    top = reels[: args.top]

    out = []
    for p in top:
        code = p.get("code")
        out.append(
            {
                "code": code,
                "url": f"https://www.instagram.com/reel/{code}/",
                "play_count": views(p),
                "like_count": p.get("like_count"),
                "comment_count": p.get("comment_count"),
                "video_duration": p.get("video_duration"),
                "taken_at": p.get("taken_at"),
                "caption": ((p.get("caption") or {}).get("text") or "")[:300],
            }
        )

    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)

    print(f"sampled {len(posts)} posts, {len(reels)} reels, wrote top {len(out)} to {args.out}", file=sys.stderr)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
