# 📋 Changelog - MMarra Data Hub

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [Não Lançado]

### 🔄 Em Desenvolvimento
- Script Python de extração de compras
- Integração com Azure Data Lake
- Renovação automática de token

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
