import Link from "next/link";
import { listarCategorias } from "@/services/api";
import { montarUrl } from "@/lib/filtros";

/** Sem a API de pé o bloco vira uma lista estática, e a home continua de pé. */
const FALLBACK = ["Processador", "Placa de Vídeo", "Placa-Mãe", "Memória RAM", "Fonte"];

export default async function CtaSection() {
  const resposta = await listarCategorias();
  const categorias = resposta.ok
    ? resposta.dados
    : FALLBACK.map((nome, indice) => ({ id: -indice, nome }));

  return (
    <section className="bg-ink py-20 text-paper md:py-28">
      <div className="container-max">
        <div className="grid gap-12 lg:grid-cols-2 lg:items-end">
          <div>
            <span className="kicker text-paper/60">Comece agora</span>
            <h2 className="mt-4 text-paper">Escolha a primeira peça.</h2>
            <p className="mt-5 max-w-md text-paper/70">
              O catálogo é curado à mão, peça por peça, com as specs que a checagem de
              compatibilidade vai usar depois.
            </p>
            <Link href="/pecas" className="btn btn-accent mt-8">
              Buscar peças
            </Link>
          </div>

          <ul className="grid gap-px border border-paper/20 bg-paper/20 sm:grid-cols-2">
            {categorias.map((categoria) => (
              <li key={categoria.nome} className="bg-ink">
                <Link
                  href={
                    resposta.ok
                      ? montarUrl({}, { categoria_id: categoria.id })
                      : "/pecas"
                  }
                  className="flex items-center justify-between px-5 py-4 font-display text-sm font-semibold tracking-tight text-paper/80 transition-colors hover:text-accent"
                >
                  {categoria.nome}
                  <span aria-hidden="true">→</span>
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
