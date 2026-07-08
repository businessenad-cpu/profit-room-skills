# GitHub Source Mode

Turn trending GitHub repos — or a single repo — into a carousel. Great for dev, AI, and tooling niches. Pick topics that fit *your* audience: if you teach a specific tool (Claude Code, LangChain, a design tool, an indie SaaS stack), filter to repos in that lane so the post feels like insider signal rather than generic dev news. The Claude/AI examples below are just one instance of the general pattern.

**Triggers:** "top repos this week/month", "trending [niche] repos", "top 5 GitHub repos", or a `github.com/owner/repo` URL.

Default style: **alternating solid** body slides + a **photo cover** from `gen_cover.py`. Body slides use `bg_mode: "light_pop"`.

---

## Mode A — Trending repos (top N)

### Fetch
Prefer a topic search over raw trending so results match your niche:
```python
import urllib.request, json
def fetch_topic(topic, sort="updated"):
    url = f"https://api.github.com/search/repositories?q=topic:{topic}&sort={sort}&order=desc&per_page=30"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github+json"})
    return json.loads(urllib.request.urlopen(req).read().decode())

# Example niches — swap the topics for your audience's stack:
results = fetch_topic("claude-code")      # or "langchain", "mcp", "ai-agents", etc.
```
If firecrawl MCP is available, scrape `https://github.com/topics/<topic>` for richer descriptions. Fallback: `https://github.com/trending?since=weekly&spoken_language_code=en`, filtered to your niche.

**Include:** tools, skills, plugins, integrations, or MCP servers a member of your audience could use or appreciate; pushed/created in the last 7 days (for "this week").
**Exclude:** raw ML/research repos (training, weights), enterprise infra, zero-star no-description repos, and the vendor's own official repos (already well-known).

Pick the top 5 by stars-in-last-7-days or recency. Store the repo data as you parse it — you'll need it for the lead-magnet DM:
```python
repos = [{"rank": 5, "name": "...", "owner": "...", "url": "https://github.com/owner/repo", "description": "..."}]
```

### Carousel structure
| Slide | Content |
|-------|---------|
| 1 (cover) | Title hook — category + timeframe. Photo bg via `gen_cover.py`. |
| 2 | Intro — "I track [niche] repos so you don't have to. Here's what dropped this week." |
| 3-7 | One slide per repo, numbered #5 down to #1 (save the best for last) |
| 8 (CTA) | Lead magnet — "Comment [KEYWORD] and I'll send you all [N] links" |

**Per-repo slide (light_pop):**
- `headline`: `"#N: Repo Name"` with `accent_phrase: "Repo Name"`
- `body`: one sentence on what it does + a concrete outcome/stat
- `bottom_summary`: the punchy why-it-matters one-liner
- `image_path`: repo screenshot (optional, via Playwright)
- `github_card`: `{"owner","name","description","language","language_color":"#3572A5","stars":"2.4k"}`
- `show_bookmark: true`

`topic_label` on the cover: keep it specific, e.g. "GITHUB THIS WEEK" or "[NICHE] THIS WEEK".

---

## Mode B — Single repo teardown

### Fetch
```python
import urllib.request
def page(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req).read().decode('utf-8')
repo_html = page("https://github.com/OWNER/REPO")
try:    readme = page("https://raw.githubusercontent.com/OWNER/REPO/main/README.md")
except: readme = page("https://raw.githubusercontent.com/OWNER/REPO/master/README.md")
```
Extract: what it does, key capabilities (3-5), who it's for, how to use it, stars/forks/activity, any demo GIF or live-demo URL in the README.

### Screenshots before copy
Decide images first — an image slide gets max 2 short sentences. Priority:
1. **Live demo URL** — navigate + screenshot the real product (dismiss modals/empty states first).
2. **Demo GIF/screenshot from README** — parse `![` tags, ignore badges (shields.io), grab the most informative image.
3. **GitHub repo page** — always take one for the credibility slide.

Before a GitHub screenshot: `mcp__playwright__browser_resize(width=900, height=1100)` (near-portrait fills the card cleanly). Save to `output/screenshots/repo_NAME_[type].jpg`. If Playwright isn't available, use a direct README image URL as `image_path`, or rely on `github_card` alone.

### Structure (Teardown framework)
| Slide | Content | Image? | bottom_summary? |
|-------|---------|--------|------------------|
| 1 (cover) | Hook — the problem it solves / tension | cover_image_path | no |
| 2 | "What is [Repo]?" — stat + one line | GitHub page shot | yes |
| 3 | The problem before — the bottleneck | no | optional |
| 4 | How it fixes it — the mechanism, 2 sentences | live demo shot | yes |
| 5 | What actually changes — 3 outcome statements | no | optional |
| 6 | Who it's for / NOT for — YES / NO | no | optional |
| 7 | The shift — paint the winner, not instructions | no | yes |
| 8 (CTA) | Your CTA | — | no |

**Copy rules:** mixed-case headlines (verb phrase, not a label). Name the outcome, not the feature. Never send viewers to the repo's own site/install inside the carousel — the carousel builds desire, your CTA converts it.

---

## Layout rules (non-negotiable)
- `github_card` ONLY on `#N:` per-repo slides (Mode A). Never on intro/CTA/long-body slides — its fixed zone collides.
- Image slides get SHORT body (max 2 sentences). More than that → drop `image_path`.
- `bottom_summary` + `image_path` together is the standard image pattern; the renderer reserves space so they don't overlap.
- Both modes use `light_pop` for all non-cover slides and `cover_image_path` on the cover.

---

## Cover image
Run `gen_cover.py` first, capture the printed path, set it as `cover_image_path` on slide 1:
```bash
cd <skill>/scripts
cover_path=$(python3 gen_cover.py)          # random context-appropriate prompt
# or: python3 gen_cover.py desk_workspace    # specific prompt
# or: python3 gen_cover.py --list            # see keys
echo "$cover_path"
```
Prompts are brand-neutral scenes with negative space for text. To brand the cover art, set env `BRAND_LOGO` (or `BRAND_MASCOT`) to an image path and `gen_cover.py` passes it as a Higgsfield reference. The renderer full-bleeds the photo, adds a dark overlay, and renders the headline in white automatically.

---

## Lead-magnet keyword
GitHub carousels use a lead-magnet CTA. Pick a random, memorable, unrelated word (e.g. `WAFFLE`, `TORCH`, `MARBLE`) — never a topic word like `REPOS`/`CODE`/`AI` (they collide across posts). If you use a comment-to-DM tool, confirm the keyword isn't already live there. The keyword goes in the **caption only**, not on the CTA slide. Then set up the keyword + DM copy (the list of repo links) in your DM-automation tool.
