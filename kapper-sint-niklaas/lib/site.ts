/**
 * Centrale site-config. Alles wat hier "PLACEHOLDER" of null is,
 * moet door de eigenaar worden aangeleverd vóór livegang.
 * Zie ook: research/kapper-sint-niklaas/DESIGN.md §11 in de repo.
 */

export const site = {
  name: "Kapper Sint Niklaas",
  legalName: "KAPPER SINT-NIKLAAS CommV",
  vat: "BE 1036.524.380",
  tagline: "Kom binnen. Ga fresh naar buiten.",
  url: "https://kapper-sint-niklaas.vercel.app", // TODO: eigen domein zodra gekocht

  address: {
    street: "Ankerstraat 61B",
    postalCode: "9100",
    city: "Sint-Niklaas",
    country: "BE",
  },
  geo: { lat: 51.1594, lng: 4.1427 }, // Ankerstraat, Sint-Niklaas (benaderd — verifieer)

  // ── PLACEHOLDERS: aan te leveren door eigenaar ────────────────────────────
  phone: null as string | null, // bv. "+32 4xx xx xx xx"
  whatsapp: null as string | null, // bv. "324xxxxxxxx" (zonder + of spaties)
  email: null as string | null,
  instagram: null as string | null, // handle zonder @, bv. "kappersintniklaas"
  tiktok: null as string | null, // handle zonder @
  /** Fresha "Book now"-link, bv. "https://www.fresha.com/book-now/..." */
  freshaBookingUrl: null as string | null,
  googleBusinessReviewUrl: null as string | null,
  // ──────────────────────────────────────────────────────────────────────────

  /** Openingsuren — PLACEHOLDER-schema, aan te passen door eigenaar. */
  hours: [
    { day: "Maandag", open: null as string | null, close: null as string | null },
    { day: "Dinsdag", open: "09:00", close: "18:00" },
    { day: "Woensdag", open: "09:00", close: "18:00" },
    { day: "Donderdag", open: "09:00", close: "18:00" },
    { day: "Vrijdag", open: "09:00", close: "20:00" },
    { day: "Zaterdag", open: "09:00", close: "20:00" },
    { day: "Zondag", open: null, close: null },
  ],
  hoursAreDraft: true, // op true blijven tot eigenaar de uren bevestigt

  bookingFallbackNote:
    "Online boeken komt eraan. Stuur ondertussen een appje of bel — dan plannen we je cut meteen in.",
} as const;

export type Service = {
  slug: string;
  name: string;
  description: string;
  /** null = prijs nog niet aangeleverd → toont "€ —" met placeholder-melding */
  price: number | null;
  durationMin: number | null;
  category: "heren" | "kids" | "baard" | "kleur";
};

/**
 * PLACEHOLDER-dienstenlijst. Namen zijn gangbare kapperdiensten,
 * prijzen zijn bewust null tot de eigenaar ze aanlevert.
 */
export const services: Service[] = [
  { slug: "knippen-heren", name: "Knippen heren", description: "Wassen, knippen, stylen. Klassiek of modern.", price: null, durationMin: 30, category: "heren" },
  { slug: "skin-fade", name: "Skin fade", description: "Strakke fade tot op de huid, afgewerkt met lineup.", price: null, durationMin: 45, category: "heren" },
  { slug: "lineup", name: "Lineup / contouren", description: "Randjes strak. Snel binnen, fresh buiten.", price: null, durationMin: 15, category: "heren" },
  { slug: "knippen-kids", name: "Knippen kids (-12)", description: "Geduldig en snel, ook voor de kleinste klanten.", price: null, durationMin: 25, category: "kids" },
  { slug: "baard-trim", name: "Baard trimmen", description: "In model brengen, contouren, verzorging.", price: null, durationMin: 20, category: "baard" },
  { slug: "cut-baard", name: "Cut + baard combo", description: "Het volledige pakket in één afspraak.", price: null, durationMin: 60, category: "baard" },
];

export const serviceCategories: { key: Service["category"]; label: string }[] = [
  { key: "heren", label: "Heren" },
  { key: "kids", label: "Kids" },
  { key: "baard", label: "Baard" },
  { key: "kleur", label: "Kleur" },
];

/**
 * Gecureerde galerij. Leg bestanden in /public/photos en registreer ze hier,
 * beste cuts eerst, gegroepeerd per stijl. Leeg = placeholder-tegels.
 */
export type GalleryItem = {
  src: string;
  alt: string;
  style: "fade" | "lineup" | "baard" | "kleur";
  /** grid-span in de Mondriaan-galerij */
  size?: "lg" | "wide" | "tall" | "sm";
};
export const gallery: GalleryItem[] = [];
