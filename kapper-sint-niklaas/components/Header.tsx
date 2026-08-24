"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

const nav = [
  { href: "/", label: "Home" },
  { href: "/prijzen", label: "Cuts & prijzen" },
  { href: "/werk", label: "Werk" },
  { href: "/over", label: "Over mij" },
  { href: "/reviews", label: "Reviews" },
  { href: "/contact", label: "Contact" },
];

export function Header() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-gold/20 bg-ink/90 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3">
        <Link
          href="/"
          className="display text-sm leading-none sm:text-base"
          onClick={() => setOpen(false)}
        >
          Kapper
          <span className="text-olive-bright"> Sint&nbsp;Niklaas</span>
        </Link>

        <nav className="hidden items-center gap-5 text-sm text-sand md:flex">
          {nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={
                pathname === item.href
                  ? "text-olive-bright"
                  : "transition-colors hover:text-bone"
              }
            >
              {item.label}
            </Link>
          ))}
          <Link
            href="/boeken"
            className="display rounded-[4px] bg-olive px-4 py-2 text-xs text-ink transition-colors hover:bg-olive-bright"
          >
            Boek nu
          </Link>
        </nav>

        <button
          type="button"
          className="display rounded-[4px] border border-gold/30 px-3 py-2 text-xs md:hidden"
          aria-expanded={open}
          aria-controls="mobile-nav"
          onClick={() => setOpen((v) => !v)}
        >
          {open ? "Sluit" : "Menu"}
        </button>
      </div>

      {open && (
        <nav
          id="mobile-nav"
          className="border-t border-gold/20 bg-surface px-4 py-4 md:hidden"
        >
          <ul className="grid gap-3 text-lg">
            {nav.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={
                    pathname === item.href ? "text-olive-bright" : "text-bone"
                  }
                  onClick={() => setOpen(false)}
                >
                  {item.label}
                </Link>
              </li>
            ))}
            <li>
              <Link
                href="/boeken"
                className="display mt-2 block rounded-[4px] bg-olive px-4 py-3 text-center text-sm text-ink"
                onClick={() => setOpen(false)}
              >
                Boek nu
              </Link>
            </li>
          </ul>
        </nav>
      )}
    </header>
  );
}
