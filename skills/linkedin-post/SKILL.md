---
name: linkedin-post
description: Write and publish a LinkedIn post in YOUR brand voice. Use this skill whenever the user asks to "write a LinkedIn post", "draft a post", "create content about X", "write something for LinkedIn", "find trending topics", "scrape Reddit for post ideas", or "publish to LinkedIn". Always trigger for LinkedIn content creation or publishing — even casual requests like "write a post about my new offer", "what's trending on Reddit", or "publish this to LinkedIn".
---

# LinkedIn Post Writer & Publisher

Full pipeline: Reddit topic discovery → write in the user's voice → optionally publish to LinkedIn.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

## Requirements

- **Reddit scraping (Phase 1):** none. Uses Reddit's public JSON API via `curl`. No key needed.
- **Publishing to LinkedIn (Phase 3) — OPTIONAL:** the content-generation value works with zero setup. To auto-publish, you need a social publishing API (the script supports any provider that has a REST post endpoint). Set these env vars:
  - `SOCIAL_API_KEY` — your publishing provider's API key
  - `SOCIAL_API_URL` — your provider's post endpoint (e.g. `https://backend.yourprovider.com/v2/posts`)
  - `LINKEDIN_ACCOUNT_ID` — your LinkedIn account ID in that provider
  - If any are not set, I'll skip publishing, hand you the finished post to paste manually, and tell you exactly what to add.
- **Comment-to-DM automation (Phase 4) — OPTIONAL:** if you use a LinkedIn auto-DM tool (comment a keyword → auto-DM the link), set `AUTODM_API_KEY` and `AUTODM_API_URL`. If not set, I'll skip it and note it.

---

## Phase 0: Load Intelligence & Apply Positioning Filter

**First, apply the positioning filter as a silent hard gate.** If you have the **positioning-filter** skill installed (or a saved positioning statement at `~/offers/positioning.md`), use it. Otherwise apply this 3-question test to every topic silently:
1. What's the unique angle only this user can take?
2. Why would their audience care (does it hit a real pain)?
3. How does it ladder to their offer?

Never ask the user how a topic connects to their brand — figure it out from the brand profile and apply it. If a topic genuinely can't be connected to their positioning, say so and suggest a reframe.

**Then load context from the brand profile** (`~/.claude/brand-profile.md`). The fields this skill leans on:
- **Audience** + **Main-pain** — who you're writing for; the pain the hook names
- **Offer(+price)** + **Transformation** — where the CTA points and the payoff it promises
- **Tone**, **Words-to-love**, **Words-to-avoid** — how it should sound
- **Proof/wins** + **Credentials** — the proof anchor that earns the CTA
- **Default-CTA**, **Booking/checkout link**, **Social-handles**, **Website**

If the user keeps a content log (e.g. `~/content/linkedin-post-log.md`), read it to avoid repeating angles, emotions, or anchors too close together. Create it on first publish if it doesn't exist.

**How to apply when writing:**
- Hooks should use the audience's own language (their Main-pain, verbatim), not marketing language.
- Story and lesson angles land hardest when built on a real moment the user has lived or coached — pull from their Proof/wins, never invent.
- Weight proven formats higher and rotate deliberately (see the content log).

---

## Proof Anchor (Required — Pick Before Writing)

Every post needs one anchor, drawn from the brand profile's **Proof/wins** and **Credentials**. Pick the anchor, build the post around it, never invent proof.

**Before picking anything:** if a content log exists, don't repeat the same audience emotion, anchor type, or topic angle used in the last 10 posts. Rotate.

