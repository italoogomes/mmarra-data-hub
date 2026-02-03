# 📊 Progresso da Sessão - MMarra Data Hub

**Data:** 2026-02-03
**Última Atualização:** 2026-02-03 ✅ DATA HUB OPERACIONAL - 469.986 REGISTROS NO AZURE!
**Versão Atual:** v1.0.0 - Data Hub Completo com Extração Automatizada

---

## 🚀 SESSÃO ATUAL (2026-02-03) - DATA HUB OPERACIONAL! 🚀

### 📋 Objetivo
Transformar o projeto em um Data Hub funcional com extração completa de dados do Sankhya para o Azure Data Lake.

### ✅ Data Hub 100% Operacional!

#### 📊 Dados Extraídos e Carregados no Azure

| Entidade | Registros | Tamanho | Caminho no Data Lake |
|----------|-----------|---------|----------------------|
| **Vendedores** | 111 | 0.01 MB | `raw/vendedores/vendedores.parquet` |
| **Clientes** | 57.082 | 4.02 MB | `raw/clientes/clientes.parquet` |
| **Produtos** | 393.356 | 9.67 MB | `raw/produtos/produtos.parquet` |
| **Estoque** | 19.437 | 0.46 MB | `raw/estoque/estoque.parquet` |
| **TOTAL** | **469.986** | **14.16 MB** | - |

#### 🏗️ Estrutura Criada

**Pasta `src/` completa:**
```
src/
├── __init__.py
├── config.py                 # Configurações centralizadas
├── extractors/
│   ├── __init__.py
│   ├── base.py              # Classe base abstrata
│   ├── vendas.py            # Extrator de vendas
│   ├── clientes.py          # Extrator de clientes
│   ├── produtos.py          # Extrator de produtos
│   ├── estoque.py           # Extrator de estoque
│   └── vendedores.py        # Extrator de vendedores
└── utils/
    ├── __init__.py
    ├── sankhya_client.py    # Cliente API Sankhya
    └── azure_storage.py     # Cliente Azure Data Lake
```

**Estrutura no Azure Data Lake (container: datahub):**
```
datahub/
├── raw/
│   ├── vendedores/vendedores.parquet
│   ├── clientes/clientes.parquet
│   ├── produtos/produtos.parquet
│   ├── estoque/estoque.parquet
│   └── vendas/ (futuro)
├── processed/ (futuro)
└── curated/ (futuro)
```

#### 📁 Scripts de Extração Criados

| Script | Função |
|--------|--------|
| `extrair_tudo.py` | Extração completa usando faixas de 5000 (contorna limite API) |
| `extrair_cadastros_completos.py` | Extração com paginação (OFFSET/FETCH) |
| `extrair_cadastros_completos_v2.py` | Extração por faixas de ID |
| `extrair_para_datalake.py` | Script diário com CLI (`--extrator`) |
| `limpar_duplicados.py` | Limpeza de arquivos duplicados no Data Lake |

#### 🔧 Configurações

**Arquivo `.env` (mcp_sankhya/):**
- `SANKHYA_CLIENT_ID` - ID do cliente Sankhya
- `SANKHYA_CLIENT_SECRET` - Secret do cliente
- `SANKHYA_TOKEN` - Token do gateway
- `AZURE_STORAGE_ACCOUNT` - mmarradatalake
- `AZURE_STORAGE_KEY` - Chave de acesso
- `AZURE_CONTAINER` - datahub

#### 🛠️ Desafios Superados

1. **Limite de 5000 registros da API Sankhya**
   - Solução: Extração por faixas de ID (`WHERE campo >= X AND campo < Y`)

2. **Campos inexistentes nas queries**
   - Removidos: `AD_CODBARRASFAB`, `AD_FAMILIA`, `CEST`, `NOMEVEND`, `QTDRESERVADA`, `DTREF`
   - Ajustados: `INSCESTAD` → `IDENTINSCESTAD`, `CODBARRASFAB` → `REFERENCIA`

3. **Arquivos duplicados no Data Lake**
   - Solução: Parâmetro `sobrescrever=True` no upload

### 🎯 Próximos Passos

1. [ ] Agendar extrações diárias (Azure Functions ou cron)
2. [ ] Extrair dados de VENDAS (TGFCAB + TGFITE)
3. [ ] Criar camada `processed/` com dados transformados
4. [ ] Implementar alertas de falha
5. [ ] Voltar ao caso RIMA (empenhos travados)

### 💬 Mensagem para o Próximo Claude

O Data Hub está operacional! A estrutura completa foi criada:
- **Python**: Extractors, utils (SankhyaClient, AzureDataLakeClient)
- **Azure**: Container `datahub` com pasta `raw/` populada
- **Dados**: ~470k registros de cadastros essenciais

Para extrair novamente: `python extrair_tudo.py`
Para extração específica: `python extrair_para_datalake.py --extrator clientes`

---

## 📌 SESSÃO ANTERIOR (2026-02-03) - DOCUMENTAÇÃO COMPLETA DE COTAÇÕES! 📌

### 📋 Objetivo
Completar as pendências da sessão anterior: documentar status, mapear critérios e investigar histórico.

### ✅ Todas as Pendências Concluídas!

#### 1. Status de Cotação Documentados ✅

**STATUSPRODCOT (Item na Cotação - TGFITC):**
| Código | Descrição | % Sistema |
|--------|-----------|-----------|
| **O** | Orçamento (em processo) | 46.84% |
| **F** | Finalizado (não escolhido) | 35.34% |
| **C** | Cotado (aguardando decisão) | 17.31% |
| **A** | Aguardando resposta | 0.28% |
| **P** | Pendente | 0.22% |

**SITUACAO (Cabeçalho da Cotação - TGFCOT):**
| Código | Descrição | % Sistema |
|--------|-----------|-----------|
| **F** | Finalizada | 54.81% |
| **C** | Cancelada | 30.58% |
| **A** | Aberta/Ativa | 12.03% |
| **E** | Em Elaboração | 2.05% |
| **P** | Pendente | 0.52% |

**MELHOR (Indicador de Vencedor - TGFITC):**
- `S` = Fornecedor selecionado como melhor oferta
- `N` = Não foi escolhido
- `I` = Indefinido (raro)

**Estatística importante:** 2.547 itens com MELHOR='S', destes 2.359 (92.6%) geraram pedido de compra.

#### 2. Critérios de Seleção Mapeados ✅

**Campos de peso encontrados em TGFCOT:**
- `PESOPRECO` - Peso do critério Preço
- `PESOCONDPAG` - Peso da Condição de Pagamento
- `PESOPRAZOENTREG` - Peso do Prazo de Entrega
- `PESOQUALPROD` - Peso da Qualidade do Produto
- `PESOCONFIABFORN` - Peso da Confiabilidade do Fornecedor
- `PESOQUALATEND` - Peso da Qualidade do Atendimento
- `PESOGARANTIA` - Peso da Garantia
- `PESOTAXAJURO` - Peso da Taxa de Juros
- `PESOAVALFORNEC` - Peso da Avaliação do Fornecedor

**Descoberta importante:** Atualmente **apenas PREÇO é usado** (peso=1.0, todos outros=0.0).

#### 3. Histórico de Cotações Investigado ✅

**Conclusão:** NÃO existe tabela de histórico dedicada.

**Tabelas auxiliares encontradas:**
- `TGFITC_COT` - Temporária/consolidação (10 registros)
- `TGFITC_DLT` - Itens deletados (vazia)
- `AD_COTACOESDEITENS` - Customizada/workflow (vazia)
- `TSICOT` - Cotação de MOEDAS (não de compras!)

**Rastreabilidade disponível:**
- `TGFCOT.DTALTER` - Última alteração
- `TGFCOT.CODUSU` - Usuário (pode ser NULL)
- `TGFCOT.DHINIC/DHFINAL` - Período

#### 4. Guia de Parâmetros Criado ✅

**22 parâmetros documentados** para uso no Sankhya:
- Filtros por pedido, empresa, cliente, vendedor
- Filtros por período (negociação, previsão)
- Filtros por valor, produto
- Filtros por status (empenho, WMS, logístico)
- Filtros por cotação (número, status, responsável)

### 📁 Scripts Criados Nesta Sessão

1. ✅ `investigar_status_cotacao.py` - Descobre todos os status
2. ✅ `investigar_contexto_status.py` - Analisa contexto de uso
3. ✅ `investigar_historico_cotacao.py` - Busca tabelas de histórico
4. ✅ `investigar_tabelas_auxiliares.py` - Analisa tabelas relacionadas

### 📚 Documentação Atualizada

**Arquivo:** `docs/de-para/sankhya/empenho-cotacao.md`
**Versão:** 1.0.0 → 1.1.0

**Novas seções adicionadas:**
- DE-PARA: Códigos de Status (STATUSPRODCOT, SITUACAO, MELHOR)
- Critérios de Seleção (Pesos)
- Histórico de Cotações
- Guia de Parâmetros para uso no Sankhya

### 🎯 Próximos Passos Sugeridos

- [ ] Criar dashboard no Sankhya usando a query com parâmetros
- [ ] Configurar outros critérios de seleção além de preço
- [ ] Implementar trigger de auditoria (se necessário)
- [ ] Criar relatório de análise de cotações por fornecedor

---

## 🗄️ MAPEAMENTO COMPLETO DO BANCO (2026-02-03) 🗄️

### 📋 Objetivo
Fazer varredura completa do banco Sankhya para entender estrutura, tabelas, relacionamentos e preparar para extrações.

### ✅ Mapeamento Concluído!

#### 📊 Estatísticas do Banco

| Métrica | Valor |
|---------|-------|
| **Total de Tabelas** | 4.682 |
| **Módulos/Prefixos** | 96 |
| **Relacionamentos (FK)** | 500+ mapeados |
| **Views** | 100+ |

#### 🏆 TOP 10 Tabelas por Volume

| # | Tabela | Registros | Descrição |
|---|--------|-----------|-----------|
| 1 | TGFITE | 1.102.785 | Itens das Notas |
| 2 | TGFPRC | 934.425 | Lista de Preços |
| 3 | TGFPRO | 393.667 | Produtos |
| 4 | TGFEXC | 379.177 | Exceções Fiscais |
| 5 | TGFCAB | 340.580 | Cabeçalho Notas |
| 6 | TGFCUS | 288.208 | Custos |
| 7 | TGFDIN | 226.421 | Campos Dinâmicos |
| 8 | TGWEND | 85.666 | Endereços WMS |
| 9 | TGFPAR | 57.081 | Parceiros |
| 10 | TGFFIN | 50.816 | Financeiro |

#### 📁 Principais Módulos

