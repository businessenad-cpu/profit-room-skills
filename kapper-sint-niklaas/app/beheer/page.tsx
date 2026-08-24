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
type ChatMsg = { role: "user" | "assistant"; text: string };

const CHAT_WELCOME: ChatMsg = {
  role: "assistant",
  text: "Hey! Zeg gewoon wat je wil veranderen aan de site — bv. “zet skin fade op €25”, “maandag zijn we gesloten”, “voeg een dienst kleuren toe voor dames” of “maak de tekst op de homepagina wat losser”. Ik voer het meteen uit.",
};

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
  const [chat, setChat] = useState<ChatMsg[]>([CHAT_WELCOME]);
  const [chatInput, setChatInput] = useState("");
  const [chatBusy, setChatBusy] = useState(false);

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

  async function sendChat() {
    const text = chatInput.trim();
    if (!text || chatBusy) return;
    const next: ChatMsg[] = [...chat, { role: "user", text }];
    setChat(next);
    setChatInput("");
    setChatBusy(true);
    try {
      const res = await fetch("/api/assistent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username,
          password,
          // welkomstbericht niet meesturen, alleen echte conversatie
          messages: next.filter((m) => m !== CHAT_WELCOME),
        }),
      });
      const body = await res.json();
      const applied: string[] = Array.isArray(body.applied) ? body.applied : [];
      const suffix =
        body.ok && applied.length > 0
          ? "\n\n✅ Aangepast — herlaad de site om het live te zien."
          : "";
      setChat((c) => [
        ...c,
        {
          role: "assistant",
          text: (body.reply ?? body.error ?? "Er ging iets mis — probeer opnieuw.") + suffix,
        },
      ]);
    } catch {
      setChat((c) => [
        ...c,
        { role: "assistant", text: "Netwerkfout — probeer het nog eens." },
      ]);
    } finally {
      setChatBusy(false);
    }
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
        Zeg tegen de assistent wat je wil veranderen, of vul het formulier
        eronder handmatig in.
      </p>

      {/* ── AI-assistent ─────────────────────────────────────────────── */}
      <h2 className="display mt-10 text-lg text-olive-bright">
        ✨ Assistent — zeg het gewoon
      </h2>
      <div className="mt-4 border border-gold/30 bg-surface">
        <div className="max-h-96 space-y-3 overflow-y-auto p-4">
          {chat.map((m, i) => (
            <div
              key={i}
              className={
                m.role === "user"
                  ? "ml-8 rounded-[4px] bg-olive-deep px-3 py-2 text-sm text-bone"
                  : "mr-8 rounded-[4px] bg-surface-2 px-3 py-2 text-sm text-sand"
              }
            >
              <p className="whitespace-pre-line">{m.text}</p>
            </div>
          ))}
          {chatBusy && (
            <p className="mr-8 px-3 py-2 text-sm text-muted">
              ✂︎ Bezig met knippen…
            </p>
          )}
        </div>
        <form
          className="flex gap-2 border-t border-gold/20 p-3"
          onSubmit={(e) => {
            e.preventDefault();
            void sendChat();
          }}
        >
          <input
            aria-label="Bericht aan de assistent"
            className={inputCls}
            placeholder="Bv. zet skin fade op €25 en maandag gesloten"
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            disabled={chatBusy}
          />
          <button
            type="submit"
            disabled={chatBusy || !chatInput.trim()}
            className="display shrink-0 rounded-[4px] bg-olive px-5 py-2 text-sm text-ink transition-colors hover:bg-olive-bright disabled:opacity-50"
          >
            Stuur
          </button>
        </form>
      </div>
      <p className="mt-2 text-xs text-muted">
        De assistent past teksten, prijzen, uren, diensten en links aan.
        Foto&apos;s, kleuren en lay-out lopen via de developer.
      </p>

      <h2 className="display mt-12 text-lg text-olive-bright">Contact</h2>
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
