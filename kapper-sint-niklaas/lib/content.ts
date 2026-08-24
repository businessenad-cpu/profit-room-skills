import { cache } from "react";
import {
  site as defaults,
  services as defaultServices,
  type Service,
} from "@/lib/site";

/**
 * Live content-overrides, beheerd via /beheer en opgeslagen in Supabase.
 * Alleen server-side gebruiken (API-sleutel hoort niet in de client-bundle).
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

/** Velden die via /beheer gezet mogen worden. */
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
] as const;

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
  /** Eigen "over mij"-verhaal; null = placeholder tonen. */
  overStory: string | null;
};

function str(o: Record<string, unknown>, key: string): string | null {
  const v = o[key];
  return typeof v === "string" && v.trim() ? v.trim() : null;
}

/** Defaults uit lib/site.ts samengevoegd met de live overrides. */
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
    };

    const prices = (o.prices ?? {}) as Record<string, unknown>;
    const services = defaultServices.map((s) => ({
      ...s,
      price:
        typeof prices[s.slug] === "number" && (prices[s.slug] as number) > 0
          ? (prices[s.slug] as number)
          : s.price,
    }));

    return { content, services };
  },
);
