---
name: daily-digest
description: "Run a daily industry digest for the user's niche — aggregates fresh tool launches, releases, and high-signal discussions from public sources (Reddit, Hacker News, GitHub, web search), filters hard, and outputs a tight briefing. No fluff, no opinion pieces, just specific things the user could act on or make content about today. Use when the user says /daily-digest, 'what's new today', 'what happened in [my niche]', 'morning briefing', 'catch me up', or 'what's trending'."
allowed-tools: Bash, WebSearch, WebFetch, Read, Write
metadata:
  argument-hint: "/daily-digest [--today | --week | --days=N]"
---

# Daily Digest — Industry Briefing

Surfaces specific, concrete launches, releases, and discussions in the user's field that they could make
a single piece of content about, or just need to know. No corporate news, no debates, no "AI is changing
everything" filler.

## Personalization
This digest is scoped to *your* niche and *your* audience. Before running, load the brand profile at
`~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your niche and who you serve).
- **NICHE** and **AUDIENCE** come from the profile and drive every search query and the relevance filter.
- The digest is tuned for a solo creator/operator by default — someone trying to grow an audience, get
  clients, or ship products. If the user's audience is different, adapt the "relevance" test to their
  audience's core question.

## Configuration (edit these for your niche)

Set these once for your field. The defaults below assume an "AI / creator tools" niche — swap them for
your own. You can paste your own values when you run the skill, or keep them here.

- **SUBREDDITS** — communities where your niche talks (default: `ClaudeAI ChatGPT SideProject indiehackers entrepreneur`)
- **GITHUB_ORGS** — orgs whose new repos = signal, if your niche is software (default: `anthropics openai google-deepmind`; leave empty for non-software niches)
- **KEYWORDS** — the tools/terms a launch would mention (default: `AI agent LLM open source tool`)
- **COMPETITOR_CHANNELS** — optional: YouTube channel IDs of creators you track (used only if vidIQ is connected; empty by default)

---

## STEP 0: Parse Timeframe

- `--today` / `--days=1` → `DAYS=1`
- `--week` / `--days=7` → `DAYS=7`
- `--days=N` → `DAYS=N`
- No flag → `DAYS=2` (last 48 hours)

Compute:
- **TODAY_ISO** — today as `YYYY-MM-DD` (from context)
- **CUTOFF_ISO** — TODAY_ISO minus DAYS days

Display before running tools:
```
🗞️ Running your [NICHE] digest for the last {DAYS} day(s)...
Scanning: Reddit · Hacker News · GitHub · web search
```

---

## STEP 1: Run Research In Parallel

**Fire the Bash call and the WebSearches in ONE message.** Replace `{DAYS}`, `{CUTOFF_ISO}`, and the
config variables with real values before firing.

**Tool call A — one Bash call across the free public APIs:**

```bash
DAYS={DAYS}
CUTOFF_ISO={CUTOFF_ISO}
SUBREDDITS="ClaudeAI ChatGPT SideProject indiehackers entrepreneur"   # ← your SUBREDDITS
GITHUB_ORGS="anthropics openai google-deepmind"                        # ← your GITHUB_ORGS (may be empty)
KEYWORDS="AI agent LLM open source tool"                               # ← your KEYWORDS
CUTOFF_EPOCH=$(python3 -c "import datetime; print(int((datetime.datetime.now()-datetime.timedelta(days=$DAYS)).timestamp()))")

