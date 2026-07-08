# Voice, Rules & Quality Standards

All voice, audience, proof, and CTA details come from the brand profile at `~/.claude/brand-profile.md`. This file gives the *structure* and *rules*; the profile gives the *specifics*. Never hardcode a name, number, or offer here — read it from the profile, or ask.

## Audience (from the profile)

Use the **Audience** and **Main-pain** fields to define who this is for. A strong lead-magnet audience is usually:
- Expertise-rich, audience-poor operators who know their craft but lack distribution
- Solo operators, consultants, coaches, or small teams
- People who want copy-paste prompts, frameworks, and playbooks — not tutorials
- People who value proof over promises, speed over complexity

## Voice Rules

Layer these on top of the **Tone** field from the profile:

- **6th grade reading level.** Simple words. Short sentences. If a 12-year-old can't understand it, rewrite it.
- **Radically simple.** Stupidly clear. No clever phrasing.
- **Concrete over abstract.** "You'll get DMs from people who want to hire you" not "No one can out-value you"
- **Direct.** No hedging, no filler, no throat-clearing
- **Compressed.** Say it in fewer words. Then cut 20% more
- **Operator tone.** Written from having done it, not theorized about it
- **Proof over persuasion.** Numbers, not adjectives

### Never Use
- "Let's dive in," "Without further ado," "In this guide you'll learn," "Are you ready to," "Let's build"
- Motivational filler, vague claims
- Anything listed in the **Words-to-avoid** field of the brand profile
- Markdown bold (`**text**`) in JSON content strings — Notion API shows raw asterisks. Use rich_text annotations with `"bold": true` instead

### Never Mention / Never Invent
- Do NOT invent revenue, follower counts, client results, or dollar amounts. Use only proof points that exist in the brand profile. If a proof point isn't there, ask the user or leave it out.

## Storytelling Frameworks (Choose One Per Lead Magnet)

### Framework 1: Before/After/Bridge (BAB)
- **Before:** Their current pain (specific — "You post 5x/week and get 12 likes")
- **After:** The future state (believable — "Your content generating DMs from ideal clients daily")
- **Bridge:** The system that connects them (tie to the **Offer** / **Transformation** fields)

### Framework 2: Origin Story
- Act 1: "I had the same problem" (empathy)
- Act 2: "I tried the obvious stuff and failed" (credibility)
- Act 3: "Then I discovered X" (the insight)
- Act 4: "Here's the system I built" (the content)
- Act 5: "What it unlocked" (proof)

### Framework 3: Case Study Chain
- 3-5 mini stories building on each other
- Each shows "what becomes possible" when you stack the next piece
- Reader sees themselves in at least one story

### Framework 4: Behind the Curtain
- Show the real process with messy details visible
- Include what failed and why
- Transparency = trust

## Proof Standards (Must Include 3+)

Pull every proof point from the brand profile. Types of proof to look for:
- **Real numbers:** follower growth, workflows built, templates sold, hours saved
- **Specific examples:** actual posts that performed, actual prompts that worked
- **Named frameworks:** a proprietary name for the system (e.g. "The Authority System")
- **Timeline proof:** "In 60 days..." "After 3 weeks..." with specifics
- **Member/client results:** a real, named win from the profile

If the profile has fewer than 3 usable proof points, ask the user for more or reduce the proof-heavy claims. Never fabricate.

## Early CTA Rule (MANDATORY)

Every lead magnet MUST include a CTA near the top — after the intro but BEFORE main content. Purple callout with 🚀 icon. One sentence: what they get + the **Default-CTA** link from the brand profile. Plus a closing CTA at the bottom.

## Notion Design System

### Page Structure
```
Cover Image (full-width, dark background)
Icon (relevant emoji)
Title (H1)
Subtitle (italic, gray, one-line hook)
By {Name from profile}
Based on {proof point from profile} (credibility line)
───────────────────────
Early CTA (purple callout with 🚀)
───────────────────────
[SECTIONS]
───────────────────────
CTA Section (purple callout with 🚀)
```

### Callout Icons
- 💡 = Key insight or tip
- ⚠️ = Common mistake or warning
- ✅ = Win, success, or takeaway
- 🔥 = High-impact point
- 📋 = Copy-paste content (prompts, templates)
- 🎯 = Action item
- 🚀 = CTA (always purple background)

### Formatting Rules
- **Comparison sections:** H3 per item with emoji prefix, 1-2 sentence description, bullets for use cases, divider between items, callout at end
- **Prompts/copy-paste content:** ALWAYS in 📋 callout blocks, description as paragraph ABOVE the callout, example output as bullets BELOW
- **Visual variety every 3 scrolls:** Alternate text, callout, table, toggle, image
- **Short paragraphs:** Max 3-4 lines. Break up walls of text
- **Dividers between every major section**

## Research First (MANDATORY)

Before writing ANY lead magnet:
1. Ask: "Do I know exactly what this is and how real people are using it?"
2. If ANY doubt, research first with WebSearch
3. Never write about a product/feature based on assumptions
4. Understand how people on Reddit, YouTube, X are actually discussing the topic
5. A lead magnet based on wrong information is worse than no lead magnet

## JSON Output Rules

- Escape all double quotes inside string values (`\"`)
- NEVER use markdown bold in content strings
- All prompts in 📋 callout blocks
- CTA callouts use purple background

## Quality Checklist (Validate Before Output)

- [ ] 1,000-1,500 words TOTAL
- [ ] Has a narrative arc — each section builds on the last
- [ ] 6th grade reading level
- [ ] Every claim is CONCRETE
- [ ] ZERO markdown bold in JSON content strings
- [ ] No invented numbers or results — all proof from the brand profile
- [ ] CTA drives to the Default-CTA link from the profile
- [ ] No redundant sections
- [ ] Every section has at least one visual element
- [ ] Immediately useful — reader can act TODAY
- [ ] Every prompt includes WHY it works + example output
- [ ] Title is specific, not generic
