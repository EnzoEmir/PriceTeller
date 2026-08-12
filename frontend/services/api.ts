import type { Categoria, FiltrosBusca, Pagina, ProdutoComOfertas } from "@/types/api";

export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

/**
 * O backend roda separado e precisa ser ligado à mão, então uma falha de rede é
 * esperada em desenvolvimento. Devolver o erro em vez de lançar deixa a página
 * renderizar um aviso em vez de estourar um 500.
 */
export type Resultado<T> = { ok: true; dados: T } | { ok: false; erro: string };

async function buscar<T>(caminho: string, init?: RequestInit): Promise<Resultado<T>> {
  try {
    const resposta = await fetch(`${API_URL}${caminho}`, init);

    if (!resposta.ok) {
      return { ok: false, erro: `A API respondeu ${resposta.status}.` };
    }

    return { ok: true, dados: (await resposta.json()) as T };
  } catch {
    return { ok: false, erro: `Não foi possível falar com a API em ${API_URL}.` };
  }
}

export function listarCategorias(): Promise<Resultado<Categoria[]>> {
  return buscar<Categoria[]>("/categorias/", { next: { revalidate: 300 } });
}

export function listarProdutos(
  filtros: FiltrosBusca,
): Promise<Resultado<Pagina<ProdutoComOfertas>>> {
  const params = new URLSearchParams();

  for (const [chave, valor] of Object.entries(filtros)) {
    if (valor !== undefined && valor !== "") {
      params.set(chave, String(valor));
    }
  }

  const query = params.toString();

  return buscar<Pagina<ProdutoComOfertas>>(`/produtos/${query ? `?${query}` : ""}`, {
    cache: "no-store",
  });
}
