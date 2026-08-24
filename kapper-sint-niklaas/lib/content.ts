import { cache } from "react";
import {
  site as defaults,
  services as defaultServices,
  type Service,
} from "@/lib/site";

/**
 * Live content-overrides, beheerd via /beheer (formulier + AI-assistent)
 * en opgeslagen in Supabase. Alleen server-side gebruiken.
 *
 * LET OP: tijdelijk in het gedeelde Supabase-project; verhuis naar een eigen
 * project + echte env-vars vóór definitieve livegang.
 */
const SUPABASE_URL =
  process.env.SUPABASE_URL ?? "https://hbbuhjftekgxzcgxkpio.supabase.co";
const SUPABASE_KEY =
  process.env.SUPABASE_ANON_KEY ??
  "sb_publishable_oawN9D7K0seS6pBgfYz__Q_fUBM3TUk";
const TABLE = "kapper_site_content";

/** Inloggegevens voor /beheer — via env-vars te overschrijven op Vercel. */
export const BEHEER_USER = process.env.BEHEER_USER ?? "nabil";
export const BEHEER_PASS = process.env.BEHEER_PASS ?? "kapper123";

/** Velden die via /beheer (formulier of AI-assistent) gezet mogen worden. */
export const EDITABLE_KEYS = [
  "phone",
  "whatsapp",
  "email",
  "instagram",
  "tiktok",
  "freshaBookingUrl",
  "googleBusinessReviewUrl",
  "hours",
  "prices",
  "overStory",
  "heroTitle",
  "heroSub",
  "tagline",
  "weekendText",
  "marquee",
  "uspCards",
  "bookingNote",
  "services",
] as const;
export type EditableKey = (typeof EDITABLE_KEYS)[number];

const restHeaders = {
  apikey: SUPABASE_KEY,
  Authorization: `Bearer ${SUPABASE_KEY}`,
};

/** Ruwe overrides zoals opgeslagen; leeg object als Supabase niet bereikbaar is. */
export const getOverrides = cache(
  async (): Promise<Record<string, unknown>> => {
    try {
      const res = await fetch(
        `${SUPABASE_URL}/rest/v1/${TABLE}?select=key,value`,
        { headers: restHeaders, cache: "no-store" },
      );
      if (!res.ok) return {};
      const rows: { key: string; value: unknown }[] = await res.json();
      return Object.fromEntries(rows.map((r) => [r.key, r.value]));
    } catch {
      return {};
    }
  },
);

