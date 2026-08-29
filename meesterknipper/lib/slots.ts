import {
  BARBERS,
  BOOKING_WINDOW_DAYS,
  CLOSED_WEEKDAYS,
  CLOSE_MINUTES,
  OPEN_MINUTES,
  SLOT_STEP_MIN,
} from "./data";
import { bookingsFor, type Booking } from "./store";

export function toMinutes(time: string): number {
  const [h, m] = time.split(":").map(Number);
  return h * 60 + m;
}

export function toTime(minutes: number): string {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
}

// "Nu" in Nederlandse tijd, ongeacht de server-tijdzone (Vercel draait op UTC).
export function nowInNL(): { date: string; minutes: number } {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Europe/Amsterdam",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  }).formatToParts(new Date());
  const get = (type: string) => parts.find((p) => p.type === type)?.value ?? "00";
  const hour = Number(get("hour")) % 24; // en-CA kan "24" geven om middernacht
  return {
    date: `${get("year")}-${get("month")}-${get("day")}`,
    minutes: hour * 60 + Number(get("minute")),
  };
}

export function weekdayOf(date: string): number {
  return new Date(`${date}T12:00:00Z`).getUTCDay();
}

export function isOpenOn(date: string): boolean {
  return !CLOSED_WEEKDAYS.includes(weekdayOf(date));
}

export function addDays(date: string, days: number): string {
  const d = new Date(`${date}T12:00:00Z`);
  d.setUTCDate(d.getUTCDate() + days);
  return d.toISOString().slice(0, 10);
}

// De komende BOOKING_WINDOW_DAYS dagen vanaf vandaag (NL-tijd).
export function upcomingDays(): { date: string; open: boolean }[] {
  const { date: today } = nowInNL();
  return Array.from({ length: BOOKING_WINDOW_DAYS }, (_, i) => {
    const date = addDays(today, i);
    return { date, open: isOpenOn(date) };
  });
}

function overlaps(startA: number, durA: number, startB: number, durB: number): boolean {
  return startA < startB + durB && startB < startA + durA;
}

export function isBarberFree(
  barberId: string,
  date: string,
  startMin: number,
  durationMin: number
): boolean {
  return !bookingsFor(date, barberId).some((b: Booking) =>
    overlaps(startMin, durationMin, toMinutes(b.time), b.durationMin)
  );
}

// Beschikbare starttijden voor een dienst bij een kapper ("any" = minstens één vrij).
export function availableSlots(
  date: string,
  durationMin: number,
  barberId: string
): string[] {
  if (!isOpenOn(date)) return [];

  const now = nowInNL();
  const slots: string[] = [];
  for (
    let start = OPEN_MINUTES;
    start + durationMin <= CLOSE_MINUTES;
    start += SLOT_STEP_MIN
  ) {
    if (date === now.date && start <= now.minutes) continue;
    const free =
      barberId === "any"
        ? BARBERS.some((b) => isBarberFree(b.id, date, start, durationMin))
        : isBarberFree(barberId, date, start, durationMin);
    if (free) slots.push(toTime(start));
  }
  return slots;
}

// Wijs bij "geen voorkeur" een vrije kapper toe.
export function pickFreeBarber(
  date: string,
  startMin: number,
  durationMin: number
): string | null {
  const counts = new Map(
    BARBERS.map((b) => [b.id, bookingsFor(date, b.id).length])
  );
  const free = BARBERS.filter((b) => isBarberFree(b.id, date, startMin, durationMin));
  if (free.length === 0) return null;
  // Kies de kapper met de minste boekingen die dag: eerlijke verdeling.
  free.sort((a, b) => (counts.get(a.id) ?? 0) - (counts.get(b.id) ?? 0));
  return free[0].id;
}
