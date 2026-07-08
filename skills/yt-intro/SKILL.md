---
name: yt-intro
description: "Write a high-retention 30-second YouTube intro from a FINISHED video transcript. Analyzes the real transcript first (extracts the actual payoff, the hardest number, the contrarian reframe, the best re-hook moment, and the video type), then writes a 5-beat intro (Hook/Payoff/Proof/Reframe/Re-hook) under an 80-word budget. Trigger on '/yt-intro', 'write the intro for this video', 'I filmed the video, now write the intro', 'rewrite my intro', 'fix my opening', or any request to script a YouTube long-form intro from a transcript the user has already recorded."
---

# YouTube Intro Writer — Retention-Engineered

Write the first 30 seconds of your long-form YouTube video. The intro is usually the single highest-leverage fix on a channel: retention data commonly shows 35-50% of viewers leave in the first ~45 seconds while the body retains fine. This skill rebuilds the open so it stops the bleed.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

Fields this skill uses: **Proof/wins** and **Credentials** (the credibility line — never invent a number), **Offer** + **Default-CTA** (the soft funnel in the proof beat), **Tone** and **Words-to-avoid** (voice).

## The Workflow This Skill Is Built For

Film the **full video first**, then hand this skill the transcript, then record the intro separately. This is the correct order. Analyzing the finished transcript means the intro promises only what the video actually delivers, and lets the skill cold-open with the real climax. A matched promise → payoff is what creates the mid-video retention recovery. Never write the intro blind.

## Input

Provide the finished video transcript (pasted text, a file path, or a YouTube video ID — pull the transcript first if only an ID is given). If nothing is provided, ask for the transcript before doing anything else.

## Step 0 — Load Intelligence

- Load the brand profile (above) for the Proof, Offer, Default-CTA, Tone, and Words-to-avoid fields.
- Optional: if the **positioning-filter** skill is installed, use it to confirm the video's angle ladders to the offer.

Voice rules (hard): obey the brand-profile words-to-avoid, spell tool and product names correctly (transcripts often mangle them), write numbers as digits.

## Step 1 — Analyze the Transcript (do this before writing a single line)

Extract and write down:

1. **The payoff / result** — the single most impressive thing the video SHOWS working. This becomes the cold-open visual and the hook. Find the demo/climax moment, not the setup.
2. **The hardest number** — the most concrete, specific figure in the video (9 platforms, 15 hours saved, 24 cents, 30 days of content, 221 leads). Prefer a number actually said in the video. The hook must contain one. If the video has none, surface that as a gap and use a Proof number from the brand profile instead.
3. **The contrarian reframe** — the "most people think X, but it's actually Y" insight. Pull it from the transcript if it's there; derive it from the video's thesis if not. This is the open loop that earns the recovery hump.
4. **The re-hook moment** — the most surprising or best single beat still coming later in the video, to tease at the end as a second, bigger loop.
5. **Video type** (classify — this changes the re-hook and verbs):
   - **Build-along tutorial** → "I'll build every piece with you, live."
   - **Showcase / demo** (you show a finished system, not building it live) → "I'll walk you through exactly how every piece works." NEVER say "let's build" for a showcase.
   - **News / breakdown** → "I'll show you what this actually means and how to use it today."
   - **Listicle / multi-tip** → tease the single best item by number ("and number 5 is the one nobody's using").
6. **The hero tool / keyword** — the specific named tool, model, or format the video is BUILT AROUND. If the video is about a named release or a named thing you built, this name belongs IN the hook (see the Hook rule). Naming the exact tool the day it drops is the "ahead of everyone" signal audiences click for. If the video isn't about any one named thing, there's no hero keyword and the hook leads with the outcome alone.

## Step 2 — Write the Intro (5 beats, hard 80-word budget)

