export type Categoria = {
  id: number;
  nome: string;
};

/**
 * Preço chega como string ("1857.90") porque é Decimal no banco.
 * Converter pra number perde precisão em soma, então guarde a string.
 */
export type MelhorOferta = {
  loja_id: number;
  loja_nome: string;
  preco: string;
  url_link: string;
};

export type Produto = {
  id: number;
  fk_categoria_id: number;
  marca: string;
  modelo: string;
  ean: string | null;
  termos_busca: string[] | null;
  specs: Record<string, unknown> | null;
};

export type ProdutoComOfertas = Produto & {
  total_ofertas: number;
  melhor_oferta: MelhorOferta | null;
};

export type Pagina<T> = {
  items: T[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
};

export const ORDENACOES = ["padrao", "menor_preco", "maior_preco", "nome"] as const;

export type Ordenacao = (typeof ORDENACOES)[number];

export const ROTULO_ORDENACAO: Record<Ordenacao, string> = {
  padrao: "Relevância",
  menor_preco: "Menor preço",
  maior_preco: "Maior preço",
  nome: "Nome (A-Z)",
};

export type FiltrosBusca = {
  q?: string;
  categoria_id?: number;
  preco_min?: string;
  preco_max?: string;
  ordenar?: Ordenacao;
  page?: number;
  limit?: number;
};
