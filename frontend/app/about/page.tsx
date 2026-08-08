import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Sobre Nós",
  description: "Quem faz o PriceTeller e com que tecnologia ele é construído.",
};

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

const stack = [
  { grupo: "Frontend", itens: ["Next.js 16", "React 19", "TypeScript", "Tailwind CSS v4"] },
  { grupo: "Backend", itens: ["FastAPI", "SQLModel", "SQLAlchemy", "Pydantic"] },
  { grupo: "Banco de dados", itens: ["SQLite (dev)", "PostgreSQL (planejado)"] },
  { grupo: "Fontes de dados", itens: ["Lomadee", "Mercado Livre"] },
];

export default function SobreNos() {
  return (
    <main>
      <header className="border-b border-rule">
        <div className="container-max py-20 md:py-28">
          <span className="kicker">Sobre</span>
          <h1 className="mt-4 max-w-3xl">O PriceTeller.</h1>
          <p className="mt-6 max-w-2xl text-lg">
            O PriceTeller reúne num só lugar o preço de processador, placa de vídeo, memória e
            fonte em lojas diferentes, pra você montar seu setup e ver o custo total. No futuro
            também vai avisar sobre incompatibilidade entre as peças.
          </p>
        </div>
      </header>

      <section className="section-alt">
        <div className="container-max">
          <span className="kicker">Quem faz</span>

          <div className="mt-8 grid gap-px border border-rule bg-rule sm:grid-cols-2">
            {criadores.map((criador) => (
              <article key={criador.nome} className="flex items-center gap-5 bg-paper p-7">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={`${criador.github}.png?size=160`}
                  alt=""
                  width={72}
                  height={72}
                  loading="lazy"
                  className="h-18 w-18 shrink-0 border border-rule"
                />
                <div>
                  <span className="block font-display text-lg font-bold tracking-tight">
                    {criador.nome}
                  </span>
                  <span className="mt-2 flex gap-4 text-sm text-ink-soft">
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
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container-max">
          <span className="kicker">Stack</span>

          <dl className="mt-8 border-t border-ink">
            {stack.map((item) => (
              <div
                key={item.grupo}
                className="flex flex-col gap-3 border-b border-rule py-5 sm:flex-row sm:items-baseline sm:gap-10"
              >
                <dt className="w-44 shrink-0 font-display text-sm font-semibold tracking-tight">
                  {item.grupo}
                </dt>
                <dd className="flex flex-wrap gap-2">
                  {item.itens.map((tecnologia) => (
                    <span key={tecnologia} className="badge bg-paper">
                      {tecnologia}
                    </span>
                  ))}
                </dd>
              </div>
            ))}
          </dl>
        </div>
      </section>
    </main>
  );
}
