"use client";

import Link from "next/link";
import { useMontagem } from "@/components/montagem/MontagemProvider";
import { formatarPreco, somarPrecos } from "@/lib/preco";
import type { ItemMontagem } from "@/lib/montagem";
import type { Categoria } from "@/types/api";

function Quantidade({ item }: { item: ItemMontagem }) {
  const { alterarQuantidade } = useMontagem();

  return (
    <div className="inline-flex items-center border border-rule">
      <button
        type="button"
        onClick={() => alterarQuantidade(item.produto_id, -1)}
        className="h-9 w-9 font-display text-sm font-semibold text-ink-soft transition-colors hover:bg-ink hover:text-paper"
      >
        −<span className="sr-only">Diminuir a quantidade de {item.modelo}</span>
      </button>

      <span className="w-9 text-center font-display text-sm font-semibold tabular-nums">
        {item.quantidade}
      </span>

      <button
        type="button"
        onClick={() => alterarQuantidade(item.produto_id, 1)}
        className="h-9 w-9 font-display text-sm font-semibold text-ink-soft transition-colors hover:bg-ink hover:text-paper"
      >
        +<span className="sr-only">Aumentar a quantidade de {item.modelo}</span>
      </button>
    </div>
  );
}

function SlotPreenchido({ item }: { item: ItemMontagem }) {
  const { remover } = useMontagem();
  const subtotal = somarPrecos([item]);

  return (
    <div className="flex flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between">
      <div className="min-w-0">
        <span className="block text-[0.8125rem] font-medium uppercase tracking-[0.08em] text-ink-soft">
          {item.marca}
        </span>
        <span className="block font-display text-base font-semibold tracking-tight">
          {item.modelo}
        </span>
        <span className="mt-1 block text-[0.8125rem] text-ink-soft">
          {formatarPreco(item.preco)} na {item.loja_nome}
          {" · "}
          <a
            href={item.url_link}
            target="_blank"
            rel="noopener noreferrer nofollow"
            className="link-sublinhado"
          >
            ver na loja ↗
          </a>
        </span>
      </div>

      <div className="flex shrink-0 items-center gap-4">
        <Quantidade item={item} />

        <span className="preco w-28 text-right text-lg">{formatarPreco(subtotal)}</span>

        <button
          type="button"
          onClick={() => remover(item.produto_id)}
          className="text-sm text-ink-soft underline decoration-rule underline-offset-4 transition-colors hover:decoration-ink hover:text-ink"
        >
          remover<span className="sr-only"> {item.modelo} da montagem</span>
        </button>
      </div>
    </div>
  );
}

function SlotVazio({ categoria }: { categoria: Categoria }) {
  return (
    <div className="flex items-center justify-between gap-4 p-5">
      <span className="text-[0.9375rem] text-ink-soft">Nenhuma peça escolhida.</span>

      <Link
        href={`/pecas?categoria_id=${categoria.id}`}
        className="chip shrink-0 hover:border-ink"
      >
        Escolher →<span className="sr-only"> {categoria.nome}</span>
      </Link>
    </div>
  );
}

export default function ListaMontagem({ categorias }: { categorias: Categoria[] }) {
  const { itens, total, pronto, limpar, itemDaCategoria } = useMontagem();

  if (!pronto) {
    return <p className="py-10 text-ink-soft">Carregando a montagem...</p>;
  }

  // Sem categorias a API caiu; ainda dá para mostrar o que já foi escolhido.
  const slots: Array<{ chave: string; nome: string; item?: ItemMontagem; categoria?: Categoria }> =
    categorias.length > 0
      ? categorias.map((categoria) => ({
          chave: `categoria-${categoria.id}`,
          nome: categoria.nome,
          item: itemDaCategoria(categoria.id),
          categoria,
        }))
      : itens.map((item) => ({
          chave: `item-${item.produto_id}`,
          nome: "Peça",
          item,
        }));

  const pecas = itens.reduce((soma, item) => soma + item.quantidade, 0);

  return (
    <>
      <div className="border border-ink">
        {slots.map((slot, indice) => (
          <section
            key={slot.chave}
            className={indice > 0 ? "border-t border-rule" : undefined}
          >
            <h2 className="kicker border-b border-rule bg-paper-alt px-5 py-2.5 text-ink">
              {slot.nome}
            </h2>

            {slot.item ? (
              <SlotPreenchido item={slot.item} />
            ) : slot.categoria ? (
              <SlotVazio categoria={slot.categoria} />
            ) : null}
          </section>
        ))}

        <div className="flex flex-wrap items-baseline justify-between gap-4 border-t border-ink bg-paper-alt px-5 py-5">
          <span className="kicker text-ink">
            Total{pecas > 0 && ` · ${pecas} ${pecas === 1 ? "peça" : "peças"}`}
          </span>
          <span className="preco grifo text-3xl">{formatarPreco(total)}</span>
        </div>
      </div>

      <div className="mt-6 flex flex-wrap items-center justify-between gap-4">
        <Link href="/pecas" className="btn btn-ghost">
          Continuar escolhendo
        </Link>

        {itens.length > 0 && (
          <button
            type="button"
            onClick={limpar}
            className="text-sm text-ink-soft underline decoration-rule underline-offset-4 transition-colors hover:decoration-ink hover:text-ink"
          >
            limpar a montagem
          </button>
        )}
      </div>
    </>
  );
}
