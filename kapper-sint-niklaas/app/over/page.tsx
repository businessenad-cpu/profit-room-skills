import type { Metadata } from "next";
import { getContent } from "@/lib/content";
import { StarField, TatreezBand } from "@/components/patterns";
import { BookCta, PhotoPlaceholder } from "@/components/ui";

export const metadata: Metadata = {
  title: "Over mij",
  description:
    "Het verhaal achter Kapper Sint Niklaas: vakmanschap, Palestijnse en Nederlandse roots, en een zaak waar je graag binnenloopt.",
};

export default async function OverPage() {
  const { content } = await getContent();
  return (
    <>
      <section className="relative overflow-hidden">
        <StarField />
        <div className="relative mx-auto grid max-w-6xl gap-10 px-4 py-16 lg:grid-cols-12">
          <div className="lg:col-span-7">
            <p className="arabic text-4xl text-gold" lang="ar">
              أهلاً وسهلاً
            </p>
            <h1 className="display mt-4 text-3xl sm:text-5xl">
              Knippen is m&apos;n vak.
              <br />
              Mensen zijn m&apos;n <span className="text-olive-bright">ding.</span>
            </h1>
            {content.overStory ? (
              <p className="mt-6 max-w-lg whitespace-pre-line text-sand">
                {content.overStory}
              </p>
            ) : (
              /* PLACEHOLDER-copy tot het eigen verhaal via /beheer is ingevuld. */
              <div className="mt-6 max-w-lg space-y-4 text-sand">
                <p>
                  ⚠ <em>Placeholder — dit stuk schrijf je zelf (kan via de
                  Beheer-pagina) of we schrijven het samen:</em>
                </p>
                <p className="border-l-2 border-gold/40 pl-4 text-muted">
                  Wie je bent, hoe je bij het vak kwam, wat je roots voor je
                  betekenen (Palestijns én Nederlands), waarom je in
                  Sint-Niklaas je eigen zaak opende, en wat een klant bij jou
                  mag verwachten. Kort, direct, jij-vorm — zoals de rest van de
                  site.
                </p>
              </div>
            )}
          </div>
          <div className="grid gap-4 lg:col-span-5">
            <PhotoPlaceholder label="Portret — jij in de zaak" className="min-h-[16rem]" />
            <PhotoPlaceholder label="Actie — jij aan het werk" className="min-h-[10rem]" />
          </div>
        </div>
      </section>

      <div className="mx-auto max-w-6xl px-4">
        <TatreezBand />
      </div>

      <section className="mx-auto max-w-6xl px-4 py-16">
        <h2 className="display text-2xl text-olive-bright sm:text-3xl">
          Waar ik voor sta
        </h2>
        <div className="mt-8 grid gap-px border border-gold/20 bg-gold/20 sm:grid-cols-3">
          {[
            {
              t: "Strak werk",
              d: "Een fade is pas af als de lineup klopt. Ik werk door tot het goed zit.",
            },
            {
              t: "Geen haast, geen wachtrij",
              d: "Op afspraak. Jouw stoel, jouw moment — niet nummer 14 in de rij.",
            },
            {
              t: "Binnenkomen is thuiskomen",
              d: "Goeie muziek, goei babbel. Je komt voor de cut, je blijft voor de sfeer.",
            },
          ].map((v) => (
            <div key={v.t} className="bg-surface p-6">
              <h3 className="display text-base">{v.t}</h3>
              <p className="mt-2 text-sm text-sand">{v.d}</p>
            </div>
          ))}
        </div>
      </section>

      <BookCta title="Kom eens langs." />
    </>
  );
}
