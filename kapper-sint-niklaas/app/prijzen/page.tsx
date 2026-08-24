import type { Metadata } from "next";
import Link from "next/link";
import { serviceCategories } from "@/lib/site";
import { getContent } from "@/lib/content";
import { TatreezBand } from "@/components/patterns";
import { BookCta } from "@/components/ui";

export const metadata: Metadata = {
  title: "Cuts & prijzen",
  description:
    "Fades, lineups, baard en meer bij Kapper Sint Niklaas. Wat je ziet is wat je betaalt — boek je cut online.",
};

export default async function PrijzenPage() {
  const { services } = await getContent();
  const hasMissingPrices = services.some((s) => s.price === null);

  return (
    <>
      <section className="mx-auto max-w-6xl px-4 py-16">
        <h1 className="display text-3xl sm:text-5xl">
          Prijzen. Geen <span className="text-olive-bright">verrassingen.</span>
        </h1>
        <p className="mt-4 max-w-md text-sand">
          Wat je ziet is wat je betaalt. Twijfel je wat je nodig hebt? Stuur
          een appje, dan denken we mee.
        </p>

        {hasMissingPrices && (
          <p className="mt-6 inline-block border border-dashed border-gold/40 bg-surface px-4 py-2 text-xs text-muted">
            ⚠ Prijslijst in opbouw — definitieve prijzen worden binnenkort
            aangevuld door de zaak. Niets hieronder is verzonnen.
          </p>
        )}

        {serviceCategories.map((cat) => {
          const items = services.filter((s) => s.category === cat.key);
          if (items.length === 0)
            return (
              <div key={cat.key} className="mt-12">
                <h2 className="display text-xl text-olive-bright">{cat.label}</h2>
                <p className="mt-3 text-sm text-muted">
                  Aanbod volgt — vraag ernaar via WhatsApp.
                </p>
              </div>
            );
          return (
            <div key={cat.key} className="mt-12">
              <h2 className="display text-xl text-olive-bright">{cat.label}</h2>
              <ul className="mt-4 grid gap-px border border-gold/20 bg-gold/20">
                {items.map((s) => (
                  <li
                    key={s.slug}
                    className="flex flex-wrap items-center justify-between gap-2 bg-surface px-5 py-4"
                  >
                    <div>
                      <h3 className="display text-base">{s.name}</h3>
                      <p className="mt-1 text-sm text-sand">{s.description}</p>
                    </div>
                    <div className="flex items-center gap-4">
                      <span className="tabular text-sm text-muted">
                        {s.durationMin ? `${s.durationMin} min` : ""}
                      </span>
                      <span className="tabular display text-base text-bone">
                        {s.price === null ? "€ —" : `€ ${s.price}`}
                      </span>
                      <Link
                        href="/boeken"
                        className="display rounded-[4px] bg-olive px-3 py-2 text-xs text-ink transition-colors hover:bg-olive-bright"
                      >
                        Boek
                      </Link>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          );
        })}

        <div className="mt-12">
          <TatreezBand />
        </div>
      </section>
      <BookCta title="Gezien wat je zocht?" />
    </>
  );
}
