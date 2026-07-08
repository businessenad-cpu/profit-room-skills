---
name: content-engine
description: "Turn a YouTube video into a full set of multi-platform content written in YOUR brand voice — LinkedIn (personal + optional company page), Facebook, X/Twitter, Instagram + TikTok carousels, Pinterest, Reddit, a short-form clip brief, and an optional free resource guide. Fetches the transcript automatically and generates every piece. Direct publishing is OPTIONAL: if you've connected a social scheduler and other integrations it can post for you, otherwise it saves everything locally to paste yourself. Trigger on phrases like 'run the content engine', 'content engine for my video', 'generate content from my video', 'repurpose this video', 'turn this video into content', 'run on my latest video', or any request to turn a YouTube video into multi-platform content."
---

# Content Engine

Turn one YouTube video into a full multi-platform content run written in *your* voice.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

The skill reads these brand-profile fields and uses them everywhere copy is generated: **Name**, **Audience**, **Offer**, **Transformation**, **Tone**, **Words-to-avoid**, **Default-CTA**, **Main-platforms**, **Social-handles**. Wherever this doc says "your offer", "your audience", "your CTA", etc., pull the real value from the profile — never hardcode a name, brand, or number.

---

## Requirements

**Everything generates and saves locally with zero setup.** The publishing integrations below are all *optional* — each step checks for its env vars and, if they're missing, writes the finished content to a file and flags it in the summary instead of failing.

| Integration | What it powers | Env vars / setup |
|---|---|---|
| **Social scheduler** (e.g. Blotato) | Direct publishing to LinkedIn / Facebook / Instagram / TikTok / X / Pinterest, and transcript fetch | `BLOTATO_API_KEY` + one account ID per platform you use (see below) |
| **Gumroad** | Auto-publishing the free resource guide | Run `scripts/gumroad-save-session.py` once (saves a gitignored browser session). Optionally `GUMROAD_SUBDOMAIN` (your `<name>.gumroad.com` handle) so links resolve |
| **Reddit** | Auto-posting to a subreddit | `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD` |
| **ManyChat** | Instagram comment-to-DM funnel | The `manychat` skill / a logged-in ManyChat browser profile. Optional `MANYCHAT_ACCOUNT_ID` for the funnel helper script |
| **LinkedIn auto-DM** (e.g. LeadShark) | Auto-DM commenters who use your keyword on the LinkedIn post | `LEADSHARK_API_KEY` |
| **YouTube Data API** | `scripts/check-new-video.py` new-upload detection | `YOUTUBE_API_KEY` + `YOUTUBE_CHANNEL_ID` |
| **Notion** (optional) | If you keep a content archive in Notion | `NOTION_TOKEN` + your database ID |

**Social scheduler account IDs** — set only the platforms you post to. Each maps to a connected account inside your scheduler:

```
BLOTATO_API_KEY
BLOTATO_LINKEDIN_ACCOUNT_ID        # your personal LinkedIn
BLOTATO_LINKEDIN_PAGE_ID           # optional: a company/second page (same account ID + this pageId)
BLOTATO_FACEBOOK_ACCOUNT_ID
BLOTATO_FACEBOOK_PAGE_ID
BLOTATO_INSTAGRAM_ACCOUNT_ID
BLOTATO_TIKTOK_ACCOUNT_ID
BLOTATO_TWITTER_ACCOUNT_ID
BLOTATO_YOUTUBE_ACCOUNT_ID
BLOTATO_PINTEREST_ACCOUNT_ID
BLOTATO_PINTEREST_BOARD_ID
```

Load your keys from a file you keep out of version control (e.g. `~/.claude/.env`) before any shell step that needs one:

```bash
set -a && source ~/.claude/.env && set +a
```

**Graceful fallback:** if none of these are set, the skill still runs end to end — it generates every piece of content, saves each to `~/content/<date>-<slug>/`, and the summary lists exactly what to paste where.

---

## Execution Model

The pipeline has hard dependencies at the start and end; the middle is independent and **should run in parallel**.

```
Phase 1 — Sequential (must complete in order):
  Step 1 → Step 2 → Step 3 → Step 4

Phase 2 — Parallel launch (fire ALL as simultaneous tool calls after Step 4):
  ├── LinkedIn personal post
  ├── LinkedIn company-page post (only if a page is configured)
  ├── Facebook post
  ├── X/Twitter thread
  ├── Pinterest pin
  ├── Reddit post
  ├── Short-form clip brief (writing only — no publish)
  ├── Resource guide HTML + description (tutorial only)
  └── Carousel images ← start first, it's the slowest

Phase 3 — After carousel images are ready:
  ├── Instagram carousel
  ├── TikTok carousel (reuses the same images)
  └── LinkedIn carousel scheduled 48h out (reuses the same images)

Phase 4 — Optional automation wiring (only if the relevant integration is configured):
  ├── ManyChat funnel (after Instagram publishes)
  └── LinkedIn auto-DM (after the LinkedIn post URL AND the guide URL both resolve)

Phase 5 — Summary report + local archive
```

