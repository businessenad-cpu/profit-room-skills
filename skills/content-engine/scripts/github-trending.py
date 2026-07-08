#!/usr/bin/env python3
"""Daily GitHub trending repos report — AI/dev-focused.

Fetches top trending repos from the GitHub search API (no API key needed)
and saves a markdown report to ~/content/github-trending/.

Usage:
  python3 github-trending.py              # run report for today
  python3 github-trending.py --print      # print to stdout instead of saving
  python3 github-trending.py --days 3     # check last 3 days instead of 7

No API key required. Uses the public GitHub search API.
"""

import json
import subprocess
import sys
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_DIR = Path.home() / "content" / "github-trending"

AI_KEYWORDS = [
    "ai", "llm", "gpt", "claude", "agent", "machine-learning", "deep-learning",
    "generative", "copilot", "assistant", "automation", "mcp", "rag",
    "vector", "embedding", "transformer", "diffusion", "multimodal",
    "dev-tool", "developer-tool", "cli", "workflow",
]


def parse_args(argv):
    args = argv[1:]
    print_stdout = False
    days = 7
    i = 0
    while i < len(args):
        if args[i] == "--print":
            print_stdout = True
            i += 1
        elif args[i] == "--days" and i + 1 < len(args):
            days = int(args[i + 1])
            i += 2
        else:
            i += 1
    return print_stdout, days


def github_search(query, count=10):
    """Call the GitHub search API via curl and return repo items."""
    params = urllib.parse.urlencode({
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": count,
    })
    url = f"https://api.github.com/search/repositories?{params}"
    result = subprocess.run(
        ["curl", "-s", "-H", "Accept: application/vnd.github.v3+json",
         "-H", "User-Agent: content-engine-trending-bot", url],
        capture_output=True, text=True, timeout=15
    )
    return json.loads(result.stdout)["items"]


def is_ai_relevant(repo):
    text = " ".join([
        repo.get("description") or "",
        repo.get("full_name") or "",
        " ".join(repo.get("topics") or []),
    ]).lower()
    return any(kw in text for kw in AI_KEYWORDS)


def fmt_stars(n):
    if n >= 1000:
        return f"{n/1000:.1f}k"
    return str(n)


def repo_block(rank, repo):
    stars = fmt_stars(repo["stargazers_count"])
    lang = repo.get("language") or "N/A"
    created = (repo.get("created_at") or "")[:10]
    topics = repo.get("topics") or []
    topic_str = ", ".join(topics[:5]) if topics else "none"
    ai_tag = " **[AI/DEV]**" if is_ai_relevant(repo) else ""
    desc = repo.get("description") or "No description"
    url = repo["html_url"]
    name = repo["full_name"]

    lines = [
        f"### {rank}. [{name}]({url}){ai_tag}",
        f"- **Stars:** {stars} | **Language:** {lang} | **Created:** {created}",
        f"- **Topics:** {topic_str}",
        f"- **Description:** {desc}",
        "",
    ]
    return "\n".join(lines)


def main():
    print_stdout, days = parse_args(sys.argv)

    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    day_of_week = today.strftime("%A")

    week_ago = (today - timedelta(days=days)).strftime("%Y-%m-%d")
    month_ago = (today - timedelta(days=30)).strftime("%Y-%m-%d")

    print(f"Fetching GitHub trending repos...", file=sys.stderr)

    try:
        weekly = github_search(f"created:>{week_ago}", count=10)
    except Exception as e:
        print(f"Error fetching weekly repos: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        monthly = github_search(f"created:>{month_ago}", count=5)
    except Exception as e:
        print(f"Error fetching monthly repos: {e}", file=sys.stderr)
        monthly = []

    # Build report
    lines = [
        f"# GitHub Trending — {date_str} ({day_of_week})",
        "",
        f"## Top 10 Trending This Week",
        f"_Repos created in the last {days} days, ranked by stars_",
        "",
    ]

    for i, repo in enumerate(weekly, 1):
        lines.append(repo_block(i, repo))

    lines += ["---", "", "## Top 5 Trending This Month",
              "_Repos created in the last 30 days, ranked by stars_", ""]

    for i, repo in enumerate(monthly, 1):
        lines.append(repo_block(i, repo))

    # Content radar
    ai_picks = [r for r in weekly if is_ai_relevant(r)]
    lines += ["---", "", "## Content Radar"]
    lines.append(f"- **AI/Dev-relevant repos today:** {len(ai_picks)} out of {len(weekly)}")

    if ai_picks:
        top = ai_picks[0]
        lines.append(f"- **Top AI pick:** [{top['full_name']}]({top['html_url']}) — {fmt_stars(top['stargazers_count'])} stars")
        lines.append(f"- **Why it matters:** {top.get('description') or 'No description'}")
        if len(ai_picks) > 1:
            also_watch = ", ".join(f"[{r['name']}]({r['html_url']})" for r in ai_picks[1:3])
            lines.append(f"- **Also watch:** {also_watch}")

    lines += [
        "",
        "## Feed into Ideation",
        "Spotted something worth a video? Search it, then feed it to your ideation workflow.",
        "",
        f"_Generated at {today.strftime('%H:%M')} on {date_str}_",
    ]

    report = "\n".join(lines)

    if print_stdout:
        print(report)
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_file = OUTPUT_DIR / f"{date_str}-trending.md"
        output_file.write_text(report, encoding="utf-8")
        print(f"Saved: {output_file}")

    return ai_picks


if __name__ == "__main__":
    main()
