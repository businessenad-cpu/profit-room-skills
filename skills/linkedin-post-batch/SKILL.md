---
name: linkedin-post-batch
description: Generate and schedule the next batch of LinkedIn posts in your brand voice — positioned authority posts with proof anchors, conviction closes, and no engagement-bait CTAs. Use whenever you say "generate the next LinkedIn batch", "schedule more LinkedIn posts", "we're running low on LinkedIn content", "refill the LinkedIn schedule", "next batch of LinkedIn posts", or anything about running out of scheduled LinkedIn content. Also trigger proactively if the current batch is ending soon.
---

# LinkedIn Post Batch Generator + Scheduler

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

Generates ~35 positioned LinkedIn posts across 4 formats, saves them to a local batch folder, and (optionally) schedules everything through your social scheduler at a fixed daily time. One command, fully automated.

---

## Requirements

**Scheduling is optional.** If no scheduler is wired up, the skill still generates the full batch and saves it locally — you publish manually or paste into whatever tool you use.

To enable automated scheduling, set these in `~/.claude/.env`:

```
# TODO: set your own scheduler credentials
SCHEDULER_API_KEY=            # API key for your social scheduler (e.g. Blotato or similar)
SCHEDULER_API_URL=            # scheduler endpoint, e.g. https://mcp.blotato.com/mcp
LINKEDIN_ACCOUNT_ID=          # TODO: set your own LinkedIn account/profile ID from your scheduler
POST_TIME_UTC=21:00           # daily post time in UTC (default 21:00 = 2pm PT)
```

If `SCHEDULER_API_KEY` or `LINKEDIN_ACCOUNT_ID` is missing, skip Steps 2 and 4 (the scheduling steps), still generate and save the batch, and tell the user how to publish manually.

**Dependency:** this is the batch/schedule sibling of the **linkedin-post** skill. It reuses the same voice rules, formats, and brand profile. If `linkedin-post` is installed, defer to its voice/format guidance where it overlaps; this skill focuses on generating *many* posts at once and scheduling them.

---

## Step 1: Load Context

Read the brand profile and any content-intel files in parallel before generating anything:

- `~/.claude/brand-profile.md` — Name, Audience, Offer, Tone, Words-to-avoid, Default-CTA, Main-platforms, proof points / results, personal stories
- Any personal content-intel files you keep (optional), e.g.:
  - `~/content/what-works-linkedin.md` — what's proven to perform for you
  - `~/content/linkedin-hooks.md` — hook patterns ranked by comment ceiling
  - `~/content/wins.md` — customer wins, testimonials, transformation stories
  - `~/content/linkedin-post-log.md` — every post published; avoid repeating angles or anchors from the last 20 posts

Only read files that exist. Pull all proof, stories, and results from the brand profile (or the optional files above). Never invent results.

Then scan any existing batch files to avoid duplication:
- `~/content/linkedin-post-batch-01.md` (and any higher-numbered batches)

Determine the next batch number.

---

## Step 2: Find the Last Scheduled Date (only if a scheduler is configured)

If `SCHEDULER_API_KEY` and `LINKEDIN_ACCOUNT_ID` are set, call your scheduler to find when the current schedule ends. The example below uses a Blotato-compatible JSON-RPC endpoint; adapt the URL/headers to your scheduler.

```bash
set -a && source ~/.claude/.env && set +a

curl -s -X POST "$SCHEDULER_API_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "blotato-api-key: $SCHEDULER_API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"blotato_list_schedules","arguments":{"limit":50}}}' \
  | python3 -c "
import sys, json, os
raw = sys.stdin.read()
acct = os.environ.get('LINKEDIN_ACCOUNT_ID', '')
for line in raw.strip().split('\n'):
    clean = line[6:] if line.startswith('data: ') else line
    try:
        obj = json.loads(clean)
        if 'result' in obj:
            content = obj['result']['content'][0]['text']
            schedules = json.loads(content)
            if schedules:
                # Filter LinkedIn only
                li = [s for s in schedules if s.get('platform') == 'linkedin' or str(s.get('accountId')) == acct]
                times = [s['scheduledTime'] for s in li if 'scheduledTime' in s]
                times.sort()
                print('Last LinkedIn scheduled:', times[-1] if times else 'none')
                print('Total LinkedIn scheduled:', len(times))
    except: pass
"
```

