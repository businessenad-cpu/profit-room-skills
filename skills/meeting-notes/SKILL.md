---
name: meeting-notes
description: Process meeting transcripts into structured markdown summaries. Use this skill whenever the user pastes a meeting transcript, shares meeting notes, or says anything like "process this meeting", "summarize this call", "extract action items", "here's a transcript from my call", or "here are my meeting notes". Works with transcripts from any tool (Fireflies, Otter, Granola, Zoom, etc.). Trigger even if the user just pastes a block of text that looks like a speaker-labeled transcript.
---

# Meeting Notes Processor

You are processing a meeting transcript (from any transcription tool) into a clean, structured markdown file saved locally.

## What to extract

Work through the transcript carefully and pull out:

1. **Meeting metadata** — date, time, participants (with roles/titles if mentioned), meeting title or topic
2. **Executive summary** — 3-5 sentences capturing the core purpose, key discussion points, and outcome of the meeting. Write this for someone who wasn't on the call.
3. **Key decisions** — concrete things the group agreed on or resolved. Distinguish from action items: decisions are outcomes, action items are tasks.
4. **Action items** — every task, follow-up, or commitment mentioned. Assign each to a specific person based on context. If a task is clearly unassigned, make your best guess based on who would logically own it, and flag it with `[UNASSIGNED - suggested owner]`.
5. **Open questions** — things raised but not resolved, questions that need answers, or topics tabled for later.
6. **Next steps** — any mentioned next meeting, deadline, or shared team goal.

## Action item assignment rules

- If someone says "I'll handle X" or "can you take care of Y?" — assign directly.
- If no one claims a task but a domain expert is on the call (e.g., task is about design and a designer is present) — assign to them and flag as `[UNASSIGNED - suggested: Name]`.
- If it's truly ambiguous with no reasonable inference — mark `[UNASSIGNED]`.
- Never invent assignments with confidence — flag uncertainty clearly.

## Output format

Save the file to `~/meeting-notes/` (create the folder if it doesn't exist) using this filename pattern:
`YYYY-MM-DD_[meeting-topic-slug].md`

Use the date from the transcript. If no date is found, use today's date. Slugify the topic (lowercase, hyphens, no special chars). Example: `2026-03-05_q1-product-review.md`

Use exactly this markdown structure:

```
# [Meeting Title]
**Date:** [Date]
**Duration:** [Duration if available]
**Participants:** [Name (Role), Name (Role), ...]

---

## Executive Summary
[3-5 sentences]

---

## Key Decisions
- [Decision 1]
- [Decision 2]

---

## Action Items

### [Person Name]
- [ ] [Task description] — *due [date if mentioned]*

### [Person Name]
- [ ] [Task description]

### Unassigned
- [ ] [Task description] — *[UNASSIGNED - suggested: Name]*

---

## Open Questions
- [Question or unresolved topic]

---

## Next Steps
- [Next meeting, deadline, or shared goal]
```

If a section has nothing to add (e.g., no open questions), omit it entirely — don't include an empty section.

## After saving

Tell the user:
- The filename and full path where it was saved
- A brief one-sentence summary of the meeting (different from the executive summary — even more condensed, like a subject line)
- How many action items were found and how many were flagged as unassigned
- Ask if they'd like any section expanded or adjusted
