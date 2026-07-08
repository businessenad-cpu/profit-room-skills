---
name: pricing-calculator
description: Set a value-based price for your product or service — priced on the outcome it creates for the buyer, not on your costs or hours. Quantifies the dollar value to the buyer, anchors 3 tiers (good/better/best), prices at a fraction of value delivered, pressure-tests against objections, and picks a payment structure. Use when the user says "how much should I charge", "what should I price this at", "am I charging too little", "price my offer", "set my rates", "should this be a subscription", or when they're about to undercharge. Push to run this whenever a price needs to be decided.
---

# Pricing Calculator — price on value, not cost

Non-technical founders almost always undercharge because they price on effort ("it only took me a weekend") instead of on the outcome the buyer gets. This skill flips that: quantify the value to the buyer, then charge a confident fraction of it. Output is a recommended price, a 3-tier table, and the value justification the user can say out loud without flinching.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

## Steps

### 1. Quantify the outcome in dollars
Pull the offer + transformation from the profile, then ask what the result is worth to the buyer. Find the number using whichever fits:
- **Makes money:** how much revenue/clients/sales does it help them get? ("first client = $2,000" or "one dashboard saves 5 hrs/week = $X").
- **Saves money:** what does it stop them spending (an agency, a tool, a hire)?
- **Saves time:** hours saved × what their time is worth.
- **Avoids pain:** cost of the problem staying unsolved (lost deals, stress, missed launches).
Write the honest value number, even a conservative range. This is the anchor for everything.

### 2. Set the price as a fraction of value
Rule of thumb: price so the buyer gets a no-brainer return — typically **10–20% of the value delivered** (i.e. a 5–10x return for them). If your work helps them make $10,000, a $1,000–$2,000 price is easy to justify. Compute a first-pass price from the value number, not from your hours.
- Sanity check the floor: it must comfortably clear your time and costs. If value-based lands below that, the offer or audience is wrong, not the price — flag it.

### 3. Anchor three tiers (good / better / best)
People choose between options better than yes/no. Build three:
- **Good** — the core outcome, most self-serve, lowest price. Makes entry easy.
- **Better** (the target — most buyers should land here) — core + the deliverables that remove the biggest obstacles (support, done-with-you, faster timeline). Price it as the obvious best value.
- **Best** — done-for-you / 1:1 / premium access / guarantee. Priced high partly to make "Better" look reasonable (the anchor).
Design "Best" so a few buyers actually want it — not just as a decoy. Put the target tier in the middle and make it visually the recommended one.

### 4. Pressure-test against objections
Say each likely objection out loud and make sure the price survives:
- "That's expensive" -> reframe against the value number and the cost of NOT solving it.
- "I could do it myself / find it cheaper" -> what's the time, risk, and gap they're really buying past?
- "How do I know it'll work" -> is there a guarantee or quick win backing the price? (If not, consider **offer-builder**.)
If an objection kills the price, adjust the price OR strengthen the offer — note which.

### 5. Choose the payment structure
Match structure to how the value shows up:
- **One-time** — a defined deliverable / transformation with an endpoint.
- **Subscription / retainer** — ongoing value, access, or maintenance. Best for predictable revenue; needs continuing value or churn hits.
- **Deposit + balance / payment plan** — higher-ticket; lowers entry friction. A deposit also filters for serious buyers.
Recommend one, and offer a plan option if the price is high enough to scare a good-fit buyer.

## Output — save it
Write the result to `~/offers/pricing.md` (create `~/offers/` if needed). Include: the buyer value number (with how it was derived), the recommended headline price, the good/better/best tier table with what's in each, the recommended payment structure, and 2–3 "say it out loud" value-justification lines the user can use on a call. Confirm the path back to the user.

## Example (input → output)
**Input:** User builds custom AI chat assistants for local service businesses. It took them a weekend; they were going to charge $300.

**Output (saved to `~/offers/pricing.md`):**
- **Value to buyer:** captures ~10 missed leads/month; each lead ≈ $150 → ~$1,500/mo, ~$18k/yr.
- **Recommended price:** $1,500 setup, priced at ~10% of first-year value.
- **Tiers:** Good — assistant setup, $1,500. **Better (target)** — setup + 3 months of tuning & support, $2,500. Best — done-for-you across 2 locations + monthly optimization retainer, $4,000 + $500/mo.
- **Structure:** one-time for Good/Better; retainer on Best; 50% deposit option on all.
- **Say it out loud:** "This pays for itself the first month it catches leads you're missing right now."

## Notes / edge cases
- Never price on your hours — a weekend build that makes the client $20k is not a $300 job.
- If the buyer genuinely can't realize much value, that's a positioning problem — send them to **positioning-filter** or a higher-value audience.
- Round to confident numbers ($1,500, not $1,487). Odd cost-plus math signals amateur.
- For a brand-new offer with zero proof, it's fine to start one notch lower to gather testimonials — say so explicitly and set the "real" price to raise to.
