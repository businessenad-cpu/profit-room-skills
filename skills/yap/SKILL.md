---
name: yap
description: Create a viral "Yap-style" short-form video for Instagram Reels / TikTok / YouTube Shorts — researches a trending topic in your niche, drafts an engagement-engineered talking-head script using the proven Yap format (contrarian hook + four-part structure), then renders it as a HeyGen avatar speaking the script (9:16, burned-in captions). Use when the user says /yap, "make a yap video", "create a yap-style reel", "yap script + avatar", "talking-head reel about X", or wants an AI-avatar short-form video from a trending topic.
---

# Yap — Viral Talking-Head Reel Generator

Turns a trending niche topic into a finished AI-avatar Reel: **research → script → HeyGen render.**

"Yap-style" = direct-to-camera, fast-paced spoken monologue/rant/storytime, high energy, burned-in karaoke captions. Follow the format rules below exactly — they are what make the format work.

---

## Personalization

This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

---

## Requirements

- **HeyGen** — a HeyGen account with at least one avatar. Connect the **HeyGen MCP** (exposes `create_video_from_avatar` + `get_video`) or use the HeyGen API directly. Never hard-code an API key; read it from the environment.
- **Your HeyGen avatar ID** — from your brand profile field `HeyGen-avatar-id`, or set `HEYGEN_AVATAR_ID`. If neither is set, list your HeyGen avatars and ask the user which one to use, then save it back to the profile.
- **(Optional) Your HeyGen voice ID** — from brand profile field `HeyGen-voice-id`, or set `HEYGEN_VOICE_ID`. If neither is set, omit it and let the avatar's default voice speak.
- **Research tools** (any one): `firecrawl_search` MCP, or built-in `WebSearch`. If none are available and the user didn't name a topic, ask them for one.
- **Fallback** — if HeyGen isn't connected, still write and deliver the script, then tell the user to connect HeyGen to render.

HeyGen MCP tools may be deferred/namespaced under your HeyGen connector. Load them first, e.g.:
`ToolSearch({ query: "select:create_video_from_avatar,get_video", max_results: 5 })`

---

## Locked render configuration (do not ask, use these)

- **Aspect ratio:** `9:16` · **Resolution:** `1080p` · **Captions:** burned-in (`style: "default"`)
- **Voice speed:** `1.1` (yap energy — fast but intelligible)
- **Avatar / voice:** pulled from your profile / env (see Requirements). Never hard-code an avatar or voice ID in this file.

---

## Step 1 — Load your niche context

Read `~/.claude/brand-profile.md` so the topic + voice are accurate to *your* audience. Pull:

- **Your audience** — who you're talking to and their pain points.
- **Your offer** — what you sell / the system you teach (for CTA context only).
- **Your voice rules** — how you sound, and what to avoid.
- **Recent hooks** — so you don't repeat one you've already used (if the profile tracks them).

If a needed field is blank, ask one quick question and save the answer back to the profile.

**Your niche** comes from the profile. If it's not set, ask: "What's your niche / what do you make content about?" and save it.

---

## Step 2 — Research trending topics

If the user named a topic, skip discovery and use it. Otherwise find what's hot **right now**.

Use `firecrawl_search` (preferred — load via ToolSearch `select:mcp__firecrawl__firecrawl_search`) or `WebSearch`. Run 3–4 searches in parallel, biased to the last 2–4 weeks, templated to the user's niche. Example shapes (swap in the profile's niche and audience):

- `new [niche] tool launch [current month year] [audience]`
- `[niche] trending reddit [current month]`
- `[niche] debate / controversy [current year]`
- `[niche] news creators this week`

**Pick ONE topic** that scores highest on:
1. **DM-shareable** — would someone send this to a friend? (the #1 reach signal)
2. **Contrarian angle available** — is there a "everyone thinks X, actually Y"?
3. **Maps to audience pain** — connects to a real frustration from the profile.

State the chosen topic and the angle in one line before scripting.

---

## Step 3 — Draft the Yap script

Target **30 seconds ≈ 70–110 words**, fast delivery. Follow the four-part structure exactly:

| Beat | Time | Words | Job |
|---|---|---|---|
| **Hook** | 0–3s | ≤12 | Stop scroll + state the promise. NO "hey guys". |
| **Body** | 3–24s | ~70 | Deliver. One idea per sentence. Vary length: punch. then longer. punch. |
| **Payoff** | 24–28s | ~15 | The actual answer, plainly. Don't withhold it. |
| **Loop/CTA** | 28–30s | short | Loop to the hook OR a question that demands a comment. |

**Hook — default to the CONTRARIAN (highest-verified) formula:**
> "Everyone says [common belief], but [contrarian truth]."

Other allowed openers: curiosity gap, callout ("If you're [X], stop doing [Y]"), bold number/result. Always deliver the promise by the 3-second mark.

**Engagement engineering (non-negotiable):**
- Open a loop early ("and it's not what you think…"), close it at the payoff.
- Write to be **saved** (reference value) or **sent** (relatable/contrarian) — not just liked.
- End on a line that earns a DM or a comment.
- Plain, spoken, first-person. Match the profile's voice rules. No corporate filler, no throat-clearing.

Write the whole thing in **your tone** and from **your take** — the opinion is yours, grounded only in what's in the profile. Output the script as clean speakable text (this is what HeyGen speaks — no stage directions, no emojis, no markdown inside the script string). Show the user the script and the chosen hook, then proceed to render (don't wait for approval unless they ask).

---

## Step 4 — Render the HeyGen avatar video

Resolve the avatar ID (profile field `HeyGen-avatar-id` → env `HEYGEN_AVATAR_ID` → ask). Resolve the voice ID the same way (optional; omit if unset).

Call `create_video_from_avatar`:

```
avatarId:    <your resolved HeyGen avatar ID>
voiceId:     <your resolved HeyGen voice ID, or omit for the avatar default>
script:      <the script text from Step 3>
aspectRatio: "9:16"
resolution:  "1080p"
caption:     { style: "default" }      // burns karaoke captions in + returns SRT sidecar
voiceSettings: { speed: 1.1 }
title:       "Yap — <topic slug>"
```

Capture the returned `video_id`.

---

## Step 5 — Poll & deliver

Poll `get_video({ videoId })` every ~20s until `status` is `completed` (or `failed`). Don't spam — space the calls.

- On **completed**: give the user the `video_url`, `duration`, and the `subtitle_url` (SRT).
- On **failed**: report the failure reason and offer to re-render (e.g. shorten script if it errored on length).

Save the final script + topic + video_url to `~/yap-outputs/<date>-<slug>.md` so there's a record.

---

## Guardrails

- Keep the spoken script under ~110 words for a 30s cut unless the user asks for longer (HeyGen will speak everything — long scripts = long videos).
- The script string must be plain speech only. No emojis, no "[pause]", no markdown.
- Funnel level is REACH (cold discovery): one value hit, soft engagement CTA. No product pitch or links unless the user asks (and if they do, use *their* offer from the profile).
- Never go full-faceless-spam — this is the user's avatar speaking their real insight. Value first.
