"use client";

import { createContext, useCallback, useContext, useMemo, useSyncExternalStore } from "react";
import {
  CHAVE_MONTAGEM,
  contarPecas,
  gravarMontagem,
  lerMontagem,
  somarMontagem,
  type ItemMontagem,
} from "@/lib/montagem";

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

// outra aba gravando a mesma chave mantém esta em dia; um ouvinte só para a
// store inteira, e não um por componente inscrito
function aoMudarStorage(evento: StorageEvent) {
  if (evento.key !== CHAVE_MONTAGEM) return;
  carregado = false;
  avisar();
}

function inscrever(ouvinte: () => void) {
  if (ouvintes.size === 0) {
    window.addEventListener("storage", aoMudarStorage);
  }

  ouvintes.add(ouvinte);

  return () => {
    ouvintes.delete(ouvinte);
    if (ouvintes.size === 0) {
      window.removeEventListener("storage", aoMudarStorage);
    }
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
  /** Soma das quantidades, que é o que a interface chama de "peças". */
  pecas: number;
  /** Falso enquanto o localStorage não foi lido, para o servidor e o cliente renderizarem igual. */
  pronto: boolean;
  escolher: (item: ItemMontagem) => void;
  trocarLoja: (produtoId: number, lojaId: number) => void;
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

  const trocarLoja = useCallback((produtoId: number, lojaId: number) => {
    guardar(
      estadoAtual().map((item) =>
        item.produto_id === produtoId ? { ...item, loja_id: lojaId } : item,
      ),
    );
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
      total: somarMontagem(itens),
      pecas: contarPecas(itens),
      pronto,
      escolher,
      trocarLoja,
      alterarQuantidade,
      remover,
      limpar,
      itemDaCategoria: (categoriaId) => itens.find((item) => item.categoria_id === categoriaId),
    }),
    [itens, pronto, escolher, trocarLoja, alterarQuantidade, remover, limpar],
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
