#!/usr/bin/env python3
"""Check your YouTube channel for videos published in the last N hours.

Uses YouTube Data API v3 with a simple API key — no auth, no crypto, just curl.

Setup (env vars):
  YOUTUBE_API_KEY      your YouTube Data API v3 key
  YOUTUBE_CHANNEL_ID   your channel ID (starts with "UC...")

Usage:
  python3 check-new-video.py              # check last 24 hours
  python3 check-new-video.py --hours 48   # check last 48 hours
  python3 check-new-video.py --json       # output JSON for scripting

Returns exit code 0 if a new video was found, 1 if none.
"""

import json
import os
import subprocess
import sys
import urllib.parse
from datetime import datetime, timezone, timedelta

CHANNEL_ID = os.environ.get("YOUTUBE_CHANNEL_ID", "")  # TODO: set your channel ID (UC...)
API_KEY = os.environ.get("YOUTUBE_API_KEY", "")
API_BASE = "https://www.googleapis.com/youtube/v3/search"


def parse_args(argv):
    args = argv[1:]
    hours = 24
    output_json = False
    i = 0
    while i < len(args):
        if args[i] == "--hours" and i + 1 < len(args):
            hours = int(args[i + 1])
            i += 2
        elif args[i] == "--json":
            output_json = True
            i += 1
        else:
            i += 1
    return hours, output_json


def fetch_recent_videos(hours):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    published_after = cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")

    params = urllib.parse.urlencode({
        "key": API_KEY,
        "channelId": CHANNEL_ID,
        "publishedAfter": published_after,
        "order": "date",
        "type": "video",
        "part": "snippet",
        "maxResults": "10",
    })
    url = f"{API_BASE}?{params}"

    result = subprocess.run(
        ["curl", "-s", "--max-time", "15", url],
        capture_output=True, text=True, timeout=20
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl failed: {result.stderr.strip()}")

    data = json.loads(result.stdout)
    if "error" in data:
        raise RuntimeError(f"YouTube API error: {data['error'].get('message', str(data['error']))}")

    videos = []
    for item in data.get("items", []):
        snippet = item.get("snippet", {})
        video_id = item.get("id", {}).get("videoId", "")
        published = snippet.get("publishedAt", "")
        videos.append({
            "id": video_id,
            "title": snippet.get("title", "Unknown"),
            "url": f"https://youtube.com/watch?v={video_id}",
            "upload_date": published[:10],
            "published_iso": published,
            "thumbnail": f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg",
        })
    return videos


def main():
    hours, output_json = parse_args(sys.argv)

    if not CHANNEL_ID or not API_KEY:
        print("Error: set YOUTUBE_API_KEY and YOUTUBE_CHANNEL_ID in your environment.", file=sys.stderr)
        sys.exit(1)

    if not output_json:
        print(f"Checking your channel for videos in the last {hours} hours...", file=sys.stderr)

    try:
        videos = fetch_recent_videos(hours)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if output_json:
        print(json.dumps(videos, indent=2))
    else:
        if videos:
            print(f"\nFound {len(videos)} new video(s):\n")
            for v in videos:
                print(f"  {v['title']}")
                print(f"  Published: {v['published_iso']}")
                print(f"  {v['url']}")
                print()
        else:
            print(f"\nNo new videos published in the last {hours} hours.")

    sys.exit(0 if videos else 1)


if __name__ == "__main__":
    main()
