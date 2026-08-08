import Link from "next/link";
import { montarUrl } from "@/lib/filtros";
import type { Categoria, FiltrosBusca } from "@/types/api";

type Props = {
  categorias: Categoria[];
  filtros: FiltrosBusca;
};

export default function FiltroCategoria({ categorias, filtros }: Props) {
  const opcoes = [{ id: undefined, nome: "Todas" }, ...categorias];

  return (
    <nav aria-label="Filtrar por categoria" className="flex flex-wrap gap-2">
      {opcoes.map((categoria) => {
        const ativa = filtros.categoria_id === categoria.id;

        return (
          <Link
            key={categoria.nome}
            href={montarUrl(filtros, { categoria_id: categoria.id })}
            aria-current={ativa ? "page" : undefined}
            className={`chip ${ativa ? "chip-ativo" : ""}`}
          >
            {categoria.nome}
          </Link>
        );
      })}
    </nav>
  );
}
