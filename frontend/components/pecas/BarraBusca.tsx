"use client";

import { useEffect, useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import { montarUrl } from "@/lib/filtros";
import type { FiltrosBusca } from "@/types/api";

export default function BarraBusca({ filtros }: { filtros: FiltrosBusca }) {
  const router = useRouter();
  const [pendente, iniciar] = useTransition();
  const [valor, setValor] = useState(filtros.q ?? "");

  const consultaAtual = filtros.q ?? "";
  const alvo = montarUrl(filtros, { q: valor.trim() || undefined });

  useEffect(() => {
    setValor(consultaAtual);
  }, [consultaAtual]);

  useEffect(() => {
    if (valor.trim() === consultaAtual) return;

    const id = setTimeout(() => iniciar(() => router.push(alvo)), 350);
    return () => clearTimeout(id);
  }, [valor, consultaAtual, alvo, router]);

  return (
    <form
      role="search"
      onSubmit={(evento) => {
        evento.preventDefault();
        iniciar(() => router.push(alvo));
      }}
      className="relative"
    >
      <label htmlFor="busca" className="sr-only">
        Buscar peças
      </label>
      <input
        id="busca"
        type="search"
        value={valor}
        onChange={(evento) => setValor(evento.target.value)}
        placeholder="Buscar por marca, modelo ou apelido: rtx 4060, r7 5700x, ddr4..."
        autoComplete="off"
        className="field h-14 pr-24 text-base"
      />
      <span
        aria-live="polite"
        className={`absolute right-4 top-1/2 -translate-y-1/2 font-display text-[0.6875rem] font-semibold uppercase tracking-[0.16em] text-ink-soft transition-opacity ${
          pendente ? "opacity-100" : "opacity-0"
        }`}
      >
        Buscando
      </span>
    </form>
  );
}
