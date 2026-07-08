---
name: warm-outreach
description: Build a prioritized warm-network outreach list and a genuine, low-pressure first message so you can land your first customer from people who ALREADY know and trust you — before you ever touch cold outreach. Trigger whenever the user says "who should I reach out to", "I need my first customer", "warm outreach", "make an outreach list", "who do I already know", "help me start selling", "I don't know who to talk to", or "how do I get my first client without being salesy".
---

# Warm Outreach — start with people who already trust you

The fastest first customer almost never comes from strangers. It comes from someone who already knows you: a past client, an old colleague, someone in a community you're in, a person who liked your last three posts. This skill helps you dump that whole network onto paper, rank it, and write a first message that opens a conversation instead of pitch-slapping a friend.

The whole point is **warm before cold, and honest before pushy.** You are not blasting anyone. You are talking to real people you'd be happy to hear from yourself.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

## Steps

### 1. Brain-dump the whole network (no filtering yet)
Ask the user to list everyone who already knows them, in loose buckets — accept messy, half-remembered answers. Prompt each bucket so they don't stall:
- **Past & current clients** — anyone who ever paid them, even once, even years ago.
- **Colleagues & work history** — old bosses, coworkers, people from past jobs.
- **Community & peers** — people in any group, cohort, Slack/Discord, mastermind, or course they're in.
- **Warm DMs & social** — people who reply to their posts, DM them, or they chat with online.
- **Friends & personal** — anyone who'd take their call, who might know someone even if they aren't the buyer themselves.

Tell them: don't judge fit yet, just get names down. Aim for 20–40. If they freeze, ask "who are the last 10 people you texted?" and "whose posts do you comment on?"

### 2. Score each person 1–3
For every name, score two quick things:
- **Fit** — how likely is this person (or someone they know) to actually want the user's offer? (3 = clear fit, 2 = maybe/adjacent, 1 = unlikely buyer but a good connector.)
- **Warmth** — how strong is the relationship right now? (3 = they'd reply within the hour, 2 = friendly but quiet lately, 1 = we've lost touch.)

Sort by fit + warmth combined. The top of the list (high-fit AND high-warmth) is who they message first. Low-fit-but-high-warmth people aren't wasted — they're **connectors** you ask for a referral, not a sale.

### 3. Write 3 opener variations
Using the brand voice, write **three** first-touch openers the user can adapt per person. Rules that keep it non-salesy:
- **Lead with them, not the pitch.** Reference something real — their work, a shared moment, why they came to mind. No offer in the first message unless it's genuinely natural.
- **Ask, don't announce.** End on a light question that's easy to answer, so it starts a conversation.
- **No fake urgency, no flattery bombing, no "quick question" bait.** Sound like the user texting a person they respect.

Make the three distinct so different relationships get the right register:
1. **Reconnect** — for someone they've lost touch with (warmth 1–2). Pure catch-up, zero pitch.
2. **Soft signal** — for a warm, relevant person (fit 2–3). Mentions what they're building now and asks if it's relevant to them.
3. **Referral ask** — for a connector (low fit, high warmth). Asks who they might know, not whether *they* want it.

Each opener should have a `[bracketed]` slot for the one personal detail the user fills in per person — that detail is what makes it not a template.

### 4. Save the artifact
Write everything to `~/warm-outreach-list.md`:
- The ranked table (Name | Bucket | Fit | Warmth | First move).
- The three opener variations with their bracketed personalization slots.
- A short "start here" line naming the top 5 people to message first this week.

Confirm the path and tell the user: message the top 5 today, personalize one detail each, and don't send more than a handful a day — this is a conversation, not a campaign.

## Input → output example
**Input:** User runs the skill. Offer (from profile): "I build simple client-onboarding automations for bookkeepers, $500 setup." They brain-dump 24 names.

**Output — `~/warm-outreach-list.md` (excerpt):**

| Name | Bucket | Fit | Warmth | First move |
|---|---|---|---|---|
| Dana R. | Past client | 3 | 3 | Soft signal (msg first) |
| Marcus (ex-coworker) | Colleague | 2 | 3 | Reconnect → soft signal |
| Priya, bookkeeping group | Community | 3 | 2 | Soft signal |
| Uncle Tom | Personal | 1 | 3 | Referral ask |

**Soft signal opener:**
> hey Dana — was just thinking about [the mess we untangled with your intake forms last year]. i've been building little automations that handle exactly that kind of onboarding busywork for bookkeepers now. no pitch, just curious — is client onboarding still a headache on your end?

**Start here:** Dana, Priya, Marcus, then two more — 5 messages this week, one personal detail each.

## Notes / edge cases
- If the user has almost no network, that's real — steer them to the "connectors" angle (referral openers) and to one warm community they're already in, rather than pushing them cold before they're ready.
- Never write an opener that misrepresents the relationship or fabricates a shared memory. If the user can't fill the `[bracket]`, the person isn't warm enough for the soft-signal version — use reconnect instead.
- Keep the batch small. A huge list sent all at once reads as a blast and kills the warmth. Top 5 first.
- Pair naturally with the **dm-writer** skill when they want to fully craft the message for one specific person.
