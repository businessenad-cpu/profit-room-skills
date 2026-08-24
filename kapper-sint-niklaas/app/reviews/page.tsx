import type { Metadata } from "next";
import { getContent } from "@/lib/content";
import { TatreezBand } from "@/components/patterns";
import { BookCta } from "@/components/ui";

export const metadata: Metadata = {
  title: "Reviews",
  description:
    "Wat klanten zeggen over Kapper Sint Niklaas. Nieuw geopend — jouw review helpt de zaak groeien.",
};

export default async function ReviewsPage() {
  const { content } = await getContent();
  return (
    <>
      <section className="mx-auto max-w-6xl px-4 py-16">
        <h1 className="display text-3xl sm:text-5xl">
          Wat klanten <span className="text-olive-bright">zeggen</span>
        </h1>

        {/* Geen verzonnen reviews (DESIGN.md): eerlijke "nieuw geopend"-sectie
            tot er echte Google-reviews zijn. */}
        <div className="mt-10 border border-gold/20 bg-surface p-8 sm:p-12">
          <p className="display text-xl text-olive-bright sm:text-2xl">
            Nieuw geopend. Eerlijk verhaal.
          </p>
          <p className="mt-4 max-w-lg text-sand">
            Deze zaak is net gestart, dus hier staan nog geen reviews — en we
            gaan er zeker geen verzinnen. Ben je langsgeweest? Jouw eerlijke
            review op Google helpt enorm.
          </p>
          <div className="mt-6">
            {content.googleBusinessReviewUrl ? (
              <a
                href={content.googleBusinessReviewUrl}
                rel="noopener"
                className="display inline-block rounded-[4px] bg-olive px-6 py-3 text-sm text-ink transition-colors hover:bg-olive-bright"
              >
                Schrijf een Google-review
              </a>
            ) : (
              <p className="inline-block border border-dashed border-gold/40 px-4 py-2 text-xs text-muted">
                ⚠ Google Business-profiel wordt aangemaakt — de reviewlink
                verschijnt hier zodra die er is.
              </p>
            )}
          </div>
        </div>

        <div className="mt-12">
          <TatreezBand />
        </div>

        <p className="mt-8 text-sm text-muted">
          Zodra de eerste Google-reviews binnen zijn, tonen we ze hier — echte
          woorden van echte klanten, met bron.
        </p>
      </section>
      <BookCta title="Word de eerste review." />
    </>
  );
}
