import Image from "next/image";
import Link from "next/link";

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
    <footer className="site-footer bg-[#1a1a1a] text-gray-400">
      <div className="container-max py-12">
        <div className="flex flex-col gap-10 md:flex-row md:justify-between">
          <div className="max-w-sm">
            <div className="flex items-center gap-2">
              <Image
                src="/logo-light.png"
                alt="PriceTeller"
                width={32}
                height={32}
                className="object-contain"
              />
              <span className="text-lg font-bold tracking-tight text-white">
                PriceTeller
              </span>
            </div>
            <span className="mt-3 block text-sm text-gray-400">
              Monte a configuração do seu PC e compare os preços das peças em tempo real.
            </span>
          </div>

          <div className="flex gap-12">
            <div>
              <span className="text-sm font-semibold uppercase tracking-wider text-gray-300">
                Navegação
              </span>
              <ul className="mt-3 space-y-2 text-sm">
                <li>
                  <Link href="/">Início</Link>
                </li>
                <li>
                  <Link href="/about">Sobre Nós</Link>
                </li>
              </ul>
            </div>

            <div>
              <span className="text-sm font-semibold uppercase tracking-wider text-gray-300">
                Criadores
              </span>
              <ul className="mt-3 space-y-3 text-sm">
                {criadores.map((criador) => (
                  <li key={criador.nome} className="flex flex-col">
                    <span className="text-gray-300">{criador.nome}</span>
                    <span className="flex gap-2">
                      <a href={criador.github} target="_blank" rel="noopener noreferrer">
                        GitHub
                      </a>
                      <span aria-hidden="true">·</span>
                      <a href={criador.linkedin} target="_blank" rel="noopener noreferrer">
                        LinkedIn
                      </a>
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        <div className="mt-10 flex flex-col gap-3 border-t border-white/10 pt-6 text-sm sm:flex-row sm:items-center sm:justify-between">
          <span>© {new Date().getFullYear()} PriceTeller</span>
          <a href={REPO_URL} target="_blank" rel="noopener noreferrer">
            Ver código no GitHub ↗
          </a>
        </div>
      </div>
    </footer>
  );
}
