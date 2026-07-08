---
name: productize-service
description: Turn a custom service (or something you keep doing manually for people) into a repeatable, sellable PRODUCT with a fixed scope, name, price, and delivery process — so you stop quoting from scratch every time and can sell the same thing over and over. Use when the user says "productize my service", "make this repeatable", "I keep doing this custom for everyone", "package what I do", "turn my service into a product", "I'm stuck trading time for money", or when they describe bespoke one-off work. Push to run this when work is repeatable but sold as custom.
---

# Productize Service — make it repeatable and sellable

Custom work doesn't scale: every sale starts at zero, scope creeps, and pricing is a guess. Productizing means finding the repeatable core of what you do and wrapping it in a fixed deliverable, a name, a price, and a delivery process — so it sells like a product on a shelf. Output is a one-page productized offer.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

## Steps

### 1. Find the repeatable core
Ask the user to describe the last 2–3 times they did this work. Then find what was the SAME every time — the 80% that repeats regardless of client. That common core is the product; the rest is custom noise.
- "What do you do on every single one of these, no matter who it's for?"
- "What's the outcome the client actually cares about at the end?"
Write the repeatable core as a single sentence: "I take [input] and turn it into [outcome]."

### 2. Define ONE fixed deliverable
Replace "it depends" with a concrete, named thing the buyer receives. Not "consulting" — a **deliverable** with clear edges.
- What exactly do they get? (a built X, a set of Y, a system, a report + walkthrough).
- What does "done" look like? Define the finish line so both sides know when it's complete.
Write the deliverable as a short bulleted spec of what's included.

### 3. Set a fixed timeline
A product has a delivery time. Give it one: "delivered in 7 days," "2-week sprint," "live within 48 hours." A fixed timeline is a selling point and it protects the user from endless revisions. Pick the realistic outer edge and state it plainly.

### 4. Cut the bespoke scope (draw the box)
This is the hard part: explicitly list what is NOT included, so the product stays repeatable. Scope creep is what turns products back into custom hell.
- Name the out-of-scope requests you'll say no to (or sell as an add-on).
- Cap the variables — e.g. "up to 5 pages," "one revision round," "one platform."
- Turn recurring custom asks into named **add-ons** with their own price instead of free extras.
Write the "included / not included / add-ons" boundaries clearly.

### 5. Name and package it
Give the product a name that sells the outcome, not the process (see **offer-builder** if you want to stack it into a full grand-slam offer). Then package the pieces so it reads like a product:
- Product name (outcome-loaded).
- One-line promise: "You get [deliverable] in [timeline], done for you."
- Price (a fixed number — hand off to **pricing-calculator** if unsure; productized work should be value-priced, never hourly).

### 6. Decide fulfillment (how it actually gets delivered)
Pick how you'll deliver it the same way every time — this is what makes it repeatable in practice:
- **Do-it-yourself:** they buy templates/a course/a tool and run it themselves (most scalable).
- **Done-with-you:** a set process + calls where you guide them (repeatable + higher touch).
- **Done-for-you:** you run your fixed process for them (highest price, cap your slots).
Then write the **standard delivery steps** — the same checklist you'll run on every order (intake -> build -> review -> handoff). This checklist is the product's operating system.

## Output — save it
Write a one-page productized offer to `~/offers/<product-name>.md` (create `~/offers/` if needed; slugify the name). The one-pager must contain: the repeatable core, the fixed deliverable spec, the timeline, the included/not-included/add-ons boundaries, the name + one-line promise + price, the fulfillment model, and the standard delivery checklist. Confirm the path back to the user.

## Example (input → output)
**Input:** User does "freelance automation help" — every job is different, quoted ad hoc, scope always creeps.

**Output (saved to `~/offers/inbox-rescue.md`):**
- **Repeatable core:** take a small business's messy lead intake and turn it into one automated pipeline.
- **Fixed deliverable:** a connected intake form → CRM → auto-reply flow, plus a Loom walkthrough.
- **Timeline:** live in 5 business days.
- **Boundaries:** included — one intake source, one CRM, one auto-reply sequence. Not included — custom code, multi-brand setups. Add-ons: extra sequence ($200), second location ($400).
- **Name / promise / price:** "Inbox Rescue — your leads captured and answered automatically in 5 days, done for you. $1,200."
- **Fulfillment:** done-for-you, 4 slots/month.
- **Delivery checklist:** intake call -> map current flow -> build -> test with sample leads -> walkthrough + handoff.

## Notes / edge cases
- If nothing repeats across their last few jobs, they may not be ready to productize one service — help them pick the single most common request and product-ize THAT first.
- Resist the urge to make the product do everything. A narrow, boring, repeatable product outsells a flexible custom one.
- Once productized, the same one-pager doubles as the sales page and the delivery SOP.
