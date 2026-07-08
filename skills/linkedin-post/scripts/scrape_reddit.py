#!/usr/bin/env python3
"""
Reddit trending topic scraper for linkedin-post skill.

Fetches trending posts from one or more subreddits via Reddit's public JSON API.
No API key required. Uses curl under the hood (Reddit blocks Python urllib).

Usage:
    # Scrape all subreddits from the config file (default mode):
    python3 scrape_reddit.py --from-config

    # Scrape specific subreddits:
    python3 scrape_reddit.py entrepreneur SaaS n8n

    # Options:
    python3 scrape_reddit.py --from-config --time month
    python3 scrape_reddit.py entrepreneur --sort hot --show 5
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


CURL_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

CONFIG_PATH = Path(__file__).parent.parent / "references" / "subreddits.json"

# Skip recurring/automated thread types
SKIP_PATTERNS = [
    "thank you thursday",
    "monday milestone",
    "weekly discussion",
    "weekly thread",
    "weekly ask",
    "weekly feedback",
    "share your",
    "self-promotion",
    "free offerings",
    "ama ",
    "podcast",
    "episode ",
    "r/entrepreneur podcast",
]


def load_config() -> dict:
    """Load subreddit config from references/subreddits.json."""
    if not CONFIG_PATH.exists():
        print(f"Config not found at {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return json.load(f)


def fetch_posts(subreddit: str, sort: str = "top", time_filter: str = "week", limit: int = 30) -> list:
    """Fetch posts from a subreddit via the JSON API using curl."""
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}&t={time_filter}"

    try:
        result = subprocess.run(
            ["curl", "-s", "-A", CURL_UA, "--max-time", "10", url],
            capture_output=True, text=True, timeout=15
        )
    except subprocess.TimeoutExpired:
        print(f"  Timeout fetching r/{subreddit}", file=sys.stderr)
        return []
    except FileNotFoundError:
        print("  Error: curl not found. Please install curl.", file=sys.stderr)
        sys.exit(1)

    if not result.stdout.strip():
        print(f"  Empty response for r/{subreddit}", file=sys.stderr)
        return []

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"  Invalid JSON from r/{subreddit}", file=sys.stderr)
        return []

    if "error" in data:
        print(f"  r/{subreddit}: {data.get('message', 'not found')}", file=sys.stderr)
        return []

    posts = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})

        if post.get("stickied") or post.get("pinned"):
            continue

        title = post.get("title", "").strip()

        if any(pattern in title.lower() for pattern in SKIP_PATTERNS):
            continue

        score = post.get("score", 0)
        if score < 10:
            continue

        posts.append({
            "title": title,
            "score": score,
            "comments": post.get("num_comments", 0),
            "upvote_ratio": post.get("upvote_ratio", 0),
            "url": f"https://reddit.com{post.get('permalink', '')}",
            "selftext": post.get("selftext", "")[:300].strip(),
            "subreddit": post.get("subreddit", subreddit),
            "created_utc": post.get("created_utc", 0),
        })

    return posts


def virality_score(post: dict) -> float:
    """Rank by upvotes + comment weight + recency bonus."""
    age_hours = (datetime.now(timezone.utc).timestamp() - post["created_utc"]) / 3600
    recency = max(0, 1 - (age_hours / 72))
    return post["score"] + (post["comments"] * 3) + (recency * 200)


def dedupe(posts: list) -> list:
    seen, unique = set(), []
    for post in posts:
        key = post["title"].lower()[:60]
        if key not in seen:
            seen.add(key)
            unique.append(post)
    return unique


def format_grouped(results: dict[str, list], show: int, show_url: bool = False) -> str:
    """Format results grouped by subreddit, with a global index across all posts."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"  TRENDING TOPICS BY SUBREDDIT")
    lines.append(f"  {datetime.now().strftime('%B %d, %Y')}")
    lines.append(f"{'='*60}")

    global_index = 1
    for subreddit, posts in results.items():
        if not posts:
            continue
        lines.append(f"\n  ── r/{subreddit} ──\n")
        for post in posts[:show]:
            lines.append(f"{global_index:3}. {post['title']}")
            lines.append(f"     ↑{post['score']:,}  ·  💬 {post['comments']}")
            if post["selftext"]:
                preview = post["selftext"].replace("\n", " ")
                ellipsis = "..." if len(post["selftext"]) >= 300 else ""
                lines.append(f"     \"{preview}{ellipsis}\"")
            if show_url:
                lines.append(f"     {post['url']}")
            lines.append("")
            global_index += 1

    lines.append(f"{'='*60}")
    lines.append(f"  {global_index - 1} topics total across {len(results)} subreddits")
    lines.append(f"{'='*60}\n")
    return "\n".join(lines)