export async function saveOverrides(
  data: Record<string, unknown>,
): Promise<boolean> {
  const rows = Object.entries(data)
    .filter(([key]) => (EDITABLE_KEYS as readonly string[]).includes(key))
    .map(([key, value]) => ({ key, value }));
  if (rows.length === 0) return true;
  const res = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}`, {
    method: "POST",
    headers: {
      ...restHeaders,
      "Content-Type": "application/json",
      Prefer: "resolution=merge-duplicates,return=minimal",
    },
    body: JSON.stringify(rows),
  });
  return res.ok;
}

export type Hours = { day: string; open: string | null; close: string | null };
export type UspCard = { title: string; text: string };

/** Default-teksten; alles hiervan is overschrijfbaar via /beheer. */
export const textDefaults = {
  // In teksten met *sterretjes* wordt dat woord in het olijfgroen gezet.
  heroTitle: "Kom binnen.\nGa *fresh* naar buiten.",
  heroSub: "Fades, lineups en baard.",
  tagline: defaults.tagline,
  weekendText:
    "Vrijdag en zaterdag zijn druk. Boek op tijd, dan zit je goed — ruime uren op het einde van de week, zodat je strak het weekend in gaat.",
  marquee: [
    "Fresh voor het weekend",
    "Vr & za ruime uren",
    "Ankerstraat 61B, Sint-Niklaas",
    "Fades · Lineups · Baard",
  ] as string[],
  uspCards: [
    {
      title: "Strak werk",
      text: "Een fade is pas af als de lineup klopt. Ik werk door tot het goed zit.",
    },
    {
      title: "Geen haast, geen wachtrij",
      text: "Op afspraak. Jouw stoel, jouw moment — niet nummer 14 in de rij.",
    },
    {
      title: "Binnenkomen is thuiskomen",
      text: "Goeie muziek, goei babbel. Je komt voor de cut, je blijft voor de sfeer.",
    },
  ] as UspCard[],
  bookingNote: defaults.bookingFallbackNote,
};

export type SiteContent = {
  phone: string | null;
  whatsapp: string | null;
  email: string | null;
  instagram: string | null;
  tiktok: string | null;
  freshaBookingUrl: string | null;
  googleBusinessReviewUrl: string | null;
  hours: Hours[];
  hoursAreDraft: boolean;
  overStory: string | null;
  heroTitle: string;
  heroSub: string;
  tagline: string;
  weekendText: string;
  marquee: string[];
  uspCards: UspCard[];
  bookingNote: string;
};

function str(o: Record<string, unknown>, key: string): string | null {
  const v = o[key];
  return typeof v === "string" && v.trim() ? v.trim() : null;
}

const validCategories = ["heren", "kids", "baard", "kleur"];

function mergeServices(o: Record<string, unknown>): Service[] {
  let base: Service[] = defaultServices;
  if (Array.isArray(o.services) && o.services.length > 0) {
    const parsed = (o.services as Record<string, unknown>[])
      .filter(
        (s) =>
          typeof s?.name === "string" &&
          s.name.trim() &&
          typeof s?.category === "string" &&
          validCategories.includes(s.category),
      )
      .map((s, i) => ({
        slug:
          typeof s.slug === "string" && s.slug.trim()
            ? s.slug.trim()
            : `dienst-${i}`,
        name: (s.name as string).trim(),
        description: typeof s.description === "string" ? s.description : "",
        price: typeof s.price === "number" && s.price > 0 ? s.price : null,
        durationMin:
          typeof s.durationMin === "number" && s.durationMin > 0
            ? s.durationMin
            : null,
        category: s.category as Service["category"],
      }));
    if (parsed.length > 0) base = parsed;
  }
  const prices = (o.prices ?? {}) as Record<string, unknown>;
  return base.map((s) => ({
    ...s,
    price:
      typeof prices[s.slug] === "number" && (prices[s.slug] as number) > 0
        ? (prices[s.slug] as number)
        : s.price,
  }));
}

/** Defaults samengevoegd met de live overrides. */
export const getContent = cache(
  async (): Promise<{ content: SiteContent; services: Service[] }> => {
    const o = await getOverrides();

    let hours: Hours[] = defaults.hours.map((h) => ({ ...h }));
    let hoursAreDraft = defaults.hoursAreDraft as boolean;
    if (Array.isArray(o.hours) && o.hours.length === 7) {
      hours = defaults.hours.map((h, i) => {
        const row = (o.hours as Record<string, unknown>[])[i] ?? {};
        const open = typeof row.open === "string" && row.open.trim() ? row.open.trim() : null;
        const close = typeof row.close === "string" && row.close.trim() ? row.close.trim() : null;
        return { day: h.day, open: open && close ? open : null, close: open && close ? close : null };
      });
      hoursAreDraft = false;
    }

    const marquee =
      Array.isArray(o.marquee) &&
      o.marquee.length > 0 &&
      (o.marquee as unknown[]).every((m) => typeof m === "string")
        ? (o.marquee as string[]).filter((m) => m.trim()).slice(0, 8)
        : textDefaults.marquee;

    const uspCards =
      Array.isArray(o.uspCards) &&
      o.uspCards.length > 0 &&
      (o.uspCards as Record<string, unknown>[]).every(
        (c) => typeof c?.title === "string" && typeof c?.text === "string",
      )
        ? (o.uspCards as UspCard[]).slice(0, 6)
        : textDefaults.uspCards;

    const content: SiteContent = {
      phone: str(o, "phone") ?? defaults.phone,
      whatsapp:
        str(o, "whatsapp")?.replace(/[^\d]/g, "") || defaults.whatsapp,
      email: str(o, "email") ?? defaults.email,
      instagram: str(o, "instagram")?.replace(/^@/, "") ?? defaults.instagram,
      tiktok: str(o, "tiktok")?.replace(/^@/, "") ?? defaults.tiktok,
      freshaBookingUrl:
        str(o, "freshaBookingUrl") ?? defaults.freshaBookingUrl,
      googleBusinessReviewUrl:
        str(o, "googleBusinessReviewUrl") ?? defaults.googleBusinessReviewUrl,
      hours,
      hoursAreDraft,
      overStory: str(o, "overStory"),
      heroTitle: str(o, "heroTitle") ?? textDefaults.heroTitle,
      heroSub: str(o, "heroSub") ?? textDefaults.heroSub,
      tagline: str(o, "tagline") ?? textDefaults.tagline,
      weekendText: str(o, "weekendText") ?? textDefaults.weekendText,
      marquee,
      uspCards,
      bookingNote: str(o, "bookingNote") ?? textDefaults.bookingNote,
    };

    return { content, services: mergeServices(o) };
  },
);
