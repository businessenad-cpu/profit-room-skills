---
name: lead-magnet
description: "Create a Notion-native lead magnet with associated LinkedIn posts. Use when: (1) user says /leadmagnet or 'create a lead magnet', (2) user wants to build a free guide, prompt pack, playbook, framework, swipe file, or cheat sheet for their audience, (3) user wants to push a lead magnet JSON to Notion. Handles the full pipeline: research the topic, write the content as Notion-ready JSON, optionally push to Notion, and draft 3 LinkedIn post variations to promote it."
allowed-tools: Bash, Read, Write, Edit, WebSearch, WebFetch, Glob, Grep, Task
metadata:
  argument-hint: "topic or description of the lead magnet"
  user-invocable: true
---

# Lead Magnet Skill

Create high-converting, story-driven lead magnets in your brand voice, write them as Notion-ready content, optionally publish to Notion, and draft LinkedIn promo posts.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

The steps below read these brand-profile fields: **Name**, **Audience**, **Main-pain**, **Offer**, **Transformation**, **Tone**, **Words-to-avoid**, and **Default-CTA**. Wherever a step needs a name, audience, offer, proof point, or CTA link, pull it from the profile — never hardcode.

## Requirements

- **Content generation (core value):** No credentials needed. Researching, writing the JSON, and drafting the LinkedIn posts all work with no setup.
- **Notion push (optional):** The `scripts/push_to_notion.py` step needs two environment variables:
  - `NOTION_TOKEN` — your Notion internal integration secret
  - `NOTION_DATABASE_ID` — the ID of the Notion database to add pages to
  - If either is not set, skip the push and tell the user exactly what to add (see Step 5). The lead magnet content is still fully delivered as a JSON file they can push later.

## Workflow

1. **Parse user input** for topic, format, and any special instructions
2. **Fetch YouTube transcript** (if a YouTube URL was provided)
3. **Research the topic** (mandatory — see references/voice-and-rules.md "Research First")
4. **Write the lead magnet** as a Notion-ready JSON file
5. **Push to Notion** (optional) using `scripts/push_to_notion.py`
6. **Draft 3 LinkedIn post variations** with different hooks
7. **Present everything** to the user for review

## Step 1: Parse Input

Extract from the user's message:
- **TOPIC**: What the lead magnet is about (if a YouTube URL is given, derive the topic after fetching the transcript)
- **FORMAT**: One of: prompt_pack, playbook, system_prompts, framework, swipe_file, guide (default: guide)
- **SPECIAL INSTRUCTIONS**: Any constraints, angles, or preferences mentioned

Display your parsing:
```
Creating lead magnet:
- Topic: {TOPIC}
- Format: {FORMAT}
- Notes: {SPECIAL INSTRUCTIONS or "none"}
```

## Step 2: Fetch YouTube Transcript (if applicable)

If the user provided a YouTube URL, extract the video ID and fetch the transcript:

```bash
python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()
transcript = api.fetch('VIDEO_ID')
text = ' '.join([t.text for t in transcript])
print(text)
"
```

Use the transcript as the primary source for the lead magnet topic and content. Extract:
- The core topic/thesis of the video
- Key frameworks, steps, or insights mentioned
- Specific numbers, tools, or examples used
- The angle to take on the subject (in your Tone from the brand profile)

Then update your parsing display with the derived topic.

## Step 3: Research (MANDATORY)

Before writing ANY lead magnet, deeply research the topic. Use WebSearch and WebFetch to understand:
- What real people are saying on Reddit, X, YouTube
- How people actually use/implement the topic
- Common pain points and questions (anchor these to the **Main-pain** field in the brand profile)
- Specific tools, numbers, and examples

Never write from assumptions. See references/voice-and-rules.md for full research requirements.

## Step 4: Write the Lead Magnet JSON

Create a JSON file in `~/lead-magnets/output/` (create the folder if it doesn't exist), following the exact structure documented in references/json-format.md. Use a kebab-case filename derived from the topic.

Critical rules (see references/voice-and-rules.md for complete list):
- **1,500 words MAX** — hard constraint
- **6th grade reading level** — radically simple
- **ZERO markdown bold** (`**text**`) in JSON content strings — Notion API shows raw asterisks
- **Story-driven** — every lead magnet needs a narrative arc (BAB, Origin Story, Case Study Chain, or Behind the Curtain)
- **Concrete proof** — real numbers, specific examples, named frameworks (use only proof points from the brand profile, or ask — never invent)
- **Early CTA** — purple callout with 🚀 after intro, linking to the **Default-CTA** from the brand profile
- **Closing CTA** — at bottom, also linking to the **Default-CTA**
- Never invent revenue, follower counts, or results for the user

## Step 5: Push to Notion (Optional)

First check that the required environment variables are set:

```bash
if [ -z "$NOTION_TOKEN" ] || [ -z "$NOTION_DATABASE_ID" ]; then
  echo "SKIP_NOTION"
fi
```

- If it prints `SKIP_NOTION`, **skip this step**. Tell the user:
  > "I've saved the lead magnet JSON. To publish it to Notion, set `NOTION_TOKEN` (your Notion internal integration secret) and `NOTION_DATABASE_ID` (the target database ID) in your environment, then run: `python3 scripts/push_to_notion.py <path-to-json>`"
- Otherwise, run the push script:

```bash
python3 "${SKILL_ROOT}/scripts/push_to_notion.py" "<path-to-json-file>"
```

The script reads `NOTION_TOKEN` and `NOTION_DATABASE_ID` from the environment. If the push fails, show the error and troubleshoot.

## Step 6: Draft 3 LinkedIn Post Variations

Write 3 LinkedIn posts promoting the lead magnet, in the **Tone** from the brand profile and respecting **Words-to-avoid**. Each must have a **different hook** (first 2 lines).

LinkedIn post rules:
- 150-200 words each
- First 2 lines are the most important — they must stop the scroll
- Use white space between sentences for mobile readability
- End with a comment-trigger CTA (e.g., "Comment KEYWORD and I'll send it")
- Include 3-5 hashtags
- Tone: pull from the brand profile
- Each variation should use a different angle:
  - **Variation A**: Contrarian or hot-take hook
  - **Variation B**: Pain-first / problem-aware hook (anchor to Main-pain)
  - **Variation C**: Results-led / proof hook (using only real proof points)

## Step 7: Present to User

Show:
1. Confirmation of the JSON file path (and the Notion page ID if it was pushed)
2. All 3 LinkedIn post variations clearly labeled
3. Ask if they want any tweaks before posting

## Content Categories

1. **Prompt Packs** — Copy-paste prompts organized by goal, each with WHY it works + example output
2. **AI Playbooks** — Step-by-step guides, story-driven, proof-backed
3. **System Prompt Templates** — Ready-to-paste AI configurations
4. **Frameworks & Blueprints** — Visual systems showing HOW something works
5. **Swipe Files** — Curated collections with commentary on WHY each works
6. **Guides** — Deep-dive on one topic, story-first

## What We Do NOT Create

- Automation tutorials (no n8n, Make.com, Zapier how-tos)
- Tool-dependent content (must work regardless of AI tool)
- Generic guides with no unique data
- Lists without narrative
- Content requiring technical skill to use

## Reference Files

- **references/voice-and-rules.md** — Complete voice rules, storytelling frameworks, proof standards, design system, quality checklist
- **references/json-format.md** — Exact JSON structure with block type examples
- **references/linkedin-examples.md** — Example LinkedIn post structure for reference

Read these references BEFORE writing. They contain critical formatting rules that prevent production issues.
