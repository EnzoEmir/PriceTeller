const pilares = [
  {
    titulo: "Uma busca, todas as lojas",
    texto:
      "O mesmo modelo aparece uma vez só, já com o menor preço entre as lojas que anunciam ele, e quantas ofertas existem no total.",
  },
  {
    titulo: "Ela entende apelido",
    texto:
      "Digite R7 5700X e o Ryzen 7 5700X aparece. A busca olha marca, modelo e os nomes alternativos que cada loja usa.",
  },
  {
    titulo: "Filtro pelo que importa",
    texto:
      "Faixa de preço e ordenação sempre se referem à oferta mais barata. Limite em R$ 2.000 e sobra só o que dá pra comprar por até isso.",
  },
];

export default function BenefitsSection() {
  return (
    <section id="como-funciona" className="section-alt scroll-mt-16">
      <div className="container-max">
        <span className="kicker">Como funciona</span>
        <h2 className="mt-4 max-w-2xl">Preço de peça muda toda semana. Comparar é sempre no mesmo lugar.</h2>

        <div className="mt-14 grid gap-px border border-rule bg-rule md:grid-cols-3">
          {pilares.map((pilar) => (
            <article key={pilar.titulo} className="bg-paper-alt p-7">
              <h3>{pilar.titulo}</h3>
              <p className="mt-3 text-[0.9375rem]">{pilar.texto}</p>
            </article>
          ))}
        </div>

        <div className="mt-10 flex flex-col gap-2 border-t border-ink pt-4 sm:flex-row sm:gap-10">
          <span className="kicker shrink-0 text-ink">Ainda não</span>
          <p className="max-w-2xl text-sm">
            Aviso de incompatibilidade entre peças e gráfico de variação de preço estão no
            roadmap. Os preços de hoje são fictícios, gerados para desenvolvimento.
          </p>
        </div>
      </div>
    </section>
  );
}