**Critical execution rule:** In Phase 2 do NOT wait for one post to finish before starting the next — fire them all as simultaneous tool calls in a single turn. Any step whose integration isn't configured just writes its content to a file and continues.

---

## Pipeline

### Phase 1 — Setup (Sequential)

### Step 1 — Get the Video

**If a URL is provided**, use it directly.

**If "latest video" or no URL**, auto-detect from the user's channel. Get the handle from the brand profile's **Social-handles** (YouTube), or ask once:
```bash
yt-dlp --flat-playlist --playlist-end 1 --print url --print title "https://www.youtube.com/@YOUR_HANDLE/videos"
```
First line = URL, second line = title. Confirm: "Found your latest video: [TITLE]. Running the content engine on this one."

Extract the **Video ID** (11-character YouTube ID) from the URL.

**Thumbnail URL:** `https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg`

---

### Step 2 — Fetch Transcript

If a social scheduler with transcript support is configured (e.g. Blotato `blotato_create_source`), use it:

```json
{ "sourceType": "youtube", "url": "<youtube-url>" }
```

Otherwise (or if it fails), fall back to yt-dlp:

**Method A — original captions:**
```bash
yt-dlp --write-sub --sub-lang en-orig --skip-download --sub-format json3 -o "/tmp/yt-transcript" "<youtube-url>"
```

**Method B — auto-generated:**
```bash
yt-dlp --write-auto-sub --sub-lang en --skip-download --sub-format json3 -o "/tmp/yt-transcript" "<youtube-url>"
```

Parse json3:
```bash
node -e "
const fs = require('fs'), path = require('path'), dir = '/tmp';
const file = fs.readdirSync(dir).find(f => f.startsWith('yt-transcript') && f.endsWith('.json3'));
if (!file) { console.error('No subtitle file found'); process.exit(1); }
const data = JSON.parse(fs.readFileSync(path.join(dir, file), 'utf8'));
const text = data.events.filter(e => e.segs).map(e => e.segs.map(s => s.utf8 || '').join('')).join(' ').replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();
console.log(text);
"
```

**Validation:** Sanity-check the first 2 sentences against the video title. If the transcript doesn't match → try the next method.

If all methods fail:
> "Captions aren't available yet — YouTube takes 30-60 minutes after upload. Try again in a bit."

Do NOT proceed without a transcript.

---

### Step 3 — Metadata and Classification

Extract:
- **Video ID** — 11-character YouTube ID
- **Video title** — from Step 1 or `yt-dlp --get-title "<url>"`
- **Slug** — lowercase-hyphenated, max 50 chars
- **Date** — today's date YYYY-MM-DD
- **Video length** — approximate from transcript word count (150 wpm)
- **CTA Keyword** — a random, fun, non-offensive word. Think silly nouns: food, animals, objects (e.g. `WAFFLE`, `GIRAFFE`, `PINEAPPLE`, `MANGO`, `PICKLE`, `FLAMINGO`, `NUGGET`, `ROCKET`). Easy to type in a comment and makes people smile. It does NOT need to relate to the topic.

  **Keep keywords unique.** If you use a comment-to-DM tool (ManyChat / LinkedIn auto-DM), each funnel needs its own keyword so comments route correctly. Check any log you keep of used keywords and pick a fresh word if there's a collision.

**Classify as tutorial or discussion:**

**Tutorial** → generates everything, including the resource guide:
- Step-by-step instructions, how-to framing, tool setup, walkthroughs, demos
- Viewer is expected to follow along or replicate something

**Discussion** → text posts + carousel, no resource guide:
- Opinions, predictions, reactions, industry analysis, comparisons
- Viewer consumes a perspective, not a process

Log the classification and CTA keyword — they appear in the Step 12 summary. Do not pause here.

---

### Step 4 — Create Output Folder
```bash
mkdir -p ~/content/YYYY-MM-DD-SLUG
```

---

### Phase 2 — Parallel Launch (fire ALL simultaneously after Step 4)

**Start carousel image generation first** (it's the slowest), then fire all remaining Phase 2 items in the same turn. Do not wait for any one post to finish before firing the others.

Everywhere below: write copy in the brand profile's **Tone**, respect **Words-to-avoid**, and use the **Default-CTA** unless a step specifies a keyword CTA. Only cite proof/numbers that exist in the profile's **Proof** section — never invent them.

### Step 5 — Generate LinkedIn Post(s)

**Generate a personal post always.** If `BLOTATO_LINKEDIN_PAGE_ID` (a company/second page) is configured, also generate a second, differently-angled page post.

#### Personal LinkedIn — Lead Magnet Format

- **Hook** — transformation or big-number (never a bland "I" statement — those get far less reach). Transformation pattern: "I went from [before] to [after] in [timeframe]." Big number: lead with the metric, impossible to scroll past. Use only real numbers from the profile's Proof; if you have none, use a curiosity/insight hook instead.
- **Second line** — "Here's X:" or "Here's how:"
- **Body** — 5-7 bullet points using `→` (never `-` or `*`). Each 8-15 words, concrete and specific.
- **Payoff line** — one line connecting the content to the reader's outcome (the profile's **Transformation**).
- **CTA** — for a lead-magnet post: exactly `Comment "[KEYWORD]" and I'll send it over.` (keyword from Step 3). Otherwise use the profile's **Default-CTA**.
- **Length** — 150+ words (long posts out-reach short ones).
- **Formatting** — no markdown, no bold, no italics. Whitespace between every sentence group. `→` bullets only.

