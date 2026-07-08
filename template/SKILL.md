---
name: skill-name
description: One or two sentences on WHAT this does and WHEN to use it. Write it slightly pushy so Claude reaches for it — name the concrete phrases a user would say ("turn this into...", "write me a...", "help me..."), even when they don't say the word "skill".
---

# Skill Name

One line on the outcome the user gets.

## Personalization
<!-- Include this block ONLY for skills that speak in the user's brand voice or use their offer/audience/proof. Delete it for generic utility skills. -->
This skill works in *your* brand voice. Before running, load the brand profile at `~/.claude/brand-profile.md`.
- If it doesn't exist, run the **personalize** skill first (or just tell me your name, niche, offer, and audience — I'll create it).
- If a field this skill needs is blank, I'll ask one or two quick questions and save the answers back to the profile so you only answer once.
- Never invent facts or results about the user — use only what's in the profile, or ask.

## Requirements
<!-- List any API keys, MCP servers, or CLI tools this skill needs. If none, delete this section. -->
- e.g. `OPENAI_API_KEY` in your environment. If it's not set, I'll tell you exactly what to add and where.

## Steps
1. ...
2. ...

## Notes / edge cases
- ...
