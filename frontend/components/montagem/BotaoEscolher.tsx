"use client";

import { useMontagem } from "@/components/montagem/MontagemProvider";
import { itemDoProduto } from "@/lib/montagem";
import type { ProdutoComOfertas } from "@/types/api";

export default function BotaoEscolher({ produto }: { produto: ProdutoComOfertas }) {
  const { escolher, itens, itemDaCategoria } = useMontagem();

  const item = itemDoProduto(produto);
  if (!item) return null;

  const escolhido = itens.find((i) => i.produto_id === produto.id);
  const ocupandoOSlot = itemDaCategoria(produto.fk_categoria_id);

  const rotulo = escolhido
    ? `Na montagem · ${escolhido.quantidade}`
    : ocupandoOSlot
      ? "Trocar"
      : "+ Adicionar";

  return (
    <button
      type="button"
      onClick={() => escolher(item)}
      className={`chip w-full justify-center ${escolhido ? "chip-ativo" : ""}`}
    >
      {rotulo}
      <span className="sr-only">
        {" "}
        {produto.marca} {produto.modelo}
        {ocupandoOSlot && !escolhido
          ? `, substituindo ${ocupandoOSlot.marca} ${ocupandoOSlot.modelo}`
          : ""}
      </span>
    </button>
  );
}