For discussion videos: transformation hook with a soft CTA pointing to the video instead of a keyword trigger. No lead-magnet offer.

#### Company / Second Page (optional) — Value-Driven Format

No lead-magnet CTA. This audience is followers of your brand — give value and speak to their transformation.

- **Hook** — what this means for your **Audience** trying to reach the goal in your **Transformation**. Frame around the outcome, not the tool.
- **Body** — explain what the build/idea does and why it matters for their situation. Speak directly to your ICP.
- **Tone** — practitioner to practitioner. Not hype, not salesy. "Here's why this matters for you" energy.
- **Bullets** — `→` format, 5-6 points, focused on what the reader can apply or understand.
- **Closing line** — one sentence connecting back to your **Offer**'s mission.
- **No keyword CTA.** End with a soft engagement prompt or a pointer to the full video.
- **Length / formatting** — same as personal.

**Publish (optional — only if `BLOTATO_LINKEDIN_ACCOUNT_ID` is set):**

```json
// Personal LinkedIn
{
  "accountId": "<BLOTATO_LINKEDIN_ACCOUNT_ID>",
  "text": "<personal post — lead magnet format>",
  "imageUrls": ["https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg"]
}

// Company / second page (only if BLOTATO_LINKEDIN_PAGE_ID is set)
{
  "accountId": "<BLOTATO_LINKEDIN_ACCOUNT_ID>",
  "pageId": "<BLOTATO_LINKEDIN_PAGE_ID>",
  "text": "<page post — value-driven format>",
  "imageUrls": ["https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg"]
}
```

Use `blotato_create_post` for each. **Store the full result** — you need the `postSubmissionId` (and the post URL once published) for the optional LinkedIn auto-DM wiring in Step 11. If no URL comes back immediately, note the `postSubmissionId` and poll `blotato_get_post_status` before Step 11.

If no scheduler is configured, save the copy and move on. Always save to `~/content/YYYY-MM-DD-SLUG/linkedin.md`.

---

### Step 6 — Facebook Post

Facebook tone: casual, community-oriented, not professional-network energy.

Write a post that:
- Leads with the most surprising or useful insight from the video
- Is conversational, not salesy
- Ends with a question to drive comments
- Final line: `Comment [KEYWORD] below and I'll send you the full video link 👇` (keyword from Step 3)

Keep under 300 words. No emojis unless the content calls for it.

**Publish (optional — only if `BLOTATO_FACEBOOK_ACCOUNT_ID` + `BLOTATO_FACEBOOK_PAGE_ID` are set):**

```json
{
  "accountId": "<BLOTATO_FACEBOOK_ACCOUNT_ID>",
  "pageId": "<BLOTATO_FACEBOOK_PAGE_ID>",
  "text": "<post content>"
}
```

Save to `~/content/YYYY-MM-DD-SLUG/facebook.md`.

---

### Step 6b — X (Twitter) Post

X rewards sharp opinions and build-in-public content. No lead-magnet mechanic — just a punchy take that drives follows and engagement.

**Main post:**
- 1-3 lines max, under 280 characters.
- Lead with the most counterintuitive or surprising thing about the build — the "wait, that's possible?" moment.
- No link in the main post (it suppresses reach). End with "🔗 in replies" or "link in thread".
- Tone: builder to builder. Direct. No hype words.

**Self-reply (thread post):**
- YouTube URL on its own line
- One-line description of what they'll find in the video

**Publish (optional — only if `BLOTATO_TWITTER_ACCOUNT_ID` is set):**

```json
{
  "accountId": "<BLOTATO_TWITTER_ACCOUNT_ID>",
  "platform": "twitter",
  "text": "<punchy take — no link — ends with '🔗 in replies'>",
  "mediaUrls": [],
  "additionalPosts": [
    { "text": "https://www.youtube.com/watch?v=VIDEO_ID\n\n<one-line video description>" }
  ]
}
```

`additionalPosts` creates the thread automatically — main tweet first, then the reply. Save to `~/content/YYYY-MM-DD-SLUG/twitter.md`.

---

### Step 7 — Instagram Carousel

**Invoke the `carousel-creator` skill (if available) to generate rendered slide images.** Do not hand-write slide copy — the carousel skill handles design, rendering, and upload. If you don't have a carousel skill, write the per-slide copy to file and note that slides need to be designed manually.

Pass to the carousel skill:
- The full transcript (or key insights from Step 3)
- Video title
- Instruction: "step-by-step framework, 7 slides, cta_keyword: [KEYWORD from Step 3]" (plus your own design system if you have one)

Once you have hosted image URLs, publish via your scheduler:

```json
{
  "accountId": "<BLOTATO_INSTAGRAM_ACCOUNT_ID>",
  "text": "<caption>",
  "imageUrls": ["<slide1-url>", "<slide2-url>", "..."]
}
```

