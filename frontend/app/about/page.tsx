import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Sobre Nós",
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
      <section className="section">
        <div className="container-max flex flex-col items-center text-center">
          <div className="mx-auto max-w-3xl">
            <h1>Sobre Nós</h1>
            <p className="mt-4 text-lg text-gray-600">
              O PriceTeller é uma ferramenta para montar configurações de PC e comparar os
              preços das peças em tempo real. Ele reúne num só lugar o preço de componentes como
              processador, placa de vídeo, memória e fonte de diferentes lojas, pra você montar
              seu setup e ver o custo total. No futuro, também vai avisar sobre incompatibilidades
              entre as peças.
            </p>
          </div>
        </div>
      </section>

      <section className="section-light">
        <div className="container-max flex flex-col items-center text-center">
          <h2>Quem faz o PriceTeller</h2>
          <div className="mt-8 grid w-full max-w-2xl gap-6 sm:grid-cols-2">
            {criadores.map((criador) => (
              <div key={criador.nome} className="card flex flex-col items-center text-center">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={`${criador.github}.png?size=200`}
                  alt={criador.nome}
                  width={96}
                  height={96}
                  loading="lazy"
                  className="h-24 w-24 rounded-full object-cover"
                />
                <span className="mt-4 font-display text-lg font-bold tracking-tight text-gray-900">
                  {criador.nome}
                </span>
                <span className="mt-2 flex items-center gap-2 text-sm">
                  <a href={criador.github} target="_blank" rel="noopener noreferrer">
                    GitHub
                  </a>
                  <span aria-hidden="true" className="text-gray-300">·</span>
                  <a href={criador.linkedin} target="_blank" rel="noopener noreferrer">
                    LinkedIn
                  </a>
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container-max flex flex-col items-center text-center">
          <h2>Stack técnica</h2>
          <div className="mt-8 grid w-full gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {stack.map((item) => (
              <div key={item.grupo} className="card flex flex-col items-center">
                <span className="font-display text-sm font-semibold uppercase tracking-wider text-gray-500">
                  {item.grupo}
                </span>
                <ul className="mt-3 flex flex-wrap justify-center gap-2">
                  {item.itens.map((tecnologia) => (
                    <li key={tecnologia} className="badge">
                      {tecnologia}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}