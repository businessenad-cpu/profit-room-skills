# Audit Playbook — capturing the real UI + brand tokens

Goal of Phase 1: a folder of clean, real screenshots and the product's *actual* palette/type —
never invented. Primary engine is the **Playwright MCP** (`mcp__playwright__browser_*`); Firecrawl
is the no-login fallback.

## 1. Navigate + (optionally) log in

```
browser_navigate(url)                      # the app or a staging build
# if creds were given:
browser_snapshot()                         # find the login fields
browser_fill_form / browser_type           # email + password
browser_click(submit)
browser_wait_for(...)                       # let the app settle
```

If the good screens are behind auth and no creds were given, ask for them in Phase 0 — or capture
the marketing site instead and note the limitation.

## 2. Set a clean capture size, then screenshot each hero screen

Match the canvas to the chosen aspect ratio so frames don't need awkward cropping later:

- `16:9` → `browser_resize(1920, 1080)`
- `9:16` → `browser_resize(1080, 1920)` (or 1242×2208)
- `1:1` → `browser_resize(1440, 1440)`

For each key route/module:
```
browser_navigate(<route>)
browser_wait_for(<a stable selector / network idle>)
# dismiss cookie banners / modals first (browser_click) so they don't pollute the frame
browser_take_screenshot(filename:"screens/<route>.png", fullPage:false)
```
Capture 5–8 of the best screens: the hero dashboard, the signature feature, a list/table view, a
detail/conversation view, a settings or pricing screen, the empty/onboarding state if striking.

**Tips for screenshots that composite well:** prefer dark-mode if the product has it; turn off
personal/PII data where possible; capture states that show real numbers (counts, charts, statuses)
— they become on-screen text. For very long pages, capture a tight crop of the hero region rather
than the whole scroll.

## 3. Read the live brand tokens off the DOM

This is the source of truth for the palette — far better than guessing from a screenshot. Use
`browser_evaluate`:

```js
() => {
  const cs = getComputedStyle(document.body);
  // accent: scan CTA candidates, take the first VIVID filled background.
  // (skips ghost/transparent buttons — validated: those return rgba(0,0,0,0))
  const isVivid = (c) => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return false;
    const [r,g,b,a=1] = m[1].split(',').map(Number); if (a === 0) return false;
    const max = Math.max(r,g,b), min = Math.min(r,g,b); return max > 40 && (max-min > 25 || max > 200); };
  let accentBg = null, accentColor = null;
  for (const el of document.querySelectorAll('button, a[class*="btn"], [class*="primary"], [class*="cta"]')) {
    const s = getComputedStyle(el);
    if (isVivid(s.backgroundColor)) { accentBg = s.backgroundColor; accentColor = s.color; break; }
  }
  // dump any CSS custom properties that look like brand tokens
  const vars = {};
  for (const s of document.styleSheets) {
    try { for (const r of s.cssRules) {
      if (r.style) for (const n of r.style) if (n.startsWith('--')) vars[n] = r.style.getPropertyValue(n).trim();
    }} catch (e) {}
  }
  return {
    bodyBg: cs.backgroundColor,
    bodyColor: cs.color,
    fontFamily: cs.fontFamily,
    accentBg, accentColor,                 // brand accent (vivid filled CTA); null if none found
    cssVars: vars,                         // often holds --accent, --background, --border, etc.
  };
}
```
Convert any `rgb()` values to hex. Identify: **background**, **surface/card**, the single
**accent**, **text**, **border**, and the **font-family**. Grab the logo too:
```js
() => {
  const link = document.querySelector('link[rel~="icon"]')?.href;
  const logo = document.querySelector('header img, nav img, [class*="logo"] img, svg[class*="logo"]');
  return { favicon: link, logoSrc: logo?.src || null };
}
```

## 4. Firecrawl fallback (no login / heavy SPA / marketing copy)

```
firecrawl_scrape(url, formats:["markdown","screenshot"])  # copy + hero colors + a hero screenshot
```
Use the marketing site for value-prop copy and brand colors when the app itself can't be reached.
Still prefer real app screenshots for the feature beats whenever you can get them.

## 5. Write `research.md`

Record, concisely:
- **Palette** — bg / surface / **accent** / text / border hexes (from the DOM, not guessed).
- **Type** — the font-family.
- **Voice** — 1–2 lines from the marketing site (hero phrasing, tone).
- **Module map** — the key screens captured and what each shows.
- **Real numbers/nouns** — anything visible in the UI worth surfacing as on-screen text.

Then theme `brief.html` from this palette (accent = the page's highlight). The audited product's
own brand always drives the brief — never impose an outside house style.

## Parallelism

For a large app, fan out subagents — one per route — each navigating, screenshotting, and
returning its screenshot path + a one-line description. Synthesize their results into `research.md`.