**Caption format (Instagram):**
```
[Hook line from slide 1]

[2-3 line value tease]

Comment [KEYWORD] and I'll send you the full breakdown 👇

Full video → link in bio

[5 relevant hashtags for your niche]
```

Save to `~/content/YYYY-MM-DD-SLUG/instagram-carousel.md` (slide content + caption).

---

### Phase 3 — After Carousel Images Are Ready

### Step 8 — TikTok Carousel

TikTok reuses the same slide images as Instagram — reuse the hosted URLs from Step 7, no re-render.

**Publish (optional — only if `BLOTATO_TIKTOK_ACCOUNT_ID` is set):**
```json
{
  "accountId": "<BLOTATO_TIKTOK_ACCOUNT_ID>",
  "text": "<caption>",
  "imageUrls": ["<slide1-url>", "<slide2-url>", "..."]
}
```

**Caption format (TikTok):**
```
[Hook line — slightly more casual than Instagram]

[2-3 lines value tease]

Comment [KEYWORD] and I'll send you the full breakdown 👇

[5 relevant hashtags for your niche]
```

> **Note:** Short-form VIDEO posts to TikTok are Phase 2 of *your* workflow — only after you edit the clips. This step covers photo carousels only.

---

### Step 8d — Schedule LinkedIn Carousel (48 hours)

Reuse the same hosted carousel image URLs from Step 7. Schedule them as a LinkedIn personal post 48 hours out so the same content gets a second wave.

**Calculate `scheduledTime`:**
```bash
python3 -c "
from datetime import datetime, timezone, timedelta
t = datetime.now(timezone.utc) + timedelta(hours=48)
print(t.strftime('%Y-%m-%dT%H:%M:%SZ'))
"
```

**Publish (optional — only if `BLOTATO_LINKEDIN_ACCOUNT_ID` is set):**
```json
{
  "accountId": "<BLOTATO_LINKEDIN_ACCOUNT_ID>",
  "platform": "linkedin",
  "text": "<caption>",
  "imageUrls": ["<slide1-url>", "<slide2-url>", "..."],
  "scheduledTime": "<ISO-8601-48h-from-now>"
}
```

**Caption format (LinkedIn carousel — professional tone, same keyword CTA):**
```
[Hook line — transformation or big number, same style as Step 5 personal but a fresh angle]

[4-6 bullet points using → format — a different angle than the original LinkedIn post]

Comment "[KEYWORD]" and I'll send it over.
```

Do NOT reuse the same hook or bullets from the initial LinkedIn personal post — this appears 48 hours later to a partially overlapping audience. Pick a different angle on the same content.

**Auto-DM note:** the scheduled carousel will have its own post URL and its own commenters, so it needs its own auto-DM automation once it publishes. Add a reminder to `~/content/YYYY-MM-DD-SLUG/auto-dm.md`:

```
## LinkedIn Carousel (scheduled — 48h)
Status: PENDING — wire the auto-DM after the post publishes on [DATE+48H]
Keyword: [KEYWORD]
Action: Run Step 11 logic against the carousel post URL once live
```

Save the scheduled post's `postSubmissionId` to `~/content/YYYY-MM-DD-SLUG/linkedin.md`.

---

### Step 8b — Pinterest Pin

Pinterest gets the video thumbnail as a static pin linked back to the video.

**Most schedulers require a hosted image — do NOT pass the raw `i.ytimg.com` URL directly** (it fails with "unsupported media source type"). Upload it first.

**Upload the thumbnail to your scheduler:**
```bash
# 1. Get a presigned upload URL from your scheduler (e.g. Blotato)
curl -s -X POST "https://backend.blotato.com/v2/media/presigned-url" \
  -H "blotato-api-key: $BLOTATO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"filename": "thumbnail.jpg"}'
# → save presignedUrl and publicUrl from the response

# 2. Download the thumbnail locally
curl -s -o /tmp/yt-thumbnail.jpg "https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg"

# 3. PUT the raw bytes to the presigned URL
curl -s -X PUT "<presignedUrl>" --data-binary "@/tmp/yt-thumbnail.jpg" -H "Content-Type: image/jpeg"
```

(Or use `blotato_create_presigned_upload_url` with filename `"thumbnail.jpg"`.) The `publicUrl` is what goes into `mediaUrls`.

**Publish (optional — only if `BLOTATO_PINTEREST_ACCOUNT_ID` + `BLOTATO_PINTEREST_BOARD_ID` are set):**
```json
{
  "accountId": "<BLOTATO_PINTEREST_ACCOUNT_ID>",
  "boardId": "<BLOTATO_PINTEREST_BOARD_ID>",
  "title": "<pin title>",
  "text": "<pin description>",
  "mediaUrls": ["<hosted-publicUrl>"],
  "link": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Pin description format:**
```
[One-line hook — what the viewer will learn or build]

[2-3 sentence value summary — specific and concrete, no fluff]

Full tutorial → link above

