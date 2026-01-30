# Data Lake - Estrutura

> **Storage**: Azure Data Lake Gen2
> **Formato**: Parquet
> **Frequência**: Diária
> **Responsável**: Ítalo

---

## Visão Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                    AZURE DATA LAKE GEN2                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Container: datahub                                            │
│   │                                                             │
│   ├── /raw/                    ← Dados brutos (Bronze)          │
│   │   └── sankhya/                                              │
│   │       ├── compras/                                          │
│   │       ├── vendas/          (futuro)                         │
│   │       ├── financeiro/      (futuro)                         │
│   │       └── rh/              (futuro)                         │
│   │                                                             │
│   ├── /processed/              ← Dados limpos (Silver) [futuro] │
│   │                                                             │
│   └── /analytics/              ← Dados agregados (Gold) [futuro]│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Estrutura de Pastas - Compras

```
/raw/sankhya/compras/
│
├── cabecalho/
│   └── ano=2026/
│       └── mes=01/
│           └── dia=27/
│               └── compras_cab_20260127_120000.parquet
│
├── itens/
│   └── ano=2026/
│       └── mes=01/
│           └── dia=27/
│               └── compras_ite_20260127_120000.parquet
│
├── fornecedores/
│   └── ano=2026/
│       └── mes=01/
│           └── dia=27/
│               └── fornecedores_20260127_120000.parquet
│
└── wms/
    └── ano=2026/
        └── mes=01/
            └── dia=27/
                └── wms_situacao_20260127_120000.parquet
```

---

## Nomenclatura dos Arquivos

**Padrão**: `{entidade}_{YYYYMMDD}_{HHmmss}.parquet`

| Componente | Descrição | Exemplo |
|------------|-----------|---------|
| `entidade` | Nome da tabela/assunto | `compras_cab`, `compras_ite` |
| `YYYYMMDD` | Data da extração | `20260127` |
| `HHmmss` | Hora da extração | `120000` |
| `.parquet` | Formato do arquivo | - |

**Exemplos:**
- `compras_cab_20260127_120000.parquet`
- `compras_ite_20260127_120000.parquet`
- `fornecedores_20260127_120000.parquet`
- `wms_situacao_20260127_120000.parquet`

---

## Particionamento

Usamos particionamento por **data** no estilo Hive:

```
ano=2026/mes=01/dia=27/
```

**Vantagens:**
- Queries mais rápidas (poda de partição)
- Fácil de gerenciar retenção
- Compatível com Spark, Databricks, Synapse

---

## Schema dos Arquivos Parquet

### compras_cab (Cabeçalho)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `nunota` | INT64 | Número único da nota (PK) |
| `numnota` | INT64 | Número da NF |
| `dtneg` | DATE | Data da negociação |
| `dtentsai` | DATE | Data entrada/saída |
| `codparc` | INT64 | Código do fornecedor |
| `codemp` | INT64 | Código da filial |
| `codtipoper` | INT64 | Tipo de operação |
| `vlrnota` | DECIMAL | Valor total |
| `vlrdesctot` | DECIMAL | Desconto total |
| `vlrfrete` | DECIMAL | Valor do frete |
| `statusnota` | STRING | Status |
| `tipmov` | STRING | Tipo de movimento |
| `codcomprador` | INT64 | Código do comprador |
| `observacao` | STRING | Observações |
| `cod_situacao_wms` | INT64 | Situação WMS |
| `situacao_wms` | STRING | Descrição situação WMS |
| `dt_extracao` | TIMESTAMP | Data/hora da extração |

### compras_ite (Itens)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `nunota` | INT64 | Número da nota (FK) |
| `sequencia` | INT64 | Sequência do item |
| `codprod` | INT64 | Código do produto |
| `qtdneg` | DECIMAL | Quantidade |
| `vlrunit` | DECIMAL | Valor unitário |
| `vlrtot` | DECIMAL | Valor total |
| `vlrdesc` | DECIMAL | Desconto |
| `codvol` | STRING | Unidade de medida |
| `dt_extracao` | TIMESTAMP | Data/hora da extração |