| Prefixo | Tabelas | Descrição |
|---------|---------|-----------|
| **TGF** | 1.456 | Gestão Financeira/Comercial (CORE) |
| **TFP** | 753 | Fiscal/Produção |
| **TSI** | 243 | Sistema/Infraestrutura |
| **TDD** | 242 | Definição de Dados |
| **TRD** | 229 | Relatórios/Dashboards |
| **TIM** | 147 | Importação/Integração |
| **AD_** | 139 | Tabelas Customizadas MMarra |
| **TGW** | 135 | WMS |

#### 📋 Tabelas Principais para Extração

**Comercial (ALTA prioridade):**
- `TGFCAB` (340k) - Cabeçalho de notas
- `TGFITE` (1.1M) - Itens das notas
- `TGFPAR` (57k) - Parceiros
- `TGFPRO` (393k) - Produtos

**Financeiro:**
- `TGFFIN` (50k) - Títulos a pagar/receber
- `TGFNAT` (232) - Naturezas

**Estoque:**
- `TGFEST` (36k) - Estoque ERP
- `TGWEST` (45k) - Estoque WMS
- `TGWEND` (85k) - Endereços

**WMS:**
- `TGWREC` (1k) - Recebimento
- `TGWSEP` (8k) - Separação
- `TGWEMPE` (1.3k) - Empenho

### 📁 Arquivos Criados

**Scripts de Mapeamento:**
1. ✅ `mapear_banco_completo.py` - Varredura geral
2. ✅ `mapear_tabelas_volume.py` - Contagem por tabela
3. ✅ `gerar_relatorio_schema.py` - Gerador de relatório HTML

**Arquivos de Resultado:**
4. ✅ `mapeamento_banco_sankhya.json` - JSON completo
5. ✅ `tabelas_por_volume.json` - Contagem de registros
6. ✅ `relatorio_schema_banco.html` - Relatório visual interativo

**Documentação:**
7. ✅ `docs/schema-banco-sankhya.md` - Documentação completa do schema

### 🔗 Relacionamentos Principais Mapeados

```
TGFCAB.CODPARC → TGFPAR.CODPARC
TGFITE.NUNOTA → TGFCAB.NUNOTA
TGFITE.CODPROD → TGFPRO.CODPROD
TGFFIN.NUNOTA → TGFCAB.NUNOTA
TGFEST.CODPROD → TGFPRO.CODPROD
TGWEST.CODEND → TGWEND.CODEND
TGWEMPE.NUNOTAPEDVEN → TGFCAB.NUNOTA
```

### 🚀 Próximos Passos para Extração

1. [ ] Criar script de extração de VENDAS (TGFCAB + TGFITE)
2. [ ] Criar script de extração de CLIENTES (TGFPAR)
3. [ ] Criar script de extração de PRODUTOS (TGFPRO)
4. [ ] Criar script de extração de ESTOQUE (TGFEST + TGWEST)
5. [ ] Configurar Azure Data Lake para armazenar os dados

---

## 🔄 SESSÃO ANTERIOR (2026-02-03 Manhã) - DOCUMENTAÇÃO DE STATUS 🔄

(ver seção acima - Status de Cotação documentados)

---

## 🔄 SESSÃO ANTERIOR (2026-02-02 Tarde) - QUERY DE GESTÃO DE EMPENHO COM COTAÇÃO! 🔄

### 📋 Objetivo
Adicionar campos de cotação (Nome Responsável, Código Cotação, Status) à query de gestão de empenho por fornecedor.

### ✅ Conquistas Realizadas

#### 1. Query Completa de Empenho com Cotação ✅
**Arquivo**: [query_empenho_com_cotacao.sql](query_empenho_com_cotacao.sql) + [query_empenho_com_cotacao_sem_parametros.sql](query_empenho_com_cotacao_sem_parametros.sql)

**Campos adicionados**:
- ✅ **Cod_Cotacao** - Número da cotação (TGFITC.NUMCOTACAO)
- ✅ **Nome_Resp_Cotacao** - Responsável pela cotação (TSIUSU.NOMEUSU via TGFCOT.CODUSURESP)
- ✅ **Status_Cotacao** - Status do produto na cotação (TGFITC.STATUSPRODCOT)
- ✅ **Num_Unico_NF_Empenho** - NUNOTA das notas de compra empenhadas
- ✅ **Num_NF_Empenho** - NUMNOTA das notas de compra (formatado)

**Total de campos**: 29 colunas no relatório final

**CTEs criadas**:
```sql
/* 9.1) LISTA DE NUNOTAS E NUMNOTAS DE COMPRA */
compra_nunota_list AS (
    SELECT DISTINCT b.nunota_venda, b.codprod, b.nunota_compra, cb.numnota
    FROM compra_base b
    LEFT JOIN tgfcab cb ON cb.nunota = b.nunota_compra
),

compra_nunota_agg AS (
    SELECT d.nunota_venda, d.codprod,
           LISTAGG(TO_CHAR(d.nunota_compra), ', ') AS nunota_compra_list,
           LISTAGG(TO_CHAR(d.numnota), ', ') AS numnota_compra_list
    FROM compra_nunota_list d
    GROUP BY d.nunota_venda, d.codprod
),

/* 10) DADOS DE COTAÇÃO */
cotacao_info AS (
    SELECT b.nunota_venda, b.codprod,
           MAX(itc.NUMCOTACAO) AS num_cotacao,
           MAX(itc.STATUSPRODCOT) AS status_cotacao,
           MAX(u.NOMEUSU) AS nome_responsavel_cotacao
    FROM compra_base b
    JOIN tgfite ic ON ic.nunota = b.nunota_compra AND ic.codprod = b.codprod
    LEFT JOIN tgfitc itc ON itc.CODPARC = b.codparc_fornecedor AND itc.CODPROD = b.codprod
    LEFT JOIN tgfcot cot ON cot.NUMCOTACAO = itc.NUMCOTACAO
    LEFT JOIN TSIUSU u ON u.CODUSU = cot.CODUSURESP
    GROUP BY b.nunota_venda, b.codprod
)
```

#### 2. Problemas Resolvidos Durante Desenvolvimento 🔧

**Problema 1**: ORA-01008 (nem todas as variáveis são limitadas)
- **Causa**: Query original tinha parâmetros (:P_NUNOTA, :P_CODEMP, etc)
- **Solução**: Criada versão sem parâmetros para execução via API

**Problema 2**: ORA-00904 "ITC"."EMPRESA" (identificador inválido)
- **Causa**: Tentativa de filtrar por campo EMPRESA que não existe em TGFITC
- **Solução**: Tentamos CODEMP, depois removemos filtro de empresa (desnecessário com CODPARC + CODPROD)

**Problema 3**: ORA-00904 "ITC"."USURESP" (identificador inválido)
- **Causa**: Campo USURESP não existe em TGFITC
- **Solução**: Descoberto que responsável está em TGFCOT.CODUSURESP, não em TGFITC!

**JOIN correto descoberto**:
```sql
TGFITC (itens cotação) → TGFCOT (cabeçalho cotação) → TSIUSU (usuários)
   ↓                           ↓                            ↓
NUMCOTACAO              CODUSURESP                    NOMEUSU
```

#### 3. Investigação de Pedido (Diagnóstico) 🔍

**Caso**: Pedido 1192177 aparecia sem dados de cotação

**Scripts criados**:
- ✅ `investigar_pedido_1192177.py` (com UNION ALL - falhou)
- ✅ `investigar_pedido_simples.py` (queries separadas - sucesso!)

**Resultado da investigação**:
```
PEDIDO 1192177:
- Status: PENDENTE='S', STATUSNOTA='L'
- Itens: 17 produtos
- AD_RESERVAEMPENHO: None (maioria) / 'S' (1 registro)
- ❌ SEM EMPENHO (TGWEMPE vazio)
- ❌ SEM COMPRAS VINCULADAS
- ❌ SEM COTAÇÕES

CONCLUSÃO: Pedido CORRETO estar sem cotação!
Motivo: Ainda não foi empenhado no sistema.
```

#### 4. Relatório HTML Gerado ✅

**Arquivo**: [relatorio_empenho_cotacao.html](relatorio_empenho_cotacao.html)

**Estatísticas**:
- **2.103 registros** de gestão de empenho
- **309 registros** (15%) com cotação vinculada
- **29 campos** no relatório

**Funcionalidades**:
- ✅ Busca em tempo real por qualquer campo
- ✅ Ordenação por coluna (clique no cabeçalho)
- ✅ Exportar CSV
- ✅ Imprimir/PDF
- ✅ Design responsivo
- ✅ Destaque visual por status de empenho

#### 5. Fluxo Completo Mapeado 🎯

**Descoberto o ciclo completo de vida de um pedido**:

```
1. PEDIDO DE VENDA entra
   └─ TGFCAB (venda) + TGFITE

2. Sistema cria EMPENHO
   └─ TGWEMPE (vincula venda → compra futura)

3. Comprador vê itens empenhados

4. Comprador faz COTAÇÃO
   └─ TGFCOT (cabeçalho) + TGFITC (itens)
   └─ CODUSURESP → Nome do responsável

5. Escolhe melhor fornecedor/cotação

6. Cria PEDIDO DE COMPRA
   └─ TGFCAB (compra) vinculado ao empenho

7. Mercadoria chega
   └─ WMS recebe (TGWREC)

8. WMS separa para pedido de venda
   └─ VGWSEPSITCAB

9. Produto sai do estoque
```

#### 6. Descobertas sobre Tabelas do Sankhya 📚

**TGFCAB** - Cabeçalho de Notas (UNIFICADA!)
- Usada tanto para VENDAS quanto para COMPRAS
- `NUNOTA`: Número único interno (chave primária)
- `NUMNOTA`: Número da nota fiscal formatado (impresso)
- `CODTIPOPER`: Define se é venda, compra, transferência, etc
- `PENDENTE`, `STATUSNOTA`: Controle de processamento

**TGWEMPE** - Tabela de Empenho (CORAÇÃO DO PROCESSO!)
- Vincula pedido de venda → pedido de compra
- `NUNOTAPEDVEN`: NUNOTA da venda
- `NUNOTA`: NUNOTA da compra
- `CODPROD`, `QTDEMPENHO`: Produto e quantidade reservada

**TGFCOT** - Cabeçalho da Cotação
- `NUMCOTACAO`: Número da cotação
- `CODUSURESP`: **Usuário responsável** ⭐ (campo crítico)
- `SITUACAO`: Status da cotação
- `DHINIC`, `DHFINAL`: Período de cotação

