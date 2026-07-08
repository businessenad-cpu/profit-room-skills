#!/usr/bin/env python3
"""
Post to Reddit via the Reddit API (password grant, no PRAW required).
Usage:
  python3 reddit-post.py --title "..." --body "..." --subreddit ClaudeAI
  python3 reddit-post.py --title "..." --body "..." --subreddit ClaudeAI --flair "Discussion"

Env vars required:
  REDDIT_CLIENT_ID
  REDDIT_CLIENT_SECRET
  REDDIT_USERNAME
  REDDIT_PASSWORD
"""

import os
import sys
import argparse
import requests

# Reddit asks that the User-Agent identify the app and the account running it.
USER_AGENT = f"content-engine/1.0 by u/{os.environ.get('REDDIT_USERNAME', 'unknown')}"

def get_token(client_id, client_secret, username, password):
    r = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=(client_id, client_secret),
        data={"grant_type": "password", "username": username, "password": password},
        headers={"User-Agent": USER_AGENT},
    )
    r.raise_for_status()
    data = r.json()
    if "access_token" not in data:
        print(f"Auth failed: {data}", file=sys.stderr)
        sys.exit(1)
    return data["access_token"]


def get_flair_id(token, subreddit, flair_text):
    r = requests.get(
        f"https://oauth.reddit.com/r/{subreddit}/api/link_flair_v2",
        headers={"Authorization": f"bearer {token}", "User-Agent": USER_AGENT},
    )
    if r.status_code != 200:
        return None
    flairs = r.json()
    for f in flairs:
        if flair_text.lower() in f.get("text", "").lower():
            return f["id"]
    return None


def submit_post(token, subreddit, title, body, flair_text=None):
    headers = {"Authorization": f"bearer {token}", "User-Agent": USER_AGENT}

    data = {
        "sr": subreddit,
        "kind": "self",
        "title": title,
        "text": body,
        "nsfw": False,
        "spoiler": False,
        "resubmit": True,
    }

    if flair_text:
        flair_id = get_flair_id(token, subreddit, flair_text)
        if flair_id:
            data["flair_id"] = flair_id
            data["flair_text"] = flair_text

    r = requests.post(
        "https://oauth.reddit.com/api/submit",
        headers=headers,
        data=data,
    )
    r.raise_for_status()
    result = r.json()

    jquery = result.get("jquery", [])
    post_url = None
    for item in jquery:
        if isinstance(item, list) and len(item) >= 4:
            val = item[3]
            if isinstance(val, list) and val and isinstance(val[0], str) and "reddit.com/r/" in val[0]:
                post_url = val[0]
                break

    errors = result.get("json", {}).get("errors", [])
    if errors:
        print(f"Reddit API errors: {errors}", file=sys.stderr)
        sys.exit(1)

    resolved = post_url or result.get("json", {}).get("data", {}).get("url")
    if not resolved:
        # New-reddit submit sometimes accepts the request (200, no errors) but
        # silently drops the post — almost always a subreddit blacklist/automod
        # rule (e.g. some subs blacklist "$", "dollar", "/day" in titles).
        # Surface the raw response and FAIL loudly so the caller never thinks
        # an un-posted submission succeeded.
        print("ERROR: Reddit accepted the request but returned no post URL. "
              "The post was likely filtered by a subreddit rule "
              "(check /api/v1/<sub>/post_requirements for blacklisted title/body strings).",
              file=sys.stderr)
        print(f"Raw response: {result}", file=sys.stderr)
        sys.exit(2)
    return resolved


def post_comment(token, post_url, comment_body):
    # Get post fullname from URL
    parts = post_url.rstrip("/").split("/")
    try:
        post_id = parts[parts.index("comments") + 1]
    except (ValueError, IndexError):
        return None

    r = requests.post(
        "https://oauth.reddit.com/api/comment",
        headers={"Authorization": f"bearer {token}", "User-Agent": USER_AGENT},
        data={"thing_id": f"t3_{post_id}", "text": comment_body},
    )
    r.raise_for_status()
    return r.json()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", required=True)
    parser.add_argument("--subreddit", required=True)
    parser.add_argument("--flair", default=None)
    parser.add_argument("--comment", default=None, help="First comment to post (for YouTube link)")
    args = parser.parse_args()

    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    username = os.environ.get("REDDIT_USERNAME")
    password = os.environ.get("REDDIT_PASSWORD")

    missing = [k for k, v in {
        "REDDIT_CLIENT_ID": client_id,
        "REDDIT_CLIENT_SECRET": client_secret,
        "REDDIT_USERNAME": username,
        "REDDIT_PASSWORD": password,
    }.items() if not v]

    if missing:
        print(f"Missing env vars: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    token = get_token(client_id, client_secret, username, password)
    post_url = submit_post(token, args.subreddit, args.title, args.body, args.flair)
    print(f"Posted: {post_url}")

    if args.comment and post_url and post_url != "unknown":
        post_comment(token, post_url, args.comment)
        print("Comment posted.")


if __name__ == "__main__":
    main()
