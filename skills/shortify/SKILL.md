---
name: shortify
description: "Turn ONE long-form video (timestamped transcript + screen recording) into 3 distinct short-form vertical cuts — proof, contrarian, and transformation — each with its own hook and b-roll, then write per-platform captions ready to publish to YouTube Shorts / Instagram Reels / TikTok / Facebook (and LinkedIn as a story lane). Use when the user wants shorts from a long-form video, says 'shortify this', 'cut this into shorts', 'make reels from my video', or /shortify."
argument-hint: "shortify <long-form transcript path + screen recording path>"
allowed-tools: Bash, Read, Write, Agent
user-invocable: true
---

# Shortify — long-form → short-form (produce → caption → publish)

Take ONE long-form video and cut it into 3 angle-distinct vertical shorts, each with its own hook and b-roll, then write per-platform captions. The screen recording of the real product/result is the STAR; generated b-roll is a spice used only for conceptual openers.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

Fields this skill uses: **Tone** + **Words-to-avoid** (script voice), **Proof/wins** (the on-screen proof stat — never invent one), **Offer** + **Default-CTA** (the end-card + caption CTA), **Main-platforms** (where to publish).

## Requirements
This skill orchestrates several media tools. It degrades gracefully — if one isn't available, I'll tell you exactly what to add or hand you the files to finish manually.
- **ffmpeg** — trimming, compositing, audio extraction (required).
- **Whisper** (local, no API key) — karaoke captions from the audio + finding caption-safe trigger words. Whisper mishears some product names (e.g. "Claude" → "cloud"/"quad"); correct these in the captions.
- **A talking-head avatar tool** (e.g. HeyGen) — optional; only if you want a synthetic presenter bottom-frame instead of your own footage.
- **An image/video generator** (e.g. Higgsfield, or Gemini image gen) — optional; for the conceptual cold-open and a few canonical b-roll scenes.
- **A social scheduler** (your platform's native scheduler, or any third-party scheduling tool) — optional; only needed for the auto-publish step. Without one, this skill still produces the finished cuts + captions and you upload them yourself. Never hardcode account IDs or keys — read them from your environment.

Never embed API keys. Read any keys the tools need from environment variables or a local `.env`.

## Inputs (from the argument / message, else ask)
- **transcript**: the long-form timestamped `.txt`
- **screencap**: the long-form screen recording `.mp4` (1080p ideal)
- **angles** (default `proof, contrarian, transformation`)
- **slug**: a short name for the output folder

## Steps

1. **SCRIPTS FIRST — review gate.** Write just the 3 scripts (cheap, no render) and show the user to approve/edit BEFORE spending any avatar/render budget. For each angle check:
   - The spoken hook matches a proven pattern (swap only the variables — tool, number, outcome — never invent a new hook shape).
   - On-screen `hook_title` is 3-4 words (hard max 4 words per line; break longer titles onto a second line so the card never spans the full frame).
   - Distinct, angle-specific openings; a concrete number in the first sentence; result before mechanism.
   - Name the real tool/feature, not a generic "AI" or "a new mode".
   Fix wording before rendering.

2. **B-ROLL plan (the make-or-break step — build carefully and VERIFY).** Per angle, align visuals beat-by-beat:
   - The screen recording of the real result is the STAR — show it EARLY (right after the cold open) and cut through its panels as the script names them.
   - Reserve generated art for the conceptual opener and a few shared canonical scenes (generate each once, reuse across angles via a cache).
   - A LIST line ("watch every line / approve every step / catch every mistake") gets one rapid-fire word card per item — a WORD card (≤4 words), never a full sentence.
   - Subagents can draft the b-roll plan, but do NOT trust it blindly — sanity-check that it's screencap-dominant with no sentence text-cards, and verify the actual frames.

3. **RENDER each cut.** Composite: presenter (your footage or an avatar) bottom, screen recording top, karaoke captions throughout, cold open, and a WIDE result payoff at the end. Trim silences/pauses so the presenter is present on frame one.

4. **CAPTIONS — per platform.** Write angle-distinct titles + first lines for each cut (never reuse the same caption across angles). Adapt the soft CTA by video type using the brand profile: tutorial → "Learn to build like this…"; showcase → "Get [your offer]…". Respect any platform hashtag limits (e.g. Instagram caps meaningful hashtags — keep it tight).

5. **PUBLISH (optional).** If a scheduler is configured, upload each cut and schedule the 3 angles into open future slots (stagger them several days apart, rotating post times). Publish to the user's Main-platforms. If no scheduler is set, output the finished files + captions and tell the user to upload them.

6. **Verify + auto-repair.** Extract frames (hook ~2s, the conceptual opener, a mid beat, the wide ending) from each cut and show the user. If any on-screen b-roll trigger didn't fire, transcribe that cut's audio with Whisper to see what was actually said, pick a plain adjacent word as the trigger (never a number or a dotted filename like `CLAUDE.md`, which Whisper writes as "claude .md"), and re-render just that cut.

## Rules baked into the method (do not override)
- **FORMATS (3 distinct shapes, never homogenized):** proof = RESULT-LED (result + number, then proof line, what, how, stakes); contrarian = BELIEF-FLIP (the wrong belief FIRST, then the result as the mic-drop proof *after* it); transformation = BEFORE/AFTER (old-world cost, then new world + result).
- **HOOKS (the most important part):** always instantiated from a proven hook pattern — keep the shape, swap only the variables; distinct per angle; end on an intrigue-building payoff description; name the real tool/feature, never "AI". A contrarian hook may be a pattern-interrupt ("STOP DOING X"). On-screen `hook_title`: 3-4 words ideal, hard max 4 words per line.
- **OPENINGS:** angle-specific and distinct (proof = the result; contrarian = the belief it breaks; transformation = the shift); the FIRST SENTENCE carries the headline number; one PROOF stat line after the payoff (use a real number from the brand profile — never invent one); a conceptual generated b-roll opens contrarian/transformation before the screen recording.
- **SCRIPTS:** obey the brand-profile words-to-avoid; name the model + feature specifically; ANSWER WHY (the pain it removes), not just what; result before mechanism; natural thought-line pauses; no spoken hard CTA.
- **B-ROLL:** per-beat source (screen recording / infographic / illustration / presenter / library clip / word card); the REAL result is the STAR, shown EARLY and carrying most beats; a LIST line gets one rapid-fire word card per item (≤4 words — a sentence is NEVER a word card); shared canonical scenes generated once; end on a WIDE result payoff; never a plain-editor/notes frame when the line isn't about that; motion variety (no camera move more than twice in a row; pan infographics, zoom illustrations).
- **CAPTIONS / TRANSCRIPTION:** auto-correct product names Whisper mishears in the karaoke captions.
- **CTA:** use the brand-profile Offer + Default-CTA. Adapt by video type: tutorial → "Learn to build like this…"; showcase → "Get [offer]…". Prefer "link in bio" with the real link in the description. Per-angle end-card text is allowed.

## Output
An output folder per run containing, per angle: the script, the b-roll plan, the rendered cut, and the caption set — plus a short summary of where each cut will publish (or a note to upload manually).
