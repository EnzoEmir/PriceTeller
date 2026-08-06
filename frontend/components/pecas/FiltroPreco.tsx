"use client";

import { useTransition } from "react";
import { useRouter } from "next/navigation";
import { montarUrl } from "@/lib/filtros";
import { normalizarDecimal } from "@/lib/preco";
import type { FiltrosBusca } from "@/types/api";

export default function FiltroPreco({ filtros }: { filtros: FiltrosBusca }) {
  const router = useRouter();
  const [pendente, iniciar] = useTransition();

  function aplicar(evento: React.FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    const dados = new FormData(evento.currentTarget);

    const destino = montarUrl(filtros, {
      preco_min: normalizarDecimal(String(dados.get("preco_min") ?? "")),
      preco_max: normalizarDecimal(String(dados.get("preco_max") ?? "")),
    });

    iniciar(() => router.push(destino));
  }

  return (
    <form
      onSubmit={aplicar}
      key={`${filtros.preco_min ?? ""}-${filtros.preco_max ?? ""}`}
      className="flex items-center gap-2"
    >
      <label htmlFor="preco_min" className="sr-only">
        Preço mínimo
      </label>
      <input
        id="preco_min"
        name="preco_min"
        inputMode="decimal"
        defaultValue={(filtros.preco_min ?? "").replace(".", ",")}
        placeholder="mín."
        className="field w-24 px-3 tabular-nums"
      />

      <span aria-hidden="true" className="text-ink-soft">
        –
      </span>

      <label htmlFor="preco_max" className="sr-only">
        Preço máximo
      </label>
      <input
        id="preco_max"
        name="preco_max"
        inputMode="decimal"
        defaultValue={(filtros.preco_max ?? "").replace(".", ",")}
        placeholder="máx."
        className="field w-24 px-3 tabular-nums"
      />

      <button type="submit" className="btn btn-ghost h-11 px-4 text-xs" disabled={pendente}>
        {pendente ? "..." : "Aplicar"}
      </button>
    </form>
  );
}
