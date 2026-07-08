---
name: dm-writer
description: Write one short, human DM or message to a specific person for a specific goal (start a conversation, share your offer, or follow up) — in your voice, so it opens a dialogue instead of pitch-slapping them. Trigger whenever the user says "write a DM", "help me message this person", "what do I say to", "reach out to [name]", "draft a message", "follow up with", "how do I bring up my offer to", or "I don't know how to word this".
---

# DM Writer — one real message to one real person

A good DM is not a broadcast. It's a message to *this* person, referencing *this* relationship, with *one* clear reason for reaching out. This skill takes the context you give it and writes a short message that sounds like you texting someone you respect — not a funnel.

Use it for a single person. If you want a whole ranked list of who to contact first, run **warm-outreach** first, then bring individuals here.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

## Steps

### 1. Get the three things a good DM needs
Ask the user for these (accept short answers; infer the rest from the profile):
- **Who** — the recipient: name, what they do, and any detail that makes them *them* (their work, a recent post, how you met).
- **Relationship** — how well you know them and when you last spoke (close, warm-but-quiet, barely know them, cold-but-mutual-connection).
- **Goal** — pick one: **start a conversation** (no ask yet) · **share the offer** (they've shown a fit) · **follow up** (you already messaged and want to nudge or re-open).

If the user only gives a name, ask the one or two questions that actually change the message — usually relationship and goal.

### 2. Match the message to the relationship
The register shifts with warmth, not with the goal:
- **Close / warm:** casual, lowercase-fine, get to the point, a real question at the end.
- **Warm-but-quiet:** reconnect first. Acknowledge the gap honestly ("been a minute"), lead with genuine interest in them, earn the right to mention what you're building.
- **Barely know / mutual connection:** name the connection or the specific reason they came to mind up front, keep it very short, make the ask tiny.

### 3. Write the message — the non-pushy rules
- **Lead with them.** First line is about the recipient or the shared context, never "So I have this offer."
- **One reason, one ask.** No stacked links, no multi-paragraph pitch, no life story.
- **End on an easy question.** The goal is a reply, not a yes. A question they can answer in one line beats a call-to-action.
- **Only name the offer if the goal is "share the offer"** — and even then, frame it as "this might be relevant to you because [specific reason]," not a feature dump.
- Honor the profile's words-to-avoid and tone. No fake urgency, no "quick question" bait, no flattery the user doesn't mean.
- Keep it to 2–5 sentences. If it's longer than a text you'd actually send, cut it.

### 4. Add a one-line follow-up
Always include a **single** follow-up line the user can send if there's no reply after a few days. It should add value or lightness, never guilt ("just bumping this" / "did you see my message?"). Good follow-ups reference something new, or gracefully let it go ("no worries if the timing's off — door's open"). One follow-up only, then stop.

### 5. Save it
Append the message + follow-up to `~/dm-drafts.md` under a heading with the recipient's name and date, so the user builds a personal swipe file of what they've sent. Confirm the path and remind them to swap in the one personal detail before sending.

## Input → output example
**Input:** "Message Sam — we did a bootcamp together last year, haven't talked in months. He runs a small Shopify agency. Goal: share my offer (I build automated post-purchase email flows)."

**Output (warm-but-quiet + share offer):**
> hey Sam! been way too long — how'd the agency end up going after the bootcamp? i actually thought of you because i've been building automated post-purchase email flows for Shopify stores lately, and i remember you had a bunch of clients who'd probably want that. worth a quick chat, or not really your thing right now?

**Follow-up (if no reply in ~4 days):**
> no pressure either way Sam — if post-purchase flows aren't a priority right now, all good. would still love to catch up sometime.

Saved to `~/dm-drafts.md`.

## Notes / edge cases
- If the goal is "share the offer" but the relationship is cold and there's no real fit signal, say so — recommend the "start a conversation" version instead. Pitching a stranger is exactly the move that makes selling feel gross and doesn't work.
- Never fabricate a shared memory or a result. If the personal detail slot can't be filled truthfully, the message drops to a lighter register.
- One message, one follow-up. If they want a whole sequence or a list of people, that's the **warm-outreach** skill — not more follow-ups to one person.
