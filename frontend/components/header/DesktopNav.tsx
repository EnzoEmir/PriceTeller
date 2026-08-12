"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { headerLinks } from "./links";

export function estaAtivo(pathname: string, href: string): boolean {
  return href === "/" ? pathname === "/" : pathname.startsWith(href);
}

export default function DesktopNav() {
  const pathname = usePathname();

  return (
    <nav className="hidden items-center gap-8 md:flex">
      {headerLinks.map((link) => {
        const ativo = estaAtivo(pathname, link.href);

        return (
          <Link
            key={link.href}
            href={link.href}
            aria-current={ativo ? "page" : undefined}
            className={`border-b-2 py-1 font-display text-sm font-semibold tracking-tight text-ink transition-colors ${
              ativo ? "border-ink" : "border-transparent hover:border-ink/30"
            }`}
          >
            {link.label}
          </Link>
        );
      })}
    </nav>
  );
}
