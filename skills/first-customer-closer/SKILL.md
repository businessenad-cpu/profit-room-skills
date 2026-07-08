---
name: first-customer-closer
description: Turn "someone's interested but I don't know how to actually sell" into a calm, honest conversation script using the CLOSER framework — built for people who hate selling. Produces a personalized call-or-DM script, the exact questions to ask, how to invite the sale without being pushy, and how to handle "let me think about it". Trigger whenever the user says "someone's interested and I don't know what to say", "I have a sales call", "how do I close", "help me sell without being salesy", "write me a sales script", "someone replied yes", "I got on a call and froze", or "how do I actually ask for the sale".
---

# First-Customer Closer — a sales conversation for people who hate selling

Someone raised their hand. Now you're panicking, because "closing" sounds like a used-car move you never want to make. Here's the reframe: a good sales conversation is just **helping someone get clear on whether this is right for them.** You ask honest questions, you listen, and if it's a fit, you make it easy to say yes. If it's not, you say so — that's what makes you trustworthy.

This skill builds you a one-page script around the **CLOSER** framework so you walk in knowing exactly what to ask and what to say.

**CLOSER** = **C**larify why they're here · **L**abel the problem · **O**verview what they've tried · **S**ell the outcome (the vacation, not the plane) · **E**xplain away concerns · **R**einforce the decision.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

## Steps

### 1. Get the situation
Ask the user for:
- **Who** the prospect is and what they do.
- **How they came in** (replied to a DM, booked a call, asked about the offer at an event).
- **The format** — live call, or back-and-forth DM/voice notes? (The script adapts: a call is spoken and flowing; DM is shorter turns, one question at a time.)
- **The offer + price** (pull from profile if set).

### 2. Build the CLOSER script
Write a spoken, human script — not a form to read robotically — through the six stages. For each stage, give the user **the goal in one line + the actual words to say**, in their voice:

- **C — Clarify why they're here.** Open by getting *them* talking about why they reached out. *"Before I say anything about what I do — what made you reach out? What's going on right now?"* This makes it their conversation, not your pitch.
- **L — Label the problem.** Reflect back the real problem in their words so they feel understood. *"So it sounds like the core thing is [X] — is that the piece that's actually costing you?"* Don't move on until they confirm it.
- **O — Overview what they've tried.** *"What have you already tried to fix this?"* This surfaces why past attempts failed (usually the exact gap the offer fills) and it stops them re-trying the free version after the call.
- **S — Sell the outcome, not the features.** Describe the *after* — their life once the problem is gone — not the mechanics of how it works. *"You wouldn't have to think about [X] anymore — it'd just run."* People buy the vacation, not the flight. Name the offer and price plainly here, once, without flinching.
- **E — Explain away concerns.** Invite objections instead of dodging them. *"What's making you hesitate?"* Then handle it honestly (pair with the **objection-handler** skill for a full response bank).
- **R — Reinforce the decision.** After a yes, remind them they made a smart call and set the very next concrete step. *"You're gonna be glad you did this — here's exactly what happens next."*

### 3. Write the key questions list
Pull out the 5–7 questions the user must ask (mostly from C, L, O). A nervous seller who has the questions on a sticky note will always beat one improvising. These questions do the selling — the prospect talks themselves into it.

### 4. Write the "invite the sale" moment
Most non-salespeople freeze right here, so script it explicitly. A clean, calm invitation — no pressure, no countdown timer:
> *"From everything you've said, I really think this'd help. Want to go ahead and get started?"*
Then **stop talking.** Silence is not your enemy. Give a version for a call and a version for DM.

### 5. Handle "let me think about it"
This almost always means an unspoken concern, not a real need for time. Script a warm response that surfaces it without pressure:
> *"Totally fair. Just so I can help — is it the price, the timing, or are you not sure it'll work for your situation?"*
Whatever they name, address it honestly, then re-offer *once*. If it's still no, leave the door open graciously — a good exit keeps them as a future yes.

### 6. Save the script
Write the full one-page script to `~/first-customer-script.md`: the six CLOSER stages with the words to say, the questions list, the invite line, and the "let me think about it" branch. Confirm the path and tell the user to read it out loud once before the conversation so it sounds like them, not like a script.

## Input → output example
**Input:** "Someone from my newsletter booked a call. She runs a yoga studio. My offer is a $600 booking-automation setup." (voice call)

**Output — `~/first-customer-script.md` (excerpt):**

**C — Clarify:** *"Before I dive in — what made you book this call? What's going on with the studio right now?"*
**L — Label:** *"So the real cost is the no-shows and the hours you spend chasing bookings — that's the piece bleeding you, yeah?"*
**S — Sell the outcome:** *"Picture Monday: bookings, reminders, waitlist — all handled without you touching your phone. That's what this does. It's a $600 one-time setup."*
**Invite:** *"I really think this'd take that off your plate. Want to get started?"* → (stop talking)
**"Let me think about it":** *"Of course. Quick one so I can actually help — is it the $600, the timing, or are you unsure it'll fit how your studio runs?"*

**Questions to ask:** why now · what's it costing you · what have you tried · what would change if it were solved · what's your hesitation.

## Notes / edge cases
- If it's genuinely not a fit, the honest move is to say so and maybe refer them elsewhere. This isn't just ethics — it's what makes the yeses real and the referrals come.
- Don't stack the invite. Ask once, go quiet, let them answer. Re-asking immediately reads as desperate and breaks trust.
- Keep price delivery flat and confident. If the user tends to over-explain or discount on the spot, flag it in the script with a "say the price, then stop" note.
- For the objection responses in stage E, hand off to **objection-handler** to build a full cheat sheet the user keeps beside this script.