[5 relevant hashtags for your niche]
```

Save to `~/content/YYYY-MM-DD-SLUG/pinterest.md`.

---

### Step 8c — Reddit Post

Post to **one subreddit**, rotating through a list you maintain. One post per run, never the same subreddit twice in a row (track last used in `~/content/.reddit-last-sub`).

**Example subreddit rotation** (edit for your niche):
```
r/SideProject, r/Entrepreneur, r/artificial, r/automation, r/IMadeThis
```

Pick the subreddit that best matches the video (build/demo → r/SideProject or r/IMadeThis; business/income → r/Entrepreneur; general AI → r/artificial; workflow → r/automation). If no clear match, fall back to rotation order.

#### Reddit Tone Guidelines

Reddit needs a completely different register from LinkedIn — the same copy in LinkedIn voice gets downvoted or removed.

**Voice: raw, specific, builder-to-builder**
- Write like you're telling a friend what you built, not presenting to an audience
- Admit the messy reality ("zero users", "scrappy", "kinda dumb but it worked") — it earns trust
- Specific numbers always: time saved, money made/spent, lines of code, node count
- Short sentences. Paragraph breaks every 2-3 lines
- `→` for list items reads well here too

**Never do:**
- No "game-changer", "revolutionary", "powerful", no hype words
- No CTA, no "join my community", no mention of your paid offer in the post body
- No link to the video in the post body — it goes in the **first comment** only
- No em-dashes
- Don't open with "I built X and you should use it" — start with the situation or the question that sparked it
- No namedropping unless it comes up naturally
- Closing question must be casual and genuine ("Anyone else tried this?"), never "What's your biggest challenge with X?" (reads as AI-written)

**Two formats:**

**Format A: Narrative story** (build demo or launch)
```
[Situation that sparked the build — 1-2 sentences]

[The messy first version]

[What you layered on top → → →]

[The result — specific, honest]

[One genuine reflection on what surprised you]

[Casual closing question]
```

**Format B: Numbered insights list** (learnings / principles video)
```
[Setup line — how long you've been at this / how many you've built]

1. [Bold header]\n[2-3 sentence explanation with a specific number or anecdote]

2. ...

[Casual closing question]
```

**Titles that work:** "I built [specific thing] in [timeframe] — here's how it works" / "N things I learned after [milestone]" / "[Counterintuitive claim] (here's why)". Avoid "How to...", "The Ultimate Guide to...", clickbait superlatives.

**Flair:** "Discussion" for insights posts; no flair or "Project" for builds (check what the subreddit offers).

**First comment (always):**
```
Made a full video on this if you want the step-by-step: [YOUTUBE_URL]
```

#### Publish (optional — only if Reddit env vars are set)

Write the post from the transcript, pick Format A or B, generate a matching title, then:

```bash
python3 ~/.claude/skills/content-engine/scripts/reddit-post.py \
  --title "TITLE" \
  --body "BODY" \
  --subreddit SUBREDDIT \
  --flair "Discussion" \
  --comment "Made a full video on this if you want the step-by-step: https://www.youtube.com/watch?v=VIDEO_ID"
```

Requires: `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD`. If they're missing, save the post content and log a warning — don't block the run.

Update `~/content/.reddit-last-sub` with the subreddit used. Save content to `~/content/YYYY-MM-DD-SLUG/reddit.md`.

---

### Step 9 — Short-Form Clip Brief

Scan the transcript for **3-5 best short-form moments** (30-90 seconds, ~75-225 words each).

**Clip-worthy signals:** self-contained insight, high shock value (surprising stat / counterintuitive take), emotional peak, quotable line, demo reveal that works vertical.

**NOT clip-worthy:** setup without payoff, references to other sections, wide-screen-only walkthroughs.

For each clip:

```
### Clip [N]: [Working Title]

**Timestamps:** [MM:SS → MM:SS] (~X seconds)
**Best for:** [reach / conversions / engagement]

**Hook:**
- Text overlay: "[2-5 words]"
- Spoken: "[First sentence]"

**Transcript excerpt:**
> [Exact words]

**Rewritten script:** [Tightened version / Use as-is]

**Caption:**
[One-line hook]
[1-2 lines value tease]
Follow for more → [your handle from the brand profile]

**Hashtags:** [5 relevant to your niche]