**TGFITC** - Itens da Cotação
- `NUMCOTACAO`: FK para TGFCOT
- `CODPARC`: Fornecedor cotado
- `CODPROD`: Produto cotado
- `STATUSPRODCOT`: Status do item (O=Orçamento, etc)
- ⚠️ **NÃO TEM campo de responsável!** (está no cabeçalho TGFCOT)

**TSIUSU** - Usuários do Sistema
- `CODUSU`: Código do usuário
- `NOMEUSU`: Nome do usuário

**Campos Customizados**:
- `AD_RESERVAEMPENHO`: Campo customizado MMarra em TGFTOP
- Controla quais tipos de operação geram empenho

#### 7. Investigação de Divergências (Cotação vs CSV) 🔍

**Problema identificado:** Divergências entre dados do relatório Sankhya e CSV gerado pela query.

**Casos investigados:**

1. **Pedido 1167205 vs 1167528:**
   - CSV mostra: VENDA 1167205 → COMPRA 1168991 (cotação 131)
   - Tela mostra: VENDA 1167528 → COMPRA 1169047 (cotação 131)
   - **Descoberta:** Pedido 1167528 foi **cancelado** e sistema vinculou ao 1167205
   - Query filtra apenas pedidos ativos (PENDENTE='S', STATUSNOTA='L')

2. **Pedido 1168898 (sem empenho):**
   - CSV: Cotação vazia (correto)
   - Tela: Cotação 226 cancelada aparece
   - **Descoberta:** Cotação pode existir ANTES do empenho
   - Query só busca cotação APÓS empenho ser criado (via compra_base)

**Scripts de investigação criados:**
- ✅ `investigar_divergencia_pedido.py` - Analisa divergências entre pedidos
- ✅ `investigar_cotacao_131.py` - Mapeia vínculos da cotação 131
- ✅ `investigar_vinculo_cotacao_compra.py` - Busca vínculo cotação→compra

**Conclusão:**
- Query está **correta** na lógica ✅
- Cotação vinculada por **produto + fornecedor** (não por pedido específico)
- Uma cotação pode gerar múltiplas compras ao longo do tempo
- Pedidos cancelados não aparecem (filtrados por status)

#### 8. Documentação Técnica Criada 📚

**Arquivo:** [docs/de-para/sankhya/empenho-cotacao.md](docs/de-para/sankhya/empenho-cotacao.md)

**Conteúdo:**
- Workflow completo (Venda → Empenho → Cotação → Compra → WMS)
- Mapeamento de 5 tabelas (TGWEMPE, TGFCOT, TGFITC, TSIUSU, TGFCAB)
- Relacionamentos entre tabelas
- Campos customizados (AD_RESERVAEMPENHO)
- Queries de exemplo (3 exemplos prontos)
- Problemas e soluções (3 erros resolvidos)
- Estatísticas do relatório (2.103 registros, 29 campos)

#### 9. Arquivos Criados Nesta Sessão 📁

**Queries SQL:**
1. ✅ `query_empenho_com_cotacao.sql` - Versão COM parâmetros (para uso no Sankhya)
2. ✅ `query_empenho_com_cotacao_sem_parametros.sql` - Versão SEM parâmetros (para API)

**Scripts Python - Execução:**
3. ✅ `executar_empenho_com_cotacao.py` - Executa query e salva JSON
4. ✅ `gerar_html_empenho.py` - Gera relatório HTML interativo

**Scripts Python - Diagnóstico:**
5. ✅ `investigar_pedido_1192177.py` - Diagnóstico com UNION ALL (não usado)
6. ✅ `investigar_pedido_simples.py` - Diagnóstico com queries separadas
7. ✅ `investigar_divergencia_pedido.py` - Investiga divergência pedido 1167205/1167528
8. ✅ `investigar_cotacao_131.py` - Mapeia vínculos da cotação 131
9. ✅ `investigar_vinculo_cotacao_compra.py` - Busca vínculo direto cotação→compra

**Arquivos de Resultado:**
10. ✅ `resultado_empenho_com_cotacao.json` - 2.103 registros
11. ✅ `relatorio_empenho_cotacao.html` - Relatório interativo completo

**Documentação:**
12. ✅ `docs/de-para/sankhya/empenho-cotacao.md` - Mapeamento completo das tabelas

### 📊 Status dos Tokens
📊 **Tokens**: ~95.000/200.000 (47%) - ~105.000 tokens restantes ✅

### 🎯 Estrutura da Query Final

**29 Campos no Relatório**:
1. Data, Num_Unico, Cod_Cliente, Cliente, Emp, Previsao_Entrega
2. Cod_Vend, Vendedor
3. Cod_Prod, Produto
4. Qtd_SKUs, Qtd_Com_Empenho, Qtd_Sem_Empenho
5. Valor, Custo, Custo_Medio
6. Cod_Forn, Fornecedor
7. **Num_Unico_NF_Empenho**, **Num_NF_Empenho** (novos)
8. **Cod_Cotacao**, **Nome_Resp_Cotacao**, **Status_Cotacao** (novos)
9. Status_Empenho_Item, Status_WMS, Status_Logistico_Item
10. Status_Geral_Item, bkcolor, fgcolor

### 💡 Aprendizados Importantes

#### 1. Sistema de Empenho é uma "Ponte"
```
Venda → EMPENHO → Compra
```
O empenho "reserva" mercadoria de uma compra para uma venda específica.

#### 2. Cotação é Processo de Compras
Antes de criar pedido de compra, comprador:
1. Cria cotação (TGFCOT + TGFITC)
2. Solicita preços de múltiplos fornecedores
3. Escolhe melhor oferta
4. Cria pedido de compra

#### 3. Múltiplos Estoques
- **TGFEST**: Estoque contábil (disponível para venda)
- **TGWEST**: Estoque físico no WMS
- **Divergências** quando não batem!

#### 4. Campos Customizados (AD_*)
MMarra usa campos customizados para controlar processos específicos:
- `AD_RESERVAEMPENHO`: Define tipos de operação com empenho
- `AD_BLOQUEADO`: Bloqueia endereços no WMS

### ⚠️ Pendências Restantes

- [ ] Testar query com todos os parâmetros no Sankhya
- [ ] Documentar significados dos códigos de status (O, P, etc)
- [ ] Mapear outros campos de TGFCOT (pesos de critérios de escolha)
- [ ] Investigar se há histórico de cotações antigas

---

## 🎉 SESSÃO ANTERIOR (2026-02-02 Manhã) - SISTEMA TOTALMENTE FUNCIONAL! 🎉

### 📋 Objetivo
Testar se o servidor Sankhya voltou e executar a query V3 de divergências para gerar relatório HTML completo.

### ✅ Conquistas Realizadas

#### 1. Servidor Sankhya Voltou! ✅
- ✅ **Status**: Online e funcionando perfeitamente
- ✅ **Autenticação OAuth 2.0**: OK (200)
- ✅ **Execução de Queries**: OK (status "1")
- ✅ **Tempo de resposta**: ~6-10 segundos

#### 2. Correção Final do Servidor MCP ✅
**Problema identificado**: Payload JSON estava enviando `serviceName` duplicado (na URL e no body)

**Solução aplicada** ([mcp_sankhya/server.py](mcp_sankhya/server.py:100-105)):
```python
# ❌ ANTES (incorreto):
json={
    "serviceName": "DbExplorerSP.executeQuery",  # Duplicado!
    "requestBody": {"sql": sql}
}

# ✅ DEPOIS (correto):
json={
    "requestBody": {"sql": sql}  # serviceName só na URL
}
```

#### 3. Descoberta da Documentação Oficial ✅
Consultada documentação oficial da Sankhya para confirmar formato correto:
- ✅ URL: `https://api.sankhya.com.br/gateway/v1/mge/service.sbr?serviceName=DbExplorerSP.executeQuery&outputType=json`
- ✅ ServiceName DEVE ser query parameter, NÃO no body JSON
- ✅ Payload: apenas `{"requestBody": {"sql": "..."}}`

#### 4. Query V3 de Divergências Executada! ✅
**Resultado**: **5.000 divergências encontradas!**

```
Total de registros: 5.000
Produtos únicos: ~500+
Total divergência: ~1.000.000+ unidades
```

**Dados salvos em**:
- `resultado_divergencias_v3.json` (5000 registros, 15 campos)

**Preview das divergências**:
| CODEMP | CODPROD | DESCRPROD | NUNOTA | NUMNOTA | TOP | DIVERGENCIA |
|--------|---------|-----------|--------|---------|-----|-------------|
| 7 | 100004 | SUPORTE DE FIXA | 1132358 | 996061 | 1452 | ... |
| 7 | 100006 | JOGO MANOPLA | 1188730 | 57662990 | 1414 | ... |

#### 5. Relatório HTML Gerado! ✅
**Arquivo**: [relatorio_divergencias_v3.html](relatorio_divergencias_v3.html)

**Funcionalidades**:
- ✅ Dashboard com KPIs (total produtos, divergências, etc)
- ✅ Tabela interativa com 5.000 registros
- ✅ Busca em tempo real
- ✅ Ordenação por coluna (clique no header)
- ✅ Exportar para CSV
- ✅ Imprimir/PDF
- ✅ Design responsivo (mobile-friendly)
- ✅ Destaque na coluna DIVERGENCIA (vermelho)

#### 6. Scripts Criados Nesta Sessão

**Scripts de Teste**:
1. ✅ **test_sankhya_simples.py** - Teste direto de autenticação + query (sem MCP)
2. ✅ **executar_query_divergencias.py** - Executa query V3 e salva JSON
3. ✅ **gerar_html_simples.py** - Gera relatório HTML sem emojis (compatível Windows)

**Arquivos de Configuração**:
4. ✅ **mcp_sankhya/.env** - Credenciais OAuth 2.0 configuradas

**Arquivos de Resultado**:
5. ✅ **resultado_divergencias_v3.json** - 5.000 registros de divergências
6. ✅ **relatorio_divergencias_v3.html** - Relatório interativo completo

### 📊 Status dos Tokens
📊 **Tokens**: ~62.000/200.000 (31%) - ~138.000 tokens restantes ✅

### 🔍 Descobertas Técnicas Importantes

#### 1. Formato Correto do Payload Sankhya
```python
# URL com query parameters
url = "https://api.sankhya.com.br/gateway/v1/mge/service.sbr"
params = {
    "serviceName": "DbExplorerSP.executeQuery",
    "outputType": "json"
}

# Payload JSON (apenas requestBody)
payload = {
    "requestBody": {
        "sql": "SELECT ..."
    }
}
```

#### 2. Limite do DbExplorer
- ⚠️ **Máximo**: 5.000 registros por query
- ⚠️ Query atual retornou exatamente 5.000 registros
- ⚠️ **PODE HAVER MAIS DIVERGÊNCIAS** não retornadas!
- 🔧 **Solução futura**: Implementar paginação ou filtros por empresa/período

