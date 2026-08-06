import Link from "next/link";
import ExemploMontagem from "./ExemploMontagem";

export default function HeroSection() {
  return (
    <section className="border-b border-rule">
      <div className="container-max grid gap-14 py-20 md:py-28 lg:grid-cols-[1.05fr_1fr] lg:items-center lg:gap-20">
        <div>
          <span className="kicker">Comparador de peças de PC</span>

          <h1 className="mt-5">
            Lista de compras <span className="grifo">poderosa</span>.
          </h1>

          <p className="mt-6 max-w-lg text-lg">
            Escolha as peças da sua máquina, veja o menor preço de cada uma e o custo total.
            Sem abrir dez abas de loja.
          </p>

          <div className="mt-9 flex flex-wrap gap-3">
            <Link href="/pecas" className="btn btn-primary">
              Buscar peças
            </Link>
            <Link href="#como-funciona" className="btn btn-ghost">
              Como funciona
            </Link>
          </div>
        </div>

        <ExemploMontagem />
      </div>
    </section>
  );
}
