---
name: launch-plan
description: Plan a simple revenue-spike launch for a product or offer — pre-sell, waitlist, Product Hunt / directory launch, or a limited-time / lifetime deal. Use when the user says "I'm launching X", "plan my launch", "how do I launch this", "I built something and want to sell it", "waitlist strategy", "do a lifetime deal", or "get a burst of sales". Picks the launch type that fits their stage, sets a date and a goal, and builds a day-by-day timeline plus an asset checklist. Saves a launch plan you can run.
---

# Launch Plan

You get a lightweight, day-by-day launch plan — the right launch type for your stage, a real date and revenue goal, the messages and assets you need, and exactly what to do each day. Built to create a spike of attention and sales in a short window.

**A launch is a spike, not your engine.** It concentrates demand you've been building into a few days for a burst of revenue and momentum. It does not replace the daily habit of showing up and making offers — treat this as an event on top of that, not a substitute for it.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

## What I need from you
1. **What are you launching?** (product, service, cohort, tool, community)
2. **What stage is it at?** Idea / building / built and ready to sell.
3. **How big is your audience right now?** (email list size, followers, or "basically none yet" — this changes the plan a lot)
4. **Do you have a date in mind, or should I set one?**
5. **What's your revenue or signup goal for the launch?** (a number to aim at)

## Steps

1. **Load the brand profile** for voice, offer, audience, price, and default CTA. If the offer/price isn't set and this launch is for it, capture it now and save it back.

2. **Pick the launch type that fits their stage.** Recommend one — don't dump all options:

   - **Pre-sell** — *product isn't built yet, or you want validation before building.* Sell it before it exists at a founder price. If it doesn't sell, you saved yourself the build. Best when you're unsure demand is real.
   - **Waitlist** — *built or nearly built, and you want to stack up demand before opening.* Collect interested people, then open to them first with urgency. Best for building anticipation with a warm-ish audience.
   - **Directory / Product Hunt launch** — *a tool, app, or software product* that benefits from a discovery-platform spike (Product Hunt, relevant directories, subreddits, communities). Best when the product is self-serve and demoable.
   - **Limited-time or lifetime deal** — *built and ready, you want a hard revenue spike now.* A deadline or a one-time lifetime price forces the decision. Best when you have some audience and want cash + momentum fast.

   If the audience is "basically none", say so plainly: a launch to nobody is just a quiet day. Recommend either a pre-sell to a small warm list / DMs, or spending the pre-launch window building an audience or a waitlist first — don't promise a spike that the reach can't produce.

3. **Set the date and the goal.** Pick (or confirm) a launch date far enough out to build the assets and warm the audience — usually 1 to 3 weeks. Write the goal as a concrete number (e.g. "30 pre-sales" / "$5,000" / "150 waitlist signups"). A launch without a number is a wish.

4. **Build the asset / message checklist.** Keep it lightweight — the minimum that makes the launch work, not a marketing-agency deliverable list. Typical set:
   - The **core offer page** (sales page, waitlist page, or Product Hunt listing) — where people actually buy or sign up.
   - A **short pre-launch teaser** sequence (2-3 posts / emails building curiosity).
   - The **launch-day announcement** (the big "it's live" message).
   - **Mid-launch** proof/urgency message(s).
   - The **closing / last-chance** message when the window ends.
   - The **checkout or signup link** (from the profile if set).
   Mark which assets they already have vs. need to make. Offer to draft any of the messages in their voice.

5. **Write the day-by-day timeline.** Work backward from launch day. A simple shape:

   - **Days before (pre-launch):** warm the audience — teasers, behind-the-scenes, "something's coming", open the waitlist. Build anticipation, don't sell yet.
   - **Launch day:** announcement goes everywhere at once. Direct people to the one link. Reply to every comment/DM.
   - **Open window (the next few days):** daily messages — new angle each day (proof, objection, a story, urgency as the deadline nears). Keep making the offer.
   - **Close day:** last-chance message(s), the deadline lands, then close the cart / end the deal. Deadlines drive the majority of sales — protect the deadline.
   - **After:** thank buyers, deliver, and note what worked for next time.

   Lay it out as an actual dated schedule (Day -7, Day -3, Day 0, Day +1...), each day with the one or two concrete actions for that day.

6. **Save the plan** as a Markdown file at `~/launches/launch-[offer-slug]-[YYYY-MM-DD].md` (create the folder if needed) containing: launch type + why, date, goal, asset checklist (with have/need marked), and the day-by-day timeline. Tell the user the path, then offer to draft the first pre-launch teaser to get them moving.

## Example

**Input:**
> "I built a Notion template pack for freelancers. It's done. I've got about 1,200 email subscribers and post on LinkedIn. Want to make some real money off it this month."

**Output (excerpt of saved plan):**

> **Launch type: Limited-time deal** — it's built, you have a warm list of 1,200, and you want cash now. A 5-day deal with a real deadline turns your existing audience into a spike.
>
> **Date:** Launch Monday July 21, close Friday July 25 midnight.
> **Goal:** 60 sales.
>
> **Checklist**
> - [have] The template pack + checkout link
> - [need] Sales page with the deadline + price
> - [need] 3 pre-launch teasers (this week)
> - [need] Launch-day email + LinkedIn post
> - [need] Daily emails Tue–Fri (proof, objection, story, last-chance)
>
> **Timeline**
> - **Day -5 to -1:** Tease it — "dropping something Monday for freelancers who hate admin." One LinkedIn post + one email.
> - **Day 0 (Mon):** It's live. Email + LinkedIn + Stories. One link. Reply to everyone.
> - **Day +1 (Tue):** Proof email — screenshots of the template in use.
> - **Day +2 (Wed):** Objection email — "is it worth it if I already use Notion?"
> - **Day +3 (Thu):** Story email + "48 hours left."
> - **Day +4 (Fri):** Two last-chance emails. Close at midnight. Do not extend.
> - **Day +5:** Thank buyers, deliver bonuses, log what converted.

## Notes / edge cases
- **Protect the deadline.** Most sales come in the final 24 hours. If you extend, you teach people your deadlines are fake and next launch converts worse.
- **Don't over-build assets.** A launch fails from no audience or no urgency, never from a missing seventh email. Ship the minimum and go.
- **Match audience size to expectation.** Set the goal against real reach — a spike is a percentage of the people who see it, not a miracle.
- **This is an event, not the engine.** Remind the user to keep their normal offer-making going after the launch spike settles.
