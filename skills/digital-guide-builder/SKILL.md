---
name: digital-guide-builder
description: "Turn one person's expertise into ONE finished, sellable digital guide/ebook, fast. Interviews the user briefly on their niche, angle, and pillars, then writes a full polished guide where every chapter delivers one concrete unlock, formats it as a clean print-ready file, and writes storefront listing copy (title, pitch, price, bullets). Use when the user wants to build a digital guide, ebook, PDF product, or storefront product from their own knowledge, says 'help me make a digital product', 'turn my knowledge into an ebook', 'build a guide I can sell', 'make me a Stan Store / Gumroad product', or /digital-guide-builder. NOT a general-purpose book-writing tool."
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
metadata:
  argument-hint: "your niche/expertise, your audience, and the transformation you help people get"
  user-invocable: true
---

# Digital Guide Builder

Turns one person's real expertise into one finished, sellable digital guide. Think of the well-known
case study of a creator with no design background who made tens of thousands of dollars in two weeks
from a short, focused first ebook sold through a simple storefront — this skill is what actually builds
their version of it.

Scope is deliberately narrow: ONE person, ONE guide, shipped fast. Not a ghostwriting service, not a
multi-book series, not a general nonfiction-writing tool. If the user wants something broader (a course,
a book series, ongoing content), point them elsewhere — this skill exists to get one sellable asset out
the door in a single session.

## Personalization
This skill writes in *your* voice, about *your* expertise. Before running, load the brand profile at
`~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your niche, audience, and the
  transformation you help people get — I'll create it).
- Prefer a writing sample the user pastes; fall back to the profile's Tone and Words-to-avoid as the
  voice baseline. Always use the user's own niche language and story.
- Never invent numbers, results, or claims the user did not give you.

## Step 1 — Intake (from the user's first message)

Pull these three things out of whatever the user gives you (or the brand profile):
- **Expertise/niche**: what they actually know how to do
- **Audience**: who they help
- **Transformation**: the result people get from following their method

If the user's opening message is thin (e.g. "help me build a guide to sell") and the profile doesn't
cover it, ask for these three directly before anything else. Don't guess at someone's expertise — a
wrong guess here means the whole guide is off.

## Step 2 — The Interview (2-4 questions, no more)

Once you have the Step 1 basics, ask ONLY what's still missing from this list. Skip anything already
answered. Never turn this into a 10-question intake — the whole point of the format is speed.

1. **The angle/story**: What's the one thing that makes THEIR version of this different — a specific
   moment, result, or mistake they can point to? (This becomes the hook of the guide and the reason
   someone buys from them instead of googling it for free.)
2. **The pillars**: 3-5 core lessons, steps, or principles they'd teach someone doing this from scratch.
   These become the chapters. If the user can't articulate them, propose a draft set based on their
   niche and confirm before writing.
3. **Length/page count**: Rough target (most first digital products run short: 20-40 pages / 4,000-8,000
   words total — a tight, high-signal guide, not a textbook). Default to short if the user has no
   preference; a guide that gets finished and read beats a long one that doesn't.
4. **Price point**: What they want to charge. If they don't know, recommend based on transformation
   value and comparable digital products: $9-$27 for a focused single-topic guide, $27-$47 if it
   includes templates/swipe files/worksheets, $47-$97 if it replaces a service they'd otherwise charge
   hundreds for. State the recommendation with the one-line reason, don't present an open menu.

Also ask, in the same round: **do you have any writing samples (a post, an email, a video transcript) I
can match your voice to?** If yes, read what they paste and write in that voice. If no, fall back to the
Tone in `~/.claude/brand-profile.md` (or a clean default: direct, confident, no fluff, short sentences,
specific over vague) — but always substitute in the user's own niche language and story.

## Step 3 — Structure the Guide

Build the chapter list from the pillars gathered in Step 2. Standard shape:

```
- Title page (title + subtitle + author name)
- Intro chapter: the hook/story (the angle from Step 2), what the reader will walk away able to do,
  who this is for
- One chapter per pillar (3-5 chapters) — see the unlock rule below
- Closing chapter: how to actually implement this, the single next action, light CTA to the reader's
  own next offer if they have one (optional, ask if unsure)
