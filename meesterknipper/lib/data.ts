export type Service = {
  id: string;
  name: string;
  price: number;
  durationMin: number;
};

export type Barber = {
  id: string;
  name: string;
  specialty: string;
  initials: string;
};

export const SALON = {
  name: "Kapper Sint Niklaas",
  address: "Stationsstraat 1, 9100 Sint-Niklaas",
  phone: "03 123 45 67",
};

export const SERVICES: Service[] = [
  { id: "knippen-heren", name: "Knippen heren", price: 22, durationMin: 30 },
  { id: "fade", name: "Fade", price: 27, durationMin: 45 },
  { id: "knippen-baard", name: "Knippen + baard", price: 35, durationMin: 60 },
  { id: "baard-trimmen", name: "Baard trimmen", price: 15, durationMin: 20 },
  { id: "kids-knippen", name: "Kids knippen (t/m 12 jaar)", price: 17, durationMin: 30 },
];

export const BARBERS: Barber[] = [
  { id: "enad", name: "Enad", specialty: "Fades & baard", initials: "E" },
  { id: "mo", name: "Mo", specialty: "Klassiek knippen", initials: "M" },
  { id: "yassin", name: "Yassin", specialty: "Kids & tondeuse", initials: "Y" },
];

// Openingstijden: di t/m za, 09:00–18:00. Zondag (0) en maandag (1) gesloten.
export const OPEN_MINUTES = 9 * 60;
export const CLOSE_MINUTES = 18 * 60;
export const SLOT_STEP_MIN = 15;
export const CLOSED_WEEKDAYS = [0, 1];
export const BOOKING_WINDOW_DAYS = 14;

export function getService(id: string): Service | undefined {
  return SERVICES.find((s) => s.id === id);
}

export function getBarber(id: string): Barber | undefined {
  return BARBERS.find((b) => b.id === id);
}
