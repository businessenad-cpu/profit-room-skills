import type { Metadata } from "next";
import { getContent } from "@/lib/content";
import { TatreezBand } from "@/components/patterns";
import { BookCta } from "@/components/ui";
import { Gallery } from "@/components/Gallery";

export const metadata: Metadata = {
  title: "Werk — fades, lineups & baard",
  description:
    "Bekijk het werk van Kapper Sint Niklaas: skin fades, lineups, baard en meer. Volg mij op Instagram en TikTok voor het nieuwste werk.",
};

export default async function WerkPage() {
  const { content } = await getContent();
  return (
    <>
      <section className="mx-auto max-w-6xl px-4 py-16">
        <h1 className="display text-3xl sm:text-5xl">
          Dit is m&apos;n <span className="text-olive-bright">werk</span>
        </h1>
        <p className="mt-4 max-w-md text-sand">
          Beste cuts eerst. Voor het allernieuwste werk: check m&apos;n socials
          hieronder.
        </p>
        <div className="mt-10">
          <Gallery />
        </div>
      </section>

      <div className="mx-auto max-w-6xl px-4">
        <TatreezBand />
      </div>

      {/* Officiële embeds — verschijnen zodra handles ingevuld zijn in lib/site.ts */}
      <section className="mx-auto max-w-6xl px-4 py-16">
        <h2 className="display text-2xl text-olive-bright sm:text-3xl">
          Vers van m&apos;n feed
        </h2>
        <div className="mt-8 grid gap-6 md:grid-cols-2">
          <div className="border border-gold/20 bg-surface p-6">
            <h3 className="display text-base">Instagram</h3>
            {content.instagram ? (
              <blockquote
                className="instagram-media mt-4"
                data-instgrm-permalink={`https://www.instagram.com/${content.instagram}/`}
                data-instgrm-version="14"
              >
                <a href={`https://www.instagram.com/${content.instagram}/`} rel="noopener">
                  @{content.instagram} op Instagram
                </a>
                {/* Officieel embed-script laadt client-side */}
                <script async src="https://www.instagram.com/embed.js" />
              </blockquote>
            ) : (
              <p className="mt-4 border border-dashed border-gold/40 p-4 text-sm text-muted">
                ⚠ Instagram-handle nog niet aangeleverd. Zodra ingevuld in{" "}
                <code>lib/site.ts</code> verschijnt hier de officiële
                Instagram-embed (geen scraping).
              </p>
            )}
          </div>
          <div className="border border-gold/20 bg-surface p-6">
            <h3 className="display text-base">TikTok</h3>
            {content.tiktok ? (
              <blockquote
                className="tiktok-embed mt-4"
                cite={`https://www.tiktok.com/@${content.tiktok}`}
                data-unique-id={content.tiktok}
                data-embed-type="creator"
              >
                <a href={`https://www.tiktok.com/@${content.tiktok}`} rel="noopener">
                  @{content.tiktok} op TikTok
                </a>
                <script async src="https://www.tiktok.com/embed.js" />
              </blockquote>
            ) : (
              <p className="mt-4 border border-dashed border-gold/40 p-4 text-sm text-muted">
                ⚠ TikTok-handle nog niet aangeleverd. Zodra ingevuld in{" "}
                <code>lib/site.ts</code> verschijnt hier de officiële
                TikTok-creator-embed.
              </p>
            )}
          </div>
        </div>
      </section>

      <BookCta title="Wil je er ook zo bijlopen?" />
    </>
  );
}