**Phase 2 accounts to post:**
- Instagram Reels → BLOTATO_INSTAGRAM_ACCOUNT_ID
- TikTok video → BLOTATO_TIKTOK_ACCOUNT_ID
- YouTube Shorts → BLOTATO_YOUTUBE_ACCOUNT_ID
```

**Rank:** 1 = best for reach, 2 = best for conversions, 3 = best for engagement.

> **This brief is Phase 2** — post video clips *after* you edit them. Upload the video files via your scheduler at that time.

Save to `~/content/YYYY-MM-DD-SLUG/short-form.md`.

---

### Step 10 — Resource Guide (TUTORIAL ONLY)

**Skip entirely if classified as discussion.**

Generate a standalone reference guide that teaches the *framework, thinking, and process* — the what and the why — so a reader understands the system and wants to watch the video and join your offer.

**If your business model is to sell/gate the exact prompts, plugins, or templates:** teach the framework in the guide and route the reader to your paid offer for the exact copy-paste assets. Replace every "here's the exact prompt" moment with a teaser + a link to your offer. Same rule for the guide's "What's Included". (If you have no such gate, include whatever you're comfortable giving away.)

**Pricing:** pay-what-you-want, minimum $0, suggested $9 (adjust to your offer).

**Embed the YouTube video** in the guide.

**Output as HTML** (style it in your own brand system if you have one):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GUIDE_TITLE_HERE</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 40px 20px; line-height: 1.7; color: #1a1a1a; }
  h1 { font-size: 28px; margin-top: 40px; }
  h2 { font-size: 22px; margin-top: 36px; border-top: 1px solid #e5e5e5; padding-top: 24px; }
  h3 { font-size: 18px; margin-top: 28px; }
  a { color: #0066cc; }
  ul, ol { padding-left: 24px; }
  li { margin-bottom: 6px; }
  code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 14px; font-family: 'SF Mono', Monaco, monospace; }
  pre { background: #f5f5f5; padding: 16px; border-radius: 6px; overflow-x: auto; }
  pre code { background: none; padding: 0; }
  .video-embed { display: block; position: relative; margin: 32px 0; border-radius: 8px; overflow: hidden; text-decoration: none; }
  .video-embed img { display: block; width: 100%; height: auto; }
  .video-embed .play-btn { position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); width: 68px; height: 48px; background: #FF0000; border-radius: 10px; display: flex; align-items: center; justify-content: center; opacity: 0.92; transition: opacity 0.15s; }
  .video-embed:hover .play-btn { opacity: 1; }
  .video-embed .play-btn svg { fill: white; width: 24px; height: 24px; margin-left: 4px; }
  .cta { background: #f0f7ff; border-left: 4px solid #0066cc; padding: 16px 20px; margin: 32px 0; border-radius: 0 8px 8px 0; }
  .cta a { font-weight: 600; }
</style>
</head>
<body>

<h1>GUIDE_TITLE_HERE</h1>
<p><em>A companion guide to the YouTube video below.</em></p>

<a class="video-embed" href="https://www.youtube.com/watch?v=VIDEO_ID" target="_blank" rel="noopener">
  <img src="https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg" alt="Watch on YouTube" loading="lazy">
  <div class="play-btn"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></div>
</a>

<!-- Guide content: h2 sections, step-by-step instructions, code blocks, etc. -->
<!-- Fill in gaps where the video showed things visually — spell out commands, config, setup steps -->

<div class="cta">
  <p><strong>Want to go deeper?</strong> <a href="YOUR_OFFER_LINK">Join [YOUR OFFER]</a> — [one line on the transformation, from your brand profile].</p>
</div>

</body>
</html>
```

Fill `YOUR_OFFER_LINK` and `[YOUR OFFER]` from the brand profile's **Offer** and **Links** (Booking/checkout link). If those are blank, use a plain "watch the video" CTA and flag it.

**Auto-publish to Gumroad (optional):**

Save the guide to `~/content/YYYY-MM-DD-SLUG/SLUG-guide.html`.

**Generate a rich description** and save to `~/content/YYYY-MM-DD-SLUG/gumroad-description.txt`. Format (emoji section headers, bold, `---` dividers):

```
**[emoji] [Section title based on the main framework/skill]**

[1-2 sentence hook: what the reader will be able to do after using this guide]

- [first bullet — text only, no bold markers]
[second bullet — NO leading "- ", the editor continues the list automatically]
[third bullet]

---

**[emoji] [Section title — tools, techniques, or process covered]**

[Hook sentence]

- [first bullet]
[second bullet]

---

**[emoji] What's Included**

- Full step-by-step framework breakdown (the system, the why, the order)
The complete walkthrough so you understand every piece
[If you gate assets: "The exact prompts/templates live inside [your offer]"]

---

[One-line pitch for your offer 👇]
[YOUR_OFFER_LINK]
```

**Format rules (critical for the Gumroad editor):**
- Section headers wrapped in `**...**` → rendered bold
- Only the FIRST item in each bullet list starts with `- `; subsequent items have no prefix (the editor continues the list)
- `---` on its own line → horizontal rule
- No blank lines between bullet items (they cause extra spacing)
- Single blank line between a header and its content, and between a list and the next header

Generate 2-3 sections from the actual video. Keep bullets tight — one line each. Then:

```bash
python3 ~/.claude/skills/content-engine/scripts/gumroad-publish.py \
  --file ~/content/YYYY-MM-DD-SLUG/SLUG-guide.html \
  --title "[VIDEO TITLE] — Free Resource Guide" \
  --description-file ~/content/YYYY-MM-DD-SLUG/gumroad-description.txt \
  --thumbnail "https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg"
```

Requires a saved Gumroad session (run `scripts/gumroad-save-session.py` once). If the script fails or no session exists, save the HTML and note "Upload manually to your Gumroad."

---

### Phase 4 — Optional Automation Wiring

Both automations below are optional and only run if their integration is configured. If not, skip and note it in the summary.

