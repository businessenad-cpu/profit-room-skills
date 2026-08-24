# DESIGN.md — Kapper Sint Niklaas

**Werktitel design-systeem: "FRESH / فريش"** — waar tatreez-precisie De Stijl ontmoet.
Status: **wacht op OK van eigenaar vóór de bouw start.**

---

## 1. Concept in één alinea (moodboard-beschrijving)

Donker, warm en strak. Je scrolt door een bijna-zwarte site met de energie van een vrijdagavond: een video-loop van fades en lineups in de hero, grote schreefloze blokletters die recht op je afkomen ("KOM BINNEN. GA FRESH NAAR BUITEN."), en een sticky olijfgroene **Boek nu**-knop die nooit uit beeld is. De Palestijnse laag zit in de details, niet in clichés: dunne tatreez-kruissteekbanden als sectiescheiders, een geometrisch achtpuntig sterpatroon dat op 4% opacity door de achtergrond weeft, en één kalligrafisch woord — **أهلاً** ("welkom") — als stil accent in hero en footer. De Nederlandse laag zit in de structuur: een asymmetrisch De Stijl-grid met harde lijnen, korte directe copy, nul poespas, alles binnen twee taps bereikbaar. Geen bruin-leer-vintage, geen corporate blauw. Dit is een zaak van een 25-jarige die weet hoe hij eruit wil zien.

**Moodboard-referenties (sfeer, niet kopiëren):** Nike-campagnestijl (donker + grote type + atletische energie) × tatreez-textiel (precisie, herhaling, aardetinten) × Mondriaan/De Stijl-grid (asymmetrische blokken, dikke lijnen) × nachtelijke straatfotografie (neon-vrij, warm licht op donker).

---

## 2. Kleurenpalet

Dark-mode is de **enige** mode in v1 (consistent, sneller te bouwen, past de vibe). Light-mode kan later als variant.

