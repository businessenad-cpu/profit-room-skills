---
name: proposal-generator
description: Turn a discovery conversation into a clean, persuasive proposal that actually closes. Use when the user says "write a proposal", "I had a call with a client, make me a proposal", "turn these notes into a proposal", "send a quote", "how do I price this", or has a prospect who needs a written offer before they'll say yes. Writes in the user's voice, structures the whole thing so the buyer sees the value before the price, and saves a ready-to-send document.
---

# Proposal Generator

You get a persuasive, ready-to-send proposal built from what you learned on your discovery call — structured so the buyer feels understood, sees the outcome, and reaches a price that already feels justified.

A proposal is not a price list. It is a short, confident document that mirrors the prospect's problem back to them, paints the after-state, and makes saying yes the obvious next step. This skill builds exactly that.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

## What I need from you
Give me whatever you have — call notes, a voice memo transcript, or just answers to these. If something's missing, I'll ask for it (I won't guess on price or scope):

1. **Who is this for?** (person + company, and what they do)
2. **What did they say they need?** The problem in their own words is gold — paste it if you have it.
3. **What outcome do they want?** What does "this worked" look like for them?
4. **What are you proposing to deliver?** The actual work / scope.
5. **Your price**, and whether you want to offer more than one option.
6. **Timeline** — when you can start and roughly how long it takes.
7. **Any guarantee or risk-reversal** you're comfortable offering (optional but it closes).

## Steps

1. **Load the brand profile** for your name, voice, offer, and any real proof/wins you can cite. Pull tone and words-to-avoid so the proposal sounds like you, not a template.

2. **Collect the inputs above.** If price, scope, or the prospect's core problem is missing, ask before writing — these are the load-bearing pieces and I won't invent them.

3. **Write the proposal** using this structure (each section short — the whole thing should be skimmable in under two minutes):

   - **Title + who it's for** — "Proposal for [Name] / [Company]", dated.
   - **The problem** — restate their situation in their own language. This is the most important section: if they don't feel understood here, price won't matter. Two or three sentences.
   - **The desired outcome** — the after-state, concrete and specific to them. What changes in their business/life when this is solved.
   - **Scope & deliverables** — a clean bulleted list of exactly what they get. Specific and countable, not vague ("3 landing page designs + 2 rounds of revisions", not "design work").
   - **Timeline** — start date, milestones if any, delivery date. Short.
   - **Investment** — the price, framed against the value of the outcome. Use an **anchored option table** (see below).
   - **Guarantee / risk-reversal** — if provided. Removes the fear of saying yes.
   - **Next step** — ONE clear action. "Reply 'yes' and I'll send the invoice and kickoff link." Never end with a vague "let me know."

4. **Build the investment table with anchoring.** Even for a single offer, present it so the recommended option looks like the smart middle choice. Default to three tiers unless the user only wants one:

   | Option | What's included | Investment |
   |---|---|---|
   | **Essential** | core deliverable only | lower price |
   | **Complete** (recommended) | core + the things that actually get the result | target price |
   | **Premium** | Complete + ongoing/extra | higher price |

   Mark the middle one "recommended". The high tier makes the target price feel reasonable; the low tier gives a yes-able floor instead of a walk-away. If the user gave only one price, build the table around it (put their price as "Complete" and construct a lighter and a heavier option), and confirm the framing with them.

5. **Match the voice.** Apply the profile's tone and words-to-avoid. No filler, no "we are pleased to present", no hedging. Confident and plain. Write like the user talks to a peer they respect.

6. **Save the proposal** as a Markdown file at `~/proposals/proposal-[client-slug]-[YYYY-MM-DD].md` (create the folder if needed). Tell the user the path and offer to also produce a copy-paste email/DM version and a clean HTML version they can send as a link.

## Example

**Input (call notes):**
> "Talked to Maria, runs a boutique Pilates studio, 3 locations. Books are a mess — she's using paper + texts, double-books constantly, loses ~10 clients/month to booking friction. Wants online booking that her non-techy front desk can run. I'd build her a booking site + automated reminders. Thinking $3,500. Can start next week, ~3 weeks of work."

**Output (excerpt of saved proposal):**

> **Proposal for Maria — [Studio Name] · 2026-07-07**
>
> **Where you are now**
> Three locations, all booked by paper and text. You're double-booking, your front desk is buried, and roughly ten clients a month walk because booking is too much friction. Every one of those is recurring revenue you already earned and lost at the door.
>
> **Where this gets you**
> One online booking page your front desk can run without training, automatic reminders that cut no-shows, and no more double-bookings — so those ten clients a month stay booked instead of slipping.
>
> **What you get**
> - Branded online booking site across all 3 locations
> - Automated SMS + email reminders (cuts no-shows)
> - Front-desk dashboard, built simple enough to hand off day one
> - 2 rounds of revisions + a 30-min training walkthrough
>
> **Timeline:** Start Monday · delivered in 3 weeks
>
> **Investment**
>
> | Option | Includes | Investment |
> |---|---|---|
> | Essential | Booking site only | $2,200 |
> | **Complete (recommended)** | Booking site + reminders + dashboard + training | **$3,500** |
> | Premium | Complete + 3 months of managed support | $4,900 |
>
> **My guarantee:** If the booking flow isn't live and working across all three locations by the delivery date, you don't pay the final half.
>
> **Next step:** Reply "let's go" and I'll send the invoice + a kickoff form. We start Monday.

## Notes / edge cases
- **Don't invent the prospect's words.** If the user didn't capture the problem in the buyer's language, ask for it or write it plainly from the notes — never fabricate a quote.
- **One clear next step.** A proposal that ends with "let me know your thoughts" stalls. Always close with a single, specific action.
- **Price is the user's call.** Suggest anchoring structure, but never set or change a number they didn't give you.
- If the user has no guarantee they're comfortable with, skip that section rather than inventing risk they don't want to take.