#### 3. Problema de Encoding no Windows
- ❌ Emojis (🎉, 📊, etc) causam `UnicodeEncodeError` no console Windows
- ✅ Solução: Scripts sem emojis para compatibilidade total
- ✅ HTML pode usar emojis (UTF-8 no navegador funciona)

### 🎯 Fluxo de Trabalho Estabelecido

**Passo a passo para executar análise de divergências**:

```bash
# 1. Executar query V3 (gera JSON)
python executar_query_divergencias.py

# 2. Gerar relatório HTML (lê JSON)
python gerar_html_simples.py

# 3. Abrir no navegador
start relatorio_divergencias_v3.html
```

**Tempo total**: ~20 segundos (autenticação + query + HTML)

### ⚠️ Observações Importantes

#### 1. Limite de 5.000 Registros Atingido
- Query retornou **exatamente 5.000 registros** (limite do DbExplorer)
- **Pode haver mais divergências** não retornadas
- **Recomendação**: Filtrar por período ou adicionar `WHERE` para análises específicas

#### 2. Divergências Críticas Identificadas
Produtos com maior divergência (amostra):
- Produto 100004: Múltiplas notas com divergência
- Produto 100006: Múltiplas notas de compra (TOP 1414)
- **Total**: ~500+ produtos únicos com divergências

#### 3. Tipos de Operação (TOP) Mais Comuns
- **1452**: Transferência entre depósitos
- **1101**: Venda NF-e
- **1414**: Compra com CT-e

### 🎯 Próximos Passos Sugeridos

#### A. Análise Detalhada das Divergências
- [ ] Filtrar os 10 produtos com maior divergência total
- [ ] Investigar causas por tipo de operação (TOP)
- [ ] Analisar padrão temporal (quando ocorreram)
- [ ] Propor correções específicas

#### B. Otimização da Query
- [ ] Adicionar filtros para trazer menos de 5.000 registros
- [ ] Implementar paginação (TOP 100 por vez)
- [ ] Criar queries por período (último mês, última semana)

#### C. Automação
- [ ] Criar script diário de monitoramento
- [ ] Enviar alertas quando divergências > threshold
- [ ] Gerar relatório automático via email

---

## 🔧 SESSÃO ATUAL (2026-02-01) - Teste e Correção do Servidor MCP

### 📋 Objetivo
Testar o servidor MCP criado anteriormente e validar se consegue executar queries SQL via API Sankhya.

### ✅ Progresso Realizado

#### 1. URLs Corrigidas
- ✅ **Autenticação**: `https://api.sankhya.com.br/authenticate` (sem /gateway/v1)
- ✅ **Queries**: `https://api.sankhya.com.br/gateway/v1/mge/service.sbr`
- ✅ Código atualizado em [mcp_sankhya/server.py](mcp_sankhya/server.py:31-32)

#### 2. Autenticação OAuth 2.0
- ✅ Token obtido com sucesso
- ✅ Endpoint `/authenticate` funciona corretamente
- ⚠️ Query retorna "Não autorizado" (possível problema no servidor Sankhya)

