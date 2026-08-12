import { formatarPreco } from "@/lib/preco";
import { resumirSpecs } from "@/lib/specs";
import type { ProdutoComOfertas } from "@/types/api";

type Props = {
  produto: ProdutoComOfertas;
  categoria?: string;
};

export default function ProdutoCard({ produto, categoria }: Props) {
  const specs = resumirSpecs(produto.specs);
  const oferta = produto.melhor_oferta;

  return (
    <article className="flex h-full flex-col border border-rule bg-paper transition-colors duration-150 hover:border-ink">
      <div className="flex-1 p-5">
        <span className="kicker">{categoria ?? "Peça"}</span>

        <h3 className="mt-3 text-lg leading-tight">
          <span className="block text-[0.8125rem] font-medium uppercase tracking-[0.08em] text-ink-soft">
            {produto.marca}
          </span>
          {produto.modelo}
        </h3>

        {specs.length > 0 && (
          <ul className="mt-4 flex flex-wrap items-center gap-x-2 gap-y-1 text-[0.8125rem] text-ink-soft">
            {specs.map((spec, indice) => (
              <li key={spec} className="flex items-center gap-2">
                {indice > 0 && (
                  <span aria-hidden="true" className="text-rule">
                    ·
                  </span>
                )}
                <span className="tabular-nums">{spec}</span>
              </li>
            ))}
          </ul>
        )}
      </div>

      {oferta ? (
        <div className="border-t border-rule p-5">
          <span className="text-xs text-ink-soft">a partir de</span>

          <p className="mt-1 flex items-baseline gap-2">
            <span className="preco grifo text-2xl">{formatarPreco(oferta.preco)}</span>
          </p>

          <div className="mt-3 flex items-center justify-between gap-3">
            <span className="text-[0.8125rem] text-ink-soft">
              {oferta.loja_nome}
              {produto.total_ofertas > 1 && ` · ${produto.total_ofertas} lojas`}
            </span>

            <a
              href={oferta.url_link}
              target="_blank"
              rel="noopener noreferrer nofollow"
              className="link-sublinhado shrink-0 font-display text-[0.8125rem] font-semibold"
            >
              Ver na loja ↗
              <span className="sr-only">
                {" "}
                {produto.marca} {produto.modelo} em {oferta.loja_nome}
              </span>
            </a>
          </div>
        </div>
      ) : (
        <div className="border-t border-rule p-5">
          <span className="text-[0.8125rem] text-ink-soft">Nenhuma loja com esta peça agora.</span>
        </div>
      )}
    </article>
  );
}
