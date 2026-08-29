import type { Metadata, Viewport } from "next";
import Link from "next/link";
import "./globals.css";
import { SALON } from "@/lib/data";

export const metadata: Metadata = {
  title: `${SALON.name} — online afspraak maken`,
  description:
    "Boek je knipbeurt online bij Kapper Sint Niklaas. Powered by Knipklok.",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#0a0a0b",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="nl">
      <body className="min-h-screen">
        <div className="bg-gold-500 text-ink-950 text-center text-xs font-semibold px-3 py-1.5">
          Knipklok demo — jouw salon, jouw klanten, 0% commissie
        </div>
        <header className="border-b border-ink-700 bg-ink-900/80 backdrop-blur sticky top-0 z-10">
          <div className="max-w-3xl mx-auto flex items-center justify-between px-4 py-3">
            <Link href="/" className="flex items-center gap-2">
              <span className="text-xl">✂️</span>
              <span className="font-bold tracking-tight text-lg">
                {SALON.name}
              </span>
            </Link>
            <Link
              href="/admin"
              className="text-xs text-zinc-400 hover:text-gold-400 transition-colors"
            >
              Admin
            </Link>
          </div>
        </header>
        <main className="max-w-3xl mx-auto px-4 py-6 pb-24">{children}</main>
        <footer className="border-t border-ink-700 py-6 text-center text-xs text-zinc-500">
          Powered by <span className="text-gold-400 font-semibold">Knipklok</span>
        </footer>
      </body>
    </html>
  );
}
