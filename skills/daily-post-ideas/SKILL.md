---
name: daily-post-ideas
description: Generate 5 personalized LinkedIn post ideas for the user, one per content category, each with a ready-to-paste hook line and a one-line angle. Use whenever the user asks for LinkedIn post ideas, says "what should I post today", "give me content ideas for LinkedIn", "5 post ideas", or invokes /daily-post-ideas. Always trigger for LinkedIn content ideation — even casual asks like "I need to post something today" or "what's a good LinkedIn topic for me".
---

# Daily LinkedIn Post Ideas

Generate 5 LinkedIn post ideas — one per category — each with a scroll-stopping hook line and a brief angle. No web search needed, no extra input required. Everything comes from the user's brand profile.

## Personalization
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

## Process

1. Read `~/.claude/brand-profile.md`. Pull the user's Audience, Main-pain, Offer, Transformation, Proof, Tone, and Words-to-avoid. These drive every idea.

2. If the user has run the **positioning-filter** skill, apply their locked angle silently so every hook sounds like *them*, not generic advice. If they haven't, just work from the profile.

3. Note today's date from context for any seasonal or timely relevance.

4. Generate exactly 5 ideas, one per category below. Use the audience's own language in the hooks — the words they'd actually use, not marketing-speak. Don't repeat the same format or angle twice.

## Output Format

Present ideas in this exact format:

---

**Here are 5 LinkedIn post ideas for today:**

**1. Lesson**
Hook: [opening sentence ready to paste as the first line of a post]
Angle: [one sentence describing where the post goes from there]

**2. Hot Take**
Hook: [opening sentence]
Angle: [one sentence]

**3. Story**
Hook: [opening sentence]
Angle: [one sentence]

**4. Tool / How-To Tip**
Hook: [opening sentence]
Angle: [one sentence]

**5. Community Pull**
Hook: [opening sentence]
Angle: [one sentence]

---

After the 5 ideas, add one line:
> Pick one and say "write it" to draft the full post.

## Category Definitions

**Lesson** — A specific insight the user earned from doing their actual work. Should feel earned, not generic. Pull from their Proof or Transformation where possible.

**Hot Take** — A contrarian or counterintuitive opinion about their industry or how people in it work. Should make someone stop scrolling. Not clickbait — a real opinion backed by experience.

**Story** — A behind-the-scenes moment: something that went wrong and got fixed, a surprising result, a client win, a change that mattered. Specific beats vague.

**Tool / How-To Tip** — One concrete, immediately actionable technique from the user's process. "Here's the exact step/setting/approach" energy. The audience should be able to use it today.

**Community Pull** — A value-first post that naturally makes the user's offer feel like the obvious next step. No hard CTA, no links. The content itself does the pulling.

## LinkedIn Rules (always apply)

- Write all hooks in **first person** — "I", "my", "me". Never use the author's name.
- **No external links or URLs** anywhere in the ideas. Links kill LinkedIn reach.
- Keep hooks under 2 lines — they need to work as the visible preview before "see more".
- Hooks should create tension, curiosity, or a strong opinion — not summarize the post.
- Respect the user's Words-to-avoid from the profile.

## What to Avoid

- Generic hooks like "AI is changing everything" or "Here's what I learned".
- Ideas that repeat the same format or angle as each other.
- Hooks that require context to land — they need to work cold.
- Mentioning the user's offer in every idea — only in the Community Pull.
