import type { Metadata } from "next";
import { site } from "@/lib/site";
import { getContent } from "@/lib/content";
import { TatreezBand } from "@/components/patterns";
import { BookCta } from "@/components/ui";

export const metadata: Metadata = {
  title: "Contact & route",
  description:
    "Kapper Sint Niklaas — Ankerstraat 61B, 9100 Sint-Niklaas. Openingsuren, route, WhatsApp en telefoon.",
};

const mapsQuery = encodeURIComponent(
  `${site.address.street}, ${site.address.postalCode} ${site.address.city}`,
);

export default async function ContactPage() {
  const { content } = await getContent();
  return (
    <>
      <section className="mx-auto max-w-6xl px-4 py-16">
        <h1 className="display text-3xl sm:text-5xl">
          Kom <span className="text-olive-bright">langs</span>
        </h1>

        <div className="mt-10 grid gap-10 lg:grid-cols-12">
          <div className="lg:col-span-5">
            <h2 className="display text-lg text-olive-bright">Adres</h2>
            <p className="mt-2 text-sand">
              {site.address.street}
              <br />
              {site.address.postalCode} {site.address.city}
            </p>
            <a
              href={`https://www.google.com/maps/dir/?api=1&destination=${mapsQuery}`}
              rel="noopener"
              className="mt-2 inline-block text-sm text-olive-bright hover:text-bone"
            >
              Route via Google Maps →
            </a>

            <h2 className="display mt-8 text-lg text-olive-bright">
              Direct contact
            </h2>
            <div className="mt-3 flex flex-wrap gap-3">
              {content.whatsapp ? (
                <a
                  href={`https://wa.me/${content.whatsapp}`}
                  rel="noopener"
                  className="display rounded-[4px] bg-olive px-5 py-3 text-sm text-ink transition-colors hover:bg-olive-bright"
                >
                  WhatsApp
                </a>
              ) : (
                <span className="display rounded-[4px] border border-dashed border-gold/40 px-5 py-3 text-sm text-muted">
                  WhatsApp volgt
                </span>
              )}
              {content.phone ? (
                <a
                  href={`tel:${content.phone.replace(/\s/g, "")}`}
                  className="display rounded-[4px] border border-gold/40 px-5 py-3 text-sm text-sand transition-colors hover:border-olive-bright hover:text-bone"
                >
                  Bel {content.phone}
                </a>
              ) : (
                <span className="display rounded-[4px] border border-dashed border-gold/40 px-5 py-3 text-sm text-muted">
                  Telefoon volgt
                </span>
              )}
            </div>

            <h2 className="display mt-8 text-lg text-olive-bright">
              Openingsuren
            </h2>
            <ul className="mt-3 grid gap-px border border-gold/20 bg-gold/20">
              {content.hours.map((h) => (
                <li
                  key={h.day}
                  className="flex items-center justify-between bg-surface px-4 py-2.5 text-sm"
                >
                  <span>{h.day}</span>
                  <span className="tabular text-sand">
                    {h.open ? `${h.open} – ${h.close}` : "gesloten"}
                  </span>
                </li>
              ))}
            </ul>
            {content.hoursAreDraft && (
              <p className="mt-2 text-xs text-muted">
                ⚠ Voorlopige uren — worden bevestigd door de zaak.
              </p>
            )}
          </div>

          <div className="lg:col-span-7">
            <iframe
              title={`Kaart: ${site.address.street}, ${site.address.city}`}
              src={`https://www.google.com/maps?q=${mapsQuery}&output=embed&hl=nl`}
              className="h-[24rem] w-full rounded-[4px] border border-gold/20 grayscale-[0.4] lg:h-full lg:min-h-[28rem]"
              loading="lazy"
              referrerPolicy="no-referrer-when-downgrade"
            />
          </div>
        </div>

        <div className="mt-12">
          <TatreezBand />
        </div>
      </section>
      <BookCta />
    </>
  );
}
