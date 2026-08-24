import Link from "next/link";
import { site } from "@/lib/site";
import { StarField, TatreezBand } from "@/components/patterns";

export function Footer() {
  return (
    <footer className="relative mt-20 overflow-hidden border-t border-gold/20 bg-surface">
      <StarField />
      <div className="relative mx-auto max-w-6xl px-4 py-12">
        <p className="arabic text-4xl text-gold" lang="ar">
          أهلاً
        </p>
        <p className="mt-2 max-w-md text-sand">
          Welkom. {site.tagline}
        </p>

        <div className="mt-8 grid gap-8 sm:grid-cols-3">
          <div>
            <h2 className="display text-sm text-olive-bright">Adres</h2>
            <p className="mt-2 text-sm text-sand">
              {site.address.street}
              <br />
              {site.address.postalCode} {site.address.city}
            </p>
          </div>
          <div>
            <h2 className="display text-sm text-olive-bright">Snel naar</h2>
            <ul className="mt-2 grid gap-1 text-sm text-sand">
              <li><Link href="/boeken" className="hover:text-bone">Boek je cut</Link></li>
              <li><Link href="/prijzen" className="hover:text-bone">Cuts & prijzen</Link></li>
              <li><Link href="/contact" className="hover:text-bone">Contact & route</Link></li>
            </ul>
          </div>
          <div>
            <h2 className="display text-sm text-olive-bright">Volg mij</h2>
            <ul className="mt-2 grid gap-1 text-sm text-sand">
              <li>
                {site.instagram ? (
                  <a href={`https://www.instagram.com/${site.instagram}/`} rel="noopener" className="hover:text-bone">Instagram</a>
                ) : (
                  <span className="text-muted">Instagram — handle volgt</span>
                )}
              </li>
              <li>
                {site.tiktok ? (
                  <a href={`https://www.tiktok.com/@${site.tiktok}`} rel="noopener" className="hover:text-bone">TikTok</a>
                ) : (
                  <span className="text-muted">TikTok — handle volgt</span>
                )}
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-10">
          <TatreezBand />
        </div>
        <p className="mt-4 text-xs text-muted">
          © {new Date().getFullYear()} {site.legalName} · BTW {site.vat} ·{" "}
          {site.address.street}, {site.address.postalCode} {site.address.city}
        </p>
      </div>
    </footer>
  );
}