def format_flat(posts: list, show_url: bool = False) -> str:
    """Format all posts as a single ranked list."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"  TRENDING TOPICS FROM REDDIT")
    lines.append(f"  {datetime.now().strftime('%B %d, %Y')}")
    lines.append(f"{'='*60}\n")

    for i, post in enumerate(posts, 1):
        lines.append(f"{i:2}. {post['title']}")
        lines.append(f"    r/{post['subreddit']}  ·  ↑{post['score']:,}  ·  💬 {post['comments']}")
        if post["selftext"]:
            preview = post["selftext"].replace("\n", " ")
            ellipsis = "..." if len(post["selftext"]) >= 300 else ""
            lines.append(f"    \"{preview}{ellipsis}\"")
        if show_url:
            lines.append(f"    {post['url']}")
        lines.append("")

    lines.append(f"{'='*60}")
    lines.append(f"  {len(posts)} topics shown")
    lines.append(f"{'='*60}\n")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Scrape trending Reddit topics for LinkedIn post ideas"
    )
    parser.add_argument(
        "subreddits", nargs="*",
        help="Subreddit name(s) to scrape. Omit to use --from-config."
    )
    parser.add_argument(
        "--from-config", action="store_true",
        help=f"Load subreddits from {CONFIG_PATH}"
    )
    parser.add_argument(
        "--sort", choices=["hot", "top", "rising", "new"], default="top"
    )
    parser.add_argument(
        "--time", choices=["day", "week", "month", "year", "all"], default="week"
    )
    parser.add_argument(
        "--limit", type=int, default=30,
        help="Posts to fetch per subreddit (default: 30)"
    )
    parser.add_argument(
        "--show", type=int, default=None,
        help="Topics to display per subreddit (default: from config or 10)"
    )
    parser.add_argument(
        "--flat", action="store_true",
        help="Show all results in one ranked list instead of grouped by subreddit"
    )
    parser.add_argument(
        "--url", action="store_true",
        help="Show Reddit URL for each post"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output raw JSON"
    )

    args = parser.parse_args()

    # Determine which subreddits to scrape
    if args.from_config or not args.subreddits:
        config = load_config()
        subs = [s["name"] for s in config["subreddits"]]
        defaults = config.get("defaults", {})
        show = args.show or defaults.get("show_per_subreddit", 10)
        sort = args.sort or defaults.get("sort", "top")
        time_filter = args.time or defaults.get("time", "week")
        limit = args.limit or defaults.get("limit", 30)
    else:
        subs = [s.strip().lstrip("r/") for s in args.subreddits]
        show = args.show or 10
        sort = args.sort
        time_filter = args.time
        limit = args.limit

    # Fetch from each subreddit
    results = {}  # subreddit -> sorted posts
    all_posts = []

    for sub in subs:
        print(f"  Fetching r/{sub} ({sort}/{time_filter})...", file=sys.stderr)
        posts = fetch_posts(sub, sort=sort, time_filter=time_filter, limit=limit)
        posts.sort(key=virality_score, reverse=True)
        posts = dedupe(posts)
        results[sub] = posts
        all_posts.extend(posts)
        print(f"  → {len(posts)} posts found", file=sys.stderr)

    if not any(results.values()):
        print("\nNo posts found.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(results, indent=2))
    elif args.flat:
        all_posts.sort(key=virality_score, reverse=True)
        all_posts = dedupe(all_posts)
        print(format_flat(all_posts[:show], show_url=args.url))
    else:
        print(format_grouped(results, show=show, show_url=args.url))


if __name__ == "__main__":
    main()
