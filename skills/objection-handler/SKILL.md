---
name: objection-handler
description: Turn the objections you actually hear ("too expensive", "no time", "let me think about it", "does this work for someone like me?") into calm, honest responses you can deliver without freezing or getting pushy — tailored to YOUR offer. Produces a saved objection-response cheat sheet using acknowledge → reframe → evidence → invite. Trigger whenever the user says "how do I respond when they say", "handle objections", "they said it's too expensive", "what do I say to no time", "people keep telling me", "I never know what to say back", or "help me answer pushback".
---

# Objection Handler — honest answers to the things people actually say

An objection is not a rejection. It's usually a real, reasonable concern the person needs answered before they can say yes. The problem is that non-salespeople either fold instantly ("oh, no worries!") or get defensive — both lose the sale *and* feel bad. This skill builds you a cheat sheet so that when you hear the objection, you already have a calm, honest, non-pushy answer ready in your voice.

The pattern for every response: **acknowledge** (make them feel heard) → **reframe** (help them see it differently) → **evidence** (a true reason it holds up) → **invite** (a light next step, never a shove).

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

## Steps

### 1. Collect the real objections
Start from the four almost everyone hears, then ask the user which they *actually* get and what else comes up:
- **"It's too expensive."**
- **"I don't have time right now."**
- **"Let me think about it."**
- **"Does this actually work for someone like me / my situation?"**

Ask: "Which of these do you hear most, and is there a specific one that always throws you?" Add any offer-specific ones they name (e.g. "I could just build this myself", "I've been burned before"). Handle the objections they truly face — a generic list they'll never use is worthless.

### 2. Understand the offer well enough to answer honestly
Pull the offer, price, transformation, and any real proof from the profile. The **evidence** step must be *true* — a real result, a genuine guarantee, an honest reframe of value. If there's no proof yet, the evidence leans on the honest logic of the offer and a risk-reducer (a small first step, a guarantee), never a fabricated testimonial.

### 3. Write the response bank
For each objection, write a response following acknowledge → reframe → evidence → invite, in the user's voice:
- **Acknowledge** — genuinely, not as a tactic. "Totally fair" / "I get that."
- **Reframe** — shift the frame honestly. Price → cost of *not* solving it, or price-per-outcome. Time → this *buys back* time. "Let me think" → what's the real hesitation underneath. "Works for me?" → the specific reason it fits their situation.
- **Evidence** — one true, concrete reason: a result, a guarantee, a comparison, or clear logic. Never invented.
- **Invite** — a low-pressure next step: a question, a small first step, or simply leaving the door open. Never a countdown or a guilt trip.

Give each objection **one primary response** plus a **one-line short version** for DMs, where a paragraph would be too much.

### 4. Add the golden rule and the graceful exit
Two things at the top of the sheet:
- **Ask before you answer.** The best response to almost any objection is a question first: *"When you say it's too expensive — is it more than you expected, or is it the timing?"* You can't handle the real objection until you know what it actually is. Half of "too expensive" is really "I'm not sure it'll work."
- **The honest no.** Script a warm exit for when it's genuinely not a fit or not the time — because being willing to hear no is exactly what makes the yeses trustworthy and keeps the door open for later.

### 5. Save the cheat sheet
Write it all to `~/objection-cheatsheet.md`: the golden rule up top, then each objection with its full response + short DM version, and the graceful exit at the bottom. Confirm the path and tell the user to skim it before any sales conversation so the answers feel ready, not rehearsed.

## Input → output example
**Input:** Offer (from profile): "$600 booking-automation setup for small studios." User hears "too expensive" and "let me think about it" most.

**Output — `~/objection-cheatsheet.md` (excerpt):**

**Golden rule:** ask before you answer. "When you say it's a lot — is it more than you budgeted, or you're not sure it'll pay off?"

**"It's too expensive."**
> Totally fair — $600 is real money. Here's how I'd look at it though: right now the no-shows and the hours you spend chasing bookings are costing you way more than that every month. This is a one-time setup that stops the leak. If it saves you even a few bookings, it's paid for itself. Want me to walk you through exactly what it'd handle for your studio?

*Short (DM):* fair — but the no-shows are costing you more than $600 a month already. this stops that leak once. want the quick breakdown?

**"Let me think about it."**
> Of course. Can I ask — is it the price, the timing, or are you not totally sure it'll work for how your studio runs? Whatever it is, I'd rather just answer it now than have you wondering.

**Graceful exit:**
> Honestly, if the timing's not right, no pressure at all — I'd rather you do this when it actually helps. I'm here whenever you're ready.

## Notes / edge cases
- The evidence step is the integrity line: never invent a result, a client count, or a guarantee the user can't honor. If proof is thin, use honest logic + a risk-reducer instead.
- If an objection is really a "no," respect it. Pushing past a genuine no is what makes selling feel gross and burns the relationship for any future yes.
- Pairs directly with **first-customer-closer** (this is the "E — explain away concerns" stage of that script) and with **dm-writer** for the short DM versions.
