"use client";

import Link from "next/link";
import { useMontagem } from "@/components/montagem/MontagemProvider";
import { formatarPreco } from "@/lib/preco";

export default function ResumoMontagem() {
  const { itens, total, pecas, pronto } = useMontagem();

  if (!pronto || itens.length === 0) return null;

  return (
    <div className="mb-8 flex flex-wrap items-center justify-between gap-x-6 gap-y-2 border border-ink bg-accent-wash px-5 py-3">
      <p className="font-display text-sm font-semibold tracking-tight text-ink">
        {pecas} {pecas === 1 ? "peça" : "peças"} na montagem
        <span className="text-ink-soft"> · </span>
        <span className="preco">{formatarPreco(total)}</span>
      </p>

      <Link href="/montagem" className="link-sublinhado font-display text-sm font-semibold">
        Ver montagem →
      </Link>
    </div>
  );
}
