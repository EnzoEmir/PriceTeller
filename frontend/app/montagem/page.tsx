import type { Metadata } from "next";
import { listarCategorias } from "@/services/api";
import ListaMontagem from "@/components/montagem/ListaMontagem";
import { ApiIndisponivel } from "@/components/pecas/Avisos";

export const metadata: Metadata = {
  title: "Montagem",
  description: "As peças que você escolheu, o preço de cada uma e o total da montagem.",
};

export default async function Montagem() {
  const categorias = await listarCategorias();

  return (
    <main>
      <header className="border-b border-rule">
        <div className="container-max py-14 md:py-20">
          <span className="kicker">Montagem</span>
          <h1 className="mt-4 max-w-3xl">
            Seu PC, <span className="grifo">peça por peça</span>.
          </h1>
          <p className="mt-5 max-w-xl text-lg">
            Um slot por categoria. Cada peça entra pela loja mais barata, e você troca a loja se
            preferir comprar em outra.
          </p>
        </div>
      </header>

      <div className="container-max py-10">
        {categorias.ok ? (
          <ListaMontagem categorias={categorias.dados} />
        ) : (
          <ApiIndisponivel erro={categorias.erro} />
        )}

        <p className="mt-8 max-w-2xl text-[0.8125rem] text-ink-soft">
          A montagem fica salva apenas neste navegador, e os preços são os de quando você
          escolheu cada peça. Ainda não há verificação de compatibilidade.
        </p>
      </div>
    </main>
  );
}
