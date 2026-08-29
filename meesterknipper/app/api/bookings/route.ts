import { NextRequest, NextResponse } from "next/server";
import {
  getBarber,
  getService,
  BOOKING_WINDOW_DAYS,
  CLOSE_MINUTES,
  OPEN_MINUTES,
} from "@/lib/data";
import { sendBookingEmails } from "@/lib/email";
import {
  addDays,
  isBarberFree,
  isOpenOn,
  nowInNL,
  pickFreeBarber,
  toMinutes,
} from "@/lib/slots";
import { addBooking, listBookings, nextBookingNumber, type Booking } from "@/lib/store";
import { isValidDutchPhone, isValidEmail } from "@/lib/validate";

export const dynamic = "force-dynamic";

export async function GET() {
  return NextResponse.json({ bookings: listBookings() });
}

export async function POST(req: NextRequest) {
  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Ongeldige aanvraag" }, { status: 400 });
  }

  const str = (key: string) => (typeof body[key] === "string" ? (body[key] as string).trim() : "");

  const serviceId = str("serviceId");
  const requestedBarberId = str("barberId") || "any";
  const date = str("date");
  const time = str("time");
  const customerName = str("customerName");
  const customerEmail = str("customerEmail");
  const customerPhone = str("customerPhone");
  const note = str("note");

  const service = getService(serviceId);
  if (!service) {
    return NextResponse.json({ error: "Kies een geldige dienst." }, { status: 400 });
  }
  if (requestedBarberId !== "any" && !getBarber(requestedBarberId)) {
    return NextResponse.json({ error: "Kies een geldige kapper." }, { status: 400 });
  }
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || !/^\d{2}:\d{2}$/.test(time)) {
    return NextResponse.json({ error: "Kies een geldige datum en tijd." }, { status: 400 });
  }
  if (!customerName) {
    return NextResponse.json({ error: "Vul je naam in." }, { status: 400 });
  }
  if (!isValidEmail(customerEmail)) {
    return NextResponse.json({ error: "Vul een geldig e-mailadres in." }, { status: 400 });
  }
  if (!isValidDutchPhone(customerPhone)) {
    return NextResponse.json(
      { error: "Vul een geldig Nederlands telefoonnummer in (bijv. 06 12 34 56 78)." },
      { status: 400 }
    );
  }

  const now = nowInNL();
  const lastDate = addDays(now.date, BOOKING_WINDOW_DAYS - 1);
  if (date < now.date || date > lastDate) {
    return NextResponse.json(
      { error: "Kies een datum binnen de komende 14 dagen." },
      { status: 400 }
    );
  }
  if (!isOpenOn(date)) {
    return NextResponse.json(
      { error: "De salon is gesloten op deze dag (zo & ma gesloten)." },
      { status: 400 }
    );
  }

  const startMin = toMinutes(time);
  if (
    startMin < OPEN_MINUTES ||
    startMin + service.durationMin > CLOSE_MINUTES ||
    startMin % 15 !== 0
  ) {
    return NextResponse.json({ error: "Deze tijd valt buiten de openingstijden." }, { status: 400 });
  }
  if (date === now.date && startMin <= now.minutes) {
    return NextResponse.json({ error: "Deze tijd is al voorbij." }, { status: 400 });
  }

  // Dubbele boekingen onmogelijk: check beschikbaarheid op het moment van boeken.
  let barberId = requestedBarberId;
  if (barberId === "any") {
    const picked = pickFreeBarber(date, startMin, service.durationMin);
    if (!picked) {
      return NextResponse.json(
        { error: "Dit tijdslot is net geboekt. Kies een andere tijd." },
        { status: 409 }
      );
    }
    barberId = picked;
  } else if (!isBarberFree(barberId, date, startMin, service.durationMin)) {
    return NextResponse.json(
      { error: "Dit tijdslot is net geboekt bij deze kapper. Kies een andere tijd." },
      { status: 409 }
    );
  }

  const booking: Booking = {
    id: nextBookingNumber(),
    serviceId,
    barberId,
    date,
    time,
    durationMin: service.durationMin,
    price: service.price,
    customerName,
    customerEmail,
    customerPhone,
    note: note || undefined,
    createdAt: new Date().toISOString(),
  };
  addBooking(booking);

  const barber = getBarber(barberId)!;
  const email = await sendBookingEmails(booking, service, barber);

  return NextResponse.json({ booking, email }, { status: 201 });
}
