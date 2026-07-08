# Guide File Format (guide.md)

Write the final guide as a single Markdown file using this exact structure. It needs to survive a
naive Markdown-to-PDF conversion (Notion export, Google Docs paste, or a free online converter), so
keep formatting simple and avoid anything that renders unpredictably.

## Structure

```markdown
# [Guide Title]
### [One-line subtitle stating the transformation]

*by [Author Name]*

---

## Introduction

[The hook/story from the user's angle. What the reader will walk away able to do. Who this
guide is for, stated plainly in one or two sentences.]

---

## Chapter 1: [Pillar Name]

[Chapter content. Concrete situation first, then the unlock, then the exact action.]

---

## Chapter 2: [Pillar Name]

[...]

---

## Chapter 3: [Pillar Name]

[...]

(repeat for each pillar, 3-5 total)

---

## Putting It Into Practice

[Closing chapter: the single next action the reader should take this week. Optional light
mention of the reader's own next step/offer if the user wants one — ask first, don't assume.]

---

*[Optional: one-line closing note or thank-you. Keep it short.]*
```

## Print-Safety Rules (why they matter)

- **Only H1 for the title, H2 for chapters, H3 for the subtitle.** Deeper heading levels often
  render inconsistently across converters.
- **No tables.** Markdown tables frequently break or overflow when converted to PDF. If you need to
  compare things, use short prose or a simple bullet list instead.
- **No code blocks.** They're irrelevant here and some converters render them with ugly monospace
  boxes that look out of place in an ebook.
- **Bullet lists: one level deep only.** Nested bullets often collapse or misindent on conversion.
  Use plain paragraphs for anything that needs sub-points.
- **Bold for emphasis only, used sparingly.** Don't bold whole sentences — it stops reading as
  emphasis and starts reading as noise.
- **Horizontal rules (`---`) between major sections** give the PDF clean page-break points in most
  converters.
- **No embedded images/HTML.** Keep the file plain Markdown so it pastes cleanly into Notion or
  Google Docs without breaking.

## Filename and Location

Save to `~/guides/[Guide Title]/guide.md` (create the folder if it doesn't exist). Keep the title
in the filename short and filesystem-safe (no slashes, colons, or emoji).
