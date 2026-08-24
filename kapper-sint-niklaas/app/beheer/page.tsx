"use client";

import { useEffect, useState } from "react";
import { services } from "@/lib/site";

/**
 * /beheer — inlogbare tab waar Nabil alle ontbrekende info kan invullen.
 * Wijzigingen worden via /api/beheer in Supabase bewaard en staan direct
 * live op de site (herlaad de pagina om ze te zien).
 */

const DAGEN = [
  "Maandag",
  "Dinsdag",
  "Woensdag",
  "Donderdag",
  "Vrijdag",
  "Zaterdag",
  "Zondag",
];

type HourRow = { open: string; close: string };

const inputCls =
  "w-full rounded-[4px] border border-gold/30 bg-surface-2 px-3 py-2 text-sm text-bone placeholder:text-muted focus:border-olive-bright focus:outline-none";
const labelCls = "mb-1 block text-xs text-sand";

export default function BeheerPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const [fields, setFields] = useState<Record<string, string>>({
    phone: "",
    whatsapp: "",
    email: "",
    instagram: "",
    tiktok: "",
    freshaBookingUrl: "",
    googleBusinessReviewUrl: "",
    overStory: "",
  });
  const [hours, setHours] = useState<HourRow[]>(
    DAGEN.map(() => ({ open: "", close: "" })),
  );
  const [prices, setPrices] = useState<Record<string, string>>(
    Object.fromEntries(services.map((s) => [s.slug, ""])),
  );

  // sessie onthouden zolang de tab open is
  useEffect(() => {
    try {
      const saved = sessionStorage.getItem("beheer-login");
      if (saved) {
        const { u, p } = JSON.parse(saved);
        setUsername(u);
        setPassword(p);
        void doLogin(u, p);
      }
    } catch {
      /* leeg formulier */
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function api(action: "load" | "save", data?: Record<string, unknown>) {
    const res = await fetch("/api/beheer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password, action, data }),
    });
    return { status: res.status, body: await res.json() };
  }

  async function doLogin(u = username, p = password) {
    setBusy(true);
    setMessage(null);
    const res = await fetch("/api/beheer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: u, password: p, action: "load" }),
    });
    const body = await res.json();
    setBusy(false);
    if (!res.ok) {
      setMessage(body.error ?? "Inloggen mislukt.");
      return;
    }
    try {
      sessionStorage.setItem("beheer-login", JSON.stringify({ u, p }));
    } catch {
      /* prima zonder sessie */
    }
    const d = (body.data ?? {}) as Record<string, unknown>;
    setFields((prev) =>
      Object.fromEntries(
        Object.keys(prev).map((k) => [
          k,
          typeof d[k] === "string" ? (d[k] as string) : "",
        ]),
      ),
    );
    if (Array.isArray(d.hours) && d.hours.length === 7) {
      setHours(
        (d.hours as Record<string, unknown>[]).map((r) => ({
          open: typeof r.open === "string" ? r.open : "",
          close: typeof r.close === "string" ? r.close : "",
        })),
      );
    }
    if (d.prices && typeof d.prices === "object") {
      const p2 = d.prices as Record<string, unknown>;
      setPrices((prev) =>
        Object.fromEntries(
          Object.keys(prev).map((k) => [
            k,
            typeof p2[k] === "number" ? String(p2[k]) : "",
          ]),
        ),
      );
    }
    setLoggedIn(true);
  }

  async function doSave() {
    setBusy(true);
    setMessage(null);
    const data: Record<string, unknown> = { ...fields };
    data.hours = hours.map((h) => ({ open: h.open, close: h.close }));
    data.prices = Object.fromEntries(
      Object.entries(prices)
        .filter(([, v]) => v.trim() !== "" && !Number.isNaN(Number(v)))
        .map(([k, v]) => [k, Number(v)]),
    );
    const { status, body } = await api("save", data);
    setBusy(false);
    setMessage(
      status === 200
        ? "✅ Opgeslagen! Herlaad de site om alles live te zien."
        : (body.error ?? "Opslaan mislukt."),
    );
  }

  if (!loggedIn) {
    return (
      <section className="mx-auto max-w-md px-4 py-24">
        <h1 className="display text-3xl">Beheer</h1>
        <p className="mt-2 text-sm text-sand">
          Log in om diensten, prijzen, uren en contactinfo aan te vullen.
        </p>
        <form
          className="mt-8 grid gap-4"
          onSubmit={(e) => {
            e.preventDefault();
            void doLogin();
          }}
        >
          <div>
            <label htmlFor="u" className={labelCls}>Gebruikersnaam</label>
            <input id="u" className={inputCls} value={username} onChange={(e) => setUsername(e.target.value)} autoComplete="username" />
          </div>
          <div>
            <label htmlFor="p" className={labelCls}>Wachtwoord</label>
            <input id="p" type="password" className={inputCls} value={password} onChange={(e) => setPassword(e.target.value)} autoComplete="current-password" />
          </div>
          <button
            type="submit"
            disabled={busy}
            className="display rounded-[4px] bg-olive px-6 py-3 text-sm text-ink transition-colors hover:bg-olive-bright disabled:opacity-50"
          >
            {busy ? "Bezig…" : "Log in"}
          </button>
          {message && <p className="text-sm text-gold">{message}</p>}
        </form>
      </section>
    );
  }

  return (
    <section className="mx-auto max-w-3xl px-4 py-16">
      <h1 className="display text-3xl">
        Beheer — hey <span className="text-olive-bright">{username}</span> 👋
      </h1>
      <p className="mt-2 text-sm text-sand">
        Vul in wat je weet en klik onderaan op opslaan. Lege velden laten de
        site gewoon &ldquo;volgt nog&rdquo; tonen.
      </p>

      <h2 className="display mt-10 text-lg text-olive-bright">Contact</h2>
      <div className="mt-4 grid gap-4 sm:grid-cols-2">
        {(
          [
            ["phone", "Telefoon (bv. +32 4xx xx xx xx)"],
            ["whatsapp", "WhatsApp (bv. 324xxxxxxxx, zonder +)"],
            ["email", "E-mail"],
          ] as const
        ).map(([k, label]) => (
          <div key={k}>
            <label htmlFor={k} className={labelCls}>{label}</label>
            <input id={k} className={inputCls} value={fields[k]} onChange={(e) => setFields({ ...fields, [k]: e.target.value })} />
          </div>
        ))}
      </div>

      <h2 className="display mt-10 text-lg text-olive-bright">Socials & boeken</h2>
      <div className="mt-4 grid gap-4 sm:grid-cols-2">
        {(
          [
            ["instagram", "Instagram-handle (zonder @)"],
            ["tiktok", "TikTok-handle (zonder @)"],
            ["freshaBookingUrl", "Fresha boekingslink (https://www.fresha.com/…)"],
            ["googleBusinessReviewUrl", "Google-reviewlink"],
          ] as const
        ).map(([k, label]) => (
          <div key={k}>
            <label htmlFor={k} className={labelCls}>{label}</label>
            <input id={k} className={inputCls} value={fields[k]} onChange={(e) => setFields({ ...fields, [k]: e.target.value })} />
          </div>
        ))}
      </div>

      <h2 className="display mt-10 text-lg text-olive-bright">Openingsuren</h2>
      <p className="mt-1 text-xs text-muted">
        Laat beide velden leeg voor een sluitingsdag. Formaat: 09:00.
      </p>
      <div className="mt-4 grid gap-2">
        {DAGEN.map((dag, i) => (
          <div key={dag} className="grid grid-cols-[6.5rem_1fr_1fr] items-center gap-3">
            <span className="text-sm text-sand">{dag}</span>
            <input aria-label={`${dag} open`} placeholder="open" className={inputCls} value={hours[i].open} onChange={(e) => setHours(hours.map((h, j) => (j === i ? { ...h, open: e.target.value } : h)))} />
            <input aria-label={`${dag} sluit`} placeholder="sluit" className={inputCls} value={hours[i].close} onChange={(e) => setHours(hours.map((h, j) => (j === i ? { ...h, close: e.target.value } : h)))} />
          </div>
        ))}
      </div>

      <h2 className="display mt-10 text-lg text-olive-bright">Prijzen (€)</h2>
      <div className="mt-4 grid gap-2">
        {services.map((s) => (
          <div key={s.slug} className="grid grid-cols-[1fr_7rem] items-center gap-3">
            <span className="text-sm text-sand">{s.name}</span>
            <input aria-label={`Prijs ${s.name}`} inputMode="decimal" placeholder="€" className={inputCls} value={prices[s.slug]} onChange={(e) => setPrices({ ...prices, [s.slug]: e.target.value })} />
          </div>
        ))}
      </div>

      <h2 className="display mt-10 text-lg text-olive-bright">Over mij</h2>
      <p className="mt-1 text-xs text-muted">
        Het verhaal op de &ldquo;Over mij&rdquo;-pagina. Kort en direct, jij-vorm.
      </p>
      <textarea
        aria-label="Over mij"
        rows={7}
        className={`${inputCls} mt-3`}
        value={fields.overStory}
        onChange={(e) => setFields({ ...fields, overStory: e.target.value })}
      />

      <div className="mt-10 flex items-center gap-4">
        <button
          type="button"
          onClick={() => void doSave()}
          disabled={busy}
          className="display rounded-[4px] bg-olive px-8 py-3 text-sm text-ink transition-colors hover:bg-olive-bright disabled:opacity-50"
        >
          {busy ? "Bezig…" : "Alles opslaan"}
        </button>
        {message && <p className="text-sm text-gold">{message}</p>}
      </div>

      <p className="mt-8 text-xs text-muted">
        Foto&apos;s en video&apos;s kunnen nog niet via deze pagina — stuur die
        gewoon door, dan zetten we ze in de galerij.
      </p>
    </section>
  );
}
