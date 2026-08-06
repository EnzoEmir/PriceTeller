import Link from "next/link";
import { montarUrl } from "@/lib/filtros";
import type { FiltrosBusca } from "@/types/api";

type Props = {
  filtros: FiltrosBusca;
  page: number;
  totalPages: number;
};

/** Primeira, última, a atual e as vizinhas. O resto vira reticência. */
function janela(atual: number, total: number): Array<number | "..."> {
  const paginas = new Set([1, total, atual - 1, atual, atual + 1]);
  const visiveis = [...paginas].filter((p) => p >= 1 && p <= total).sort((a, b) => a - b);

  return visiveis.flatMap((pagina, indice) => {
    const anterior = visiveis[indice - 1];
    return anterior && pagina - anterior > 1 ? ["..." as const, pagina] : [pagina];
  });
}

export default function Paginacao({ filtros, page, totalPages }: Props) {
  if (totalPages <= 1) return null;

  return (
    <nav
      aria-label="Paginação dos resultados"
      className="mt-12 flex items-center justify-between gap-4 border-t border-rule pt-6"
    >
      {page > 1 ? (
        <Link href={montarUrl(filtros, { page: page - 1 })} rel="prev" className="btn btn-ghost h-10 px-4 text-xs">
          ← Anterior
        </Link>
      ) : (
        <span className="btn h-10 px-4 text-xs" aria-disabled="true">
          ← Anterior
        </span>
      )}

      <ul className="hidden items-center gap-1 sm:flex">
        {janela(page, totalPages).map((item, indice) =>
          item === "..." ? (
            <li key={`salto-${indice}`} className="px-2 text-ink-soft">
              …
            </li>
          ) : (
            <li key={item}>
              <Link
                href={montarUrl(filtros, { page: item })}
                aria-current={item === page ? "page" : undefined}
                className={`flex h-10 min-w-10 items-center justify-center border px-3 font-display text-xs font-semibold tabular-nums transition-colors ${
                  item === page
                    ? "border-ink bg-ink text-paper"
                    : "border-transparent text-ink-soft hover:border-ink hover:text-ink"
                }`}
              >
                {item}
              </Link>
            </li>
          ),
        )}
      </ul>

      <span className="font-display text-xs font-semibold tabular-nums text-ink-soft sm:hidden">
        {page} / {totalPages}
      </span>

      {page < totalPages ? (
        <Link href={montarUrl(filtros, { page: page + 1 })} rel="next" className="btn btn-ghost h-10 px-4 text-xs">
          Próxima →
        </Link>
      ) : (
        <span className="btn h-10 px-4 text-xs" aria-disabled="true">
          Próxima →
        </span>
      )}
    </nav>
  );
}
