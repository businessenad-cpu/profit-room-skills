# Lead Magnet JSON Format

Save all lead magnet JSON files to: `~/lead-magnets/output/` (create the folder if it doesn't exist).

Use kebab-case filenames: `topic-name-here.json`

Wherever a CTA URL or byline appears below, substitute the **Default-CTA** and **Name** fields from the brand profile at `~/.claude/brand-profile.md`.

## Top-Level Structure

```json
{
  "notion_document": {
    "title": "Lead Magnet Title",
    "subtitle": "One-line hook",
    "metadata": {
      "created": "YYYY-MM-DD",
      "version": "1.0",
      "target_audience": "Who this is for",
      "prose_word_count": "~N words",
      "cta_url": "{Default-CTA from brand profile}",
      "cta_label": "{Your offer name}"
    },
    "page_settings": {
      "cover": {
        "type": "solid_color",
        "color": "#0F1117",
        "note": "Dark near-black background."
      },
      "icon": "emoji here",
      "full_width": true,
      "small_text": false,
      "font": "Default Sans"
    },
    "sections": [ ... ]
  },
  "social_promo": {
    "linkedin_hook": "First line for LinkedIn post",
    "instagram_hook": "Hook for Instagram/TikTok",
    "cta_trigger": "KEYWORD"
  }
}
```

## Section Structure

Each section has an `id`, `label`, and `blocks` array:

```json
{
  "id": "section_name",
  "label": "Human-readable label",
  "blocks": [ ... ]
}
```

## Block Types

### Heading

```json
{
  "type": "heading_1",
  "content": "Page Title",
  "styling": { "color": "default", "bold": true }
}
```

Levels: `heading_1`, `heading_2`, `heading_3`. Colors: default, blue, purple, green, orange, red.

### Paragraph

```json
{
  "type": "paragraph",
  "content": "Body text here.",
  "styling": { "color": "default", "italic": false, "bold": false }
}
```

Use `"color": "gray"` + `"italic": true` for subtitles and metadata lines.

### Callout

```json
{
  "type": "callout",
  "icon": "💡",
  "content": "Callout text here.",
  "styling": { "background": "yellow" }
}
```

Backgrounds: yellow, blue, gray, purple, red, orange, green, default.

CTA callouts always use (substitute your offer name and Default-CTA link):
```json
{
  "type": "callout",
  "icon": "🚀",
  "content": "Description of your offer.\n\n👉 Join free at {Default-CTA}",
  "styling": { "background": "purple", "cta_url": "{Default-CTA}" }
}
```

Prompt/copy-paste callouts always use 📋 icon with gray background.

### Bulleted List Item

```json
{
  "type": "bulleted_list_item",
  "content": "List item text"
}
```

### Numbered List Item

```json
{
  "type": "numbered_list_item",
  "content": "Step text"
}
```

### Divider

```json
{
  "type": "divider"
}
```

Use between every major section and before/after CTA blocks.

### Table

```json
{
  "type": "table",
  "has_header": true,
  "children": [
    { "type": "table_row", "cells": ["Header 1", "Header 2", "Header 3"] },
    { "type": "table_row", "cells": ["Data 1", "Data 2", "Data 3"] }
  ]
}
```

Max 3-5 columns. Use for comparisons and prompt collections.

### Code Block

```json
{
  "type": "code",
  "language": "bash",
  "content": "code here"
}
```

## Required Section Order

1. **Header** — H1 title, subtitle (gray italic), byline, credibility line, divider, early CTA (purple 🚀), divider
2. **Intro/How-to-Use** — Context, what they'll learn, golden rule callout
3. **Main Content Sections** — The actual lead magnet content (3-6 sections)
4. **Pro Tips / Key Takeaways** — Optional summary section
5. **CTA** — Closing CTA with purple 🚀 callout

## Critical Reminders

- NEVER use `**bold**` markdown in content strings — shows raw asterisks in Notion
- Escape all `"` in content strings as `\"`
- Every prompt goes in a 📋 callout, never as plain paragraph
- Descriptions go ABOVE the prompt callout, not inside it
- Dividers between every major section
- Alternate visual elements every 3 scrolls (text → callout → table → bullets)
