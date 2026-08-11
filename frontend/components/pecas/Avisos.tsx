import Link from "next/link";
import { ROTA_PECAS } from "@/lib/filtros";

export function SemResultados({ consulta }: { consulta?: string }) {
  return (
    <div className="border border-rule bg-paper-alt px-6 py-16 text-center">
      <span className="kicker">Nenhum resultado</span>
      <p className="mx-auto mt-4 max-w-md text-ink">
        {consulta
          ? `Nada encontrado para "${consulta}" com os filtros atuais.`
          : "Nenhuma peça bate com os filtros atuais."}
      </p>
      <Link href={ROTA_PECAS} className="btn btn-ghost mt-6 h-10 px-4 text-xs">
        Limpar filtros
      </Link>
    </div>
  );
}

export function ApiIndisponivel({ erro }: { erro: string }) {
  return (
    <div className="border border-ink bg-accent-wash px-6 py-12">
      <span className="kicker">Backend fora do ar</span>
      <p className="mt-4 max-w-xl text-ink">{erro}</p>
      <p className="mt-2 max-w-xl text-sm text-ink-soft">
        Suba a API com <code className="bg-paper px-1.5 py-0.5">uvicorn main:app --reload</code> na
        pasta <code className="bg-paper px-1.5 py-0.5">backend</code>. Se o banco estiver vazio,
        rode também{" "}
        <code className="bg-paper px-1.5 py-0.5">python -m app.test.builder.seed_catalogo</code>.
      </p>
    </div>
  );
}
