import Link from "next/link";
import { site } from "@/lib/site";
import { getContent } from "@/lib/content";
import { Accent } from "@/components/Accent";
import { HeroGeo, StarField, TatreezBand } from "@/components/patterns";
import { BookCta, Marquee } from "@/components/ui";
import { Gallery } from "@/components/Gallery";

export default async function Home() {
  const { content, services } = await getContent();
  const topServices = services.filter((s) =>
    ["skin-fade", "cut-baard", "lineup"].includes(s.slug),
  );

  return (
    <>
      {/* ── Hero ─────────────────────────────────────────────────────── */}
      <section className="relative overflow-hidden border-b border-gold/20">
        <StarField />
        <HeroGeo />
        {/* Placeholder voor video-loop: langzaam bewegende gradient (DESIGN.md §6) */}
        <div
          aria-hidden
          className="hero-shift pointer-events-none absolute inset-0 opacity-40"
          style={{
            background:
              "radial-gradient(60% 80% at 70% 30%, #3e4722 0%, transparent 70%)",
          }}
        />
        <div className="relative mx-auto grid max-w-6xl gap-10 px-4 py-20 sm:py-28 lg:grid-cols-12">
          <div className="lg:col-span-7">
            <p className="arabic text-5xl text-gold sm:text-6xl" lang="ar">
              أهلاً
            </p>
            <h1 className="display mt-4 text-4xl sm:text-6xl lg:text-7xl">
              <Accent text={content.heroTitle} />
            </h1>
            <p className="mt-5 max-w-md text-lg text-sand">
              {content.heroSub} {site.address.street}, {site.address.city}.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link
                href="/boeken"
                className="display rounded-[4px] bg-olive px-6 py-3 text-sm text-ink transition-colors hover:bg-olive-bright"
              >
                Boek je cut
              </Link>
              <Link
                href="/werk"
                className="display rounded-[4px] border border-gold/40 px-6 py-3 text-sm text-sand transition-colors hover:border-olive-bright hover:text-bone"
              >
                Check m&apos;n werk
              </Link>
            </div>
          </div>
          <div className="relative min-h-[16rem] lg:col-span-5">
            <div className="flex h-full items-center justify-center border border-dashed border-gold/40 bg-surface/60">
              <p className="max-w-[18rem] p-4 text-center text-xs text-muted">
                🎬 Hier komt jouw video-loop
                <br />
                <span className="text-sand">
                  10–20 sec knippen of eindresultaat (mag een Reel zijn)
                </span>
              </p>
            </div>
          </div>
        </div>
      </section>

      <Marquee items={content.marquee} />

      {/* ── Top-diensten ─────────────────────────────────────────────── */}
      <section className="mx-auto max-w-6xl px-4 py-16">
        <h2 className="display text-2xl text-olive-bright sm:text-4xl">
          Waarvoor kom je?
        </h2>
        <div className="mt-8 grid gap-px border border-gold/20 bg-gold/20 sm:grid-cols-3">
          {topServices.map((s) => (
            <Link
              key={s.slug}
              href="/prijzen"
              className="group bg-surface p-6 transition-colors hover:bg-surface-2"
            >
              <h3 className="display text-lg group-hover:text-olive-bright">
                {s.name}
              </h3>
              <p className="mt-2 text-sm text-sand">{s.description}</p>
              <p className="tabular mt-4 text-sm text-muted">
                {s.durationMin} min ·{" "}
                {s.price === null ? "prijs volgt" : `€ ${s.price}`}
              </p>
            </Link>
          ))}
        </div>
        <Link
          href="/prijzen"
          className="mt-4 inline-block text-sm text-olive-bright hover:text-bone"
        >
          Alle cuts & prijzen →
        </Link>
      </section>

      <TatreezBand className="mx-auto max-w-6xl px-4" />

      {/* ── Fresh voor het weekend ───────────────────────────────────── */}
      <section className="mx-auto grid max-w-6xl gap-8 px-4 py-16 lg:grid-cols-12">
        <div className="lg:col-span-5">
          <h2 className="display text-2xl sm:text-4xl">
            Fresh voor het <span className="text-olive-bright">weekend</span>
          </h2>
          <p className="mt-4 whitespace-pre-line text-sand">
            {content.weekendText}
          </p>
          <Link
            href="/boeken"
            className="display mt-6 inline-block rounded-[4px] bg-olive px-6 py-3 text-sm text-ink transition-colors hover:bg-olive-bright"
          >
            Plan je weekend-cut
          </Link>
        </div>
        <div className="lg:col-span-7">
          <ul className="grid gap-px border border-gold/20 bg-gold/20">
            {content.hours
              .filter((h) => ["Vrijdag", "Zaterdag"].includes(h.day))
              .map((h) => (
                <li
                  key={h.day}
                  className="flex items-center justify-between bg-surface px-5 py-4"
                >
                  <span className="display text-sm">{h.day}</span>
                  <span className="tabular text-sm text-olive-bright">
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
      </section>

      {/* ── Galerij-teaser ───────────────────────────────────────────── */}
      <section className="mx-auto max-w-6xl px-4 py-8">
        <div className="mb-6 flex items-end justify-between">
          <h2 className="display text-2xl sm:text-4xl">Dit is m&apos;n werk</h2>
          <Link href="/werk" className="text-sm text-olive-bright hover:text-bone">
            Alles zien →
          </Link>
        </div>
        <Gallery limit={4} />
      </section>

      <BookCta />
    </>
  );
}
