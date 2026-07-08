# Contributing

Thanks for wanting to add or improve a skill. This repo follows the [Agent Skills](https://agentskills.io) format and the structure of [`anthropics/skills`](https://github.com/anthropics/skills).

## Skill layout

One folder per skill under `skills/`. The folder name must match the `name` in the SKILL.md frontmatter.

```
skills/
└── your-skill-name/
    ├── SKILL.md          # required
    ├── scripts/          # optional — any code the skill runs
    ├── references/       # optional — docs the skill loads on demand
    ├── assets/           # optional — templates, images, fonts
    └── evals/            # optional — evals.json test prompts (encouraged)
```

## SKILL.md rules

- **Frontmatter:** `name` (lowercase, hyphens only, ≤64 chars) and `description` (≤1024 chars) are required. The `description` is how Claude decides when to use the skill — say what it does *and* when to reach for it, and name the phrases a user would actually type.
- **Body:** write for a non-technical user. Imperative, step-by-step, with a short input→output example. Explain *why* briefly instead of stacking rules. Keep it under ~500 lines; move long detail into `references/` and point to it.
- **Ship everything it uses.** If your SKILL.md calls a script or loads a file, that file must be in the folder. A skill that references something it doesn't include is broken.

## The brand profile

Skills that write in the user's voice (content, YouTube, money skills) read a shared profile at `~/.claude/brand-profile.md`, created once by the **personalize** skill. If your skill uses the user's name, offer, audience, voice, or proof, add the standard **Personalization** block near the top of the body (copy it from `template/SKILL.md`) and read profile fields instead of hardcoding anything.

## No personal data, no secrets

Never commit API keys, session files, or anything tied to a specific person's accounts. Read credentials from environment variables and document them in a `## Requirements` section with a graceful fallback. The `.gitignore` already blocks `.env`, session files, and browser profiles — keep it that way.

## Before you open a PR

- Copy `template/SKILL.md` as your starting point.
- Confirm every path your SKILL.md references exists in the folder.
- Test the skill end-to-end at least once.
- Add an `evals/evals.json` with a few trigger prompts if you can — it's the best signal a skill actually works.
