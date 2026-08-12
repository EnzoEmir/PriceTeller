"use client";

import { useTransition } from "react";
import { useRouter } from "next/navigation";
import { montarUrl } from "@/lib/filtros";
import { ORDENACOES, ROTULO_ORDENACAO, type FiltrosBusca, type Ordenacao } from "@/types/api";

export default function SeletorOrdenacao({ filtros }: { filtros: FiltrosBusca }) {
  const router = useRouter();
  const [, iniciar] = useTransition();

  return (
    <div className="flex items-center gap-3">
      <label
        htmlFor="ordenar"
        className="font-display text-[0.6875rem] font-semibold uppercase tracking-[0.16em] text-ink-soft"
      >
        Ordenar
      </label>
      <select
        id="ordenar"
        value={filtros.ordenar ?? "padrao"}
        onChange={(evento) =>
          iniciar(() =>
            router.push(montarUrl(filtros, { ordenar: evento.target.value as Ordenacao })),
          )
        }
        className="field h-11 w-auto cursor-pointer pr-8 font-display text-xs font-semibold"
      >
        {ORDENACOES.map((opcao) => (
          <option key={opcao} value={opcao}>
            {ROTULO_ORDENACAO[opcao]}
          </option>
        ))}
      </select>
    </div>
  );
}
