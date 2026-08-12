import Image from "next/image";
import Link from "next/link";
import { headerLinks } from "@/components/header/links";

const REPO_URL = "https://github.com/EnzoEmir/PriceTeller";

const criadores = [
  {
    nome: "Enzo Emir",
    github: "https://github.com/EnzoEmir",
    linkedin: "https://www.linkedin.com/in/enzoemir",
  },
  {
    nome: "Caio Venâncio",
    github: "https://github.com/caio-venancio",
    linkedin: "https://www.linkedin.com/in/caio-venâncio-do-rosário-2725492a2/",
  },
];

export default function Footer() {
  return (
    <footer className="border-t border-ink bg-paper-alt">
      <div className="container-max py-14">
        <div className="grid gap-12 md:grid-cols-[1.4fr_1fr_1fr]">
          <div>
            <div className="flex items-center gap-2">
              <Image src="/logo.png" alt="" width={28} height={28} className="object-contain" />
              <span className="font-display text-lg font-bold tracking-tight">PriceTeller</span>
            </div>
            <p className="mt-4 max-w-xs text-sm">
              Monte a configuração do seu PC e compare os preços das peças entre lojas.
            </p>
          </div>

          <div>
            <span className="kicker">Navegação</span>
            <ul className="mt-4 space-y-2 text-sm">
              {headerLinks.map((link) => (
                <li key={link.href}>
                  <Link href={link.href} className="link-sublinhado text-ink-soft hover:text-ink">
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <span className="kicker">Criadores</span>
            <ul className="mt-4 space-y-3 text-sm">
              {criadores.map((criador) => (
                <li key={criador.nome}>
                  <span className="block font-display font-semibold tracking-tight">
                    {criador.nome}
                  </span>
                  <span className="mt-1 flex gap-3 text-ink-soft">
                    <a
                      href={criador.github}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="link-sublinhado hover:text-ink"
                    >
                      GitHub
                    </a>
                    <a
                      href={criador.linkedin}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="link-sublinhado hover:text-ink"
                    >
                      LinkedIn
                    </a>
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-12 flex flex-col gap-3 border-t border-rule pt-6 text-sm text-ink-soft sm:flex-row sm:items-center sm:justify-between">
          <span>© {new Date().getFullYear()} PriceTeller</span>
          <a
            href={REPO_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="link-sublinhado hover:text-ink"
          >
            Ver código no GitHub ↗
          </a>
        </div>
      </div>
    </footer>
  );
}
