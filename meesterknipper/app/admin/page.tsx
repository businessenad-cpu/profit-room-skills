"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { BARBERS, getBarber, getService } from "@/lib/data";
import { formatDateNL, formatPrice } from "@/lib/format";

type Booking = {
  id: string;
  serviceId: string;
  barberId: string;
  date: string;
  time: string;
  durationMin: number;
  price: number;
  customerName: string;
  customerPhone: string;
  note?: string;
};

export default function AdminPage() {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDate, setSelectedDate] = useState("");
  const [resetting, setResetting] = useState(false);

  const load = useCallback(async () => {
    const res = await fetch("/api/bookings", { cache: "no-store" });
    const data = await res.json();
    setBookings(data.bookings ?? []);
    setLoading(false);
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const dates = useMemo(
    () => Array.from(new Set(bookings.map((b) => b.date))).sort(),
    [bookings]
  );

  useEffect(() => {
    if (dates.length > 0 && !dates.includes(selectedDate)) {
      setSelectedDate(dates[0]);
    }
  }, [dates, selectedDate]);

  const dayBookings = bookings.filter((b) => b.date === selectedDate);

  const revenueByDate = useMemo(() => {
    const map = new Map<string, number>();
    for (const b of bookings) {
      map.set(b.date, (map.get(b.date) ?? 0) + b.price);
    }
    return map;
  }, [bookings]);

  async function resetDemo() {
    if (!window.confirm("Alle demo-boekingen wissen?")) return;
    setResetting(true);
    await fetch("/api/reset", { method: "POST" });
    setResetting(false);
    setSelectedDate("");
    load();
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-3">
        <h1 className="text-2xl font-bold">Admin-overzicht</h1>
        <button
          onClick={resetDemo}
          disabled={resetting || bookings.length === 0}
          className="rounded-xl border border-red-500/50 px-4 py-2 text-sm text-red-400 hover:bg-red-500/10 transition-colors disabled:opacity-40"
        >
          {resetting ? "Bezig…" : "Demo resetten"}
        </button>
      </div>

      {loading ? (
        <p className="text-sm text-zinc-500">Boekingen laden…</p>
      ) : bookings.length === 0 ? (
        <div className="rounded-2xl border border-ink-600 bg-ink-900 p-8 text-center text-zinc-400">
          Nog geen boekingen. Maak een boeking via de{" "}
          <a href="/" className="text-gold-400 underline underline-offset-4">
            boekingspagina
          </a>
          .
        </div>
      ) : (
        <>
          {/* Dagkeuze */}
          <div className="flex flex-wrap gap-2">
            {dates.map((d) => (
              <button
                key={d}
                onClick={() => setSelectedDate(d)}
                className={`rounded-xl border px-3 py-2 text-sm transition-colors ${
                  selectedDate === d
                    ? "border-gold-500 bg-gold-500 text-ink-950 font-bold"
                    : "border-ink-600 bg-ink-900 hover:border-gold-500/60"
                }`}
              >
                {formatDateNL(d)}
              </button>
            ))}
          </div>

          {/* Agenda per kapper */}
          <section>
            <h2 className="mb-3 text-sm font-semibold text-zinc-300">
              Agenda {selectedDate && formatDateNL(selectedDate, true)} —{" "}
              <span className="text-gold-400">
                {formatPrice(revenueByDate.get(selectedDate) ?? 0)} verwachte omzet
              </span>
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {BARBERS.map((barber) => {
                const list = dayBookings
                  .filter((b) => b.barberId === barber.id)
                  .sort((a, b) => a.time.localeCompare(b.time));
                return (
                  <div
                    key={barber.id}
                    className="rounded-2xl border border-ink-600 bg-ink-900 p-3"
                  >
                    <h3 className="mb-2 flex items-center gap-2 font-semibold">
                      <span className="flex h-7 w-7 items-center justify-center rounded-full bg-gold-500/15 border border-gold-500/40 text-gold-400 text-xs font-bold">
                        {barber.initials}
                      </span>
                      {barber.name}
                      <span className="ml-auto text-xs text-zinc-500">
                        {list.length} afspr.
                      </span>
                    </h3>
                    {list.length === 0 ? (
                      <p className="py-4 text-center text-xs text-zinc-600">
                        Geen afspraken
                      </p>
                    ) : (
                      <ul className="space-y-2">
                        {list.map((b) => (
                          <li
                            key={b.id}
                            className="rounded-xl border-l-4 border-gold-500 bg-ink-800 p-2.5 text-sm"
                          >
                            <div className="flex justify-between font-semibold">
                              <span>{b.time}</span>
                              <span className="text-gold-400">
                                {formatPrice(b.price)}
                              </span>
                            </div>
                            <div className="text-zinc-300">{b.customerName}</div>
                            <div className="text-xs text-zinc-500">
                              {getService(b.serviceId)?.name} · {b.durationMin} min
                            </div>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                );
              })}
            </div>
          </section>

          {/* Alle boekingen */}
          <section>
            <h2 className="mb-3 text-sm font-semibold text-zinc-300">
              Alle boekingen ({bookings.length})
            </h2>
            <div className="overflow-x-auto rounded-2xl border border-ink-600">
              <table className="w-full min-w-[640px] text-sm">
                <thead className="bg-ink-900 text-left text-xs text-zinc-400">
                  <tr>
                    <th className="px-3 py-2.5">Nr.</th>
                    <th className="px-3 py-2.5">Datum</th>
                    <th className="px-3 py-2.5">Tijd</th>
                    <th className="px-3 py-2.5">Klant</th>
                    <th className="px-3 py-2.5">Dienst</th>
                    <th className="px-3 py-2.5">Kapper</th>
                    <th className="px-3 py-2.5 text-right">Prijs</th>
                  </tr>
                </thead>
                <tbody>
                  {bookings.map((b) => (
                    <tr key={b.id} className="border-t border-ink-700">
                      <td className="px-3 py-2.5 font-mono text-xs text-gold-400">
                        {b.id}
                      </td>
                      <td className="px-3 py-2.5">{formatDateNL(b.date)}</td>
                      <td className="px-3 py-2.5">{b.time}</td>
                      <td className="px-3 py-2.5">
                        {b.customerName}
                        <span className="block text-xs text-zinc-500">
                          {b.customerPhone}
                        </span>
                      </td>
                      <td className="px-3 py-2.5">{getService(b.serviceId)?.name}</td>
                      <td className="px-3 py-2.5">{getBarber(b.barberId)?.name}</td>
                      <td className="px-3 py-2.5 text-right font-semibold">
                        {formatPrice(b.price)}
                      </td>
                    </tr>
                  ))}
                </tbody>
                <tfoot>
                  {dates.map((d) => (
                    <tr key={d} className="border-t border-ink-700 bg-ink-900/60 text-xs">
                      <td colSpan={6} className="px-3 py-2 text-zinc-400">
                        Totaal {formatDateNL(d, true)}
                      </td>
                      <td className="px-3 py-2 text-right font-bold text-gold-400">
                        {formatPrice(revenueByDate.get(d) ?? 0)}
                      </td>
                    </tr>
                  ))}
                </tfoot>
              </table>
            </div>
          </section>
        </>
      )}
    </div>
  );
}
