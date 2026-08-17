import type { Metadata } from "next";
import { listarCategorias } from "@/services/api";
import ListaMontagem from "@/components/montagem/ListaMontagem";

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
            Um slot por categoria. O preço de cada peça é o da loja mais barata no momento em que
            você escolheu.
          </p>
        </div>
      </header>

      <div className="container-max py-10">
        <ListaMontagem categorias={categorias.ok ? categorias.dados : []} />

        <p className="mt-8 max-w-2xl text-[0.8125rem] text-ink-soft">
          A montagem fica salva apenas neste navegador. Ainda não há verificação de
          compatibilidade entre as peças.
        </p>
      </div>
    </main>
  );
}
