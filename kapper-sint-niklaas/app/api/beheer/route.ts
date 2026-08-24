import { NextResponse } from "next/server";
import {
  BEHEER_USER,
  BEHEER_PASS,
  getOverrides,
  saveOverrides,
} from "@/lib/content";

export const dynamic = "force-dynamic";

type Body = {
  username?: string;
  password?: string;
  action?: "load" | "save";
  data?: Record<string, unknown>;
};

export async function POST(req: Request) {
  let body: Body;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ ok: false, error: "invalid" }, { status: 400 });
  }

  if (body.username !== BEHEER_USER || body.password !== BEHEER_PASS) {
    return NextResponse.json(
      { ok: false, error: "Foute login. Check je gebruikersnaam en wachtwoord." },
      { status: 401 },
    );
  }

  if (body.action === "load") {
    return NextResponse.json({ ok: true, data: await getOverrides() });
  }

  if (body.action === "save" && body.data && typeof body.data === "object") {
    const saved = await saveOverrides(body.data);
    return NextResponse.json(
      saved
        ? { ok: true }
        : { ok: false, error: "Opslaan mislukt — probeer opnieuw." },
      { status: saved ? 200 : 502 },
    );
  }

  return NextResponse.json({ ok: false, error: "invalid" }, { status: 400 });
}
