# MMarra Data Hub

**Plataforma de Dados Inteligente da MMarra**

> *"O centro de conexão entre dados, análises e decisões"*

---

## Visão Geral

O Nexus é uma plataforma SaaS de análise de dados que integra o Sankhya ERP com um Data Lake no Azure, permitindo consultas em linguagem natural através de agentes de IA especializados.

### Conceito

Inspirado em apps como MotoFlash, mas para dados: uma interface simples onde o usuário pergunta e recebe respostas instantâneas sobre vendas, compras, financeiro e RH.

```
"Qual o total de vendas do último mês?"
"Quantos pedidos de compra estão pendentes?"
"Quem são os top 10 clientes?"
```

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              MMARRA DATA HUB v1.0                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   FONTES                           ARMAZENAMENTO                            │
│   ┌──────────┐                     ┌─────────────────────────────────────┐  │
│   │ SANKHYA  │──── Python ────────►│  AZURE DATA LAKE                    │  │
│   │   API    │     Extractor       │                                     │  │
│   └──────────┘                     │  /raw/sankhya/vendas/               │  │
│                                    │  /raw/sankhya/compras/              │  │
│   ┌──────────┐                     │  /raw/sankhya/financeiro/           │  │
│   │  CLARA   │─────────────────────│  /raw/sankhya/rh/                   │  │
│   │   API    │                     │                                     │  │
│   └──────────┘                     └──────────────┬──────────────────────┘  │
│                                                   │                         │
│                                                   ▼                         │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    AGENTES DE IA                                    │   │
│   │                                                                     │   │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
│   │  │  Agente     │  │   Agente    │  │   Agente    │                  │   │
│   │  │ Engenheiro  │◄─┤  Analista   │◄─┤  Cientista  │                  │   │
│   │  │             │  │             │  │             │                  │   │
│   │  │ - Extrai    │  │ - Agrega    │  │ - Previsões │                  │   │
│   │  │ - Valida    │  │ - Calcula   │  │ - Anomalias │                  │   │
│   │  │ - Carrega   │  │ - Formata   │  │ - Clusters  │                  │   │
│   │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
│   │                          │                                          │   │
│   │                          ▼                                          │   │
│   │               ┌─────────────────────┐                               │   │
│   │               │   Agente LLM        │                               │   │
│   │               │   (Orquestrador)    │                               │   │
│   │               │                     │                               │   │
│   │               │   "Qual o total     │                               │   │
│   │               │    de vendas?"      │                               │   │
│   │               └─────────────────────┘                               │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                         INTERFACE                                   │   │
│   │              Chat (WhatsApp/Web) + Dashboards                       │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Stack Tecnológica

| Camada | Tecnologia | Status |
|--------|------------|--------|
| **Fonte** | Sankhya API | Em mapeamento |
| **Armazenamento** | Azure Data Lake Gen2 | Já existe |
| **Extração** | Python | Próximo passo |
| **Agentes IA** | LangChain/CrewAI | Futuro |
| **Interface** | Web + WhatsApp | Futuro |

---

## Fase Atual: Mapeamento de Compras

```
┌─────────────┐         ┌──────────────────────┐
│   SANKHYA   │ ──API──►│   AZURE DATA LAKE    │
│     ERP     │         │   (dados brutos)     │
└─────────────┘         └──────────────────────┘
       │
       │  Fase atual: Mapeando tabelas de COMPRAS via Postman
       │
       ▼
   [ Postman ]
```

### Tabelas já mapeadas (Compras)

| Tabela | Conteúdo | Status |
|--------|----------|--------|
| `TGFCAB` | Cabeçalho dos pedidos | ✅ |
| `TGFITE` | Itens dos pedidos | ✅ |
| `TGFPAR` | Fornecedores | ✅ |
| `TGFPRO` | Produtos | ✅ |
| `TGWREC` | Recebimento WMS | ✅ |
| `VGWRECSITCAB` | Situação WMS | ✅ |

