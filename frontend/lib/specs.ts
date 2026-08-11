type Specs = Record<string, unknown>;

function texto(valor: unknown): string | undefined {
  return typeof valor === "string" && valor.trim() ? valor : undefined;
}

function numero(valor: unknown): number | undefined {
  return typeof valor === "number" && Number.isFinite(valor) ? valor : undefined;
}

/**
 * `specs` é JSON livre e as chaves mudam por categoria. A ordem daqui é a ordem
 * em que a spec aparece no card, e chave ausente simplesmente não entra, então a
 * mesma lista serve para as cinco categorias.
 */
const LEITORES: Array<(specs: Specs) => string | undefined> = [
  (s) => texto(s.socket),
  (s) => {
    const nucleos = numero(s.nucleos);
    const threads = numero(s.threads);
    return nucleos && threads ? `${nucleos}C/${threads}T` : undefined;
  },
  (s) => {
    const vram = numero(s.vram_gb);
    return vram ? `${vram} GB VRAM` : undefined;
  },
  (s) => texto(s.chipset),
  (s) => texto(s.form_factor),
  (s) => texto(s.tipo),
  (s) => {
    const capacidade = numero(s.capacidade_gb);
    const pentes = numero(s.pentes);
    if (!capacidade) return undefined;
    return pentes ? `${capacidade} GB (${pentes}x)` : `${capacidade} GB`;
  },
  (s) => {
    const frequencia = numero(s.frequencia_mhz);
    return frequencia ? `${frequencia} MHz` : undefined;
  },
  (s) => {
    const potencia = numero(s.potencia_w);
    return potencia ? `${potencia} W` : undefined;
  },
  (s) => texto(s.certificacao),
  (s) => {
    const tdp = numero(s.tdp);
    return tdp ? `${tdp} W TDP` : undefined;
  },
  (s) => {
    const slots = numero(s.slots_ram);
    return slots ? `${slots} slots` : undefined;
  },
];

export function resumirSpecs(specs: Specs | null, maximo = 3): string[] {
  if (!specs) return [];

  return LEITORES.map((ler) => ler(specs))
    .filter((item): item is string => Boolean(item))
    .slice(0, maximo);
}
