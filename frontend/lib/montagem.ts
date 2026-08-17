import type { ProdutoComOfertas } from "@/types/api";

export const CHAVE_MONTAGEM = "priceteller:montagem";

/**
 * Guarda um retrato da peça no momento da escolha, e não só o id, para a
 * montagem renderizar sem depender da API. O preço aqui envelhece: é o menor
 * preço de quando o usuário escolheu, não o de agora.
 */
export type ItemMontagem = {
  produto_id: number;
  categoria_id: number;
  marca: string;
  modelo: string;
  preco: string;
  loja_nome: string;
  url_link: string;
  quantidade: number;
};

export function itemDoProduto(produto: ProdutoComOfertas): ItemMontagem | null {
  if (!produto.melhor_oferta) return null;

  return {
    produto_id: produto.id,
    categoria_id: produto.fk_categoria_id,
    marca: produto.marca,
    modelo: produto.modelo,
    preco: produto.melhor_oferta.preco,
    loja_nome: produto.melhor_oferta.loja_nome,
    url_link: produto.melhor_oferta.url_link,
    quantidade: 1,
  };
}

function valido(item: unknown): item is ItemMontagem {
  if (typeof item !== "object" || item === null) return false;

  const candidato = item as Record<string, unknown>;

  return (
    typeof candidato.produto_id === "number" &&
    typeof candidato.categoria_id === "number" &&
    typeof candidato.marca === "string" &&
    typeof candidato.modelo === "string" &&
    typeof candidato.preco === "string" &&
    typeof candidato.loja_nome === "string" &&
    typeof candidato.url_link === "string" &&
    typeof candidato.quantidade === "number" &&
    candidato.quantidade > 0
  );
}

/**
 * O que está no localStorage foi gravado por uma versão anterior do site e pode
 * não ter o formato de hoje, então descarta o que não valida em vez de confiar.
 */
export function lerMontagem(): ItemMontagem[] {
  try {
    const bruto = window.localStorage.getItem(CHAVE_MONTAGEM);
    if (!bruto) return [];

    const dados: unknown = JSON.parse(bruto);
    return Array.isArray(dados) ? dados.filter(valido) : [];
  } catch {
    return [];
  }
}

export function gravarMontagem(itens: ItemMontagem[]): void {
  try {
    window.localStorage.setItem(CHAVE_MONTAGEM, JSON.stringify(itens));
  } catch {
    // navegação privada e cota cheia derrubam o setItem; a montagem
    // continua funcionando na sessão, só não sobrevive ao recarregar
  }
}
