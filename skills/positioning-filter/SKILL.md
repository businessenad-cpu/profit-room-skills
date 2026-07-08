---
name: positioning-filter
description: Find and lock the ONE angle that makes your offer and content stand out, so you stop sounding like everyone else in your niche. Runs a 3-question filter (what's my unique angle, why would my audience care, how does it ladder to my offer) plus a "what to cut" test, and saves a reusable positioning statement + a one-line differentiator. Use when the user says "help me stand out", "what's my angle", "why would anyone pick me", "I sound like everyone else", "find my positioning", "sharpen my message", or when their content or offer feels generic. Push to run this before writing content or a sales page.
---

# Positioning Filter — lock your angle

Most people fail not because their offer is bad but because it's indistinct. This skill forces a single, defensible angle through three questions and a cut test, then saves a positioning statement and a one-line differentiator the user can reuse across their bio, content, and pitch.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

## Steps

### 1. Question 1 — What's my unique angle?
Pull the user's What-you-do, Audience, and Proof from the profile, then ask them to finish these until one feels sharp and true:
- "Everyone in my niche says ___. I say ___ instead."
- "The thing I do differently is ___."
- "My unfair advantage / weird background is ___." (their past job, their own transformation, a method they use, a specific audience they get deeply).
Push for a *contrast* — an angle only earns attention when it pushes against the default advice. Write the strongest candidate down.

### 2. Question 2 — Why would my audience care?
An angle is only positioning if the audience feels it. Translate the angle into the audience's language using the profile's Main-pain:
- "For [audience] who are tired of [the common approach], I [angle] so they can [outcome]."
- Pressure-test: does this hit a pain they'd say out loud? If it's clever but they wouldn't nod, it's a slogan, not positioning. Rewrite until it lands on a real pain.

### 3. Question 3 — How does it ladder to my offer?
The angle has to point at what they sell, or it's just personality. Connect them:
- "My angle naturally leads someone to want [offer] because ___."
- If the angle attracts an audience that would never buy the offer, it's the wrong angle — flag that and adjust.

### 4. The "what to cut" test
Positioning is defined as much by what you refuse to be. Run these cuts:
- **Cut the audience:** who is this explicitly NOT for? Name them. Repelling the wrong people sharpens the pull on the right ones.
- **Cut the topics:** list 2–3 things in the niche the user will deliberately NOT talk about, so they own a lane instead of covering everything.
- **Cut the hedges:** strip "I also do X, and Y, and Z." One spearpoint beats five.
Write down what got cut — it's proof the positioning is specific.

### 5. Assemble the positioning statement + one-liner
Write a short positioning statement in this shape:
> "I help [specific audience] [achieve outcome] by [unique angle/method], without [the thing they dread]. Unlike [the default in the niche], I [differentiator]."

Then compress it into a single reusable **differentiator line** for their bio/hook, e.g. "The [outcome] guy for [audience] who hate [common approach]." Keep both in the user's tone and banned/loved words.

## Output — save it
Write the result to `~/offers/positioning.md` (create `~/offers/` if needed). Include: the chosen angle, the audience-facing "why they care" line, the offer ladder link, the cut list (who/what it's NOT), the full positioning statement, and the one-line differentiator. Confirm the path and tell the user they can paste the one-liner into their bio and reuse the statement on any sales page.

## Example (input → output)
**Input:** User teaches non-technical people to build software with AI tools. Niche is flooded with "learn to code" and "AI hacks" content.

**Output (saved to `~/offers/positioning.md`):**
- **Angle:** "Everyone says learn to code. I say you don't need to — you need to build one real thing people pay for."
- **Why they care:** "For career-changers who are tired of tutorials that go nowhere, I get you to a working, sellable product, not a certificate."
- **Ladders to offer:** points straight at the "build your first paid product" program.
- **Cut:** not for professional developers; won't cover algorithms, whiteboard interviews, or which framework is best.
- **Positioning statement:** "I help non-technical career-changers build and sell their first software product using AI, without learning to code the hard way. Unlike coding bootcamps, I optimize for a paying customer, not a portfolio."
- **One-liner:** "The 'skip the bootcamp, build the product' guy for non-technical builders."

## Notes / edge cases
- If the user gives three different angles, make them pick ONE to lock now; they can test others later. Diffuse positioning is the failure mode.
- Generalize from the user's own story and audience — never borrow another creator's angle wholesale.
- If the angle doesn't ladder to any offer they have, that's a signal to fix the offer (hand off to **offer-builder**) or the angle, not to ship it as-is.
