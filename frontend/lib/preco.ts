/**
 * Formata o Decimal que a API manda como string ("1857.90") sem passar por
 * float. `Number` arredondaria valores altos e a soma da montagem depende disso.
 */
export function formatarPreco(valor: string): string {
  const negativo = valor.trimStart().startsWith("-");
  const [inteiroBruto = "0", decimalBruto = ""] = valor.replace("-", "").trim().split(".");

  const centavos = `${decimalBruto}00`.slice(0, 2);
  const inteiro = inteiroBruto.replace(/\B(?=(\d{3})+(?!\d))/g, ".");

  return `${negativo ? "-" : ""}R$ ${inteiro},${centavos}`;
}

/**
 * Aceita o que o usuário digita em pt-BR ("1.500,90") e devolve o formato que a
 * query string da API espera ("1500.90"). Devolve undefined se não sobrar número.
 */
export function normalizarDecimal(entrada: string): string | undefined {
  const limpo = entrada.replace(/[^\d.,]/g, "");

  if (!limpo) return undefined;

  const separadoDecimal = limpo.includes(",")
    ? limpo.replace(/\./g, "").replace(",", ".")
    : limpo;

  const numerico = separadoDecimal.match(/^\d+(\.\d{0,2})?/)?.[0];

  return numerico || undefined;
}
