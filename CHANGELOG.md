# 📋 Changelog - MMarra Data Hub

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [Não Lançado]

### 🔄 Em Desenvolvimento
- Script Python de extração de compras
- Integração com Azure Data Lake
- Investigação de casos críticos (produtos 261302 e 263340)

---

## [0.4.0] - 2026-02-01 🚀 SERVIDOR MCP

### ✅ Adicionado

#### Servidor MCP Sankhya
- Criado servidor MCP completo para integração com Claude Code
- 5 tools disponíveis:
  - `executar_query_sql` - Executa queries SQL customizadas
  - `executar_query_divergencias` - Query V3 de divergências (corrigida)
  - `executar_query_analise_produto` - Análise detalhada de produto
  - `gerar_relatorio_divergencias` - Geração automática de HTML
  - `listar_queries_disponiveis` - Lista queries do projeto
- Renovação automática de token (válido 23h)
- Tratamento de erros e timeouts configuráveis

#### Arquivos MCP
- `mcp_sankhya/server.py` - Servidor MCP principal (650+ linhas)
- `mcp_sankhya/requirements.txt` - Dependências (mcp, httpx)
- `mcp_sankhya/.env.example` - Template de configuração
- `mcp_sankhya/README.md` - Documentação completa do MCP
- `mcp_sankhya/install.bat` - Instalador automático Windows
- `GUIA_RAPIDO_MCP.md` - Guia rápido de uso

### 🎯 Benefícios
- ✅ Execução de queries diretamente na conversa com Claude
- ✅ Processamento automático de JSON
- ✅ Geração de relatórios sem sair do VS Code
- ✅ Elimina necessidade de Postman/scripts manuais
- ✅ Workflow completo: query → análise → relatório em 1 comando

---

## [0.3.0] - 2026-02-01 ⭐ CORREÇÃO DEFINITIVA

### 🐛 Corrigido

#### Query V3 Definitiva - SEM MULTIPLICAÇÃO
- **Problema identificado**: TGFEST sem GROUP BY causava multiplicação por CODLOCAL
- **Causa raiz**: Produto com estoque em múltiplos locais gerava N linhas (triplicação)
- **Solução**: Subquery com SUM() + GROUP BY no TGFEST (mesmo padrão do TGWEST)

#### Arquivos
- `query_divergencias_v3_definitiva.sql` - Query SQL corrigida DEFINITIVA
- `curl_divergencias_v3_definitiva.txt` - cURL para Postman V3
- Atualizado `PROGRESSO_SESSAO.md` com seção "Sessão 2026-02-01"

### ✅ Garantias V3
- ✅ TGFTOP: GROUP BY elimina duplicação por ATUALEST
- ✅ TGFEST: SUM() + GROUP BY elimina multiplicação por CODLOCAL
- ✅ TGWEST: SUM() + GROUP BY (já estava correto)
- ✅ Resultado: 1 linha única por CODPROD + NUNOTA
- ✅ Valores: Corretos (somas consolidadas)

### 📊 Histórico de Correções
| Versão | Problema | Status |
|--------|----------|--------|
| V1 | TGFTOP sem GROUP BY | ❌ Multiplicação 3x |
| V2 | TGFTOP corrigido, TGFEST sem GROUP BY | ⚠️ Ainda multiplica |
| V3 | TGFTOP + TGFEST ambos corrigidos | ✅ DEFINITIVA |

---

## [0.2.0] - 2026-01-31 📊 RELATÓRIOS HTML

### ✅ Adicionado

#### Relatórios HTML Interativos
- `relatorio_divergencias.html` - Template HTML com dashboard completo
- Design profissional (gradientes roxo/azul)
- Features: busca, ordenação, export CSV, print/PDF
- Responsivo (mobile-friendly)
- Dashboard com 4 KPIs

#### Scripts Python
- `converter_json_para_html.py` - Conversor JSON → HTML
- `gerar_relatorio.py` - Gerador interativo (cola JSON no terminal)
- Suporte para 14 campos (V1) e 15 campos com CODEMP (V2)
- Detecção automática de formato

#### Query de Análise Detalhada
- `query_analise_detalhada_produto.sql` - 200+ linhas com CTEs
- `curl_analise_detalhada_produto.txt` - cURL para Postman
- Calcula 8 camadas de disponibilidade:
  - ESTOQUE, RESERVADO, WMSBLOQUEADO
  - DISPONIVEL_COMERCIAL, SALDO_WMS_TELA
  - QTD_PEDIDO_PENDENTE, WMS_APOS_PEDIDOS
  - DISPONIVEL_REAL_FINAL

#### Documentação
- `README_RELATORIO.md` - Guia completo de uso dos relatórios

### 🔧 Modificado
- Adicionado campo `CODEMP` em todas as queries (agora 15 campos)
- Atualizado `query_divergencias_corrigida.sql` com CODEMP
- Atualizado `curl_divergencias_corrigida.txt` com CODEMP

### 📊 Análises Realizadas
- Produto 263340: 5.894 unidades de divergência
- Produto 261302: Disponível negativo (-157), crítico
- Identificados 100+ notas pendentes (STATUS='P')

---

## [0.1.0] - 2026-01-30

### ✅ Adicionado

#### Documentação
- Criado `CLAUDE.md` com instruções completas para o Claude
- Criado `PROGRESSO_SESSAO.md` para rastrear contexto entre sessões
- Criado `PLANO_MAPEAMENTO.md` com estratégia completa de mapeamento
- Criado `QUERIES_EXPLORACAO.sql` com 50+ queries organizadas
- Criado `docs/tabelas/TEMPLATE.md` como modelo de documentação

#### Estrutura do Projeto
- Criadas pastas: `docs/tabelas/`, `metadata/`, `src/extractors/`, `src/utils/`, `tests/`
- Estrutura base para futuro desenvolvimento

#### Mapeamento de Tabelas
- Documentadas tabelas de Compras: TGFCAB, TGFITE, TGFPAR, TGFPRO
- Documentada estrutura WMS: TGWREC, VGWRECSITCAB
- Identificadas 28 tabelas-alvo para mapeamento completo

### 📝 Documentado
- Relacionamentos entre tabelas principais
- Situações WMS (códigos -1 a 100)
- Query principal de extração de compras
- Estrutura do Data Lake (particionamento, formato Parquet)

### 🎯 Planejado
- Roadmap de 4 fases (Compras, Estoque, Vendas, Financeiro)
- Cronograma de 4 semanas para mapeamento completo
- Estratégia de metadata para ML/LLM

---

## [0.0.1] - 2026-01-27

### ✅ Adicionado (Pré-projeto)
- Configuração inicial do Postman
- Autenticação OAuth 2.0 com Sankhya
- Primeiras queries exploratórias
- Identificação de tabelas principais

### 📝 Documentado
- README.md inicial
- docs/de-para/sankhya/compras.md (versão inicial)
- docs/de-para/sankhya/wms.md
- docs/data-lake/estrutura.md

---

## Tipos de Mudanças

- `✅ Adicionado` - para novas funcionalidades
- `🔧 Modificado` - para mudanças em funcionalidades existentes
- `❌ Depreciado` - para funcionalidades que serão removidas
- `🗑️ Removido` - para funcionalidades removidas
- `🐛 Corrigido` - para correções de bugs
- `🔐 Segurança` - para correções de vulnerabilidades

---

**Última atualização:** 2026-01-30
