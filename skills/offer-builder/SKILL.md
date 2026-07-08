---
name: offer-builder
description: Build a Hormozi-style "Grand Slam Offer" so good people feel stupid saying no — engineered around the Value Equation (bigger dream outcome, higher belief it'll work, less time, less effort). Use this when the user says "build my offer", "make my offer irresistible", "help me package what I sell", "I don't know how to price/pitch this", "grand slam offer", "I built a product but nobody's buying", or when they have a thing to sell but no compelling way to present it. Push to run this before they try to sell anything.
---

# Offer Builder — engineer a Grand Slam Offer

Turn "here's my product" into an offer that's so stacked and de-risked the prospect feels dumb passing it up. You walk the user through the Value Equation, stack deliverables that each kill a specific obstacle, then name it and bolt on a guarantee, urgency, and bonuses. Output is a written, ready-to-pitch offer plus a one-line grand-slam statement they can say out loud.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

## The idea in one breath
People buy when the perceived value is high. Value goes UP when the **dream outcome** is bigger and the **likelihood they'll actually achieve it** feels higher. Value goes DOWN the more **time** it takes and the more **effort and sacrifice** it costs. So a great offer maximizes the top two and crushes the bottom two. Everything below is just doing that on purpose.

## Steps

### 1. Anchor the dream outcome
Ask the user (or pull from the profile's Audience + Transformation): *what does your buyer most want on the other side of this?* Get it concrete and emotional — not "learn marketing" but "land your first paying client in 30 days without cold-calling." Write it down as the headline promise. This is the top of the Value Equation.

### 2. List the obstacles (this is the goldmine)
Ask: *what stops your buyer from getting that result on their own?* Get 4–8 real obstacles — the fears, the missing skills, the time it eats, the past failures, the "I don't know where to start." Each obstacle is a bump the offer will smooth out. Write them as a list.

### 3. Stack deliverables — one per obstacle
For every obstacle, invent a deliverable that removes it. This is the core move: the offer isn't one thing, it's a stack where each item visibly kills an objection.
- Obstacle "I don't know where to start" -> a step-by-step roadmap or checklist.
- Obstacle "no time" -> done-for-you templates / a done-with-you sprint.
- Obstacle "what if it doesn't work for me" -> a live review or 1:1 call.
- Obstacle "I've failed before" -> a proven framework + examples.
Write each deliverable next to the obstacle it solves, and give each a tangible name and a rough standalone value.

### 4. Attack the bottom of the equation
Now cut time and effort explicitly:
- **Time delay:** what's the fastest first win, and can you name a timeframe? ("first result in 7 days"). Front-load a quick win.
- **Effort & sacrifice:** what can you make done-for-you, templated, or automated so they do less? Every "we do it for you" raises value.

### 5. Name the offer
Give the whole stack a name that implies the outcome (not the mechanism). "The 30-Day First-Client System" beats "My Coaching Package." Keep it short and outcome-loaded, in the user's tone.

### 6. De-risk it with a guarantee
Write a guarantee that reverses the risk onto you. Pick the strongest one the user is comfortable with: unconditional refund, conditional ("do the work, don't get X, full refund"), or a performance guarantee ("we keep working free until you get your first sale"). A specific guarantee beats a vague one.

### 7. Add real scarcity or urgency
Give a reason to act now that is TRUE — never fake a countdown. Legit forms: limited spots (you can only serve N people well), a cohort start date, a price that rises after launch, a bonus that expires. Write the exact line.

### 8. Sweeten with bonuses
Add 1–3 bonuses that handle the *next* objection after they say yes ("okay but how do I keep clients?"). Each bonus should feel like it could be sold on its own. Name each and give a value.

### 9. Write the finished offer + the grand-slam line
Assemble everything into a clean, pitch-ready offer, then distill it into ONE sentence they can say on a call or put on a page:
> "You get [dream outcome] in [timeframe], with [core stack], backed by [guarantee] — for [price]. Only [scarcity]."

## Output — save it
Write the finished offer to `~/offers/<offer-name>.md` (create the `~/offers/` folder if needed; slugify the name, e.g. `~/offers/30-day-first-client-system.md`). Confirm the path back to the user. The file must contain: the dream-outcome headline, the obstacle→deliverable stack table, the name, guarantee, scarcity, bonuses, total "value" vs price, and the one-line grand-slam statement.

## Example (input → output)
**Input:** User sells a $500 "Notion setup" service to freelancers. Dream outcome: "stop losing track of clients and projects." Obstacles: don't know how to structure it, no time to build it, tried before and abandoned it, scared it won't fit their workflow.

**Output (excerpt saved to `~/offers/freelancer-command-center.md`):**
- **Name:** The Freelancer Command Center
- **Promise:** Every client, project, and deadline in one dashboard within 5 days — without building anything yourself.
- **Stack:** Done-for-you Notion build (kills "no time") + a 20-min personalization call (kills "won't fit me") + a 1-page daily operating checklist (kills "I'll abandon it") + a Loom walkthrough (kills "don't know how to run it").
- **Guarantee:** If it's not saving you time in 14 days, I rebuild it or refund you.
- **Scarcity:** 4 builds a month so each gets personalized.
- **Bonus:** Client-onboarding template pack.
- **Grand-slam line:** "Get your whole freelance business running from one dashboard in 5 days, done for you, guaranteed — 4 spots this month."

## Notes / edge cases
- If the user has no proof yet, lean the guarantee and quick-win harder — those substitute for a track record.
- Keep pricing out of the deep end here; if they want help setting the number, hand off to the **pricing-calculator** skill.
- Don't overstack — 3–5 deliverables that each kill a real obstacle beats 12 filler items.
