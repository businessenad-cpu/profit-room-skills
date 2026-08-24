import Link from "next/link";
import { site } from "@/lib/site";

/** Sticky "Boek nu"-balk onderaan op mobiel — altijd zichtbaar. */
export function StickyCta() {
  return (
    <div className="fixed inset-x-0 bottom-0 z-50 border-t border-gold/20 bg-ink/95 p-3 pb-[calc(0.75rem+env(safe-area-inset-bottom))] backdrop-blur md:hidden">
      <Link
        href="/boeken"
        className="display block rounded-[4px] bg-olive px-4 py-3 text-center text-sm text-ink"
      >
        Boek nu · {site.address.street}
      </Link>
    </div>
  );
}

/** Trage marquee: "Fresh voor het weekend". */
export function Marquee() {
  const items = [
    "Fresh voor het weekend",
    "Vr & za ruime uren",
    "Ankerstraat 61B, Sint-Niklaas",
    "Fades · Lineups · Baard",
  ];
  const row = items.map((t, i) => (
    <span key={i} className="mx-6 inline-flex items-center gap-6">
      {t} <span aria-hidden className="text-gold">{"✂︎"}</span>
    </span>
  ));
  return (
    <div
      className="display overflow-hidden border-y border-gold/20 bg-surface py-3 text-sm text-sand"
      aria-label={items.join(" · ")}
    >
      <div className="marquee-track flex w-max whitespace-nowrap" aria-hidden>
        <span>{row}</span>
        <span>{row}</span>
      </div>
    </div>
  );
}

/** Duidelijk gemarkeerde foto-placeholder tot eigen beeld is aangeleverd. */
export function PhotoPlaceholder({
  label,
  className = "",
}: {
  label: string;
  className?: string;
}) {
  return (
    <div
      className={`flex items-center justify-center border border-dashed border-gold/40 bg-surface-2 ${className}`}
    >
      <p className="max-w-[16rem] p-4 text-center text-xs text-muted">
        📷 Jouw foto hier
        <br />
        <span className="text-sand">{label}</span>
      </p>
    </div>
  );
}

/** Grote afsluitende call-to-action onder elke pagina. */
export function BookCta({
  title = "Klaar voor een fresh cut?",
}: {
  title?: string;
}) {
  return (
    <section className="mx-auto max-w-6xl px-4 py-16 text-center">
      <h2 className="display text-3xl sm:text-5xl">{title}</h2>
      <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
        <Link
          href="/boeken"
          className="display rounded-[4px] bg-olive px-6 py-3 text-sm text-ink transition-colors hover:bg-olive-bright"
        >
          Boek je cut
        </Link>
        {site.whatsapp ? (
          <a
            href={`https://wa.me/${site.whatsapp}`}
            rel="noopener"
            className="display rounded-[4px] border border-gold/40 px-6 py-3 text-sm text-sand transition-colors hover:border-olive-bright hover:text-bone"
          >
            Stuur een appje
          </a>
        ) : (
          <Link
            href="/contact"
            className="display rounded-[4px] border border-gold/40 px-6 py-3 text-sm text-sand transition-colors hover:border-olive-bright hover:text-bone"
          >
            Contact
          </Link>
        )}
      </div>
    </section>
  );
}
