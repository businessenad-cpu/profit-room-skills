import { NextResponse } from "next/server";
import Anthropic from "@anthropic-ai/sdk";
import { z } from "zod";
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";
import {
  BEHEER_USER,
  BEHEER_PASS,
  EDITABLE_KEYS,
  getContent,
  saveOverrides,
  type EditableKey,
} from "@/lib/content";

export const dynamic = "force-dynamic";
export const maxDuration = 60;

/**
 * AI-assistent voor /beheer: Nabil beschrijft in gewone taal wat hij wil,
 * Claude vertaalt dat naar content-updates die meteen live gaan.
 * Alleen de whitelisted content-velden zijn aanpasbaar — geen code.
 */

const AssistantSchema = z.object({
  reply: z.string(),
  updates: z.array(
    z.object({
      key: z.enum(EDITABLE_KEYS),
      /** JSON-gecodeerde waarde, bv. "\"+32 470 12 34 56\"" of "[{...}]" */
      valueJson: z.string(),
    }),
  ),
});

const SYSTEM = `Je bent de website-assistent van "Kapper Sint Niklaas" (kapperszaak, Ankerstraat 61B, Sint-Niklaas, België). De beheerder (Nabil) vertelt in gewone taal wat er op de site moet veranderen; jij vertaalt dat naar content-updates.

STIJL VAN DE SITE (bewaken!): informeel Vlaams-Nederlands, jij-vorm, kort en direct ("Kom binnen. Ga fresh naar buiten."), zelfverzekerd maar nooit schreeuwerig of cringe. Schrijf nieuwe teksten altijd in die stijl.

JE MAG UITSLUITEND deze velden aanpassen (key → vorm van de JSON-waarde):
- phone → string, bv. "+32 470 12 34 56"
- whatsapp → string, alleen cijfers met landcode, bv. "32470123456"
- email → string
- instagram / tiktok → string handle zonder @
- freshaBookingUrl → string https-URL van Fresha "Book now"
- googleBusinessReviewUrl → string https-URL
- hours → array van exact 7 objecten {"day":"Maandag".."Zondag","open":"09:00"|null,"close":"18:00"|null}, maandag eerst; null+null = gesloten
- prices → object {slug: prijsInEuro}, bv. {"skin-fade":25}
- services → volledige dienstenlijst: array van {"slug","name","description","price":nummer|null,"durationMin":nummer|null,"category":"heren"|"kids"|"baard"|"kleur"} — gebruik dit om diensten toe te voegen, te verwijderen of te herschrijven; neem ALTIJD de volledige lijst op (bestaande + nieuwe)
- overStory → string, het "Over mij"-verhaal (\\n voor alinea's)
- heroTitle → string, grote titel op home; \\n = regeleinde, *woord* = accentkleur
- heroSub → string, zin onder de hero-titel
- tagline → string, slogan in de footer
- weekendText → string, tekst bij "Fresh voor het weekend"
- marquee → array van korte strings (max 8) voor de lopende tekstband
- uspCards → array (max 6) van {"title","text"} voor "Waar ik voor sta"
- bookingNote → string, tekst op de boekpagina zolang er geen boekingslink is

REGELS:
1. Geef in "updates" alleen de velden die echt moeten veranderen; "valueJson" is de waarde als JSON-string (dus een string-waarde inclusief aanhalingstekens).
2. Baseer wijzigingen op de HUIDIGE CONTENT die je meekrijgt; verzin geen telefoonnummers, prijzen, handles of reviews — vraag ernaar als ze ontbreken.
3. Kan iets niet met deze velden (foto's/video's uploaden, lay-out, kleuren, nieuwe pagina's, code)? Leg dat vriendelijk uit in "reply", geef updates:[] en zeg dat de developer dat oppakt.
4. "reply" is kort, informeel Nederlands: bevestig wát je aanpaste, of stel gerichte vragen bij twijfel (bv. welke prijs precies). Bij een dubbelzinnig verzoek: eerst vragen, niets aanpassen.
5. Wijzigingen staan meteen live; zeg dat de pagina herladen moet worden om ze te zien.`;

type ChatMsg = { role: "user" | "assistant"; text: string };

type Body = {
  username?: string;
  password?: string;
  messages?: ChatMsg[];
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
      { ok: false, error: "Foute login." },
      { status: 401 },
    );
  }

  if (!process.env.ANTHROPIC_API_KEY) {
    return NextResponse.json({
      ok: false,
      error:
        "De AI-assistent is nog niet geactiveerd: voeg de env-var ANTHROPIC_API_KEY toe in Vercel (Settings → Environment Variables) en redeploy.",
    });
  }

  const history = (body.messages ?? [])
    .filter(
      (m): m is ChatMsg =>
        (m?.role === "user" || m?.role === "assistant") &&
        typeof m?.text === "string" &&
        m.text.length > 0 &&
        m.text.length <= 4000,
    )
    .slice(-12);
  if (history.length === 0 || history[history.length - 1].role !== "user") {
    return NextResponse.json({ ok: false, error: "invalid" }, { status: 400 });
  }

  const { content, services } = await getContent();
  const client = new Anthropic();

  try {
    const response = await client.messages.parse({
      model: "claude-opus-5",
      max_tokens: 16000,
      output_config: {
        format: zodOutputFormat(AssistantSchema),
        effort: "low",
      },
      system: `${SYSTEM}\n\nHUIDIGE CONTENT:\n${JSON.stringify({ ...content, services }, null, 1)}`,
      messages: history.map((m) => ({ role: m.role, content: m.text })),
    });

    if (response.stop_reason === "refusal" || !response.parsed_output) {
      return NextResponse.json({
        ok: false,
        error: "De assistent kon dit verzoek niet verwerken — probeer het anders te formuleren.",
      });
    }

    const { reply, updates } = response.parsed_output;
    const data: Record<string, unknown> = {};
    for (const u of updates) {
      try {
        data[u.key as EditableKey] = JSON.parse(u.valueJson);
      } catch {
        data[u.key as EditableKey] = u.valueJson;
      }
    }

    let saved = true;
    if (Object.keys(data).length > 0) {
      saved = await saveOverrides(data);
    }

    return NextResponse.json({
      ok: saved,
      reply: saved
        ? reply
        : `${reply}\n\n(⚠ Opslaan in de databank mislukte — probeer opnieuw.)`,
      applied: Object.keys(data),
    });
  } catch (err) {
    if (err instanceof Anthropic.AuthenticationError) {
      return NextResponse.json({
        ok: false,
        error: "De ANTHROPIC_API_KEY in Vercel is ongeldig — controleer de sleutel.",
      });
    }
    if (err instanceof Anthropic.RateLimitError) {
      return NextResponse.json({
        ok: false,
        error: "Even te druk bij de AI — probeer het over een minuutje opnieuw.",
      });
    }
    if (err instanceof Anthropic.APIError) {
      return NextResponse.json({
        ok: false,
        error: `AI-fout (${err.status ?? "?"}) — probeer opnieuw.`,
      });
    }
    throw err;
  }
}
