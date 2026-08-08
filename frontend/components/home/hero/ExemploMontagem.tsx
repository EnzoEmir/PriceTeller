import { formatarPreco } from "@/lib/preco";

const pecas = [
  { categoria: "Processador", nome: "AMD Ryzen 7 5700X", loja: "Kabum", preco: "965.90" },
  { categoria: "Placa de Vídeo", nome: "Gigabyte RTX 4060 Eagle OC", loja: "Kabum", preco: "1857.90" },
  { categoria: "Memória RAM", nome: "Kingston Fury Beast 16GB", loja: "Pichau", preco: "289.90" },
];

const total = "3113.70";

export default function ExemploMontagem() {
  return (
    <figure className="border border-ink bg-paper">
      <figcaption className="flex items-center justify-between border-b border-ink px-5 py-3">
        <span className="kicker text-ink">Exemplo de montagem</span>
        <span className="text-[0.6875rem] text-ink-soft">valores ilustrativos</span>
      </figcaption>

      <ul>
        {pecas.map((peca) => (
          <li
            key={peca.categoria}
            className="flex items-center justify-between gap-4 border-b border-rule px-5 py-4"
          >
            <div className="min-w-0">
              <span className="block text-[0.6875rem] uppercase tracking-[0.14em] text-ink-soft">
                {peca.categoria}
              </span>
              <span className="block truncate font-display text-sm font-semibold tracking-tight">
                {peca.nome}
              </span>
            </div>
            <div className="shrink-0 text-right">
              <span className="preco block text-sm">{formatarPreco(peca.preco)}</span>
              <span className="block text-[0.6875rem] text-ink-soft">{peca.loja}</span>
            </div>
          </li>
        ))}
      </ul>

      <div className="flex items-baseline justify-between gap-4 px-5 py-4">
        <span className="kicker text-ink">Total</span>
        <span className="preco grifo text-xl">{formatarPreco(total)}</span>
      </div>
    </figure>
  );
}
