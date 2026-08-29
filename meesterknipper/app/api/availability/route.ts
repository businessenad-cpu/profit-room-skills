import { NextRequest, NextResponse } from "next/server";
import { getService } from "@/lib/data";
import { availableSlots, upcomingDays } from "@/lib/slots";

export const dynamic = "force-dynamic";

// GET /api/availability?serviceId=...&barberId=...  -> dagen
// GET /api/availability?serviceId=...&barberId=...&date=YYYY-MM-DD -> tijdslots
export async function GET(req: NextRequest) {
  const serviceId = req.nextUrl.searchParams.get("serviceId") ?? "";
  const barberId = req.nextUrl.searchParams.get("barberId") ?? "any";
  const date = req.nextUrl.searchParams.get("date");

  const service = getService(serviceId);
  if (!service) {
    return NextResponse.json({ error: "Onbekende dienst" }, { status: 400 });
  }

  if (!date) {
    return NextResponse.json({ days: upcomingDays() });
  }

  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) {
    return NextResponse.json({ error: "Ongeldige datum" }, { status: 400 });
  }

  return NextResponse.json({
    slots: availableSlots(date, service.durationMin, barberId),
  });
}
