"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { BARBERS, SALON, SERVICES, getBarber, getService } from "@/lib/data";
import { formatDateNL, formatPrice } from "@/lib/format";
import { isValidDutchPhone, isValidEmail } from "@/lib/validate";

type Day = { date: string; open: boolean };

type EmailPreview = { to: string; subject: string; html: string };

type BookingResult = {
  booking: {
    id: string;
    serviceId: string;
    barberId: string;
    date: string;
    time: string;
    price: number;
  };
  email: {
    demoMode: boolean;
    sent: boolean;
    error?: string;
    customerEmail: EmailPreview;
    salonEmail: EmailPreview | null;
  };
};

const STEPS = ["Dienst", "Kapper", "Datum & tijd", "Gegevens", "Bevestigen"];

export default function BookingFlow() {
  const [step, setStep] = useState(0);
  const [serviceId, setServiceId] = useState("");
  const [barberId, setBarberId] = useState("");
  const [days, setDays] = useState<Day[]>([]);
  const [date, setDate] = useState("");
  const [slots, setSlots] = useState<string[] | null>(null);
  const [time, setTime] = useState("");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [note, setNote] = useState("");
  const [formError, setFormError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<BookingResult | null>(null);
  const [showEmail, setShowEmail] = useState(false);

  const service = getService(serviceId);

  // Dagen laden zodra we bij stap 3 komen.
  useEffect(() => {
    if (step !== 2 || !serviceId) return;
    fetch(`/api/availability?serviceId=${serviceId}&barberId=${barberId || "any"}`)
      .then((r) => r.json())
      .then((d) => setDays(d.days ?? []))
      .catch(() => setDays([]));
  }, [step, serviceId, barberId]);

  const loadSlots = useCallback(
    (d: string) => {
      setDate(d);
      setTime("");
      setSlots(null);
      fetch(
        `/api/availability?serviceId=${serviceId}&barberId=${barberId || "any"}&date=${d}`
      )
        .then((r) => r.json())
        .then((res) => setSlots(res.slots ?? []))
        .catch(() => setSlots([]));
    },
    [serviceId, barberId]
  );

  const detailsValid = useMemo(
    () => name.trim().length > 0 && isValidEmail(email) && isValidDutchPhone(phone),
    [name, email, phone]
  );

  async function submitBooking() {
    setSubmitting(true);
    setFormError("");
    try {
      const res = await fetch("/api/bookings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          serviceId,
          barberId: barberId || "any",
          date,
          time,
          customerName: name.trim(),
          customerEmail: email.trim(),
          customerPhone: phone.trim(),
          note: note.trim(),
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        setFormError(data.error ?? "Er ging iets mis. Probeer het opnieuw.");
        if (res.status === 409) {
          // Slot net bezet: terug naar tijdkeuze en slots verversen.
          setStep(2);
          loadSlots(date);
        }
        return;
      }
      setResult(data);
    } catch {
      setFormError("Er ging iets mis. Probeer het opnieuw.");
    } finally {
      setSubmitting(false);
    }
  }

  if (result) {
    const b = result.booking;
    const bookedService = getService(b.serviceId);
    const bookedBarber = getBarber(b.barberId);
    return (
      <div className="space-y-5">
        <div className="rounded-2xl border border-gold-500/40 bg-ink-800 p-6 text-center">
          <div className="text-5xl mb-3">✅</div>
          <h1 className="text-2xl font-bold">Afspraak bevestigd!</h1>
          <p className="mt-1 text-zinc-400 text-sm">
            Je ontvangt een bevestiging per e-mail.
          </p>
          <div className="mt-4 inline-block rounded-full bg-gold-500 px-4 py-1.5 text-ink-950 font-bold tracking-wide">
            {b.id}
          </div>
          <dl className="mt-6 space-y-2 text-left text-sm">
            <Row label="Dienst" value={bookedService?.name ?? b.serviceId} />
            <Row label="Kapper" value={bookedBarber?.name ?? b.barberId} />
            <Row label="Datum & tijd" value={`${formatDateNL(b.date, true)}, ${b.time}`} />
            <Row label="Prijs" value={formatPrice(b.price)} bold />
            <Row label="Adres" value={SALON.address} />
          </dl>
        </div>

        {result.email.demoMode && (
          <div className="rounded-2xl border border-ink-600 bg-ink-900 p-4">
            <p className="text-sm text-gold-400 font-semibold">
              Demo-modus: dit is de mail die verstuurd zou worden
            </p>
            <p className="mt-1 text-xs text-zinc-400">
              Aan: {result.email.customerEmail.to}
              <br />
              Onderwerp: {result.email.customerEmail.subject}
            </p>
            <button
              onClick={() => setShowEmail((v) => !v)}
              className="mt-3 text-sm text-gold-400 underline underline-offset-4"
            >
              {showEmail ? "Verberg mail" : "Bekijk mail"}
            </button>
            {showEmail && (
              <div
                className="mt-3 rounded-xl overflow-hidden border border-ink-600"
                dangerouslySetInnerHTML={{ __html: result.email.customerEmail.html }}
              />
            )}
          </div>
        )}
        {!result.email.demoMode && result.email.error && (
          <p className="text-sm text-amber-400 text-center">{result.email.error}</p>
        )}

        <button
          onClick={() => window.location.reload()}
          className="w-full rounded-xl border border-ink-600 py-3 text-sm text-zinc-300 hover:border-gold-500 transition-colors"
        >
          Nieuwe afspraak maken
        </button>
      </div>
    );
  }

  return (
    <div>
      {/* Stappenindicator */}
      <ol className="flex items-center gap-1 mb-6">
        {STEPS.map((label, i) => (
          <li key={label} className="flex-1">
            <div
              className={`h-1 rounded-full ${i <= step ? "bg-gold-500" : "bg-ink-700"}`}
            />
            <span
              className={`mt-1 hidden sm:block text-[10px] ${
                i === step ? "text-gold-400" : "text-zinc-500"
              }`}
            >
              {label}
            </span>
          </li>
        ))}
      </ol>
      <p className="sm:hidden text-xs text-zinc-500 mb-4 -mt-3">
        Stap {step + 1} van {STEPS.length}: <span className="text-gold-400">{STEPS[step]}</span>
      </p>

      {step === 0 && (
        <section className="space-y-3">
          <h1 className="text-xl font-bold">Kies je dienst</h1>
          {SERVICES.map((s) => (
            <button
              key={s.id}
              onClick={() => {
                setServiceId(s.id);
                setDate("");
                setTime("");
                setStep(1);
              }}
              className={`w-full flex items-center justify-between rounded-2xl border p-4 text-left transition-colors ${
                serviceId === s.id
                  ? "border-gold-500 bg-ink-800"
                  : "border-ink-600 bg-ink-900 hover:border-gold-500/60"
              }`}
            >
              <span>
                <span className="block font-semibold">{s.name}</span>
                <span className="block text-xs text-zinc-400 mt-0.5">
                  {s.durationMin} min
                </span>
              </span>
              <span className="text-gold-400 font-bold text-lg">
                {formatPrice(s.price)}
              </span>
            </button>
          ))}
        </section>
      )}

      {step === 1 && (
        <section className="space-y-3">
          <h1 className="text-xl font-bold">Kies je kapper</h1>
          {BARBERS.map((b) => (
            <button
              key={b.id}
              onClick={() => {
                setBarberId(b.id);
                setDate("");
                setTime("");
                setStep(2);
              }}
              className={`w-full flex items-center gap-4 rounded-2xl border p-4 text-left transition-colors ${
                barberId === b.id
                  ? "border-gold-500 bg-ink-800"
                  : "border-ink-600 bg-ink-900 hover:border-gold-500/60"
              }`}
            >
              <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-gold-500/15 border border-gold-500/40 text-gold-400 font-bold text-lg">
                {b.initials}
              </span>
              <span>
                <span className="block font-semibold">{b.name}</span>
                <span className="block text-xs text-zinc-400 mt-0.5">{b.specialty}</span>
              </span>
            </button>
          ))}
          <button
            onClick={() => {
              setBarberId("any");
              setDate("");
              setTime("");
              setStep(2);
            }}
            className={`w-full rounded-2xl border p-4 text-left transition-colors ${
              barberId === "any"
                ? "border-gold-500 bg-ink-800"
                : "border-dashed border-ink-600 bg-ink-900 hover:border-gold-500/60"
            }`}
          >
            <span className="font-semibold">Geen voorkeur</span>
            <span className="block text-xs text-zinc-400 mt-0.5">
              We plannen je in bij een beschikbare kapper
            </span>
          </button>
          <BackButton onClick={() => setStep(0)} />
        </section>
      )}

      {step === 2 && (
        <section className="space-y-4">
          <h1 className="text-xl font-bold">Kies datum &amp; tijd</h1>
          <div className="grid grid-cols-4 sm:grid-cols-7 gap-2">
            {days.map((d) => (
              <button
                key={d.date}
                disabled={!d.open}
                onClick={() => loadSlots(d.date)}
                className={`rounded-xl border px-1 py-2.5 text-center text-sm transition-colors ${
                  date === d.date
                    ? "border-gold-500 bg-gold-500 text-ink-950 font-bold"
                    : d.open
                      ? "border-ink-600 bg-ink-900 hover:border-gold-500/60"
                      : "border-ink-700 bg-ink-900/40 text-zinc-600 cursor-not-allowed"
                }`}
              >
                {formatDateNL(d.date)}
                {!d.open && <span className="block text-[10px]">gesloten</span>}
              </button>
            ))}
          </div>
          {date && (
            <div>
              <h2 className="text-sm font-semibold text-zinc-300 mb-2">
                Beschikbare tijden op {formatDateNL(date)}
              </h2>
              {slots === null ? (
                <p className="text-sm text-zinc-500">Beschikbaarheid laden…</p>
              ) : slots.length === 0 ? (
                <p className="text-sm text-zinc-400">
                  Geen tijden meer beschikbaar op deze dag. Kies een andere dag.
                </p>
              ) : (
                <div className="grid grid-cols-4 sm:grid-cols-6 gap-2">
                  {slots.map((t) => (
                    <button
                      key={t}
                      onClick={() => {
                        setTime(t);
                        setStep(3);
                      }}
                      className={`rounded-xl border py-2.5 text-sm transition-colors ${
                        time === t
                          ? "border-gold-500 bg-gold-500 text-ink-950 font-bold"
                          : "border-ink-600 bg-ink-900 hover:border-gold-500/60"
                      }`}
                    >
                      {t}
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}
          <p className="text-xs text-zinc-500">
            Open di t/m za, 09:00–18:00 · zondag en maandag gesloten
          </p>
          <BackButton onClick={() => setStep(1)} />
        </section>
      )}

      {step === 3 && (
        <section className="space-y-4">
          <h1 className="text-xl font-bold">Jouw gegevens</h1>
          <Field label="Naam *">
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Voor- en achternaam"
              className={inputCls}
              autoComplete="name"
            />
          </Field>
          <Field
            label="E-mailadres *"
            error={email.length > 0 && !isValidEmail(email) ? "Ongeldig e-mailadres" : ""}
          >
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="naam@voorbeeld.nl"
              className={inputCls}
              autoComplete="email"
            />
          </Field>
          <Field
            label="Telefoonnummer *"
            error={
              phone.length > 0 && !isValidDutchPhone(phone)
                ? "Ongeldig NL-nummer (bijv. 06 12 34 56 78)"
                : ""
            }
          >
            <input
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="06 12 34 56 78"
              className={inputCls}
              autoComplete="tel"
            />
          </Field>
          <Field label="Opmerking (optioneel)">
            <textarea
              value={note}
              onChange={(e) => setNote(e.target.value)}
              placeholder="Bijv. graag met 1 op de zijkanten"
              rows={2}
              className={inputCls}
            />
          </Field>
          <button
            disabled={!detailsValid}
            onClick={() => setStep(4)}
            className={primaryBtn}
          >
            Naar bevestiging
          </button>
          <BackButton onClick={() => setStep(2)} />
        </section>
      )}

      {step === 4 && service && (
        <section className="space-y-4">
          <h1 className="text-xl font-bold">Bevestig je afspraak</h1>
          <div className="rounded-2xl border border-ink-600 bg-ink-900 p-5">
            <dl className="space-y-2 text-sm">
              <Row label="Dienst" value={service.name} />
              <Row
                label="Kapper"
                value={barberId === "any" ? "Geen voorkeur" : getBarber(barberId)?.name ?? ""}
              />
              <Row label="Datum & tijd" value={`${formatDateNL(date, true)}, ${time}`} />
              <Row label="Duur" value={`${service.durationMin} min`} />
              <Row label="Prijs" value={formatPrice(service.price)} bold />
              <Row label="Naam" value={name} />
              <Row label="E-mail" value={email} />
              <Row label="Telefoon" value={phone} />
              {note && <Row label="Opmerking" value={note} />}
            </dl>
          </div>
          {formError && <p className="text-sm text-red-400">{formError}</p>}
          <button onClick={submitBooking} disabled={submitting} className={primaryBtn}>
            {submitting ? "Bezig met boeken…" : "Afspraak bevestigen"}
          </button>
          <BackButton onClick={() => setStep(3)} />
        </section>
      )}
    </div>
  );
}

const inputCls =
  "w-full rounded-xl border border-ink-600 bg-ink-900 px-4 py-3 text-base placeholder:text-zinc-600 focus:border-gold-500 focus:outline-none";

const primaryBtn =
  "w-full rounded-xl bg-gold-500 py-3.5 text-base font-bold text-ink-950 transition-colors hover:bg-gold-400 disabled:opacity-40 disabled:cursor-not-allowed";

function Field({
  label,
  error,
  children,
}: {
  label: string;
  error?: string;
  children: React.ReactNode;
}) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-sm text-zinc-300">{label}</span>
      {children}
      {error && <span className="mt-1 block text-xs text-red-400">{error}</span>}
    </label>
  );
}

function Row({ label, value, bold }: { label: string; value: string; bold?: boolean }) {
  return (
    <div className="flex justify-between gap-4">
      <dt className="text-zinc-400">{label}</dt>
      <dd className={`text-right ${bold ? "font-bold text-gold-400" : ""}`}>{value}</dd>
    </div>
  );
}

function BackButton({ onClick }: { onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="w-full rounded-xl border border-ink-600 py-3 text-sm text-zinc-400 hover:border-gold-500/60 transition-colors"
    >
      ← Terug
    </button>
  );
}