### fornecedores

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `codparc` | INT64 | Código do parceiro (PK) |
| `razaosocial` | STRING | Razão social |
| `nomeparc` | STRING | Nome fantasia |
| `cgc_cpf` | STRING | CNPJ |
| `codcid` | INT64 | Código da cidade |
| `email` | STRING | Email |
| `telefone` | STRING | Telefone |
| `ativo` | STRING | Ativo (S/N) |
| `dt_extracao` | TIMESTAMP | Data/hora da extração |

### wms_situacao

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `nunota` | INT64 | Número da nota |
| `cod_situacao` | INT64 | Código situação WMS |
| `descricao` | STRING | Descrição |
| `grupo` | STRING | Grupo (Recebimento/Final/etc) |
| `dt_extracao` | TIMESTAMP | Data/hora da extração |

---

## Metadados de Controle

Cada extração gera um arquivo de metadados:

```
/raw/sankhya/compras/_metadata/
└── ano=2026/
    └── mes=01/
        └── dia=27/
            └── extracao_20260127_120000.json
```

**Conteúdo do JSON:**
```json
{
  "extracao_id": "20260127_120000",
  "inicio": "2026-01-27T12:00:00",
  "fim": "2026-01-27T12:05:32",
  "status": "sucesso",
  "registros": {
    "cabecalho": 150,
    "itens": 1200,
    "fornecedores": 45,
    "wms": 150
  },
  "periodo_dados": {
    "data_inicio": "2026-01-26",
    "data_fim": "2026-01-27"
  },
  "fonte": "sankhya_api",
  "versao_extrator": "1.0.0"
}
```

---

## Estratégia de Carga

### Carga Diária (Incremental)

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUXO DE EXTRAÇÃO                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Ler última data extraída (metadata)                     │
│                    │                                        │
│                    ▼                                        │
│  2. Buscar dados do Sankhya (DTNEG >= última_data)          │
│                    │                                        │
│                    ▼                                        │
│  3. Transformar para Parquet                                │
│                    │                                        │
│                    ▼                                        │
│  4. Salvar no Data Lake (particionado por data)             │
│                    │                                        │
│                    ▼                                        │
│  5. Atualizar metadata                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Horário de Execução

| Extração | Horário | Descrição |
|----------|---------|-----------|
| Compras | 06:00 | Antes do expediente |
| Vendas | 06:15 | (futuro) |
| Financeiro | 06:30 | (futuro) |
| RH | 06:45 | (futuro) |

---

## Retenção de Dados

| Camada | Retenção | Motivo |
|--------|----------|--------|
| `/raw/` | 2 anos | Histórico completo |
| `/processed/` | 1 ano | Dados limpos |
| `/analytics/` | 5 anos | Agregados para análise |

---

## Acesso e Segurança

### Containers e Permissões

| Container | Quem acessa | Permissão |
|-----------|-------------|-----------|
| `datahub` | Extrator Python | Read/Write |
| `datahub` | Agente Analista | Read |
| `datahub` | Power BI | Read |

### Hierarquia de Acesso (RLS no futuro)

```
/raw/sankhya/compras/
│
├── Diretor: acesso total
├── Gerente Regional: filtro por CODEMP da região
├── Gerente Filial: filtro por CODEMP específico
└── Comprador: filtro por CODCOMPRADOR
```

---

## Checklist de Setup

- [ ] Criar container `datahub` no Storage Account
- [ ] Criar estrutura de pastas inicial
- [ ] Configurar permissões (RBAC/ACL)
- [ ] Criar Service Principal para o extrator
- [ ] Testar upload de arquivo Parquet
- [ ] Documentar connection string (Key Vault)

---

## Histórico

| Data | Alteração | Responsável |
|------|-----------|-------------|
| Jan/2026 | Estrutura inicial | Ítalo |
