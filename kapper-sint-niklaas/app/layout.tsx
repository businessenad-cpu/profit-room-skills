import type { Metadata } from "next";
import { Archivo, Inter, Amiri } from "next/font/google";
import Script from "next/script";
import { Analytics } from "@vercel/analytics/next";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { StickyCta } from "@/components/ui";
import { site } from "@/lib/site";
import "./globals.css";

const archivo = Archivo({
  subsets: ["latin"],
  axes: ["wdth"],
  variable: "--font-archivo",
});
const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const amiri = Amiri({
  subsets: ["arabic"],
  weight: ["400", "700"],
  variable: "--font-amiri",
});

export const metadata: Metadata = {
  metadataBase: new URL(site.url),
  title: {
    default: "Kapper Sint-Niklaas — boek online | fades, lineups & baard",
    template: "%s | Kapper Sint Niklaas",
  },
  description:
    "Kapper in hartje Sint-Niklaas (Ankerstraat 61B). Fades, lineups, baard. Kom binnen, ga fresh naar buiten. Boek je cut online.",
  openGraph: {
    type: "website",
    locale: "nl_BE",
    siteName: site.name,
    url: site.url,
  },
  robots: { index: true, follow: true },
};

function JsonLd() {
  const data = {
    "@context": "https://schema.org",
    "@type": ["HairSalon", "LocalBusiness"],
    name: site.name,
    legalName: site.legalName,
    url: site.url,
    image: `${site.url}/opengraph-image`,
    address: {
      "@type": "PostalAddress",
      streetAddress: site.address.street,
      postalCode: site.address.postalCode,
      addressLocality: site.address.city,
      addressCountry: site.address.country,
    },
    geo: {
      "@type": "GeoCoordinates",
      latitude: site.geo.lat,
      longitude: site.geo.lng,
    },
    ...(site.phone ? { telephone: site.phone } : {}),
    priceRange: "€€",
    currenciesAccepted: "EUR",
  };
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const gaId = process.env.NEXT_PUBLIC_GA_ID;
  return (
    <html lang="nl-BE" className="dark">
      <body
        className={`${archivo.variable} ${inter.variable} ${amiri.variable} pb-16 md:pb-0`}
      >
        <Header />
        <main>{children}</main>
        <Footer />
        <StickyCta />
        <JsonLd />
        <Analytics />
        {gaId && (
          <>
            <Script
              src={`https://www.googletagmanager.com/gtag/js?id=${gaId}`}
              strategy="afterInteractive"
            />
            <Script id="ga4" strategy="afterInteractive">
              {`window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','${gaId}');`}
            </Script>
          </>
        )}
      </body>
    </html>
  );
}
