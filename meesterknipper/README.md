# ✂️ Meesterknipper — Knipklok demo

Online boekingssysteem-demo voor kapperszaken. Klanten boeken in 5 stappen
(dienst → kapper → datum & tijd → gegevens → bevestiging), krijgen een
bevestigingsmail via Resend, en de salon ziet alles direct terug in het
admin-overzicht op `/admin`.

**Stack:** Next.js 14 (App Router) · TypeScript · Tailwind CSS · Resend ·
in-memory store (geen database nodig — snelst deploybaar op Vercel;
boekingen blijven binnen een sessie zichtbaar in het admin-overzicht).

## Lokaal draaien

```bash
npm install
cp .env.example .env.local   # optioneel invullen, zie hieronder
npm run dev
```

Open http://localhost:3000 (boekingsflow) en http://localhost:3000/admin
(admin-overzicht). Zonder `.env.local` draait alles gewoon — mails worden dan
niet verstuurd maar getoond in demo-modus (in de UI én in de serverconsole).

## Resend instellen (echte mails)

1. Maak een gratis account op [resend.com](https://resend.com) en kopieer je API key.
2. Zet in `.env.local`:

   ```
   RESEND_API_KEY=re_xxxxxxxxxxxx
   EMAIL_FROM=Kapper Sint Niklaas <onboarding@resend.dev>
   SALON_EMAIL=jouw-adres@example.com
   ```

   `SALON_EMAIL` ontvangt bij elke boeking een korte notificatie.
3. Herstart `npm run dev`.

> Zonder eigen geverifieerd domein bij Resend kun je `onboarding@resend.dev`
> als afzender gebruiken; Resend levert dan alleen af aan het e-mailadres van
> je eigen Resend-account. Met een geverifieerd domein mail je naar iedereen.

## Deployen naar Vercel (3 stappen)

1. Push deze code naar GitHub en importeer de repo op
   [vercel.com/new](https://vercel.com/new). Zet **Root Directory** op
   `meesterknipper` (als de app in een submap staat). Framework wordt
   automatisch herkend als Next.js.
2. Voeg onder *Environment Variables* toe: `RESEND_API_KEY`, `EMAIL_FROM` en
   `SALON_EMAIL` (allemaal optioneel — zonder key draait de demo in
   demo-modus).
3. Klik **Deploy**. Klaar — deel de URL met je klant.

> **Let op (demo):** boekingen staan in het geheugen van de server. Op Vercel
> blijven ze zichtbaar zolang dezelfde serverless-instantie warm is — prima
> voor een live demo, niet voor productie. De knop "Demo resetten" op `/admin`
> maakt alles leeg.

## Seed data

- **Salon:** Kapper Sint Niklaas (di t/m za 09:00–18:00, slots per 15 min)
- **Kappers:** Enad (fades & baard), Mo (klassiek knippen), Yassin (kids & tondeuse)
- **Diensten:** Knippen heren €22/30min · Fade €27/45min · Knippen + baard
  €35/60min · Baard trimmen €15/20min · Kids knippen €17/30min

## Features

- Mobiel-first boekingsflow in het Nederlands, NL-datumnotatie (za 5 sep, 14:30)
- Dubbel boeken van hetzelfde slot bij dezelfde kapper is onmogelijk
  (server-side gecheckt, ook bij "Geen voorkeur")
- NL-telefoonnummervalidatie
- Boekingsnummers (KK-0001, KK-0002, …)
- HTML-bevestigingsmail naar de klant + notificatie naar de salon
- Admin-agenda per kapper met omzet per dag en demo-reset