**Account ID:** `$LINKEDIN_ACCOUNT_ID` (your LinkedIn profile in your scheduler)
**Platform:** `linkedin`

The new batch starts the day after the last scheduled LinkedIn post. If nothing is scheduled yet, start tomorrow.

---

## Step 3: Generate 35 Posts Across 4 Formats

### Format Distribution

- **FA — Results Hook + System Reveal:** ~10 posts
- **FB — Personal Story Arc:** ~10 posts
- **FC — Customer Transformation:** ~8 posts
- **FD — Contrarian Conviction:** ~7 posts

---

### FA — Results Hook + System Reveal

**Structure:**
```
[Results-first hook — specific metric, no preamble]

[What the system is — 3-5 arrow bullets, each labeled]
→ [Component 1 — what it does + result]
→ [Component 2]
→ [Component 3]
→ [Component 4 optional]

[Conviction close — declarative, no question]
```

**Conviction close examples (rotate, don't repeat):**
- "That's the system. It runs without me."
- "Build the machine once. The machine does the rest."
- "This is what compound leverage looks like."
- "The old way required a team. This doesn't."

Use only real numbers from the brand profile. If you have no metric, use a qualitative result — never fabricate a figure.

**Hook patterns to pull from (ranked by performance — lean on top):**
1. `[Tool] grew my [platform] from [X] to [Y]+.`
2. `I replaced [N hours/week] of [task] with [system/agents].`
3. `I went from [time-consuming pain] to zero.`
4. `[Dollar amount] [thing]. Built in [short time].`

---

### FB — Personal Story Arc

**Structure:**
```
[Hook: a moment, a number, or a gap — 1 line]

[The before state — what was true, what was painful, what I believed]

[The shift — what changed, what I built, what I decided]

[The after — specific result or realized outcome]

[Conviction close — the principle the story proves]
```

Pull stories from the brand profile (career pivots, origin of your offer, building without a team, a specific build that replaced a bottleneck). Use only stories the user has actually shared.

**Conviction close examples:**
- "The system didn't come first. The decision to build it did."
- "Invisible to inbound isn't a content problem. It's a decision problem."
- "I didn't hire a team. I built one."

---

### FC — Customer Transformation

**Structure:**
```
[Hook: their before state or the specific result — not generic, verbatim if available]

[Their situation before — what they were doing, what wasn't working]

[What shifted — the thing they built or changed]

[The specific result — numbers when available]

[What this proves for the reader — the transferable principle]

[Conviction close]
```

Pull from your proof bank / brand profile. Every FC post must use a real customer or member. No invented proof. If you have no customer results yet, skip FC and redistribute those posts across FA/FB/FD.

**Hook frames:**
- `A [customer descriptor] in [your offer] [specific result].`
- `One of my members went from [stuck state] to [outcome] in [time].`
- `[Name/role] came to me [before state]. [Time] later: [specific result].`

**Conviction close examples:**
- "They didn't need more time. They needed a system."
- "The result wasn't magic. It was momentum."
- "That's what happens when the right tool meets a person who actually ships."

---

### FD — Contrarian Conviction

**Structure:**
```
[The thing most people believe — stated plainly, 1 line]

[Why it's wrong — specific, not vague. What actually happens when you follow that belief.]

[The reframe — what's actually true. The harder, more accurate version.]

[Supporting proof — personal result or customer example. 1-2 lines.]

[Conviction close — the declarative version of the reframe]
```

**Hard rules for FD:**
- Never use "That's not X, it's Y" or "Don't do X, do Y" patterns — sounds like AI copy
- The contrarian position must be defensible and specific, not just edgy
- Must have proof attached. Opinion without proof is just opinion.

**Topics to rotate across (adapt to your niche, don't repeat):**
- "Your content problem is actually a distribution problem"
- "Referrals aren't a business model, they're a side effect"
- "Personal branding isn't about being known, it's about being chosen"
- "AI won't replace you, but a version of you who uses AI will make you irrelevant"
- "Consistency matters more than quality at the start — but no one believes it until they've quit twice"
- "The bottleneck isn't ideas, it's shipping. Everyone has ideas."
- "Your audience doesn't care about your process. They care about your results."

---

### Hard Rules for All Posts

- **Length:** 800-1,400 chars. Shorter than you think you need.
- **No hashtag walls.** Max 2 hashtags at the end, or none. Never mid-copy.
- **No emojis** unless they replace a bullet (→ is fine).
- **No question CTAs.** "What are you building today?" / "Have you tried this?" / "Drop a comment if..." are all banned. They look AI-generated and they are.
- **No em dashes.** Period or restructure.
- **No filler openers.** Never start with "I want to talk about", "Hot take:", "Unpopular opinion:", "Just a reminder".
- **Every post ends with a conviction close** — a declarative statement that earns the reader's agreement without asking for it.
- **Every post needs a proof anchor** — either your own result/story or a real customer outcome from the brand profile. Pure opinion posts don't get published.
- **Honor Words-to-avoid** from the brand profile.
- **No repetition.** Check your post log before writing. Don't reuse the same audience emotion, proof anchor, or format within 10 posts of each other.

---

### Conviction Close Principles

A conviction close is a declarative statement, not a question. It states the principle the post proves. It doesn't beg for engagement — it earns agreement.

**Structure:** `[Action/state] + [because/so/and] + [inevitable outcome].`

Examples:
- "Build the machine. The machine builds the audience."
- "Inbound doesn't happen to you. You build toward it."
- "The compounding starts the day you stop treating content like a task."
- "Most people quit at day 60. That's why day 90 is so quiet."
- "The system works. You just have to run it."
- "Visibility isn't luck. It's infrastructure."

A conviction close is NOT:
- A question ("What would change for you if...")
- A CTA ("Comment X if you want...")
- A hedge ("This worked for me, might not work for everyone")
- An invitation ("I'd love to hear your thoughts")

If the brand profile specifies a Default-CTA, use it sparingly (at most 1 in every ~5 posts) and never as engagement bait.

---

## Step 4: Schedule (only if a scheduler is configured)

If no scheduler is configured, skip this step — save the batch (Step 5) and tell the user to publish manually.

### 1 post/day at `$POST_TIME_UTC` (default 21:00 UTC / 2pm PT)

For post index `i`, starting from `base_date` (day after last scheduled):
- `scheduled_time = base_date + timedelta(days=i) at POST_TIME_UTC`

The example below targets a Blotato-compatible endpoint. Adapt `url`, headers, and the `create_post` argument shape to your scheduler.

```python
import json, urllib.request, time, os

def schedule_linkedin_post(index, text, scheduled_time, api_key, api_url, account_id):
    payload = {
        "jsonrpc": "2.0",
        "id": index + 1,
        "method": "tools/call",
        "params": {
            "name": "blotato_create_post",
            "arguments": {
                "accountId": account_id,
                "platform": "linkedin",
                "text": text,
                "mediaUrls": [],
                "scheduledTime": scheduled_time
            }
        }
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        api_url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "blotato-api-key": api_key
        }
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode('utf-8')
        for line in raw.strip().split('\n'):
            clean = line[6:] if line.startswith('data: ') else line
            try:
                obj = json.loads(clean)
                if 'result' in obj:
                    return True, "scheduled"
                elif 'error' in obj:
                    return False, obj['error'].get('message', 'error')
            except:
                pass
    return True, "scheduled"

# api_key = os.environ["SCHEDULER_API_KEY"]
# api_url = os.environ["SCHEDULER_API_URL"]
# account_id = os.environ["LINKEDIN_ACCOUNT_ID"]
```

Add `time.sleep(0.3)` between calls. Print `[OK] #N scheduled_time — first 60 chars...` for each. Print final summary: `Scheduled: X/35`.

---

## Step 5: Save the Batch Locally

Save the full batch to:
`~/content/linkedin-post-batch-[N].md` (or wherever the user keeps content).

```markdown
---
tags: [content, linkedin, batch-0N]
source: brand-profile
updated: YYYY-MM-DD
status: scheduled | drafted
schedule: [START_DATE] through [END_DATE], 1/day at [POST_TIME]
---

# LinkedIn Post Batch [N]

35 posts. [START] through [END]. 1/day at [POST_TIME].

## FA — Results Hook + System Reveal ([count])
[numbered list]

## FB — Personal Story Arc ([count])
...

## FC — Customer Transformation ([count])
...

## FD — Contrarian Conviction ([count])
...
```

---

## Step 6: Report Back

One line, e.g.: "LinkedIn Batch 02 scheduled: 35 posts, June 3 through July 7. 0 failures." If scheduling was skipped, say: "LinkedIn Batch 02 generated and saved: 35 posts. Scheduler not configured — publish manually."