```

Every chapter must be built around ONE unlock, not a pile of information. An unlock is a specific,
actionable insight the reader didn't have before, paired with exactly how to apply it to their own
situation. Hormozi-style: plain words, no padding, no restating the same point three ways, no chapter
that could be summarized as "here's some context." If a chapter doesn't end with the reader knowing
exactly what to do differently, it's not done. Concrete over clever: never sacrifice clarity to hit a
word or page target.

Confirm the chapter list with the user in one short message before writing the full guide — this is the
one checkpoint where a wrong structure would waste the whole write. Keep it to a numbered list, not a
lengthy pitch.

## Step 4 — Write the Guide

Write the full guide once the structure is confirmed. Per chapter:
- Open with the concrete situation or question the reader is in, not a definition
- Teach the ONE unlock plainly, with a real example (from the user's angle/story where possible,
  otherwise a plausible scenario in their niche)
- Give the exact action to take, not just the idea
- Keep paragraphs short. White space does work. No jargon without explaining it in plain words.

Reuse the voice-and-rules checklist in `references/voice-and-rules.md` before finalizing: 6th-8th grade
reading level, no filler openers ("In today's world..."), no hedging language, specifics and numbers
over vague claims, never invent a stat or result the user didn't tell you about.

## Step 5 — Format for Export

Write the guide to a single Markdown file styled for clean PDF conversion — see
`references/guide-template.md` for the exact heading/structure convention (H1 title page, H2 per chapter,
no tables, no code blocks, no nested lists more than one level deep — all of these render badly in naive
Markdown-to-PDF converters). Keep formatting print-safe: standard headings, bold for emphasis only, no
HTML embeds. Save to a working folder named after the guide title, e.g. `~/guides/[Guide Title]/guide.md`.

Tell the user directly: paste this Markdown into a converter like Notion, Google Docs, or a
Markdown-to-PDF tool (many are free) and export as PDF — that's the file that gets uploaded to their
storefront. Do not attempt to generate a binary PDF yourself; the deliverable is the clean,
ready-to-export Markdown.

## Step 6 — Storefront Listing Copy

Write this as a separate block, ready to paste directly into a storefront product page (Stan Store,
Gumroad, Payhip, etc.), in this exact shape:

```
TITLE: [short, benefit-forward, matches the guide title]

PITCH (one paragraph, 3-5 sentences): who it's for, the transformation, why this person specifically is
credible to teach it (their real angle/story from Step 2), and what makes it different from free content
on the same topic.

SUGGESTED PRICE: $[X] — [one-line reason tied to the transformation value]

3 OUTCOME BULLETS:
- [Concrete thing the reader will be able to do]
- [Concrete thing the reader will be able to do]
- [Concrete thing the reader will be able to do]
```

Keep the pitch grounded in the real transformation from Step 1, never inflate it with numbers or claims
the user didn't give you.

## Step 7 — The Manual Steps Checklist (always end here)

This skill has no storefront or payment-processor access. Always close with this exact checklist so the
user knows precisely what's left and that nothing else is automatable from here:

```
WHAT'S LEFT (manual, can't be automated from here):
[ ] Create a storefront account (Stan Store, Gumroad, Payhip — pick one)
[ ] Connect a payment processor (e.g. Stripe) so you can get paid
[ ] Convert guide.md to PDF (paste into Notion/Docs/a free Markdown-to-PDF tool, export)
[ ] Create a new Digital Product in your storefront and upload the PDF
[ ] Paste in the title, pitch, and outcome bullets from above
[ ] Set the price
[ ] Publish and share your storefront link
```

## Output Format (final message to the user)

```
GUIDE STRUCTURE
[confirmed chapter list]

FILE: [path to guide.md]

----- STOREFRONT LISTING COPY -----
[title / pitch / price / 3 bullets]

----- MANUAL STEPS CHECKLIST -----
[the checklist from Step 7]
```

## Key Principles

- One person, one guide, shipped fast — not a general ebook-writing tool.
- The interview is short (2-4 questions) on purpose. Speed is the point.
- Every chapter is one unlock plus the exact action to take, never just information.
- Voice comes from the user's own samples first, the brand profile only as a fallback frame (niche and
  language always the user's own).
- Output is a clean, print-safe Markdown file, not a fragile HTML/PDF the skill can't verify.
- Never invent numbers, results, or claims the user didn't provide.
- Always end with the manual-steps checklist — this skill cannot touch a storefront or payment processor.
