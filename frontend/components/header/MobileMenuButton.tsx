"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { headerLinks } from "./links";
import { estaAtivo } from "./DesktopNav";

export default function MobileMenuButton() {
  const [aberto, setAberto] = useState(false);
  const pathname = usePathname();

  return (
    <div className="md:hidden">
      <button
        type="button"
        aria-expanded={aberto}
        aria-controls="menu-mobile"
        aria-label={aberto ? "Fechar menu" : "Abrir menu"}
        onClick={() => setAberto(!aberto)}
        className="flex h-10 w-10 items-center justify-center border border-ink text-ink"
      >
        <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="2">
          {aberto ? (
            <path d="M3 3l12 12M15 3L3 15" />
          ) : (
            <path d="M2 5h14M2 13h14" />
          )}
        </svg>
      </button>

      {aberto && (
        <div id="menu-mobile" className="absolute left-0 top-16 w-full border-b border-ink bg-accent">
          <nav className="container-max flex flex-col py-2">
            {headerLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setAberto(false)}
                aria-current={estaAtivo(pathname, link.href) ? "page" : undefined}
                className="border-b border-ink/15 py-3 font-display text-sm font-semibold tracking-tight text-ink last:border-b-0"
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </div>
      )}
    </div>
  );
}