**HARD GATE for the LinkedIn auto-DM — do not start Step 11 until BOTH are true:**
1. `blotato_get_post_status` for the LinkedIn personal post returned a real post URL (not `https://www.linkedin.com/feed/`)
2. The Gumroad publish script returned a confirmed product URL (not a placeholder)

Kick Gumroad off early in Phase 2 so it has time to complete. Never fire an auto-DM with a placeholder URL — most of these tools have no update endpoint, so a wrong URL can't be fixed without deleting and recreating the automation.

### Step 11 — Wire LinkedIn Auto-DM (optional)

**Requires `LEADSHARK_API_KEY` (or your equivalent LinkedIn auto-DM tool). Skip if not set, or if this is a discussion video with no guide.**

The tool auto-DMs anyone who comments the keyword on your personal LinkedIn post.

**1. Resolve the post URN from the tool itself — this is the ONLY authoritative source.**

⚠️ **Do NOT construct the URN by parsing a LinkedIn URL.** LinkedIn's `activity`, `share`, and `ugcPost` URNs use *different numeric IDs* for the same post. Reformatting a number from a `feed/update/urn:li:share:XXXX` URL into `urn:li:ugcPost:XXXX` produces a URN that points at nothing — the tool silently never detects comments and no DMs send. Always pull the `social_id` the tool *itself* indexed, verbatim.

**Primary path — match your post in the tool's index by its first line:**

The tool indexes every post from your connected account within ~1-2 min of publishing. Poll its post-stats endpoint and match on the first line of your post text. Use whatever `social_id` it returns *exactly as-is*.

```bash
for i in {1..12}; do
  match=$(curl -s "https://apex.leadshark.io/api/post-stats" \
    -H "x-api-key: $LEADSHARK_API_KEY" | python3 -c "
import sys, json
hook = '''FIRST_LINE_OF_YOUR_POST'''.strip().lower()
items = json.load(sys.stdin).get('items', [])
m = next((i for i in items if (i.get('text') or '').strip().lower().startswith(hook)), None)
print(json.dumps({'social_id': m.get('social_id'), 'share_url': m.get('share_url')}) if m else '')
")
  if [[ -n "$match" ]]; then echo "MATCH: $match"; break; fi
  sleep 15
done
```

- `social_id` → use **verbatim** as `post_id` (do not reformat).
- `share_url` → use as `linkedin_post_url`.

If after 3 minutes there's still no match, do NOT fall back to constructing a URN. Save the post text + keyword to `auto-dm.md` with status `PENDING — re-run post-stats match`, flag it, and move on. A delayed automation is recoverable; a wrong-URN one is silently dead.

**2. Build the DM template** (tutorial videos):
```
Hey {{firstName}}!

Here's the [VIDEO TITLE] guide + the full video walkthrough:

Guide (free): [GUMROAD_URL]
Video: [YOUTUBE_URL]
[Optional: one line + link to your paid offer]

[One-line value statement summarizing what they'll get]

Enjoy! Let me know if you have any questions.
```

For discussion videos (no guide): skip this step.

**3. Create the automation:**

```bash
curl -s -X POST "https://apex.leadshark.io/api/automations" \
  -H "x-api-key: $LEADSHARK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "[VIDEO TITLE] — [KEYWORD]",
    "post_id": "SOCIAL_ID_VERBATIM_FROM_POST_STATS",
    "linkedin_post_url": "SHARE_URL_FROM_POST_STATS",
    "keywords": ["KEYWORD"],
    "dm_template": "DM_TEMPLATE_HERE",
    "comment_reply_template": [
      "{{fullNameMention}} just sent!",
      "{{fullNameMention}} check your inbox!",
      "{{fullNameMention}} check your DMs!",
      "{{fullNameMention}} sent!"
    ],
    "non_first_degree_reply_template": ["{{fullNameMention}} connect with me!"],
    "auto_connect": true,
    "auto_like": true,
    "enable_follow_up": true,
    "follow_up_template": "Hey {{firstName}}!\n\nDid you get a chance to check it out?",
    "follow_up_delay_minutes": 4320,
    "follow_up_only_if_no_response": false
  }'
```

`follow_up_delay_minutes: 4320` = 72 hours. A `409` means the automation already exists for this post — treat as success. If `LEADSHARK_API_KEY` isn't set, log a warning and skip. Save the automation ID to `~/content/YYYY-MM-DD-SLUG/auto-dm.md`.

---

### Step 11b — Wire ManyChat Funnel (Instagram, optional)

**Requires a configured ManyChat (the `manychat` skill or a logged-in ManyChat browser profile). Skip if not available.** Run for both tutorial and discussion — the Instagram carousel always uses a keyword CTA.

**Context at this point:** Keyword (Step 3), Video title (Step 3), YouTube URL (Step 1), Guide URL (Step 10, tutorial only).

**Generate copy (no approval pause):**
- **Opening DM:** one sentence, curiosity or direct value. One button, max 20 chars. e.g. "Want the free [VIDEO TITLE] guide? Tap below 👇" → button "Send me the link".
- **Link DM:** short delivery, links as buttons only. Button 1: YouTube URL → "Watch the video". Button 2: Guide URL → "Free guide" (tutorial only). Body: "Here you go 👇".
- **Follow-up DM:** one gentle line, no URLs. e.g. "Did you grab it? Link's still above 👆".

