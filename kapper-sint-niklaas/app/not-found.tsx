import Link from "next/link";

export default function NotFound() {
  return (
    <section className="mx-auto max-w-6xl px-4 py-24 text-center">
      <p className="display text-6xl text-olive-bright">404</p>
      <h1 className="display mt-4 text-2xl sm:text-4xl">
        Deze pagina heeft een slechte haardag.
      </h1>
      <p className="mt-4 text-sand">
        Geen stress — een fresh start is zo geregeld.
      </p>
      <Link
        href="/"
        className="display mt-8 inline-block rounded-[4px] bg-olive px-6 py-3 text-sm text-ink transition-colors hover:bg-olive-bright"
      >
        Terug naar home
      </Link>
    </section>
  );
}