**How to choose (match to the post angle):**
- Post angle is the user's own result, system, or experiment → **Personal story** (default — most authentic, highest-performing)
- Post angle is "look what's possible" or an audience transformation → **Client/member win or testimonial** (use their verbatim language when available in Proof/wins)
- Post angle is a common mistake, pattern, or insight → **Teaching moment** (positions the user as the expert who sees across many people they've helped)

When in doubt: default to personal story. The anchor goes in the body, after the hook.

---

## Phase 1: Topic Discovery (when no topic is given)

When the user says "write me a post for today" without a topic, run this flow:

**Step 1 — Scrape Reddit for what the audience is talking about right now:**

```bash
python3 scripts/scrape_reddit.py --from-config
```

**Scrape a specific subreddit:**
```bash
python3 scripts/scrape_reddit.py SaaS
```

**Options:** `--time day|week|month` · `--sort top|hot|rising` · `--show N` · `--flat` · `--url`

**Adding subreddits**: Edit `references/subreddits.json` — add a new entry to the `"subreddits"` array. Tailor the list to the user's Audience.

**Step 2 — For each top thread, ask: does this match a pain the user has lived or solved?**
Look for threads where the audience is expressing a pain that maps to the brand profile's Main-pain. The goal is a real conversation happening right now, connected to the user's story or a client result. Trending pain + the user's proof = timely and personal.

If Reddit doesn't surface a strong match, fall back to **Path B**: pick a recurring pain from the brand profile's Main-pain and treat it as the topic. Evergreen pain + fresh proof = still a strong post.

**Step 3 — Present 3 options, pre-angled:**
Don't show a raw list of Reddit threads. Show 3 post angles, each with:
- The audience pain it taps (one line, their language)
- The user's proof anchor (personal story / client win / teaching moment)
- Proposed hook (one sentence)

Ask: "Which of these? Or tell me the angle you want." Wait for the user to choose before writing.

---

## The Core Post Logic (Apply to Every Post)

Every post follows one underlying structure, regardless of topic or format:

**Audience pain → the user's proof → their offer as the bridge**

| Post element | What it does | Where it comes from |
|---|---|---|
| Hook | Names the pain the audience already feels | Audience language from the profile or Reddit |
| Setup line | Creates a scroll-stop ("Here's what changed:") | Fixed formula |
| Body | The user's proof that it's solvable | Proof anchor (personal story / client win / teaching moment) |
| Pivot | The insight or shift that made it possible | One sentence — the "a-ha" |
| Payoff | What the audience gets with the same shift | Their dream outcome, in their language (Transformation) |
| CTA | The offer as the path to that outcome | The user's Default-CTA — usually a comment "KEYWORD" mechanic |

**Audience emotions to activate (one per post — don't try to hit all of them):**
- **Fear:** "I'm falling behind / wasting time / invisible"
- **Frustration:** "I'm doing the work and seeing nothing"
- **Aspiration:** the audience's dream outcome (from Transformation)
- **Identity:** "I want to be someone who can actually do this"
- **Relief:** "What if this could be easier than I thought"

Pick the one that best fits the proof anchor. The hook names it. The body resolves it.

---

## Phase 2: Write the Post

Once a topic is confirmed, write the LinkedIn post following all rules below. Show the finished post to the user and ask:

> "Ready to publish now, schedule it, or just keep the draft?"

---

## Phase 3: Publish (OPTIONAL)

Only runs if the publishing env vars are set (see Requirements). If they're not, hand the user the finished post to paste manually and tell them what to add.

### Step 1 — Generate CTA Keyword

Pick a fun, non-offensive noun (food item, animal, object — e.g. `WAFFLE`, `GIRAFFE`, `PICKLE`, `FLAMINGO`, `NUGGET`). Easy to type, makes people smile. Doesn't need to relate to the post topic.

**Before choosing:** if the user keeps a keyword/funnel log, read it and make sure your chosen keyword isn't already in use. Pick a different word on collision.

The keyword goes in the post CTA: `Comment "KEYWORD" and I'll send you the link.`

### Step 2 — Publish via your provider's API

**Default behavior: always schedule. Never post immediately unless the user explicitly says "post now" or "publish now".**

If no time is given, ask when they want it to go out (offer their usual cadence if the profile records one).

Generic publish call — works with any provider that exposes a REST post endpoint. Read the account ID and key from env, never hardcode them:

```bash
# TODO: set these in your environment for your publishing provider
: "${SOCIAL_API_KEY:?set SOCIAL_API_KEY}"
: "${SOCIAL_API_URL:?set SOCIAL_API_URL}"
: "${LINKEDIN_ACCOUNT_ID:?set LINKEDIN_ACCOUNT_ID}"

# To schedule (default) — adjust the JSON shape to your provider's schema
curl -s -X POST "$SOCIAL_API_URL" \
  -H "Authorization: Bearer $SOCIAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"accountId\": \"$LINKEDIN_ACCOUNT_ID\",
    \"platform\": \"linkedin\",
    \"content\": {\"text\": \"<post text>\", \"mediaUrls\": []},
    \"scheduledTime\": \"YYYY-MM-DDTHH:MM:SSZ\"
  }"

# To post immediately — omit scheduledTime
```

Post to the **personal profile** by default. **Store the post/submission ID** from the response — needed for Phase 4.

> Many publishing providers (Buffer, Publer, Typefully, and others) offer an MCP server or REST API. If you have one configured as an MCP tool, call that instead of curl — same fields (account ID from env, platform `linkedin`, text, optional `scheduledTime`).

### Step 3 — Confirm and Log

- If scheduled → confirm the date/time.
- If posted immediately → poll status until published, then report the public URL.

**After confirming:** if the user keeps a content log (`~/content/linkedin-post-log.md`), append a row with today's date, the hook (first line), the audience emotion targeted, the anchor type/used, the topic/angle, and the CTA keyword. Do this automatically. Also append the keyword to their keyword/funnel log so future runs avoid collisions.

**Important**: Strip the `---` hook-formula note from the bottom of the post before publishing. Only the post body goes to LinkedIn.

---

## Phase 4: Wire Comment-to-DM Automation (OPTIONAL)

If the user runs a LinkedIn comment-to-DM tool, this auto-DMs anyone who comments the keyword. Only runs if `AUTODM_API_KEY` and `AUTODM_API_URL` are set — otherwise skip and note it.

**HARD GATE — do not start until the real LinkedIn post URL is resolved** (not a generic feed URL). Poll your publishing provider's status endpoint until the post is published and returns a public URL.

### DM Templates (built from the brand profile)

Pull the **Offer(+price)**, **Booking/checkout link**, and **Transformation** from the profile. Never hardcode a specific offer.

**Initial DM (sent immediately on keyword comment):**
```
Hey {{firstName}}!

Here's the link: {{Booking/checkout link}}

{{One line on the offer + price and what's inside, from the profile}}

See you inside.
```

**Follow-up DM (sent ~72 hours later, only if they haven't replied):**
```
Hey {{firstName}}, quick question — {{a segmenting question that maps to the two things the audience is usually trying to do}}. Which one's you?
```

The follow-up question segments leads invisibly and moves the conversation to the primary inbox once they reply.

### Create the automation

```bash
: "${AUTODM_API_KEY:?set AUTODM_API_KEY}"
: "${AUTODM_API_URL:?set AUTODM_API_URL}"

# Shape the JSON to your comment-to-DM provider's schema.
curl -s -X POST "$AUTODM_API_URL" \
  -H "Authorization: Bearer $AUTODM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "[POST TOPIC] — [KEYWORD]",
    "post_id": "<LinkedIn post URN or activity id>",
    "linkedin_post_url": "<POST_URL>",
    "keywords": ["KEYWORD"],
    "dm_template": "<initial DM from above>",
    "auto_connect": true,
    "enable_follow_up": true,
    "follow_up_template": "<follow-up DM from above>",
    "follow_up_delay_minutes": 4320
  }'
```

`follow_up_delay_minutes: 4320` = 72 hours. A `409` usually means the automation already exists for this post — treat as success.

If `AUTODM_API_KEY` is not set, log a warning and skip. Never block publishing on this step.

---

## The Most Important Thing: The Hook

The hook is the first 1-2 lines. It must stop the scroll. LinkedIn shows only these lines before "see more."

**Hook selection process — run this every time, in order:**

**Step 1 — Identify the content type of the post:**
- Metric outcome / before-after result → Results-First / Before-After Transformation
- Giving away a resource or guide → Effort Proof + Free Resource
- Tool or model just dropped → Breaking News + Speed Flex
- Result + removing an excuse → Results-First + Permission Removal
- Cost contrast (cheap new way vs. expensive old way) → Bold Claim + Cost Contrast
- Honest gap or self-audit → Confession / Gap Reveal
- Contrarian take on common advice → DON'T Do X — Do Y Instead
- Core psychological block (invisibility, fear) → Intimidation Barrier Opener
- Authority proof + bold claim → Authority Proof + Bold Claim

**Step 2 — Adapt, don't copy.** Shape the hook to the specific post; never reuse a template verbatim.

**Step 3 — Rotate.** If the same pattern (or audience emotion, or anchor) shows up in the last 2-3 posts in the content log, force a different one. The goal is variety within what's proven.

**Hook rules (apply to every hook regardless of pattern):**
- One sentence. Two max.
- Specific number, dollar amount, timeframe, or result. Never vague.
- First person ("I") — never third-person, never a quote.
- No ellipsis, no exclamation marks. Confident, not hyped.
- Only use numbers the user can verify (from Proof/wins). Never fabricate a stat.
- If the pattern doesn't yield a strong first line, try the next best match — don't force a weak hook to fit a pattern.

---

## Post Structure & Voice

Read both sub-files before writing:

- `formats.md` — Format A/B/C/D with full templates, objection remover rules, proof anchor guidance
- `voice.md` — voice, tone, formatting rules, output format

Also read `references/example-posts.md` before writing — internalize the rhythm and brevity, then write in the user's own tone (Words-to-love / Words-to-avoid from the profile).
