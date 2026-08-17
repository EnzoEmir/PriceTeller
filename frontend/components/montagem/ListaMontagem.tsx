"use client";

import Link from "next/link";
import { useMontagem } from "@/components/montagem/MontagemProvider";
import { formatarPreco } from "@/lib/preco";
import { ofertaEscolhida, somarMontagem, type ItemMontagem } from "@/lib/montagem";
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

function SeletorDeLoja({ item }: { item: ItemMontagem }) {
  const { trocarLoja } = useMontagem();
  const oferta = ofertaEscolhida(item);

  if (item.ofertas.length === 1) {
    return (
      <span className="text-[0.8125rem] text-ink-soft">
        {formatarPreco(oferta.preco)} na {oferta.loja_nome}
      </span>
    );
  }

  return (
    <label className="inline-flex items-center gap-2">
      <span className="sr-only">Loja escolhida para {item.modelo}</span>

      <select
        value={item.loja_id}
        onChange={(evento) => trocarLoja(item.produto_id, Number(evento.target.value))}
        className="field h-9 w-auto py-0 text-[0.8125rem] tabular-nums"
      >
        {item.ofertas.map((opcao) => (
          <option key={opcao.loja_id} value={opcao.loja_id}>
            {opcao.loja_nome} · {formatarPreco(opcao.preco)}
          </option>
        ))}
      </select>
    </label>
  );
}

function SlotPreenchido({ item }: { item: ItemMontagem }) {
  const { remover } = useMontagem();
  const oferta = ofertaEscolhida(item);
  const subtotal = somarMontagem([item]);

  return (
    <div className="flex flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between">
      <div className="min-w-0">
        <span className="block text-[0.8125rem] font-medium uppercase tracking-[0.08em] text-ink-soft">
          {item.marca}
        </span>
        <span className="block font-display text-base font-semibold tracking-tight">
          {item.modelo}
        </span>

        <div className="mt-2 flex flex-wrap items-center gap-x-3 gap-y-2">
          <SeletorDeLoja item={item} />

          <a
            href={oferta.url_link}
            target="_blank"
            rel="noopener noreferrer nofollow"
            className="link-sublinhado text-[0.8125rem] text-ink-soft"
          >
            ver na loja ↗
          </a>
        </div>
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
  const { itens, total, pecas, pronto, limpar, itemDaCategoria } = useMontagem();

  if (!pronto) {
    return <p className="py-10 text-ink-soft">Carregando a montagem...</p>;
  }

  return (
    <>
      <div className="border border-ink">
        {categorias.map((categoria, indice) => {
          const item = itemDaCategoria(categoria.id);

          return (
            <section
              key={categoria.id}
              className={indice > 0 ? "border-t border-rule" : undefined}
            >
              <h2 className="kicker border-b border-rule bg-paper-alt px-5 py-2.5 text-ink">
                {categoria.nome}
              </h2>

              {item ? <SlotPreenchido item={item} /> : <SlotVazio categoria={categoria} />}
            </section>
          );
        })}

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