| Token | Hex | Gebruik |
|---|---|---|
| `ink` | `#0E0E0B` | Pagina-achtergrond (warm bijna-zwart, geen puur #000) |
| `surface` | `#181812` | Kaarten, secties, header |
| `surface-2` | `#22221A` | Hover-states, inputs |
| `olive` | `#7A8B3F` | **Primair accent**: CTA's, links, actieve staat |
| `olive-bright` | `#A6BD5A` | Hover op CTA, focus-ringen, highlights |
| `olive-deep` | `#3E4722` | CTA-hover-achtergrond, pattern-vlakken |
| `sand` | `#D9C9A3` | Secundaire tekst, prijzen, subtiele vlakken |
| `gold` | `#C6A250` | **Alleen lijnwerk**: tatreez-banden, dividers, grid-lijnen, kalligrafie |
| `bone` | `#F4F1E6` | Primaire tekst (warm off-white) |
| `muted` | `#8A8878` | Bijschriften, meta-info |

Regels:
- Goud is nooit een vlak of knop — alleen lijnen en het Arabische accent. Zo blijft het discreet.
- Olijf is de enige "doe iets"-kleur: alles wat klikbaar richting boeken leidt is olijf.
- Contrast: `bone` op `ink` = ~15:1, `olive-bright` op `ink` = ~8:1, `sand` op `ink` = ~11:1 — alles ruim boven WCAG AA. `bone` op `olive-deep` voor tekst op groene vlakken.

---

## 3. Typografie

| Rol | Font (next/font/google) | Stijl |
|---|---|---|
| Display / headings | **Archivo** (variable, width-as 125% "Expanded") | 800–900, UPPERCASE, strakke letterspacing (-1%), grote maten: hero clamp(3rem → 7rem) |
| Body / UI | **Inter** | 400/500/600, 16–18px, ruime regelafstand 1.6 |
| Arabisch accent | **Amiri** | Alleen voor أهلاً in hero + footer, `gold`, groot maar rustig |
| Cijfers (prijzen/uren) | Inter met `font-variant-numeric: tabular-nums` | Prijslijsten lijnen perfect uit |

- Headings altijd kort en imperatief: "BOEK JE CUT", "DIT IS M'N WERK", "PRIJZEN. GEEN VERRASSINGEN."
- Archivo Expanded geeft de De Stijl-blokletter-energie zonder een display-font-licentie nodig te hebben; alles via `next/font` (self-hosted, geen layout shift).

---

## 4. Pattern-assets (tatreez & geometrie)

Alle patterns worden **handgecodeerde inline SVG's** (currentColor, dus herkleurbaar via CSS), geen stockafbeeldingen. Drie assets:

1. **`tatreez-band.svg`** — sectiescheider. Eén rij kruissteek-motieven (herhalend X-stitch met ruitvorm, geïnspireerd op klassieke tatreez-randmotieven zoals de cipres/ster, geabstraheerd). 12–16px hoog, `gold` op 60% opacity, full-width, `background-repeat: repeat-x`. Vervangt elke `<hr>`.
2. **`star-field.svg`** — achtergrondtextuur. Achtpuntige ster (khatam) als tegelbaar patroon, 96×96px tile, `bone` op **3–4% opacity** over `ink`. Alleen op Home-hero, Over mij en footer — niet overal, anders wordt het behang.
3. **`hero-geo.svg`** — groot geometrisch Arabisch patroon (achtpuntige ster-tessellatie) als **masker/overlay** aan één zijde van de video-hero, in `olive-deep` → transparant verloop. Geeft de hero identiteit ook als de video nog placeholder is.

Expliciet **niet**: vlaggen, kleurencombinatie rood-groen-zwart-wit als vlag-referentie, kufiya-dessin op knoppen, of Arabische tekst als decoratie-behang. Eén woord, één keer groot, klaar.

---

## 5. Layout & grid (De Stijl-laag)

- 12-koloms grid, maar **asymmetrisch** gebruikt: hero-tekst op 7 kolommen, video op 5; galerij in blokken van wisselend formaat (2×2, 1×1, 2×1) als een Mondriaan-compositie.
- **Harde lijnen**: 1px `gold`/20% gridlijnen tussen secties en galerijcellen; kaarten hebben `border-radius: 4px` max — hoekig, niet bubbly.
- **Sticky CTA**: op mobiel een vaste onderbalk "📅 Boek nu — Ankerstraat 61B" (olijf, full-width, veilig boven de home-indicator); op desktop een sticky knop rechtsboven in de header. Altijd zichtbaar, op elke pagina.
- Mobile-first: alles ontworpen op 390px breed, daarna pas desktop.

---

## 6. Motion & interactie

- **Hero**: video-loop (muted, `playsInline`, lazy poster) van cuts uit ./photos zodra aangeleverd; tot dan een langzaam bewegende gradient over `hero-geo.svg` als duidelijk gemarkeerde placeholder.
- **Marquee** "FRESH VOOR HET WEEKEND ✂ VR & ZA RUIME UREN ✂" als scheiding tussen hero en diensten — traag, subtiel, pauzeert bij `prefers-reduced-motion`.
- Hover: kaarten liften 2px + `olive-bright` rand; galerijfoto's zoomen 3% met olijf-overlay en dienstlabel ("skin fade", "lineup").
- Alle animatie respecteert `prefers-reduced-motion: reduce`.

---

## 7. Tone of voice & microcopy (voorbeelden)

- Hero: **"Kom binnen. Ga fresh naar buiten."** — sub: "Fades, lineups en baard. Ankerstraat 61B, Sint-Niklaas."
- CTA's: "Boek je cut" / "Check m'n werk" / "Stuur een appje"
- Prijzen: "Prijzen. Geen verrassingen." — sub: "Wat je ziet is wat je betaalt."
- Weekend-sectie: "Fresh voor het weekend" — "Vrijdag en zaterdag zijn druk. Boek op tijd, dan zit je goed."
- Over mij: "Ik ben Elif. Knippen is m'n vak, mensen zijn m'n ding." *(placeholder — eigen verhaal aan te leveren)*
- 404: "Deze pagina heeft een slechte haardag."
- Jij-vorm, korte zinnen, Vlaams-Nederlands ("appje", "zit je goed"), nul uitroeptekens-spam, geen "😎🔥"-overkill (max 1 schaar-emoji waar het past).

---

## 8. Pagina's → secties

| Pagina | Route | Kern |
|---|---|---|
| Home | `/` | Video-hero + أهلاً, marquee, top-3 diensten, "Fresh voor het weekend", galerij-teaser, reviews-teaser, kaart + uren |
| Cuts & prijzen | `/prijzen` | Prijslijst per categorie (heren/kids/baard/kleur) — **placeholders tot aanlevering**, elk item boekbaar |
| Boeken | `/boeken` | Embed van gekozen tool óf eigen Supabase-flow (zie §10) |
| Over mij | `/over` | Verhaal, foto, roots, waarom deze zaak |
| Werk | `/werk` | Mondriaan-galerij (gecureerd: fade/lineup/baard/kleur) + officiële Instagram- en TikTok-embeds |
| Reviews | `/reviews` | Google-reviews (echte, zodra Business-profiel er is) — tot dan "nieuw geopend"-sectie, géén verzonnen reviews |
| Contact | `/contact` | Kaart Ankerstraat 61B, uren, WhatsApp-knop, bel-knop, route |

SEO-basis per pagina: nl-BE, unieke title/meta ("Kapper Sint-Niklaas — boek online | fades, lineups & baard"), `HairSalon` + `LocalBusiness` JSON-LD met NAP, OG-images in huisstijl, sitemap + robots.

---

## 9. Fotografie-richtlijn + AAN TE LEVEREN

`./photos` is momenteel **leeg/afwezig** → v1 gebruikt gemarkeerde placeholders ("📷 JOUW FOTO HIER — zie lijst").

Aanleverlijst (mag gewoon een dump van je Instagram-media zijn, ik cureer):
1. **Hero-video**: 10–20 sec verticaal of 16:9, knippen in actie of eindresultaat-reveal (mag een Reel zijn).
2. **6–12 resultaatfoto's**: per stijl minstens 2 — skin fade, lineup, baard, (kleur indien aangeboden). Liefst zelfde belichting/hoek.
3. **1–2 foto's van jou** (portret + aan het werk) voor Over mij.
4. **1 zaakfoto** (interieur of gevel Ankerstraat 61B) voor Contact.
5. Bevestiging dat je de **rechten** hebt en dat klanten op de foto's akkoord zijn.

Behandeling: next/image, AVIF/WebP, blur-placeholder, lazy loading, max 200KB per beeld boven de vouw.

---

## 10. Boeken — beslisboom

- **Gebruik je al Salonkee / Salonized / Fresha / iets anders?** → embed/booking-link, klaar in een dag.
- **Nog niets?** → eigen flow: dienst → datum/tijd → naam + telefoon, op **Supabase** (tabellen: services, availability, blocks, bookings), bevestiging per e-mail (Resend) en optioneel SMS, plus `/admin` (login) voor openingsuren, blokkades en afspraakoverzicht.
- Mijn advies uit RESEARCH.md: start eventueel met **Fresha** (geen abonnement) of **Salonized** (€19/mnd) voor no-show-herinneringen en kassa — de eigen flow is goedkoper maar jij beheert alles zelf. Beide kunnen; zeg wat je wil.

---

## 11. Wat ik van jou nodig heb

**Blokkerend voor de bouwstart: niets** — ik bouw met placeholders. Maar vóór livegang:

| # | Item | Waarvoor |
|---|---|---|
| 1 | **OK op dit design** (of aanpassingen) | Bouwstart |
| 2 | Keuze boekingstool óf "bouw eigen flow" | `/boeken` |
| 3 | Instagram- & TikTok-handle | Embeds op /werk |
| 4 | Prijslijst + dienstenlijst | /prijzen |
| 5 | Openingsuren + telefoon/WhatsApp | Contact, JSON-LD, sticky CTA |
| 6 | Foto's/video's (zie §9) | Hero, galerij, over |
| 7 | Wil je أهلاً, je naam in kalligrafie, of iets anders als accent? | Hero/footer |
