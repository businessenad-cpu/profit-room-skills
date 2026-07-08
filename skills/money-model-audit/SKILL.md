---
name: money-model-audit
description: Audit an existing offer to find more revenue from the SAME customers — without more traffic, more leads, or a bigger audience. Use when the user says "audit my offer", "how do I make more money from what I have", "I'm leaving money on the table", "add an upsell", "should I raise my price", "how do I add recurring revenue", or "my offer only makes money once". Walks through the current single offer and surfaces 3-5 concrete backend moves ranked by effort. Saves a money-model action list.
---

# Money Model Audit

You get 3-5 concrete, ranked moves to make more money from the customers you *already* have — no new traffic required. Most people obsess over getting more leads while the real money is sitting in the offer they already sell. This audit finds it.

**The idea:** the same customer can be worth far more than a single one-time sale. Raise the price to match the value, add a bump at checkout, offer an upsell after yes, catch the no's with a downsell, add something recurring, and keep buyers longer. Each move is revenue you're currently leaving on the table with the exact same audience.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

## What I need from you
Walk me through your current offer:
1. **What do you sell, and at what price?** (the one main thing)
2. **Is it one-time or recurring?**
3. **Roughly how many do you sell a month, and does the number hold or do people leave?**
4. **What happens right after someone buys** — do you offer them anything else? (bump, upsell, next step, or nothing)
5. **What do people who say NO usually say?** (too expensive, not ready, too much)
6. **What outcome does the buyer actually get** — and how big is that outcome to them in money or time?

## Steps

1. **Load the brand profile** and combine it with the answers above to picture the current money model: one offer, one price, one transaction, and what (if anything) happens around it.

2. **Run the offer through the six backend levers.** For each, decide whether it's a real, specific opportunity for *this* offer — skip the ones that don't fit rather than forcing all six:

   - **Price to value (raise the price).** If the outcome is worth far more than the price, the price is too low. Look for signals: no one ever pushes back on price, you close nearly everyone, buyers are thrilled. Propose a specific new price and the value justification.
   - **Order bump (at checkout).** A small, cheap, instantly-relevant add-on offered right at the point of sale ("add X for $Y?"). Low effort, pure margin. What natural companion could ride along with the main purchase?
   - **Upsell (right after yes).** A bigger, related offer presented immediately after they buy, when trust is highest. "You got X — want me to also do Z / do it for you / go deeper?" What's the obvious next level up?
   - **Downsell (catch the no's).** A smaller/cheaper/payment-plan version for people who wanted in but the yes was too big. Turns some no's into smaller yeses. What's a lighter version of the offer?
   - **Recurring element.** Turn a one-time sale into ongoing revenue — a membership, retainer, support/maintenance plan, updates, or a subscription layer on top. What would people happily pay for month after month? This is usually the single biggest lever for a one-time offer.
   - **Retention (keep buyers longer).** If it's already recurring, plugging churn is cheaper than any new sale. Look at why people leave (from answer #3/#5) and propose one concrete fix — onboarding, a quick early win, a reason to stay.

3. **Pick the 3-5 strongest moves** for this specific offer. Don't list all six generically — choose the ones with real leverage here and make each one concrete: exactly what to add, roughly what to charge, and the one-line pitch/mechanism.

4. **Rank them by effort (fastest money first).** Order the moves so the user does the easy, high-return ones first:
   - **Quick wins (do this week):** usually price increase, order bump, downsell — mostly a decision + a sentence, little to build.
   - **Medium (this month):** upsell, a simple recurring add-on.
   - **Bigger (this quarter):** a full recurring/membership layer, a premium tier, a retention system.
   For each move include: the move, the specific implementation, estimated revenue impact (directional, honest — "roughly +20-30% on every sale", not a fake exact number), and effort level.

5. **Add one "premium tier" idea if it fits.** A done-for-you / VIP / higher-touch version at a notably higher price. Even if few buy it, it anchors the main offer and captures the customers who want the best. Sketch what it includes and a price.

6. **Save the audit** as a Markdown file at `~/money-model/audit-[offer-slug]-[YYYY-MM-DD].md` (create the folder if needed): the current model in one line, then the ranked action list with implementation + impact + effort for each move, plus the premium-tier idea. Tell the user the path and recommend they start with the top quick win this week. Offer to draft the actual bump/upsell/downsell copy for whichever move they pick.

## Example

**Input:**
> "I sell a $300 one-time website audit for small e-commerce brands. Do about 15/month. After they buy I don't offer anything else. People who say no usually say they'd rather I just fix the stuff. The audit typically finds issues costing them thousands in lost sales."

**Output (excerpt of saved audit):**

> **Current model:** One-time $300 audit · ~15/mo · nothing offered after · ~$4,500/mo.
>
> **Ranked moves**
>
> 1. **Raise price to $500 — quick win.** You find thousands in lost sales for $300; the price is far under the value and no one's pushing back. Impact: +$3,000/mo on the same volume. Effort: change one number.
> 2. **Downsell → "fix-it" done-for-you at $1,500 — quick win.** Your no's are literally asking you to fix it. Offer the implementation as the next step for anyone who declines (or accepts) the audit. Impact: even 3/mo = +$4,500/mo. Effort: write one offer.
> 3. **Order bump: "priority 48-hr turnaround +$100" — quick win.** Offered at checkout. Impact: pure margin on ~a third of buyers. Effort: one checkbox.
> 4. **Recurring: $200/mo "growth monitoring" retainer — medium.** Ongoing check-ins after the fix. Turns one-time buyers into monthly revenue. Impact: the biggest long-term lever. Effort: define the monthly deliverable.
>
> **Premium tier:** "Full teardown + 90-day done-with-you" at $4,000 — anchors the audit and captures brands who want it handled end to end.

## Notes / edge cases
- **Same customer, more value — that's the whole point.** This never assumes more leads. If the user only has "get more traffic" energy, redirect them here first: the backend is cheaper.
- **Be honest about impact.** Give directional ranges, not invented precise figures. Never fabricate what a change "will" earn.
- **Don't force all six levers.** A clean 3-move list that fits beats six generic suggestions. Skip what doesn't apply.
- **Deliverability matters.** Adding upsells/recurring only works if the user can actually deliver them — flag any move that would overload them so it doesn't wreck fulfillment.
- **Price is the user's call.** Recommend a number and the reasoning; let them set it.
