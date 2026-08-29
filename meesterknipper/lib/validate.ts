// NL-telefoonnummer: 0612345678, 06 12 34 56 78, +31 6 12345678, 0031612345678,
// of vast nummer zoals 0201234567.
export function isValidDutchPhone(phone: string): boolean {
  const cleaned = phone.replace(/[\s\-().]/g, "");
  return /^(\+31|0031)[1-9]\d{8}$/.test(cleaned) || /^0[1-9]\d{8}$/.test(cleaned);
}

export function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.trim());
}
