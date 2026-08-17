"use client";

import { createContext, useCallback, useContext, useMemo, useSyncExternalStore } from "react";
import { CHAVE_MONTAGEM, gravarMontagem, lerMontagem, type ItemMontagem } from "@/lib/montagem";
import { somarPrecos } from "@/lib/preco";

/**
 * O localStorage é uma fonte de dados fora do React, então a leitura passa por
 * `useSyncExternalStore` em vez de efeito. O cache existe porque `getSnapshot`
 * precisa devolver a mesma referência enquanto nada mudar, senão o React
 * rerenderiza em loop.
 */
const VAZIO: ItemMontagem[] = [];

let cache: ItemMontagem[] = VAZIO;
let carregado = false;
const ouvintes = new Set<() => void>();

function avisar() {
  for (const ouvinte of ouvintes) ouvinte();
}

function inscrever(ouvinte: () => void) {
  ouvintes.add(ouvinte);

  // outra aba gravando a mesma chave mantém esta em dia
  const aoMudarStorage = (evento: StorageEvent) => {
    if (evento.key !== CHAVE_MONTAGEM) return;
    carregado = false;
    avisar();
  };

  window.addEventListener("storage", aoMudarStorage);

  return () => {
    ouvintes.delete(ouvinte);
    window.removeEventListener("storage", aoMudarStorage);
  };
}

function estadoAtual(): ItemMontagem[] {
  if (!carregado) {
    cache = lerMontagem();
    carregado = true;
  }

  return cache;
}

function estadoNoServidor(): ItemMontagem[] {
  return VAZIO;
}

function guardar(proximos: ItemMontagem[]) {
  cache = proximos;
  carregado = true;
  gravarMontagem(proximos);
  avisar();
}

type Montagem = {
  itens: ItemMontagem[];
  total: string;
  /** Falso enquanto o localStorage não foi lido, para o servidor e o cliente renderizarem igual. */
  pronto: boolean;
  escolher: (item: ItemMontagem) => void;
  alterarQuantidade: (produtoId: number, delta: number) => void;
  remover: (produtoId: number) => void;
  limpar: () => void;
  itemDaCategoria: (categoriaId: number) => ItemMontagem | undefined;
};

const MontagemContext = createContext<Montagem | null>(null);

export default function MontagemProvider({ children }: { children: React.ReactNode }) {
  const itens = useSyncExternalStore(inscrever, estadoAtual, estadoNoServidor);
  const pronto = useSyncExternalStore(
    inscrever,
    () => true,
    () => false,
  );

  /**
   * Um slot por categoria: escolher outra peça da mesma categoria troca a que
   * estava lá. Escolher a mesma de novo soma na quantidade.
   */
  const escolher = useCallback((item: ItemMontagem) => {
    const atuais = estadoAtual();
    const existente = atuais.find((i) => i.produto_id === item.produto_id);

    if (existente) {
      guardar(
        atuais.map((i) =>
          i.produto_id === item.produto_id ? { ...i, quantidade: i.quantidade + 1 } : i,
        ),
      );
      return;
    }

    guardar([...atuais.filter((i) => i.categoria_id !== item.categoria_id), item]);
  }, []);

  const alterarQuantidade = useCallback((produtoId: number, delta: number) => {
    guardar(
      estadoAtual().flatMap((item) => {
        if (item.produto_id !== produtoId) return [item];

        const quantidade = item.quantidade + delta;
        return quantidade > 0 ? [{ ...item, quantidade }] : [];
      }),
    );
  }, []);

  const remover = useCallback((produtoId: number) => {
    guardar(estadoAtual().filter((item) => item.produto_id !== produtoId));
  }, []);

  const limpar = useCallback(() => guardar([]), []);

  const valor = useMemo<Montagem>(
    () => ({
      itens,
      total: somarPrecos(itens),
      pronto,
      escolher,
      alterarQuantidade,
      remover,
      limpar,
      itemDaCategoria: (categoriaId) => itens.find((item) => item.categoria_id === categoriaId),
    }),
    [itens, pronto, escolher, alterarQuantidade, remover, limpar],
  );

  return <MontagemContext.Provider value={valor}>{children}</MontagemContext.Provider>;
}

export function useMontagem(): Montagem {
  const contexto = useContext(MontagemContext);

  if (!contexto) {
    throw new Error("useMontagem precisa estar dentro de <MontagemProvider>.");
  }

  return contexto;
}
