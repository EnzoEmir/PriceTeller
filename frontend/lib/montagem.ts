import { somarPrecos } from "@/lib/preco";
import type { OfertaDaLoja, ProdutoComOfertas } from "@/types/api";

export const CHAVE_MONTAGEM = "priceteller:montagem";

/**
 * Guarda um retrato das ofertas no momento da escolha, e não só o id do produto,
 * para a montagem renderizar e trocar de loja sem depender da API. Os preços aqui
 * envelhecem: são os de quando o usuário escolheu, não os de agora.
 */
export type ItemMontagem = {
  produto_id: number;
  categoria_id: number;
  marca: string;
  modelo: string;
  loja_id: number;
  ofertas: OfertaDaLoja[];
  quantidade: number;
};

export function ofertaEscolhida(item: ItemMontagem): OfertaDaLoja {
  return item.ofertas.find((oferta) => oferta.loja_id === item.loja_id) ?? item.ofertas[0];
}

export function somarMontagem(itens: ItemMontagem[]): string {
  return somarPrecos(
    itens.map((item) => ({ preco: ofertaEscolhida(item).preco, quantidade: item.quantidade })),
  );
}

export function contarPecas(itens: ItemMontagem[]): number {
  return itens.reduce((soma, item) => soma + item.quantidade, 0);
}

export function itemDoProduto(produto: ProdutoComOfertas): ItemMontagem | null {
  if (!produto.melhor_oferta) return null;

  return {
    produto_id: produto.id,
    categoria_id: produto.fk_categoria_id,
    marca: produto.marca,
    modelo: produto.modelo,
    loja_id: produto.melhor_oferta.loja_id,
    ofertas: produto.ofertas,
    quantidade: 1,
  };
}

function ofertaValida(oferta: unknown): oferta is OfertaDaLoja {
  if (typeof oferta !== "object" || oferta === null) return false;

  const candidata = oferta as Record<string, unknown>;

  return (
    typeof candidata.loja_id === "number" &&
    typeof candidata.loja_nome === "string" &&
    typeof candidata.preco === "string" &&
    typeof candidata.url_link === "string"
  );
}

function valido(item: unknown): item is ItemMontagem {
  if (typeof item !== "object" || item === null) return false;

  const candidato = item as Record<string, unknown>;

  return (
    typeof candidato.produto_id === "number" &&
    typeof candidato.categoria_id === "number" &&
    typeof candidato.marca === "string" &&
    typeof candidato.modelo === "string" &&
    typeof candidato.loja_id === "number" &&
    Array.isArray(candidato.ofertas) &&
    candidato.ofertas.length > 0 &&
    candidato.ofertas.every(ofertaValida) &&
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
