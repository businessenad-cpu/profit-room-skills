// Datum als "za 5 sep" — werkt met een YYYY-MM-DD string, tijdzone-veilig.
export function formatDateNL(date: string, withYear = false): string {
  const d = new Date(`${date}T12:00:00Z`);
  return new Intl.DateTimeFormat("nl-NL", {
    weekday: "short",
    day: "numeric",
    month: "short",
    ...(withYear ? { year: "numeric" } : {}),
    timeZone: "UTC",
  }).format(d);
}

export function formatPrice(price: number): string {
  return `€${price % 1 === 0 ? price : price.toFixed(2).replace(".", ",")}`;
}
