import { NextResponse } from "next/server";
import { resetBookings } from "@/lib/store";

export const dynamic = "force-dynamic";

export async function POST() {
  resetBookings();
  return NextResponse.json({ ok: true });
}