| Beat | Time | Rule |
|---|---|---|
| 1. Hook | 0-3s | One sentence. Specific outcome + a number. **If the video has a hero tool/keyword (Step 1, item 6), name it here** — lead with the named tool doing the result. At most ONE named tool plus the thing it made; do NOT stack two pieces of jargon a viewer doesn't know before they've seen the payoff. Every other word stays plain. No vague superlatives ("craziest thing ever"). Never deflate it. |
| 2. Payoff | 3-12s | Show it working. Lead straight into the demonstration with plain verbs. Do NOT describe the process/plumbing, and do NOT open with a short-form filler imperative ("Watch." / "Check this out." / "Look."). |
| 3. Proof | 12-18s | One line, as validation of what they just saw. Here is the SOFT FUNNEL: drop your offer/community naturally, using your **Default-CTA** framing. Pair it with ONE real credibility anchor from your **Proof/Credentials** fields (never invent one). Not a résumé, not before the payoff. |
| 4. Reframe + stakes | 18-24s | Pivot with exactly one "But," shape "X. But what you really need is Y." CRITICAL: X must be the WRONG FIX people reach for (more hours, hiring a VA, posting more, working harder), so the But logically contrasts it with the real fix Y. X must NOT be a feeling or a pain. Fold the self-focused stake INTO the wrong fix, and keep it CONCRETE — name the literal action, never a vague abstraction like "keeping up". **FIFTH-GRADE READING LEVEL — this beat fails most on word choice.** The wrong fix X must be something the viewer ACTUALLY believes in their own words ("you'd have to learn to code," "you'd have to hire someone," "you'd spend a whole weekend on it"), NOT industry framing they'd never say out loud. The real fix Y must use plain words — BAN jargon like "orchestrator," "pipeline," "architecture," "framework," "infrastructure." Say "one AI," "the right prompt," "one machine," "one click" instead. NEVER frame stakes as a comparison to less-skilled or less-deserving people — it reads as petty. |
| 5. Re-hook | 24-30s | A second, bigger loop matched to video type. Then the close. |

**Master rule: proof before plumbing.** The finished result is on screen by second 10. Explanation comes after they commit.

## Step 3 — Enforce Constraints (run every output through these)

- **Word budget: 75-85 words. Target ~80, NOT a hard wall.** ~80 words is a true 30 seconds at ~185 wpm with visual beats. **NATURAL DELIVERY ALWAYS WINS OVER THE CAP.** If hitting the budget forces a clipped, robotic, or unnatural line, go 5-15 words over and write the sentence the way a person would actually say it out loud. **When cutting to fit, NEVER leave a fragment — every line must stay a complete sentence with its object intact.**
- **Redundancy check:** no filler noun (e.g. "system," "content," "workflow") appears 3+ times. Swap to synonyms or cut. (Keep the user's preferred words from the brand profile — the rule targets filler nouns, not strong verbs the user likes.)
- **Concrete over vague (every beat):** name the specific action, tool, or outcome. Ban fuzzy abstractions like "keeping up," "staying relevant," "the grind," "leveling up." Say the literal thing. **NEVER end a beat on a vague placeholder payoff** ("and it just works," "and you're done," "and it does the rest"). If a beat's last clause could be deleted and the viewer would lose no specific information, it's vague — rewrite it.
- **Number in the hook:** non-negotiable.
- **Hero keyword in the hook when one exists:** name it; one named tool max.
- **Fifth-grade reading level:** every line should sound like the user talking, not a tech blog. Ban jargon a normal person wouldn't say out loud. The reframe beat breaks this most — check it hardest.
- **Exactly one "But":** every intro pivots on a single "But," normally in the reframe beat. Not zero, not three.
- **Soft funnel in the proof line:** drop the offer/community using the Default-CTA framing, once, softly. Never omit it, never hard-sell it.
- **Proof after payoff:** never lead with the bio.
- **Second loop in the re-hook:** must open something new, not just "let's go."
- **Script only:** output the spoken words only. NO scene direction, NO on-screen/visual cues, NO "(on screen: ...)" notes.

## Step 4 — Output Format

```
## /yt-intro — [video title]

**Video type:** [build-along / showcase / news / listicle]

---

[Hook, 0-3s] ...spoken line...

[Payoff, 3-12s] ...

[Proof, 12-18s] ...

[Reframe, 18-24s] ...

[Re-hook, 24-30s] ...

---
**Word count:** XX / 85
**Redundancy check:** [pass, or flag repeated words]
**Hardest number used:** ...
```

Then offer 2 alternate **hook lines only** (beat 1) so the user can pick the strongest open. Don't regenerate the whole intro unless asked.

## Reference: The Standard (a tightened example — swap in the user's real proof)

For "I replaced my content team" (a showcase, 77 words, "system" used 0x):

> [Hook] I fired my whole content team and replaced them with this.
> [Payoff] One click. It finds my next video, writes the hooks, builds the thumbnails, and posts everywhere while I do nothing.
> [Proof] I built [your credibility anchor] with no team, and I run [your community/offer] where we do exactly this.
> [Reframe] Everyone thinks keeping up means hiring a VA. You just need one workflow that thinks like you.
> [Re-hook] I'll walk you through exactly how every piece works. The last one broke my brain. Let's go.
