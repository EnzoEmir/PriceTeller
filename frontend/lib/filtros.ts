import { ORDENACOES, type FiltrosBusca, type Ordenacao } from "@/types/api";
import { normalizarDecimal } from "@/lib/preco";

export const LIMITE_PADRAO = 12;
export const ROTA_PECAS = "/pecas";

export type ParamsBusca = Record<string, string | string[] | undefined>;

function primeiro(valor: string | string[] | undefined): string | undefined {
  const bruto = Array.isArray(valor) ? valor[0] : valor;
  return bruto?.trim() || undefined;
}

function inteiroPositivo(valor: string | undefined): number | undefined {
  if (!valor || !/^\d+$/.test(valor)) return undefined;
  const numero = Number(valor);
  return numero > 0 ? numero : undefined;
}

/**
 * A URL é a única fonte de verdade da busca: filtro compartilhável, botão voltar
 * funcionando e nenhum estado duplicado no cliente.
 */
export function lerFiltros(params: ParamsBusca): FiltrosBusca {
  const ordenar = primeiro(params.ordenar);

  return {
    q: primeiro(params.q),
    categoria_id: inteiroPositivo(primeiro(params.categoria_id)),
    preco_min: normalizarDecimal(primeiro(params.preco_min) ?? ""),
    preco_max: normalizarDecimal(primeiro(params.preco_max) ?? ""),
    ordenar: ORDENACOES.includes(ordenar as Ordenacao) ? (ordenar as Ordenacao) : "padrao",
    page: inteiroPositivo(primeiro(params.page)) ?? 1,
    limit: LIMITE_PADRAO,
  };
}

/**
 * Qualquer mudança de filtro volta pra primeira página, senão o usuário filtra e
 * cai numa página que não existe mais.
 */
export function montarUrl(atuais: FiltrosBusca, mudancas: Partial<FiltrosBusca>): string {
  const filtros = { ...atuais, ...mudancas };
  const params = new URLSearchParams();

  if (filtros.q) params.set("q", filtros.q);
  if (filtros.categoria_id) params.set("categoria_id", String(filtros.categoria_id));
  if (filtros.preco_min) params.set("preco_min", filtros.preco_min);
  if (filtros.preco_max) params.set("preco_max", filtros.preco_max);
  if (filtros.ordenar && filtros.ordenar !== "padrao") params.set("ordenar", filtros.ordenar);

  const page = mudancas.page ?? 1;
  if (page > 1) params.set("page", String(page));

  const query = params.toString();

  return query ? `${ROTA_PECAS}?${query}` : ROTA_PECAS;
}

export function temFiltroAtivo(filtros: FiltrosBusca): boolean {
  return Boolean(
    filtros.q ||
      filtros.categoria_id ||
      filtros.preco_min ||
      filtros.preco_max ||
      (filtros.ordenar && filtros.ordenar !== "padrao"),
  );
}