Then either invoke the `manychat` skill with this copy, or run `scripts/manychat-funnel.py` (see its header for flags). Save the flow name + keyword to `~/content/YYYY-MM-DD-SLUG/manychat.md`.

---

### Phase 5 — Summary + Archive

### Step 12 — Summary Report

```
## Content Engine Complete — [VIDEO TITLE]

**Video:** [URL]
**Type:** Tutorial / Discussion
**Saved to:** ~/content/YYYY-MM-DD-SLUG/

### Published ✓ (or "Saved locally — paste manually" if no scheduler)
- LinkedIn personal — [post ID / saved]
- LinkedIn page — [post ID / saved / n/a]
- Facebook — [post ID / saved]
- Instagram carousel — [post ID / saved]
- TikTok carousel — [post ID / saved]
- X/Twitter — [post ID / saved]
- Pinterest — [pin ID / saved]
- Reddit — [post URL / saved]

### LinkedIn auto-DM (tutorial only, if configured)
- Keyword / Automation ID / what the DM sends / which post

### LinkedIn Carousel (scheduled) ⏳
- Scheduled 48h out; auto-DM PENDING until it publishes

### ManyChat (if configured)
- Keyword / Flow name / what it sends

### Phase 2 (after you edit clips)
- short-form.md has 3-5 clip briefs → post to Reels / TikTok / Shorts

### Files
linkedin.md, facebook.md, twitter.md, instagram-carousel.md, pinterest.md,
reddit.md, short-form.md, auto-dm.md (tutorial), manychat.md, guide.html (tutorial)

### Pending / manual
- [anything that needs a manual paste or a missing integration]
```

---

### Step 13 — Log the Video Locally (archive)

**Local write only — publishes NOTHING.** Writes one archive card so your other skills can see this video as "already covered."

Write to `~/content/video-archive/[PUBLISH_DATE]-[slug].md` (or your own archive location / Notion DB if you keep one).
- **PUBLISH_DATE** — the video's actual publish date (`YYYY-MM-DD`) from `yt-dlp --print upload_date "<url>"` (returns `YYYYMMDD` → reformat). Fall back to today if unavailable.
- **slug** — kebab-case of the title.

**Idempotent — check before writing.** If a file with the same name (or a `# ` title heading matching this video, case-insensitive) already exists, UPDATE it in place rather than duplicating. Preserve human-added sections; refresh only the fields this skill owns and bump `updated`.

```
---
tags: [youtube, video-archive]
video_id: <11-char YouTube ID>
published: <PUBLISH_DATE — YYYY-MM-DD>
format: <long or short>
topic: <one-sentence topic>
icp: <one-sentence who it's for>
updated: <today YYYY-MM-DD>
source: content-engine
---

# <Video Title>

## Hook
**Format:** <hook type>
"<opening line(s) verbatim from the transcript>"
<one line: the pain/gap + the promise>

## Structure
- <bullets describing the video's segments>

## Frameworks Taught
<any frameworks/systems, distilled>

## ICP Language Captured
- <verbatim audience-language phrases from the transcript, or "- (none captured)">
```

Field notes: `format` = `short` if under ~3 min, else `long`. `topic`/`icp` = one tight sentence each, in your lane. Pull the `## Hook` opening line verbatim. Write with the Write tool (or Edit if updating). Invoke no publishing path here.

---

## Autonomy Rules

- **"Just do everything"** — skip approval pauses, publish where integrations are configured, save all files.
- **Only one piece needed** — still fetch the transcript, generate only that piece.
- **A publish call fails** — log the error, save the content to file, flag it in the summary. Never silently skip.
- **No integrations configured** — generate and save everything locally; the summary tells the user exactly what to paste where.

---

## Voice Guidelines

- Write in the brand profile's **Tone**; honor **Words-to-avoid**.
- Direct, practitioner-to-practitioner. Not influencer energy.
- Avoid by default: "game-changer", "dive deep", "navigate", "it's worth noting", "let's explore", "revolutionize".
- No em-dashes in body copy.
- LinkedIn: short paragraphs (1-3 lines), lots of whitespace, hooks that open a curiosity gap.
- Specific beats vague: "I built this in 2 hours" > "AI can save you time".
- All CTAs funnel to the YouTube video first, your offer second.

---

## Scripts (in `scripts/`)

- `reddit-post.py` — post + first comment via the Reddit API (env-var auth).
- `gumroad-publish.py` — publish the HTML guide to Gumroad (uses a saved browser session).
- `gumroad-save-session.py` — run once to save that session (nothing is hardcoded; the session file is gitignored).
- `manychat-funnel.py` — generic ManyChat comment-to-DM funnel builder (all values passed as flags).
- `check-new-video.py` — detect new uploads on your channel (`YOUTUBE_API_KEY` + `YOUTUBE_CHANNEL_ID`).
- `github-trending.py` — optional daily trending-repo report to feed video ideas.
