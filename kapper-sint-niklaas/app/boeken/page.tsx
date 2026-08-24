import type { Metadata } from "next";
import Link from "next/link";
import { site } from "@/lib/site";
import { getContent } from "@/lib/content";
import { TatreezBand } from "@/components/patterns";

export const metadata: Metadata = {
  title: "Boek je cut",
  description:
    "Boek online je afspraak bij Kapper Sint Niklaas — Ankerstraat 61B. Kies je cut, kies je moment, klaar.",
};

export default async function BoekenPage() {
  const { content } = await getContent();
  return (
    <section className="mx-auto max-w-6xl px-4 py-16">
      <h1 className="display text-3xl sm:text-5xl">
        Boek je <span className="text-olive-bright">cut</span>
      </h1>
      <p className="mt-4 max-w-md text-sand">
        Kies je cut, kies je moment. Boeken duurt geen minuut.
      </p>

      <div className="mt-10">
        {content.freshaBookingUrl ? (
          <>
            {/* Officiële Fresha-boekingslink — embed via iframe op eigen pagina */}
            <iframe
              src={content.freshaBookingUrl}
              title="Online boeken via Fresha"
              className="h-[80vh] w-full rounded-[4px] border border-gold/20 bg-surface"
            />
            <p className="mt-3 text-xs text-muted">
              Opent het niet?{" "}
              <a
                href={content.freshaBookingUrl}
                rel="noopener"
                className="text-olive-bright hover:text-bone"
              >
                Boek rechtstreeks op Fresha →
              </a>
            </p>
          </>
        ) : (
          <div className="border border-dashed border-gold/40 bg-surface p-8">
            <h2 className="display text-lg text-olive-bright">
              ⚠ Online boeken wordt aangesloten
            </h2>
            <p className="mt-3 max-w-lg text-sm text-sand">
              {site.bookingFallbackNote}
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              {content.whatsapp ? (
                <a
                  href={`https://wa.me/${content.whatsapp}?text=${encodeURIComponent("Hey! Ik wil graag een afspraak boeken.")}`}
                  rel="noopener"
                  className="display rounded-[4px] bg-olive px-6 py-3 text-sm text-ink transition-colors hover:bg-olive-bright"
                >
                  WhatsApp
                </a>
              ) : (
                <span className="display rounded-[4px] border border-dashed border-gold/40 px-6 py-3 text-sm text-muted">
                  WhatsApp-nummer volgt
                </span>
              )}
              {content.phone ? (
                <a
                  href={`tel:${content.phone.replace(/\s/g, "")}`}
                  className="display rounded-[4px] border border-gold/40 px-6 py-3 text-sm text-sand transition-colors hover:border-olive-bright hover:text-bone"
                >
                  Bel {content.phone}
                </a>
              ) : (
                <span className="display rounded-[4px] border border-dashed border-gold/40 px-6 py-3 text-sm text-muted">
                  Telefoonnummer volgt
                </span>
              )}
            </div>
            <p className="mt-6 text-xs text-muted">
              (Voor de zaak: vul <code>freshaBookingUrl</code> in{" "}
              <code>lib/site.ts</code> in zodra je Fresha-account klaar is —
              dan verschijnt hier automatisch de boekingsmodule.)
            </p>
          </div>
        )}
      </div>

      <div className="mt-12">
        <TatreezBand />
      </div>
      <p className="mt-6 text-sm text-sand">
        Liever eerst kijken wat het kost?{" "}
        <Link href="/prijzen" className="text-olive-bright hover:text-bone">
          Cuts & prijzen →
        </Link>
      </p>
    </section>
  );
}
