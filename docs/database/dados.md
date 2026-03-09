# Dicionário de Dados

Este documento detalha a estrutura do banco de dados relacional (PostgreSQL).

---

## 1. Tabela: `CATEGORIA`
Armazena os grupos lógicos de produtos (ex: CPU, GPU, RAM).

| Campo | Tipo | Chave | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | `INT` | **PK** | Identificador único da categoria. |
| `nome` | `VARCHAR(50)` | - | Nome amigável (ex: 'Processador', 'Fonte'). |

---

## 2. Tabela: `PRODUTO`
Entidade central que armazena os dados técnicos universais de cada peça.

| Campo | Tipo | Chave | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | `SERIAL` | **PK** | Identificador único do produto. |
| `FK_CATEGORIA_id` | `INT` | **FK** | Referência à categoria do produto. |
| `marca` | `VARCHAR(100)` | - | Fabricante (ex: Intel, AMD, ASUS). |
| `modelo` | `VARCHAR(255)` | - | Nome completo do modelo. |
| `specs` | `JSONB` | - | Atributos técnicos dinâmicos para compatibilidade. |

---

## 3. Tabela: `LOJA`
Cadastro das lojas de e-commerce que serão monitoradas.

| Campo | Tipo | Chave | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | `SERIAL` | **PK** | Identificador único da loja. |
| `nome` | `VARCHAR(100)` | - | Nome da loja (ex: Kabum, Pichau). |
| `url_base` | `TEXT` | - | Domínio principal da loja. |

---

## 4. Tabela: `OFERTA`
Representa o preço de um produto em uma loja específica em tempo real.

| Campo | Tipo | Chave | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | `SERIAL` | **PK** | Identificador único da oferta. |
| `FK_PRODUTO_id` | `INT` | **FK** | Referência ao produto universal. |
| `FK_LOJA_id` | `INT` | **FK** | Referência à loja anunciante. |
| `preco_atual` | `DECIMAL(10,2)`| - | Valor atualizado capturado pelo sistema. |
| `url_link` | `TEXT` | - | Link direto para a página do produto na loja. |

---

## 5. Tabela: `HISTORICO`
Armazena a variação de preços ao longo do tempo.

| Campo | Tipo | Chave | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | `BIGSERIAL` | **PK** | ID de alta capacidade para grande volume de dados. |
| `FK_OFERTA_id` | `INT` | **FK** | Referência à oferta monitorada. |
| `preco` | `DECIMAL(10,2)`| - | Valor registrado no momento da captura. |
| `data` | `TIMESTAMPTZ` | - | Data e hora exata do registro (com fuso horário). |

---