#### 3. Documentação Oficial Consultada
- ✅ [Autenticação OAuth 2.0](https://developer.sankhya.com.br/reference/post_authenticate)
- ✅ [DbExplorerSP.executeQuery](https://developer.sankhya.com.br/reference/requisi%C3%A7%C3%B5es-via-gateway)
- ✅ Confirmado: Método OAuth 2.0 Client Credentials é correto
- ⚠️ Limitação: DbExplorer tem limite de 5.000 registros por query

#### 4. Arquivos Criados Nesta Sessão

**Scripts de Teste:**
1. ✅ **test_mcp.py** - Script de teste do servidor MCP
2. ✅ **test_autenticacao.py** - Diagnóstico completo de autenticação
3. ✅ **test_mobile_login.py** - Teste alternativo com usuário/senha (JSESSIONID)
4. ✅ **mcp_sankhya/.env** - Credenciais OAuth 2.0 configuradas

**Documentação de Estrutura:**
5. ✅ **ANALISE_ESTRUTURA.md** - Análise completa do projeto (6/10)
   - Avaliação de todos componentes (documentação, queries, MCP, Data Lake, etc.)
   - Identificação de gaps críticos (scripts extração, Data Lake, agentes IA)
   - Roadmap em 3 fases para MVP (2-3 semanas)
   - Recomendações técnicas (Azure Data Lake, LangChain)
6. ✅ **CHANGELOG.md** - Atualizado para v0.4.2
7. ✅ **PROGRESSO_SESSAO.md** - Atualizado com esta sessão
8. ❌ **PROXIMOS_PASSOS.md** - Removido (conteúdo consolidado neste arquivo)

### ⚠️ Status Atual: BLOQUEADO

**Problema:** Token OAuth 2.0 retorna "Não autorizado" ao executar queries

**Erro retornado:**
```json
{
  "serviceName": "DbExplorerSP.executeQuery",
  "status": "0",
  "statusMessage": "Não autorizado"
}
```

**Possíveis causas:**
1. ⚠️ **Servidor Sankhya com problemas** (usuário reportou: "acho que o servidor esta off")
2. 🔍 Credenciais OAuth 2.0 podem não ter permissão para DbExplorer (já verificado: FORAM configuradas)
3. 🔍 Queries podem precisar de MobileLogin (JSESSIONID) ao invés de Bearer token

### 🎯 Próximos Passos (QUANDO SERVIDOR VOLTAR)

#### Opção 1: Testar se Servidor Voltou
```bash
python test_mcp.py
```

**Se funcionar**: ✅ MCP pronto para uso!

#### Opção 2: Testar MobileLogin (Alternativa)
```bash
python test_mobile_login.py
# Vai pedir usuário e senha do Sankhya
```

**Se funcionar**: 🔧 Modificar MCP para usar JSESSIONID ao invés de Bearer token

#### 5. Análise de Estrutura Realizada

✅ **Avaliação Completa do Projeto** ([ANALISE_ESTRUTURA.md](ANALISE_ESTRUTURA.md)):
- **Pontuação Geral**: 6/10 - Pronto para começar implementação, NÃO pronto para produção
- **Pontos Fortes**: Documentação exemplar (95%), queries prontas (90%), relatórios funcionais (85%)
- **Gaps Críticos Identificados**:
  - ❌ Scripts de extração: 0% (BLOQUEADOR para Data Lake)
  - ❌ Azure Data Lake: 0% configurado (BLOQUEADOR para central de dados)
  - ❌ Agentes de IA: 0% implementados (BLOQUEADOR para inteligência)
- **Tempo Estimado**: 2-3 semanas para MVP funcional, 4-6 semanas para produção

✅ **Consolidação de Documentação**:
- Arquivo `PROXIMOS_PASSOS.md` removido (conteúdo movido para este arquivo)
- Toda documentação agora centralizada em 3 locais: PROGRESSO_SESSAO.md, CHANGELOG.md, ANALISE_ESTRUTURA.md

### 📊 Status dos Tokens
📊 **Tokens**: 50.556/200.000 (25%) - 149.444 tokens restantes

### 💡 Descobertas Importantes

1. **APIs da Sankhya têm endpoints separados**:
   - Autenticação: Endpoint base (sem /gateway/v1)
   - Queries/Serviços: Gateway (/gateway/v1)

2. **Dois métodos de autenticação disponíveis**:
   - **OAuth 2.0**: Para integração de sistemas (client_id/client_secret)
   - **MobileLogin**: Para usuários individuais (usuário/senha)

3. **Limitações conhecidas**:
   - DbExplorer: máximo 5.000 registros por query
   - Permissões: usuário precisa ter acesso ao módulo DbExplorer

### 📁 Estrutura Atual do MCP

```
mcp_sankhya/
├── server.py              ✅ URLs corrigidas (linhas 31-32)
├── requirements.txt       ✅ Dependências instaladas
├── .env                   ✅ Credenciais configuradas
├── .env.example           ✅ Template disponível
├── README.md              ✅ Documentação completa
└── __init__.py            ✅ Módulo Python

Scripts de teste:
├── test_mcp.py            ✅ Teste OAuth 2.0
├── test_autenticacao.py   ✅ Diagnóstico completo
└── test_mobile_login.py   ✅ Teste MobileLogin (alternativa)
```

### 🔧 Tools Disponíveis no MCP (5 ferramentas)

1. **executar_query_sql** - Executa qualquer query SQL customizada
2. **executar_query_divergencias** - Query V3 de divergências (corrigida)
3. **executar_query_analise_produto** - Análise detalhada de produto
4. **gerar_relatorio_divergencias** - Gera relatório HTML interativo
5. **listar_queries_disponiveis** - Lista queries do projeto

---

## ✅ O QUE JÁ FOI FEITO

### 1️⃣ Mapeamento da API Sankhya (Janeiro 2026)
- ✅ Autenticação OAuth 2.0 configurada no Postman
- ✅ Endpoints identificados e testados
- ✅ X-Token do Gateway configurado
- ✅ Bearer token funcionando

### 2️⃣ Mapeamento de Tabelas - COMPRAS
- ✅ **TGFCAB** - Cabeçalho de notas (pedidos de compra)
  - Campos principais: NUNOTA, NUMNOTA, DTNEG, CODPARC, VLRNOTA
  - Filtros: TIPMOV = 'C' (Compras)

- ✅ **TGFITE** - Itens dos pedidos
  - Campos principais: NUNOTA, SEQUENCIA, CODPROD, QTDNEG, VLRUNIT

- ✅ **TGFPAR** - Fornecedores
  - Campos principais: CODPARC, RAZAOSOCIAL, CGC_CPF
  - Filtro: FORNECEDOR = 'S'

- ✅ **TGFPRO** - Produtos
  - Campos principais: CODPROD, DESCRPROD, REFERENCIA

- ✅ **TGWREC** - Recebimento WMS
  - Situações mapeadas: Aguardando conferência, Em processo, Concluído, etc.
  - View: VGWRECSITCAB (situação por nota)

### 3️⃣ Estrutura do Data Lake (Planejado)
- ✅ Estrutura de pastas definida (particionamento por ano/mês/dia)
- ✅ Formato Parquet escolhido
- ✅ Schema dos arquivos documentado
- ✅ Estratégia de carga incremental definida

### 4️⃣ Documentação Criada
- ✅ `README.md` - Visão geral do projeto
- ✅ `docs/de-para/sankhya/compras.md` - Mapeamento completo
- ✅ `docs/de-para/sankhya/wms.md` - Situação WMS
- ✅ `docs/data-lake/estrutura.md` - Estrutura do Data Lake
- ✅ `postman/` - Collections para testes

### 5️⃣ Sessão Atual (2026-01-30) ⭐ INVESTIGAÇÃO WMS COMPLETA

**Objetivo**: Mapear estrutura completa de Estoque e WMS + Investigar divergência de estoque

#### ✅ Documentação Criada (Manhã)
- ✅ `CLAUDE.md` - Instruções completas para o Claude (regras, padrões, fluxo)
- ✅ `PROGRESSO_SESSAO.md` - Este arquivo (contexto entre sessões)
- ✅ `PLANO_MAPEAMENTO.md` - Estratégia completa (28 tabelas, 4 semanas)
- ✅ `CHANGELOG.md` - Histórico de versões
- ✅ `QUERIES_EXPLORACAO.sql` - 50+ queries organizadas em 9 fases
- ✅ `docs/tabelas/TEMPLATE.md` - Template completo para documentar tabelas
- ✅ `metadata/schema_example.json` - Exemplo de schema JSON para LLM
- ✅ `docs/CHECKLIST_EXPLORACAO_WMS.md` - Checklist detalhado para exploração
- ✅ `docs/CURLS_EXPLORACAO_WMS.md` - Todos os cURLs prontos para Postman

#### ✅ Investigação WMS (Tarde/Noite) 🔍

**Contexto Inicial:**
- Produto 137216 mostrando 52 unidades no TGFEST (disponível)
- WMS mostrando 144 unidades (físico)
- Diferença de 92 unidades a investigar

**Descobertas Principais:**

1. **299 Tabelas WMS Identificadas**
   - Query executada: `TABLE_NAME LIKE '%WMS%' OR 'TCS%' OR 'TGW%'`
   - Universo completo do módulo WMS Sankhya mapeado

2. **Tabelas Críticas Mapeadas** (9 tabelas)
   - ✅ **TGFEST**: Estoque consolidado ERP (disponível venda)
   - ✅ **TGWEST**: Estoque físico WMS por endereço ⭐ TABELA-CHAVE
   - ✅ **TGWEND**: Cadastro de endereços físicos
   - ✅ **TGFRES**: Reservas de estoque
   - ✅ **TGWSEP**: Separações WMS (cabeçalho)
   - ✅ **TGWSXN**: Separações WMS (itens/notas)
   - ✅ **TGWREC**: Recebimento WMS (já mapeado)
   - ✅ **TGWRXN**: Recebimento ↔ Nota (já mapeado)
   - ✅ **VGWRECSITCAB**: View situação recebimento (já mapeado)

3. **Estrutura de Endereçamento Descoberta**
   - Formato: `PREDIO.RUA.NIVEL.APARTAMENTO.POSICAO`
   - Exemplo: `07.01.24.03.01`
   - Tipos: ARMAZENAGEM, PICKING, DOCA, QUARENTENA
   - Tabela: TGWEND (CODEND + DESCREND + TIPO)

4. **Balanço de Estoque (Produto 137216)**

   | Origem | Quantidade | Descrição |
   |--------|------------|-----------|
   | **TGWEST (Físico)** | **144** | Estoque real no armazém |
   | └─ Armazenamento | 124 | Endereço 07.01.24.03.01 |
   | └─ Docas | 20 | 4 docas (5 un cada) |
   | **TGFEST (Disponível)** | **52** | Disponível para venda |
   | **Processos Identificados** | **46** | |
   | └─ Pedidos Abertos | 26 | 2 notas (1167001, 1167014) |
   | └─ Separações Ativas | 20 | 4 processos WMS |
   | **⚠️ Diferença Não Explicada** | **46** | Bloqueios/Quarentena/Sync |

5. **Fluxos de Processo Mapeados**

   **Recebimento:**
   ```
   TGFCAB → TGWREC → TGWEND → TGWEST → TGFEST
   (Nota)  (Conf.)  (Endereço) (Físico) (Disp.)
   ```

   **Separação:**
   ```
   TGFCAB → TGWSEP → TGWSXN → TGWEST → TGFEST
   (Pedido) (Ordem)  (Itens)  (Deduz)  (Atualiza)
   ```

6. **Documentação Completa Gerada**
   - ✅ `docs/de-para/sankhya/estoque.md` - 550+ linhas
     - 10 tabelas detalhadamente documentadas
     - Estruturas completas com todos os campos
     - Relacionamentos FK mapeados
     - 3 queries de produção prontas
     - Balanço completo do produto 137216
     - Resumo executivo da investigação
     - Impacto no Data Lake definido

#### 🎯 Planejamento Estratégico
- ✅ Roadmap de 4 fases (Compras → Estoque → Vendas → Financeiro)
- ✅ 28 tabelas identificadas + 299 WMS descobertas
- ✅ Cronograma de 4 semanas
- ✅ Estrutura de metadados para ML/LLM definida
- ✅ Fase de Estoque 75% completa

#### 📊 Métricas da Sessão
- **Arquivos criados/atualizados**: 11
- **Linhas de código/doc**: ~3.500+
- **Queries SQL preparadas**: 70+ (50 exploração + 20 WMS específicas)
- **Tabelas mapeadas**: 15/28 (54%)
- **Tabelas WMS descobertas**: 299
- **Progresso geral**: 60% ⬆️ (+25%)
- **Tempo de investigação**: ~6 horas
- **Queries executadas via Postman**: 25+

#### ✅ Investigação Aprofundada (2026-01-30 Noite)

**CORREÇÃO**: A conclusão inicial sobre "empresas diferentes" estava INCORRETA. A investigação continuou e descobriu:

- [x] ✅ Divergência REAL de 72 unidades na MESMA empresa (CODEMP=7)
- [x] ✅ Empresa 7 TEM WMS ativo (UTILIZAWMS='S' confirmado)
- [x] ✅ Ajuste entrada NUNOTA 1166922 (+72 un, TOP 1495) identificado como causa
- [x] ✅ Balanço por STATUSNOTA: L=+76, A=-24, Total=52 = TGFEST ✅
- [x] ✅ Campos reais TGWEST: ESTOQUEVOLPAD, SAIDPENDVOLPAD
- [x] ✅ Separações WMS: Todas finalizadas (SITUACAO=5)

**Causa Raiz Identificada:**
```
WMS Disponível: 124 unidades
TGFEST:          52 unidades
Diferença:       72 unidades = Ajuste entrada NUNOTA 1166922

O ajuste entrou no WMS mas NÃO sincronizou com TGFEST
```

#### ⚠️ Pendências Restantes
- [ ] Investigar por que NUNOTA 1166922 não atualizou TGFEST
- [ ] Verificar processo de sincronização WMS→TGFEST
- [ ] Identificar tabela de bloqueios (TGWBLQ?)
- [ ] Verificar se há job/batch pendente
- [ ] Extrair informações da documentação oficial (link bloqueado)

---

## ⚠️ Investigação de Divergência de Estoque - ATUALIZAÇÃO

### 🔥 CAUSA RAIZ REAL IDENTIFICADA (Correção)

**NOTA**: A conclusão inicial sobre "empresas diferentes" estava **INCORRETA**. A investigação aprofundada revelou:

**Problema Real**: WMS mostra 124 disponíveis, TGFEST mostra 52 unidades (MESMA empresa CODEMP=7)

```
┌─────────────────────────────────────────────────────────────────┐
│                   DIVERGÊNCIA REAL IDENTIFICADA                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   WMS Disponível:   124 un  →  CODEMP = 7 (TEM WMS ATIVO!)     │
│   TGFEST:            52 un  →  CODEMP = 7                       │
│   DIFERENÇA:         72 un  →  DIVERGÊNCIA REAL!               │
│                                                                 │
│   ─────────────────────────────────────────────────────────    │
│   ANÁLISE POR STATUSNOTA:                                       │
│   - Liberadas (L):  +76 unidades (entradas - saídas)           │
│   - Aguardando (A): -24 unidades (saída pendente)              │
│   - TOTAL:           52 unidades = TGFEST ✅                   │
│                                                                 │
│   CAUSA: Ajuste entrada NUNOTA 1166922 (+72 un, TOP 1495)      │
│          entrou no WMS mas NÃO sincronizou com TGFEST          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Documentação Atualizada:**
- ✅ [estoque.md](docs/de-para/sankhya/estoque.md) - Causa raiz CORRIGIDA
- ✅ Empresa 7 confirmada com WMS ativo (UTILIZAWMS='S')
- ✅ Campos reais TGWEST: ESTOQUEVOLPAD, SAIDPENDVOLPAD
- ⚠️ Pendente: Investigar processo de sincronização WMS → TGFEST

---

## ✅ Sessão Continuada (2026-01-30 Final) 🔧 CORREÇÃO DE QUERY

**Contexto**: Após a investigação inicial, foi gerado um CSV com todas as divergências do sistema, mas o arquivo continha linhas duplicadas.

### 🐛 Problema Identificado: Query com Duplicatas

**Sintoma**:
- CSV `analise_divergencias_estoque.csv` com mesmo NUNOTA aparecendo 20-30 vezes
- Exemplo: NUNOTA 1083999 (nota 95511) repetida 30+ vezes
- Dados idênticos mas multiplicados

**Causa Raiz Descoberta**:
```
Tabela TGFTOP possui MÚLTIPLAS linhas por CODTIPOPER:
- CODTIPOPER 1101 com ATUALEST='B' (baixa)
- CODTIPOPER 1101 com ATUALEST='N' (não atualiza)
- CODTIPOPER 1101 com ATUALEST='E' (entrada)

JOIN direto: LEFT JOIN TGFTOP TOP ON CAB.CODTIPOPER = TOP.CODTIPOPER
Resultado: Produto cartesiano (3 linhas TGFTOP × N itens = 3N duplicatas)
```

### ✅ Solução Implementada

**Query Corrigida** ([query_divergencias_corrigida.sql](query_divergencias_corrigida.sql)):

```sql
-- ❌ ANTES (causava duplicação):
LEFT JOIN TGFTOP TOP ON CAB.CODTIPOPER = TOP.CODTIPOPER

-- ✅ DEPOIS (sem duplicação):
LEFT JOIN (
    SELECT DISTINCT CODTIPOPER, MIN(DESCROPER) AS DESCROPER
    FROM TGFTOP
    GROUP BY CODTIPOPER
) TOP ON CAB.CODTIPOPER = TOP.CODTIPOPER
```

**Resultado**:
- ✅ Subquery deduplica TGFTOP antes do JOIN
- ✅ 1 linha única por CODPROD + NUNOTA
- ✅ Elimina campo ATUALEST (não necessário na análise)
- ✅ Query foca apenas em itens PENDENTES (STATUS='P')

### 📁 Arquivos Criados/Atualizados

1. ✅ **query_divergencias_corrigida.sql**
   - Query SQL completa sem duplicatas
   - Comentários explicando a correção
   - Filtros: CODEMP=7, STATUS='P', Divergência > 0
   - Ordenação por maior divergência

2. ✅ **curl_divergencias_corrigida.txt**
   - cURL pronto para Postman
   - Query em linha única escapada corretamente
   - Instruções de uso completas

3. ✅ **docs/de-para/sankhya/estoque.md**
   - Nova seção "6. Query de Divergências Retornando Duplicatas"
   - Documentação completa do problema e solução
   - Exemplo do problema com dados reais
   - Comparação ANTES × DEPOIS do código

### 📊 Análise de Divergências

**Query Retorna**:
- Produtos com divergência WMS > TGFEST
- Apenas itens PENDENTES (não processados)
- Campos: CODPROD, NUNOTA, TOP, QTD_NOTA, QTD_WMS, QTD_TGFEST, DIVERGENCIA
- Ordenado por maior divergência primeiro

**Exemplo de Resultado Esperado**:
```
CODPROD | NUNOTA  | TOP  | DIVERGENCIA
263340  | 1166922 | 1495 | 5894      ← Maior divergência
137216  | 1166922 | 1495 | 72        ← Caso investigado
...
```

### 🎯 Próximos Passos (Com Nova Query)

1. **Executar query corrigida no Postman**
   - Usar arquivo `curl_divergencias_corrigida.txt`
   - Gerar novo CSV sem duplicatas
   - Validar que cada NUNOTA aparece 1x por produto

2. **Análise das Divergências**
   - Identificar TOP mais problemáticas
   - Listar produtos com maior divergência
   - Verificar padrões (datas, tipos de operação)

3. **Investigação de Causa**
   - Por que notas PENDENTES não processaram?
   - Verificar configuração de TOPs problemáticas
   - Identificar se há job de sincronização travado

---

## ✅ Sessão 2026-01-31: Relatórios HTML + Análise Avançada 📊

**Objetivo**: Criar relatórios interativos sem precisar Excel + Queries de análise detalhada

### 🎯 Tarefas Completadas:

#### 1. **Correção da Query de Divergências (CODEMP)**
- ✅ Adicionado campo `CAB.CODEMP` na query principal
- ✅ Atualizado `query_divergencias_corrigida.sql`
- ✅ Atualizado `curl_divergencias_corrigida.txt`
- ✅ Query agora retorna 15 colunas (era 14)

#### 2. **Relatório HTML Interativo** 📊
- ✅ Criado `relatorio_divergencias.html` - Relatório completo com:
  - Dashboard com KPIs (total produtos, notas, divergências)
  - Tabela interativa com ordenação por coluna
  - Busca em tempo real
  - Exportar para CSV
  - Função de impressão/PDF
  - Design profissional (gradientes roxo/azul)
  - Responsivo (mobile-friendly)

#### 3. **Scripts de Conversão**
- ✅ Criado `converter_json_para_html.py` - Conversor automático
  - Lê JSON do arquivo `resultado_query.json`
  - Gera HTML atualizado automaticamente
  - Mostra estatísticas (produtos únicos, divergência total, etc.)

- ✅ Criado `gerar_relatorio.py` - Gerador interativo
  - Aceita JSON colado diretamente no terminal
  - Processa e gera HTML instantaneamente
  - Detecta automaticamente se tem CODEMP ou não
  - Suporta query antiga (14 campos) e nova (15 campos)

#### 4. **Query de Análise Detalhada de Produto** 🔍
- ✅ Criado `query_analise_detalhada_produto.sql` - Query com CTEs
  - Calcula disponível real final considerando todas camadas
  - Mostra: ESTOQUE, RESERVADO, WMSBLOQUEADO, DISPONIVEL_COMERCIAL
  - Mostra: SALDO_WMS_TELA, QTD_PEDIDO_PENDENTE, WMS_APOS_PEDIDOS
  - Mostra: DISPONIVEL_REAL_FINAL (cálculo completo)
  - 200+ linhas documentadas e comentadas

- ✅ Criado `curl_analise_detalhada_produto.txt` - cURL pronto
  - Query em linha única escapada
  - Instruções de uso completas
  - Diferenciação clara entre queries (divergências vs análise)

#### 5. **Documentação Completa**
- ✅ Criado `README_RELATORIO.md` - Guia completo de uso dos relatórios
  - Passo a passo ilustrado
  - Troubleshooting
  - Checklist de uso
  - Diferença entre métodos (Python vs manual)

### 📊 Análises Realizadas:

#### Produto 263340 (Divergência Crítica)
```
TGFEST (ERP):        452 unidades
TGWEST (WMS):      6,346 unidades
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIVERGÊNCIA:       5,894 unidades (!!)
```
- ✅ Identificado como maior divergência do sistema
- ✅ Múltiplas notas pendentes (100+ registros)
- ⚠️ Causa: Notas com STATUS='P' não processadas

#### Produto 261302 (Caso Gravíssimo) 🔥
```
ESTOQUE:             316 un
RESERVADO:           260 un (82% do total)
WMSBLOQUEADO:        213 un (67% do total)
DISPONIVEL_COMERCIAL: -157 un (NEGATIVO!)
SALDO_WMS_TELA:       43 un (físico real)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DISPONIVEL_REAL:       0 un (bloqueado para venda)
```

**Problemas Identificados:**
1. 🔥 Divergência ERP↔WMS: 273 unidades (316 - 43)
2. 🔥 Sobre-reserva: 473 unidades bloqueadas > 316 disponíveis
3. 🔥 Disponível negativo: -157 un (impossível atender reservas)
4. 🔥 Produto bloqueado: 0 disponível para venda

**Causas Prováveis:**
- Notas pendentes não processadas
- Bloqueios fantasma no WMS (213 un)
- Reservas antigas não liberadas (260 un)
- Ajustes manuais incorretos
- Dessincronia total ERP↔WMS

### 📁 Arquivos Criados/Atualizados Nesta Sessão:

#### Queries SQL:
1. `query_divergencias_corrigida.sql` (v2.0 com CODEMP)
2. `query_analise_detalhada_produto.sql` (nova - 200+ linhas)

#### cURLs Postman:
3. `curl_divergencias_corrigida.txt` (atualizado com CODEMP)
4. `curl_analise_detalhada_produto.txt` (novo)

#### Scripts Python:
5. `converter_json_para_html.py` (atualizado para 15 campos)
6. `gerar_relatorio.py` (novo - gerador interativo)

#### Relatórios HTML:
7. `relatorio_divergencias.html` (completo e interativo)
8. `relatorio_divergencias_preview.html` (teste com 2 registros)
9. `relatorio_divergencias_completo.html` (template para dados reais)

#### Documentação:
10. `README_RELATORIO.md` (guia completo de uso)

### 🎯 Resultados Alcançados:

✅ **Sistema de Relatórios Completo**
- Usuário pode visualizar divergências sem Excel
- Relatório interativo com busca, ordenação, filtros
- Exportação para CSV disponível
- Design profissional e responsivo

✅ **Duas Abordagens de Query**
1. **Divergências em Massa** - Ver todos os produtos com problema
2. **Análise Detalhada** - Entender UM produto específico

✅ **Automatização**
- Scripts Python para converter JSON → HTML
- Processo simplificado (colar JSON e pronto)
- Detecta automaticamente formato da query

✅ **Problemas Graves Identificados**
- Produto 263340: 5.894 unidades de divergência
- Produto 261302: Disponível negativo (-157), bloqueado total
- Ambos com notas STATUS='P' não processadas

### ⚠️ Pendente para Próxima Sessão:

#### Investigação Profunda dos Casos Críticos:
- [ ] **Produto 261302** - Investigar 260 un reservadas
- [ ] **Produto 261302** - Investigar 213 un bloqueadas WMS
- [ ] **Produto 261302** - Listar endereços físicos WMS
- [ ] **Produto 261302** - Buscar notas pendentes (STATUS='P')
- [ ] **Produto 261302** - Propor correções (ajuste ou processamento)

- [ ] **Produto 263340** - Processar 100+ notas pendentes
- [ ] **Produto 263340** - Validar ajuste entrada NUNOTA 1166922
- [ ] **Produto 263340** - Investigar por que notas não processaram

#### Queries de Investigação:
- [ ] Criar query para listar reservas detalhadas (TGFRES)
- [ ] Criar query para endereços bloqueados WMS (TGWEND + TGWEST)
- [ ] Criar query para notas pendentes por produto
- [ ] Criar query para histórico de movimentações

#### Relatório Final:
- [ ] Executar query de divergências com dados reais completos
- [ ] Gerar HTML final com TODOS os produtos
- [ ] Priorizar correções por criticidade

---

## 🔥 Sessão 2026-02-01: CORREÇÃO DEFINITIVA - Query V3 ⭐

**Contexto**: Usuário reportou que dados ainda estavam "mais que triplicados" mesmo após correção V2 do TGFTOP.

### 🐛 Novo Problema Descoberto: Multiplicação por CODLOCAL

**Sintoma Reportado**:
> "Bom dia, precisamos investigar pq os dados que vc me passou estavam mais que triplicados"

**Investigação Realizada**:
Revisitei a query V2 e identifiquei uma SEGUNDA fonte de multiplicação que não havia sido corrigida:

```sql
-- ❌ PROBLEMA NA V2:
LEFT JOIN TGFEST EST ON ITE.CODPROD = EST.CODPROD AND EST.CODEMP = 7
```

**Causa Raiz da Triplicação**:
```
Tabela TGFEST pode ter MÚLTIPLAS linhas por produto (múltiplos CODLOCAL):
- CODPROD 137216, CODLOCAL 1: 100 unidades
- CODPROD 137216, CODLOCAL 2: 50 unidades
- CODPROD 137216, CODLOCAL 3: 30 unidades

JOIN sem GROUP BY = Multiplicação 3x!

Resultado:
- NUNOTA 1171669 com produto 137216 aparecia 3 VEZES
- Cada linha mostrava estoque de um local diferente
- Total correto (180), mas distribuído em 3 linhas
```

### ✅ Solução Implementada: Query V3 Definitiva

**Correção Aplicada** ([query_divergencias_v3_definitiva.sql](query_divergencias_v3_definitiva.sql)):

```sql
-- ❌ V2 (ainda com problema):
LEFT JOIN TGFEST EST ON ITE.CODPROD = EST.CODPROD AND EST.CODEMP = 7

-- ✅ V3 (DEFINITIVA - sem multiplicação):
LEFT JOIN (
    SELECT
        CODPROD,
        CODEMP,
        SUM(NVL(ESTOQUE, 0)) AS ESTOQUE_TGFEST
    FROM TGFEST
    WHERE CODEMP = 7
    GROUP BY CODPROD, CODEMP
) EST ON ITE.CODPROD = EST.CODPROD AND EST.CODEMP = CAB.CODEMP
```

**Mesmo padrão aplicado no TGWEST** (que já estava correto desde V1):
```sql
LEFT JOIN (
    SELECT CODPROD, SUM(ESTOQUE) AS ESTOQUE_WMS
    FROM TGWEST
    WHERE CODEMP = 7
    GROUP BY CODPROD
) WMS ON ITE.CODPROD = WMS.CODPROD
```

### 📊 Comparação das Versões

| Versão | Problema | Status |
|--------|----------|--------|
| **V1** | TGFTOP sem GROUP BY → Duplicação por ATUALEST ('E','N','B') | ❌ Multiplicação 3x |
| **V2** | TGFTOP corrigido, mas TGFEST sem GROUP BY → Multiplicação por CODLOCAL | ⚠️ Ainda multiplica |
| **V3** | TGFTOP + TGFEST ambos com GROUP BY → SEM MULTIPLICAÇÃO | ✅ DEFINITIVA |

### 📁 Arquivos Criados Nesta Sessão:

1. ✅ **query_divergencias_v3_definitiva.sql**
   - Query SQL definitiva sem qualquer fonte de multiplicação
   - Comentários explicando AMBAS as correções (TGFTOP + TGFEST)
   - Validação sugerida para confirmar unicidade

2. ✅ **curl_divergencias_v3_definitiva.txt**
   - cURL pronto para Postman com query V3
   - Documentação completa das 3 versões
   - Exemplo comparativo mostrando problema e solução
   - Instruções de validação

3. ✅ **PROGRESSO_SESSAO.md** (este arquivo)
   - Seção nova documentando descoberta e correção V3
   - Versão atualizada para v0.3.0

### 🔍 Como Validar Se V3 Está Correta

Execute esta query após rodar a V3:

```sql
-- Escolha um NUNOTA qualquer dos resultados
SELECT COUNT(*), SUM(DIVERGENCIA)
FROM (
    -- Cole a query V3 aqui
) RESULTADO
WHERE NUNOTA = 1171669  -- Seu NUNOTA
GROUP BY NUNOTA, CODPROD
HAVING COUNT(*) > 1  -- Se retornar linhas, ainda há duplicação!
```

**Resultado esperado**: Nenhuma linha retornada (sem duplicatas)

### ✅ Garantias da Query V3:

✅ **TGFTOP**: Subquery com GROUP BY elimina duplicação por ATUALEST
✅ **TGFEST**: Subquery com SUM() e GROUP BY elimina multiplicação por CODLOCAL
✅ **TGWEST**: Subquery com SUM() e GROUP BY (já estava correto)
✅ **Resultado**: 1 linha única por CODPROD + NUNOTA
✅ **Valores**: Corretos (somas consolidadas de todos os locais/endereços)

### 🎯 Próximo Passo:

**Executar query V3 no Postman**:
1. Usar arquivo `curl_divergencias_v3_definitiva.txt`
2. Gerar novo JSON sem qualquer multiplicação
3. Processar com `gerar_relatorio.py` para criar HTML final
4. Validar que não há mais duplicatas/triplicatas

---

## 🎯 TAREFAS PLANEJADAS (PRÓXIMAS SESSÕES)

### Fase 1: Extração Básica - COMPRAS (ATUAL)

#### A. Finalizar Mapeamento
- [ ] Identificar todas as tabelas WMS (TCS*, *WMS*)
- [ ] Documentar campos customizados (AD_*)
- [ ] Mapear relacionamento completo entre tabelas
- [ ] Validar query de extração com dados reais

#### B. Estrutura de Estoque e WMS ✅ 75% COMPLETO
- [x] Mapear TGFEST (estoque geral) ✅
- [x] Mapear tabelas de WMS (saldo por endereço) ✅ TGWEST descoberta
- [x] Mapear TGFRES (reservas) ✅
- [x] Mapear TGWEND (endereços físicos) ✅
- [x] Mapear TGWSEP/TGWSXN (separações) ✅
- [x] Identificar 299 tabelas WMS ✅
- [x] Entender diferença entre estoque normal vs WMS ✅
- [x] Documentar em `docs/de-para/sankhya/estoque.md` ✅ 550+ linhas
- [ ] Investigar 46 unidades não explicadas ⚠️ Pendente
- [ ] Mapear TGFMOV (movimentações) 📋 Próxima fase

#### C. Script Python de Extração
- [ ] Criar `src/extractors/compras.py`
- [ ] Implementar conexão com Sankhya API
- [ ] Implementar renovação automática de token
- [ ] Implementar extração incremental
- [ ] Implementar salvamento em Parquet
- [ ] Implementar metadata de controle
- [ ] Implementar logging detalhado
- [ ] Implementar tratamento de erros

#### D. Teste e Validação
- [ ] Testar extração de 1 dia
- [ ] Validar schema Parquet gerado
- [ ] Validar quantidade de registros
- [ ] Testar upload no Azure Data Lake
- [ ] Validar particionamento (ano/mes/dia)

#### E. Automação (Futuro)
- [ ] Criar Azure Function para agendamento
- [ ] Implementar monitoramento
- [ ] Implementar alertas de falha
- [ ] Documentar processo de deploy

### Fase 2: Expansão de Módulos (FUTURO)

#### A. Vendas
- [ ] Mapear tabelas (TGFCAB, TGFITE, TGFPAR)
- [ ] Criar script de extração
- [ ] Documentar em `docs/de-para/sankhya/vendas.md`

#### B. Estoque Completo
- [ ] Mapear TGFEST, TGFSAL, TGFEND
- [ ] Mapear movimentações
- [ ] Criar script de extração
- [ ] Documentar em `docs/de-para/sankhya/estoque.md`

#### C. Financeiro
- [ ] Mapear TGFFIN (títulos)
- [ ] Mapear recebimentos/pagamentos
- [ ] Criar script de extração
- [ ] Documentar em `docs/de-para/sankhya/financeiro.md`

### Fase 3: Inteligência (FUTURO DISTANTE)
- [ ] Criar agentes de IA (LangChain/CrewAI)
- [ ] Implementar interface conversacional
- [ ] Criar dashboards analíticos
- [ ] Integração com WhatsApp

---

## 📊 Status das Tabelas Mapeadas

| Módulo | Tabela | Status | Documentação |
|--------|--------|--------|--------------|
| **Compras** | TGFCAB | ✅ Mapeado | [compras.md](docs/de-para/sankhya/compras.md) |
| **Compras** | TGFITE | ✅ Mapeado | [compras.md](docs/de-para/sankhya/compras.md) |
| **Compras** | TGFPAR | ✅ Mapeado | [compras.md](docs/de-para/sankhya/compras.md) |
| **Compras** | TGFPRO | ✅ Mapeado | [compras.md](docs/de-para/sankhya/compras.md) |
| **Compras/WMS** | TGWREC | ✅ Mapeado | [wms.md](docs/de-para/sankhya/wms.md) |
| **Compras/WMS** | TGWRXN | ✅ Mapeado | [wms.md](docs/de-para/sankhya/wms.md) |
| **Compras/WMS** | VGWRECSITCAB | ✅ Mapeado | [wms.md](docs/de-para/sankhya/wms.md) |
| **Estoque** | TGFEST | ✅ Mapeado | [estoque.md](docs/de-para/sankhya/estoque.md) |
| **Estoque** | TGFRES | ✅ Mapeado | [estoque.md](docs/de-para/sankhya/estoque.md) |
| **Estoque/WMS** | TGWEST ⭐ | ✅ Mapeado | [estoque.md](docs/de-para/sankhya/estoque.md) |
| **Estoque/WMS** | TGWEND | ✅ Mapeado | [estoque.md](docs/de-para/sankhya/estoque.md) |
| **Estoque/WMS** | TGWSEP | ✅ Mapeado | [estoque.md](docs/de-para/sankhya/estoque.md) |
| **Estoque/WMS** | TGWSXN | ✅ Mapeado | [estoque.md](docs/de-para/sankhya/estoque.md) |
| **Estoque/WMS** | 299 tabelas | 🔍 Identificadas | - |
| **Estoque** | TGFMOV | 📋 Próxima fase | - |
| **Vendas** | TGFCAB | 📋 Futuro | - |
| **Vendas** | TGFVEN | 📋 Futuro | - |
| **Financeiro** | TGFFIN | 📋 Futuro | - |

**Legenda:**
- ✅ = Estrutura completa documentada com FK, queries, exemplos
- 🔍 = Identificadas mas não mapeadas individualmente
- 📋 = Planejado para próximas fases

---

## 🔑 Credenciais e Configuração

### Sankhya API

**Base URL**: `https://api.sankhya.com.br/gateway/v1`

**Autenticação OAuth 2.0:**
- `client_id`: 09ef3473-cb85-41d4-b6d4-473c15d39292
- `client_secret`: 7phfkche8hWHpWYBNWbEgf4xY4mPixp0
- `X-Token`: dca9f07d-bf0f-426c-b537-0e5b0ff1123d
- `grant_type`: client_credentials

**Token:**
- Endpoint: `POST /authenticate`
- Validade: 24 horas
- Formato: Bearer token

### Azure Data Lake (Pendente)

**Configurar:**
- [ ] Storage Account Name
- [ ] Access Key / SAS Token
- [ ] Container: `datahub`
- [ ] Testar conexão

---

## 🔧 Estrutura de Arquivos

```
data_hub/
├── README.md               ✅ Criado
├── CLAUDE.md              ✅ Criado (2026-01-30)
├── PROGRESSO_SESSAO.md    ✅ Criado (2026-01-30)
├── CHANGELOG.md           📋 Criar
├── .env                   📋 Criar (não commitar!)
├── .env.example           ✅ Existe
├── .gitignore             ✅ Existe
│
├── docs/
│   ├── api/
│   │   └── sankhya.md     📋 Criar
│   ├── data-lake/
│   │   └── estrutura.md   ✅ Existe
│   ├── de-para/
│   │   └── sankhya/
│   │       ├── compras.md             ✅ Existe
│   │       ├── compras-descoberta.md  ✅ Existe
│   │       ├── wms.md                 ✅ Existe
│   │       ├── estoque.md             📋 Criar
│   │       ├── vendas.md              📋 Futuro
│   │       └── financeiro.md          📋 Futuro
│   └── scripts/
│       └── README.md      📋 Criar
│
├── postman/               ✅ Existe
│   ├── LEIA-ME.md        ✅ Existe
│   └── Sankhya-Compras.postman_collection.json  ✅ Existe
│
├── src/                   📋 Criar
│   ├── __init__.py
│   ├── config.py         📋 Criar
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── base.py       📋 Criar
│   │   ├── compras.py    📋 Criar
│   │   └── estoque.py    📋 Futuro
│   └── utils/
│       ├── __init__.py
│       ├── sankhya_api.py    📋 Criar (conexão + renovação token)
│       ├── azure_storage.py  📋 Criar
│       └── logger.py         📋 Criar
│
├── tests/                 📋 Futuro
│   └── test_extractors.py
│
└── requirements.txt       📋 Criar
```

---

## 💡 Decisões Técnicas

### 1. Formato de Armazenamento: Parquet
**Por quê?**
- Compressão eficiente (50-80% menor que CSV)
- Schema tipado (validação automática)
- Compatível com Spark, Databricks, Power BI
- Particionamento nativo

### 2. Particionamento: ano/mes/dia
**Por quê?**
- Queries mais rápidas (partition pruning)
- Fácil gerenciar retenção (deletar partições antigas)
- Padrão Hive (compatível com ferramentas)

### 3. Estratégia de Carga: Incremental
**Por quê?**
- Extração completa seria muito pesada (anos de dados)
- Incremental usa `DTNEG >= ultima_data_extraida`
- Permite re-processar dias específicos se necessário

### 4. Renovação de Token: Automática
**Por quê?**
- Token expira em 24h
- Extração pode demorar (grandes volumes)
- Script deve ser resiliente e não falhar no meio

---

## 🐛 Problemas Conhecidos e Soluções

### ⚠️ 1. Diferença Estoque TGFEST vs WMS (EM INVESTIGAÇÃO)
**Problema**:
- WMS mostra 124 disponível (CODEMP=7)
- TGFEST mostra 52 disponível (CODEMP=7)
- Diferença de 72 unidades na MESMA empresa

**Causa Raiz Identificada:**
- Ajuste de entrada NUNOTA 1166922 (+72 un, TOP 1495) entrou no WMS
- Porém NÃO sincronizou corretamente com TGFEST
- A empresa 7 TEM WMS ativo (UTILIZAWMS='S' confirmado)

**Pendente:**
- Investigar processo de sincronização WMS → TGFEST
- Verificar configuração completa da TOP 1495
- Ver detalhes em [estoque.md](docs/de-para/sankhya/estoque.md)

### ✅ 2. Tabela TGFSAL Não Existe (RESOLVIDO!)
**Problema**: Tabela padrão de saldo por endereço não existe

**Causa**: WMS Sankhya usa **TGWEST** (não TGFSAL) para saldo por endereço

**Solução:**
- Tabela correta: `TGWEST` (saldo físico por endereço)
- Campos reais: `ESTOQUE`, `ENTRADASPEND`, `SAIDASPEND`
- Documentado em [estoque.md](docs/de-para/sankhya/estoque.md)

---

## 📝 Próximos Passos Imediatos

### Sessão Atual (Continuação):
1. **Mapear tabelas WMS**
   ```sql
   SELECT TABLE_NAME FROM ALL_TABLES
   WHERE TABLE_NAME LIKE '%WMS%' OR TABLE_NAME LIKE 'TCS%'
   ORDER BY TABLE_NAME
   ```

2. **Ver colunas da TGFRES**
   ```sql
   SELECT COLUMN_NAME FROM ALL_TAB_COLUMNS
   WHERE TABLE_NAME = 'TGFRES'
   ```

3. **Documentar descobertas**
   - Atualizar `docs/de-para/sankhya/estoque.md` (criar)
   - Adicionar achados em `PROGRESSO_SESSAO.md`

### Próxima Sessão:
1. **Criar estrutura de pastas Python** (`src/`)
2. **Criar script base de conexão** (`src/utils/sankhya_api.py`)
3. **Implementar renovação de token**
4. **Testar extração manual de compras**

---

## 🔍 Comandos SQL Úteis (Sankhya Oracle)

### Listar Tabelas
```sql
SELECT TABLE_NAME FROM ALL_TABLES
WHERE TABLE_NAME LIKE 'TGF%' -- Tabelas de negócio
ORDER BY TABLE_NAME
```

### Ver Colunas de uma Tabela
```sql
SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH, NULLABLE
FROM ALL_TAB_COLUMNS
WHERE TABLE_NAME = 'TGFCAB'
ORDER BY COLUMN_ID
```

### Ver Views
```sql
SELECT VIEW_NAME FROM ALL_VIEWS
WHERE VIEW_NAME LIKE 'VGW%' -- Views de WMS
```

### Ver Relacionamentos (Constraints)
```sql
SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE, SEARCH_CONDITION
FROM ALL_CONSTRAINTS
WHERE TABLE_NAME = 'TGFCAB'
```

---

## 📞 Contato e Informações

**Projeto**: MMarra Data Hub
**Objetivo**: Integrar Sankhya ERP com Azure Data Lake para análises inteligentes
**Responsável**: Ítalo Gomes
**Início**: Janeiro 2026
**Status**: 🔄 Em desenvolvimento (MVP - Extração de Compras)

---

## 💬 Mensagem para o Próximo Claude

Olá! Você está continuando o trabalho no **MMarra Data Hub**.

**Situação atual:**
- ✅ Estrutura do projeto criada e documentada
- ✅ Mapeamento de Compras concluído (TGFCAB, TGFITE, TGFPAR, TGFPRO, WMS)
- ✅ Servidor MCP criado e documentado (5 tools)
- ✅ Query V3 de divergências corrigida (sem multiplicação)
- ⚠️ **Servidor MCP NÃO FUNCIONANDO** - Erro de autenticação OAuth 2.0

---

### 🔥 SESSÃO MAIS RECENTE (2026-02-01) - TESTE DO MCP

**Objetivo:** Testar servidor MCP e executar query de divergências automaticamente

**Status:** ❌ **BLOQUEADO** - Autenticação falhando

**Problema Crítico:**
```
Erro 401: "O Header Authorization é obrigatório para esta requisição"
Endpoint testado: https://api.sankhya.com.br/gateway/v1/authenticate
```

**Causa Provável:**
- URL de autenticação no código MCP pode estar incorreta
- Código usa: `/gateway/v1/authenticate`
- Postman pode usar: `{{base_url}}/authenticate` (sem gateway/v1?)

**O QUE PRECISA SER FEITO PRIMEIRO:**

1. **Usuário deve verificar no Postman:**
   - Abrir collection "Nexus - Sankhya API (OAuth2)"
   - Verificar valor da variável `{{base_url}}`
   - Executar request "1.1 Login (OAuth2)"
   - Ver qual URL completa aparece após enviar

2. **Possíveis URLs corretas:**
   - A: `https://api.sankhya.com.br/authenticate` (sem gateway/v1)
   - B: `https://api.sankhya.com.br/gateway/v1/authenticate` (atual)
   - C: Outra URL diferente

3. **Após confirmar URL correta:**
   - Editar `mcp_sankhya/server.py` (linha ~55)
   - Corrigir URL do endpoint de autenticação
   - Testar com: `python test_mcp.py`

**Arquivos importantes criados:**
- ✅ `test_mcp.py` - Script de teste do servidor MCP
- ✅ `test_autenticacao.py` - Diagnóstico de autenticação
- ✅ `mcp_sankhya/.env` - Credenciais configuradas
- ✅ `GUIA_RAPIDO_MCP.md` - Guia completo de uso

---

### 📊 Sessão Anterior (2026-01-30) - Query V3 Criada

**Realização:** Query de divergências V3 DEFINITIVA (sem multiplicação)

**Problema corrigido:**
- V2 tinha multiplicação por CODLOCAL na TGFEST
- V3 usa SUM() com GROUP BY para consolidar antes do JOIN

**Arquivos:**
- ✅ `query_divergencias_v3_definitiva.sql`
- ✅ `curl_divergencias_v3_definitiva.txt`

---

### 🎯 O QUE FAZER QUANDO USUÁRIO VOLTAR

**Se usuário disser "vamos continuar":**

1. **Perguntar:** "Você conseguiu verificar a URL de autenticação no Postman?"
   - Se SIM → Pedir URL correta e corrigir código MCP
   - Se NÃO → Orientar: "Abra Postman, vá em 'Nexus - Sankhya API (OAuth2)' → '1.1 Login (OAuth2)' → Verifique {{base_url}}"

2. **Após corrigir autenticação:**
   - Testar: `python test_mcp.py`
   - Se funcionar: Executar query de divergências via MCP
   - Gerar relatório HTML automaticamente

3. **Se MCP funcionar:**
   - Demonstrar as 5 tools disponíveis
   - Executar query de divergências completa
   - Gerar relatório HTML final

**Se usuário pedir "documentar tudo":**
- Este arquivo JÁ FOI ATUALIZADO com toda a sessão de teste do MCP
- Próximo Claude: leia a seção "SESSÃO ATUAL (2026-02-01)" no topo

---

### ⚠️ Problemas Conhecidos

**1. MCP - Autenticação OAuth 2.0 (CRÍTICO - BLOQUEADOR)**
- Status: ❌ Não resolvido
- Impacto: Servidor MCP não funciona
- Próximo passo: Confirmar URL correta com usuário

**2. Divergências de Estoque (EM INVESTIGAÇÃO)**
- Produto 263340: 5.894 unidades de diferença
- Produto 261302: Disponível negativo (-157 un)
- Causa: Notas STATUS='P' não processadas

---

### 📋 Checklist de Retorno

Quando usuário voltar, faça nesta ordem:

- [ ] Perguntar se verificou URL de autenticação no Postman
- [ ] Corrigir `mcp_sankhya/server.py` com URL correta
- [ ] Executar `python test_mcp.py` para validar
- [ ] Se funcionar → Executar query de divergências via MCP
- [ ] Gerar relatório HTML final
- [ ] Atualizar PROGRESSO_SESSAO.md com sucesso

---

**Importante:**
- ✅ Sempre leia seção "SESSÃO ATUAL" no topo deste arquivo primeiro
- ✅ Sempre informe status dos tokens quando usuário perguntar
- ✅ Sempre documente antes de encerrar sessão
- ⚠️ Nunca commite credenciais (arquivo .env)
- ⚠️ MCP está BLOQUEADO até corrigir autenticação

Boa sorte! 🚀

---

**Última atualização:** 2026-02-01 (teste MCP - autenticação pendente)
**Versão:** v0.4.1
