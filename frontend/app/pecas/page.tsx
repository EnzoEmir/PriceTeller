import type { Metadata } from "next";
import Link from "next/link";
import { listarCategorias, listarProdutos } from "@/services/api";
import { lerFiltros, temFiltroAtivo, ROTA_PECAS, type ParamsBusca } from "@/lib/filtros";
import BarraBusca from "@/components/pecas/BarraBusca";
import FiltroCategoria from "@/components/pecas/FiltroCategoria";
import FiltroPreco from "@/components/pecas/FiltroPreco";
import SeletorOrdenacao from "@/components/pecas/Ordenacao";
import ProdutoCard from "@/components/pecas/ProdutoCard";
import Paginacao from "@/components/pecas/Paginacao";
import { ApiIndisponivel, SemResultados } from "@/components/pecas/Avisos";

export const metadata: Metadata = {
  title: "Peças",
  description: "Busque processadores, placas de vídeo, memórias e fontes e compare o preço entre lojas.",
};

export default async function Pecas({ searchParams }: { searchParams: Promise<ParamsBusca> }) {
  const filtros = lerFiltros(await searchParams);

  const [categorias, produtos] = await Promise.all([listarCategorias(), listarProdutos(filtros)]);

  const listaCategorias = categorias.ok ? categorias.dados : [];
  const nomePorCategoria = new Map(listaCategorias.map((c) => [c.id, c.nome]));

  return (
    <main>
      <header className="border-b border-rule">
        <div className="container-max py-14 md:py-20">
          <span className="kicker">Catálogo</span>
          <h1 className="mt-4 max-w-3xl">
            Cada peça, <span className="grifo">o menor preço</span>.
          </h1>
          <p className="mt-5 max-w-xl text-lg">
            Uma busca varre marca, modelo e apelido. O preço mostrado é sempre o da loja mais barata
            entre as que anunciam a peça.
          </p>
        </div>
      </header>

      <div className="sticky top-16 z-40 border-b border-rule bg-paper/95 backdrop-blur">
        <div className="container-max py-4">
          <BarraBusca filtros={filtros} />

          <div className="mt-4 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <FiltroCategoria categorias={listaCategorias} filtros={filtros} />

            <div className="flex flex-wrap items-center gap-x-6 gap-y-3">
              <FiltroPreco filtros={filtros} />
              <SeletorOrdenacao filtros={filtros} />
            </div>
          </div>
        </div>
      </div>

      <div className="container-max py-10">
        {!produtos.ok ? (
          <ApiIndisponivel erro={produtos.erro} />
        ) : (
          <>
            <div className="flex flex-wrap items-baseline justify-between gap-x-6 gap-y-2 border-b border-rule pb-4">
              <p className="font-display text-sm font-semibold tabular-nums text-ink">
                {produtos.dados.total} {produtos.dados.total === 1 ? "resultado" : "resultados"}
                {temFiltroAtivo(filtros) && (
                  <>
                    {" · "}
                    <Link href={ROTA_PECAS} className="link-sublinhado font-normal text-ink-soft">
                      limpar filtros
                    </Link>
                  </>
                )}
              </p>

              <p className="text-xs text-ink-soft">
                Preços e lojas ainda são fictícios, gerados para desenvolvimento.
              </p>
            </div>

            {produtos.dados.items.length === 0 ? (
              <div className="mt-10">
                <SemResultados consulta={filtros.q} />
              </div>
            ) : (
              <ul className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {produtos.dados.items.map((produto) => (
                  <li key={produto.id}>
                    <ProdutoCard
                      produto={produto}
                      categoria={nomePorCategoria.get(produto.fk_categoria_id)}
                    />
                  </li>
                ))}
              </ul>
            )}

            <Paginacao
              filtros={filtros}
              page={produtos.dados.page}
              totalPages={produtos.dados.total_pages}
            />
          </>
        )}
      </div>
    </main>
  );
}