# ── Reddit hot posts (real upvote signal; score >= 150 is strong) ──
echo "=== Reddit Hot Posts ==="
for sub in $SUBREDDITS; do
  echo "--- r/$sub ---"
  curl -fsSL -H "User-Agent: daily-digest/1.0" \
    "https://www.reddit.com/r/${sub}/hot.json?limit=10" 2>/dev/null \
    | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for post in data['data']['children']:
        p = post['data']
        if p.get('score', 0) >= 150:
            print(f\"{p['score']}up  {p['title'][:120]}  |  https://reddit.com{p['permalink']}\")
except Exception as e:
    print(f'WARN: {e}')
" 2>/dev/null || echo "WARN: r/$sub fetch failed"
done

# ── Hacker News (Show HN + discussions, real points, date-filtered) ──
echo "=== HN Show HN ==="
curl -fsSL "https://hn.algolia.com/api/v1/search?query=$(echo $KEYWORDS | tr ' ' '+')&tags=show_hn&numericFilters=created_at_i%3E${CUTOFF_EPOCH},points%3E50&hitsPerPage=15" 2>/dev/null \
  | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for hit in sorted(data.get('hits', []), key=lambda h: h.get('points', 0), reverse=True):
        print(f\"{hit.get('points',0)}pts | {hit.get('title','')} | https://news.ycombinator.com/item?id={hit.get('objectID','')}\")
except Exception as e:
    print(f'WARN: {e}')
" 2>/dev/null || echo "WARN: HN Show HN failed"

echo "=== HN Discussions ==="
curl -fsSL "https://hn.algolia.com/api/v1/search?query=$(echo $KEYWORDS | tr ' ' '+')&numericFilters=created_at_i%3E${CUTOFF_EPOCH},points%3E100&hitsPerPage=5" 2>/dev/null \
  | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for hit in data.get('hits', []):
        print(f\"{hit.get('points',0)}pts | {hit.get('title','')} | https://news.ycombinator.com/item?id={hit.get('objectID','')}\")
except Exception as e:
    print(f'WARN: {e}')
" 2>/dev/null || echo "WARN: HN discussions failed"

# ── New GitHub repos from key orgs (software niches only; catches drops at source) ──
if [ -n "$GITHUB_ORGS" ]; then
  echo "=== New GitHub repos from key orgs ==="
  for org in $GITHUB_ORGS; do
    echo "--- $org ---"
    curl -fsSL "https://api.github.com/orgs/${org}/repos?sort=created&direction=desc&per_page=10" 2>/dev/null \
      | python3 -c "
import sys, json
org='${org}'; cutoff='${CUTOFF_ISO}'
try:
    for r in json.load(sys.stdin):
        created = r.get('created_at','')[:10]
        if created >= cutoff:
            desc = (r.get('description') or '')[:80]
            print(f\"{created} | {org}/{r['name']} | ★{r.get('stargazers_count',0)} | {desc} | {r['html_url']}\")
except Exception as e:
    print(f'WARN: {e}')
" 2>/dev/null || echo "WARN: $org fetch failed"
  done
fi
```

Use timeout **300000ms** (5 minutes).

**Tool calls B–F — WebSearches (fire in the same message).** Replace `[NICHE]`/`[KEYWORDS]` with the
user's values and always anchor recency with `after:{CUTOFF_ISO}` (a bare "this month" returns the same
cached results every day):
1. `[NICHE] new tool OR feature OR release OR update after:{CUTOFF_ISO}`
2. `[NICHE] "just launched" OR "just shipped" OR "just released" after:{CUTOFF_ISO} -enterprise`
3. `[main tool/platform in the niche] new feature OR changelog after:{CUTOFF_ISO}`
4. `site:producthunt.com [NICHE] launch after:{CUTOFF_ISO}`
5. Discovery (no keyword lock): `"just released" OR "open source" [broad niche term] after:{CUTOFF_ISO}` — catches tools before you know their names

**Optional — competitor videos (only if vidIQ MCP is connected and COMPETITOR_CHANNELS is set):**
Load the schemas first with ToolSearch (`select:mcp__claude_ai_vidIQ_for_Claude__vidiq_channel_videos,mcp__claude_ai_vidIQ_for_Claude__vidiq_outliers,mcp__claude_ai_vidIQ_for_Claude__vidiq_video_comments`),
then pull recent uploads (`popular=false`, 7-day window) and outliers for each channel, and scan the
comments on any tool-specific video for questions/pain points. If vidIQ isn't available, skip the
COMPETITORS and TOP COMMENTS sections entirely.

---

## STEP 2: Filter Hard

**DEDUP:** Read `~/.claude/digest-seen.txt` (lines `YYYY-MM-DD|title-slug`). Skip any item whose title
(lowercased, spaces→dashes) or URL matches an entry from the last 7 days. If the file doesn't exist,
continue without dedup.

**EXCLUDE anything that is:** safety/alignment/regulation debate, corporate earnings/funding/valuations,
enterprise B2B that doesn't touch a solo creator, geopolitics/policy, general "X is changing everything"
opinion, or any item whose only angle is "put this on your resume / land a better job." (The default
audience is trying to build something of their own, not climb a ladder.)

**INCLUDE only:** a specific new tool/feature/release, something a solo creator could try or demo today,
a concrete workflow or technique that changes how you work, or a named product launch and what it does.

**Relevance test** (calibrate to the profile's AUDIENCE): *"Can someone in my audience use this today to
grow their audience, get clients, or make something?"* If yes, it belongs. If it's for a 500-person
enterprise, cut it.

**First-mover check:** for each launch, note if no creator content exists on it yet — mark it 🟢. Those
rank higher; the content window is open.

**Wave check:** if 3+ independent sources reference the same tool within the window, prefix it `🌊` and
surface it first — the content window is closing fast.

**One-phrase audience note:** every DROPS item gets one line reframing it as leverage for the user's
audience. One phrase, not a paragraph. If you can't write an honest one that passes the relevance test,
the item doesn't belong in DROPS.

---

## STEP 3: Output the Digest

Exactly these sections, in order (omit any that are empty): **DROPS**, **SIGNAL**, and — only if vidIQ
was used — **COMPETITORS** and **TOP COMMENTS**. Quality over quantity: 2 sharp items beat 5 vague ones.
Every item needs a source link.

```
🗞️ [NICHE] DIGEST — {Day}, {Date} · {DAYS}d

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 DROPS

→ ⭐ 🆕 *{Tool}* — {what it is / changed, one phrase}  [source](URL)
  ↳ {one-phrase audience note}
→ 🟢 *{Tool}* — {…}  [source](URL)
  ↳ {audience note}

Labels: ⭐ lead item (the one thing to act on today, exactly 1) · 🟢 first mover · 🌊 wave forming · 🆕 new release
[3-5 items max. Omit the section if nothing genuinely dropped.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ SIGNAL

→ r/{sub} {score}↑: "{post title}"  [reddit](URL)
→ {N}pts HN: "{Show HN title}"  [hn](URL)

[Reddit hot threads + HN discussions. Max 7. Show scores. Skip anything without something specific.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔭 COMPETITORS   (only if vidIQ used)

→ {Channel}: "{Video title}" — {views}/{days}d ↑outlier  [yt](URL)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 TOP COMMENTS   (only if vidIQ used)

→ "{Verbatim comment}" — @handle on {Channel}
  *Angle: {one video the user could make that answers this}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 {N} sources · {N} deduped
```

Pick the single strongest item (first-mover window open + clean relevance + high signal) and mark it ⭐
in DROPS.

---

## STEP 4: Save Dedup State

Append one line per DROPS and SIGNAL item to `~/.claude/digest-seen.txt`:
```
{TODAY_ISO}|{title-slug}
```
`title-slug` = title/handle lowercased, spaces→dashes, truncated at 60 chars. Then prune lines older than
7 days.

---

## STEP 5: Follow-Up

```
---
Go deeper on anything: name it and I'll run a full dive, draft a post, or turn it into a content idea.
```

## Notes

- **Recency is everything.** Always use `after:{CUTOFF_ISO}` in web searches. A bare month/year returns
  the same cached popular articles regardless of date.
- **Source priority (earlier = more first-to-know):** GitHub org watcher → HN Show HN (12-24h before
  Twitter/Reddit) → web search launches → Reddit hot threads.
- If the user's niche isn't software, drop GITHUB_ORGS and lean on Reddit + web search + Product Hunt.
