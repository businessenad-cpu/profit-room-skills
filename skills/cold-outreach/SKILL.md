---
name: cold-outreach
description: A simple cold outreach system for people who've ALREADY closed at least one sale by hand and want to reach more of the same buyer on purpose. Use when the user says "cold outreach", "cold email", "cold DMs", "how do I get clients", "reach out to prospects", "build a prospect list", or "I need more leads". Defines a tight target list, helps find 25-50 real prospects, writes a personalized first line per prospect, and lays out a short 3-touch cadence. Saves a prospect list template + the message cadence.
---

# Cold Outreach

You get a small, sharp cold outreach system: a clearly-defined target, a list of real prospects, a personalized opener for each, and a 3-touch message cadence — the whole thing built to start real conversations, not blast spam.

**Do this only after you've made at least one sale by hand.** Cold outreach scales a sale you already know how to close. If you've never had someone say yes and pay you, don't automate that yet — go make one manual sale first (a warm intro, a DM, a friend of a friend), learn what actually lands, then come back and scale it. Automating a sale you've never made just scales confusion.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

## Requirements
This skill is **tool-agnostic** — you can run the whole thing by hand. Some steps go faster with tools, all optional:
- **Finding prospects:** manual (LinkedIn/Google/directories) always works. A scraping tool (e.g. an Apollo/PhantomBuster-type list builder) or a web-scraping MCP can speed up list-building if you have one.
- **Sending:** manual sending (one by one) is fine and actually converts better early on. A cold-email tool (Instantly, Smartlead, etc.) or your normal inbox both work.
- If you don't have any tool set up, that's fine — I'll produce a list template and messages you send by hand. I'll never send on your behalf or use a key you haven't given me.

## What I need from you
1. **Confirm you've made at least one sale.** What did you sell, and to whom? (Your best existing customer is the blueprint for the whole list.)
2. **What are you offering** in this outreach, and the rough price?
3. **Which channel** — cold email, LinkedIn DMs, or Instagram/X DMs?
4. Anything you already know about **where your buyers hang out** (industries, job titles, communities, locations).

## Steps

1. **Load the brand profile** for voice, offer, audience, proof, and words-to-avoid. The messages must sound like the user, not like a sales robot.

2. **Define tight target criteria.** Vague targeting kills cold outreach. Nail down a specific, findable profile — the more specific, the more personal every message can be. Pin these:
   - **Who** — role/title + type of business (e.g. "owner of a 2-5 location dental practice", not "healthcare").
   - **Trigger / fit signal** — something observable that means they need this now (hiring, just launched, running ads, bad website, recent funding, a visible pain).
   - **Where to find them** — the specific place this person is listable (a directory, a LinkedIn search, a subreddit, a conference attendee list, a tool's public users).
   - **Disqualifiers** — who to skip so you don't waste touches.
   Anchor the target on the user's *existing* buyer: "more people like the one who already paid me."

3. **Find and list 25-50 real prospects.** Quality over volume — 30 well-fit prospects beat 500 random ones. Help the user gather them (manually or, if they have a scraping tool/MCP, assist with that). For each prospect capture: name, company, role, channel handle/email, and **one specific observation** (something real about them you can reference — a recent post, their website, a launch, a review). That observation is the raw material for personalization; a row with no observation gets a generic message, which fails.

   Write these into the **prospect list template** at `assets/prospect-list-template.csv` (ship a copy for the user to fill / append to). Save the working list to `~/outreach/prospects-[target-slug]-[YYYY-MM-DD].csv`.

4. **Write a personalized first line per prospect.** The opener is the whole game — it proves you're a human who looked, not a blast. Rules:
   - Reference the **specific observation** from their row (their post, their site, their launch), not a generic "love what you're doing."
   - Make it about *them*, not you. No "My name is X and I do Y" opener.
   - One sentence. Then a short, relevant reason you're reaching out.
   Generate a custom first line for each prospect and store it in the list (a `first_line` column). If a row has no real observation, flag it — don't fake specificity.

5. **Write the 3-touch cadence.** Short, spaced, and each touch adds something new — never "just bumping this." Default shape (adapt to channel):
   - **Touch 1 (day 0):** personalized opener → the one-sentence problem you solve for people like them → a soft, low-friction ask (a question or "worth a quick look?"), not a hard pitch.
   - **Touch 2 (day 3-4):** new angle — a relevant proof point, a specific result, or a useful resource. Adds value, doesn't nag.
   - **Touch 3 (day 7-8):** the clean close / breakup — "Should I close the loop, or is this worth a 15-min chat?" Gives an easy yes or a clean out.
   Keep every message short (a few sentences), in the user's voice, with the profile's default CTA. Write the templates with a `{{first_line}}` merge slot so each send is personalized.

6. **Save the system** as a Markdown file at `~/outreach/cadence-[target-slug].md` containing: the target criteria, the 3 message templates, and cadence timing. Point the user to both files (the prospect CSV and the cadence doc), and tell them the honest next move: **send the first 10 by hand**, watch what gets replies, then tune the opener before scaling. Offer to draft first lines for the rest of the list once the opener is working.

## Example

**Input:**
> "I closed one client — built a booking website for a local barber, he paid $1,500 and loves it. Want to get more local service businesses. Cold email."

**Output (excerpt):**

> **Target:** Owners of local service businesses (barbers, salons, detailers, gyms) with an outdated or no website, 1-3 locations, in [their metro]. Trigger: their current site looks broken on mobile OR they only have an Instagram, no site. Find them via Google Maps + Instagram local business tags. Skip: chains, anyone with a slick modern site.
>
> **Prospect row example:**
> `Marco's Barbershop | Marco Ruiz | owner | marco@... | "IG only, no website, 4.9 stars / 300 reviews" | first_line: "Marco — 300 five-star reviews and no website to send them to? That's a lot of walk-ins you can't rebook."`
>
> **Cadence — Touch 1 (email):**
> Subject: quick thought on Marco's Barbershop
> "{{first_line}} I build simple booking sites for shops like yours — clients book themselves, you stop losing the after-hours ones. I just did one for a barber down the road and rebooks went up. Worth a quick look at what it'd be for you?"
>
> **Touch 2 (day 4):** send a screenshot of the barber site you built + the one-line result.
> **Touch 3 (day 8):** "Want me to close the loop on this, or is a 15-min call worth it? Either's fine."

## Notes / edge cases
- **One manual sale first — non-negotiable.** If the user hasn't closed anyone, redirect them to make one warm/manual sale before scaling. Don't build the machine on an unproven offer.
- **Personalization is the point.** A row with no real observation produces a generic message that gets ignored. Flag those rows; don't fabricate a detail about a real person.
- **Send small first.** The first 10-20 sends are a test, not the campaign. Tune the opener on real replies before mass-sending.
- **Respect the channel's rules.** Don't blast hundreds of DMs/day (you'll get flagged) and follow cold-email basics (real domain, easy opt-out) — but keep volume low and quality high regardless.
- **Never fabricate proof.** Use only real wins from the profile in Touch 2. One honest result beats an invented case study.
