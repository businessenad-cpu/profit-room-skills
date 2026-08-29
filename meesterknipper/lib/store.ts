// In-memory store. Simpel en snel voor een demo: boekingen blijven zichtbaar
// zolang de serverinstantie leeft (op Vercel: per warme serverless-instantie).
export type Booking = {
  id: string; // bijv. KK-0001
  serviceId: string;
  barberId: string;
  date: string; // YYYY-MM-DD
  time: string; // HH:MM
  durationMin: number;
  price: number;
  customerName: string;
  customerEmail: string;
  customerPhone: string;
  note?: string;
  createdAt: string;
};

type Store = {
  bookings: Booking[];
  counter: number;
};

// Op globalThis zodat de store hot-reloads en meerdere route-modules overleeft.
const g = globalThis as unknown as { __meesterknipperStore?: Store };

function getStore(): Store {
  if (!g.__meesterknipperStore) {
    g.__meesterknipperStore = { bookings: [], counter: 0 };
  }
  return g.__meesterknipperStore;
}

export function listBookings(): Booking[] {
  return [...getStore().bookings].sort((a, b) =>
    a.date === b.date ? a.time.localeCompare(b.time) : a.date.localeCompare(b.date)
  );
}

export function nextBookingNumber(): string {
  const store = getStore();
  store.counter += 1;
  return `KK-${String(store.counter).padStart(4, "0")}`;
}

export function addBooking(booking: Booking): void {
  getStore().bookings.push(booking);
}

export function resetBookings(): void {
  const store = getStore();
  store.bookings = [];
  store.counter = 0;
}

export function bookingsFor(date: string, barberId?: string): Booking[] {
  return getStore().bookings.filter(
    (b) => b.date === date && (!barberId || b.barberId === barberId)
  );
}
