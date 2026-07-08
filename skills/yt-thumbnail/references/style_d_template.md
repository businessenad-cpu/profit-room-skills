# Style D — App Window + Face

## Description
A Mac-style browser/app window dominates the left ~60% of the frame. The person's face peeks from the right edge, overlapping the window. Dark navy background. No title text — the content inside the window IS the message. Best for new features, slash commands, specific tool reveals.

## Full Prompt Template

```
A professional, high-resolution YouTube thumbnail in WIDE 16:9 landscape format. Wider than it is tall — never portrait.

**Background:** Deep dark navy blue (#0D1B2A), uniform and clean. This fills the entire canvas behind all elements.

**Main element — Mac app window (left 60% of frame):**
A large, rounded-corner browser/app window frame sits on the left side of the image, slightly angled or perfectly frontal. The window has:
- A white top bar with the three macOS traffic light dots (red, yellow, green) in the top-left corner
- A large white interior canvas below the title bar, filling most of the window
- The window has a subtle drop shadow against the dark navy background

**Inside the window (two zones):**
TOP HALF of the window interior (white background):
[INSERT TOP ZONE CONTENT — e.g., "The orange Anthropic asterisk logo on the left, and 'Claude' in large black serif text on the right. Clean, minimal, lots of white space."]

BOTTOM HALF of the window interior (dark terminal block):
A dark (#1A1A2E or near-black) rounded rectangle fills the bottom half of the window, styled like a terminal or command input. On the left side, a white "›" chevron prompt character. In the center, monospaced text in a glowing blue color reads: [INSERT COMMAND TEXT — e.g., "/goal|"] with a blinking blue cursor bar at the end.

**Person (right side, overlapping the window):**
The person from your reference photo (Image 1) — match their exact likeness. They appear on the right third of the frame, their face and upper chest visible. They are positioned so their left shoulder/side overlaps and sits IN FRONT OF the right edge of the app window (they're physically between the camera and the window). Big, genuine smile. Photorealistic portrait quality. They fill roughly 60% of the frame height.

**Lighting on the person:** Warm studio lighting from the front. A subtle cool blue rim light from the left (from the terminal glow inside the window) catching the left side of their face and glasses.

**No title text on the image** — the content inside the window communicates everything.

**CRITICAL:** Wide 16:9 landscape. Window on left, person peeking from right overlapping window edge. Dark navy fills the background.
```

## Placeholder Guide

### [INSERT TOP ZONE CONTENT]
Describe what's in the white upper area of the window:
- For tool-specific: "[Tool logo on left] + [Tool name in large text on right]"
- For feature reveal: "Large title text of the feature name, centered"
- Example: "The orange Anthropic asterisk/snowflake logo on the left. The word 'Claude' in large black Georgia/serif font on the right."

### [INSERT COMMAND TEXT]
The text shown in the terminal bar. Usually a slash command or key term:
- `/goal|` — for a goal-setting feature
- `/linkedin|` — for a LinkedIn skill
- `CLAUDE CODE` — for Claude Code content
- Keep it short — max 2 words. The cursor `|` always appears at the end.

## When to Use
- New Claude feature reveal
- Slash command tutorial
- "Here's the tool I use" format
- Feature Name Only title format (from title_rules.md)
- Works without any title text overlaid — the command inside the window IS the hook

## Logo Handling
Always pass the tool logo via `--logos [Tool]` so the logo inside the window is accurate.