---

## Roadmap

### Fase 1: Mapeamento - COMPRAS (ATUAL)
- [x] Configurar Postman com autenticação Sankhya
- [x] Explorar tabelas relacionadas a Compras
- [x] Mapear situação WMS completa
- [ ] Identificar campos customizados (AD_*)
- [ ] Criar query de extração funcional
- [ ] Testar extração manual

### Fase 2: ETL Básico - COMPRAS
- [ ] Script Python de extração
- [ ] Salvar no Data Lake (formato Parquet)
- [ ] Testar carga incremental
- [ ] Agendar execução diária

### Fase 3: Expandir Mapeamento
- [ ] Adicionar VENDAS
- [ ] Adicionar FINANCEIRO
- [ ] Adicionar RH

### Fase 4: Agentes de IA
- [ ] Agente Engenheiro (ETL automatizado)
- [ ] Agente Analista (relatórios)
- [ ] Agente LLM (interface conversacional)

### Fase 5: Interface
- [ ] Chat Web
- [ ] Integração WhatsApp
- [ ] Dashboards básicos

---

## Estrutura do Data Lake

**Storage**: Azure Data Lake Gen2
**Formato**: Parquet
**Frequência**: Diária (06:00)

```
Container: datahub/

/raw/sankhya/compras/
├── cabecalho/
│   └── ano=2026/mes=01/dia=27/
│       └── compras_cab_20260127_060000.parquet
├── itens/
│   └── ano=2026/mes=01/dia=27/
│       └── compras_ite_20260127_060000.parquet
├── fornecedores/
│   └── ano=2026/mes=01/dia=27/
│       └── fornecedores_20260127_060000.parquet
├── wms/
│   └── ano=2026/mes=01/dia=27/
│       └── wms_situacao_20260127_060000.parquet
└── _metadata/
    └── ano=2026/mes=01/dia=27/
        └── extracao_20260127_060000.json
```

Ver documentação completa em [docs/data-lake/estrutura.md](docs/data-lake/estrutura.md)

---

## Segurança - RLS (Row Level Security)

Como o Data Hub será um SaaS multi-tenant, cada usuário só pode ver seus próprios dados.

### Níveis de Acesso

| Persona | Acesso |
|---------|--------|
| Diretor | Todos os dados, todas as filiais |
| Gerente Regional | Dados da sua região |
| Gerente Filial | Dados da sua filial |
| Comprador | Seus próprios pedidos |
| Vendedor | Seus próprios dados |

### Campos para RLS

| Campo | Tabela | Uso |
|-------|--------|-----|
| `CODEMP` | TGFCAB | Filtro por filial |
| `CODCOMPRADOR` | TGFCAB | Filtro por comprador |
| `CODVEND` | TGFCAB | Filtro por vendedor |
| `CODPARC` | TGFCAB | Filtro por parceiro |

---

## Estrutura do Projeto

```
nexus/
├── README.md
├── docs/
│   ├── data-lake/
│   │   └── estrutura.md                   # Estrutura do Data Lake
│   └── de-para/
│       └── sankhya/
│           ├── compras.md                 # DE-PARA Compras
│           ├── compras-descoberta.md      # Anotações da exploração
│           └── wms.md                     # Mapeamento WMS
└── postman/
    ├── LEIA-ME.md
    └── Nexus-Sankhya-Compras.postman_collection.json
```

---

## Como Começar

1. **Explorar com Postman**
   - Importe a collection em `postman/`
   - Siga o guia em `postman/LEIA-ME.md`

2. **Documentar descobertas**
   - Anote em `docs/de-para/sankhya/compras-descoberta.md`

3. **Próximo passo**
   - Criar script Python de extração

---

## Contato

**Desenvolvido por**: Ítalo Gomes
**Projeto**: MMarra Data Hub

---

*Versão 1.0 - Janeiro 2026*
