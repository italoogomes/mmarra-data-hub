# 🤖 Instruções para Claude - MMarra Data Hub

> Este arquivo é lido automaticamente pelo Claude Code no VS Code.

---

## 📋 REGRAS OBRIGATÓRIAS

### 1. Antes de Qualquer Coisa
- **SEMPRE** leia `PROGRESSO_SESSAO.md` para entender onde paramos
- **SEMPRE** consulte `docs/` antes de modificar código
- **SEMPRE** pergunte qual tarefa o usuário quer continuar

### 2. Durante o Trabalho
- Faça **um passo de cada vez** e confirme antes de prosseguir
- **Documente tudo** que fizer em `docs/` e `PROGRESSO_SESSAO.md`
- Siga o estilo dos arquivos existentes
- Teste credenciais e tokens antes de rodar extrações

### 3. Sobre Tokens/Contexto ⚠️ CRÍTICO
- **SEMPRE INFORME** o status dos tokens quando o usuário perguntar "como estão os tokens?"
- **SEMPRE AVISE PROATIVAMENTE** quando atingir 60% de uso (120k de 200k tokens)
- **SUGIRA** salvar o progresso no `PROGRESSO_SESSAO.md` quando atingir 70%
- **DOCUMENTE TUDO** antes de atingir 80% para evitar perda de contexto
- **NUNCA** deixe trabalho sem documentar antes de encerrar
- **FORMATO DO AVISO**: "📊 Tokens: X/200.000 (Y%) - Z tokens restantes"

### 4. Ao Finalizar Qualquer Tarefa
- Atualize `PROGRESSO_SESSAO.md` com o que foi feito
- Atualize `CHANGELOG.md` se houver mudança de versão
- Liste os próximos passos claros
- Informe status dos tokens ao finalizar

### 5. Comandos Rápidos do Usuário

Quando o usuário perguntar sobre:

| Pergunta do Usuário | Como Responder |
|---------------------|----------------|
| "Como estão os tokens?" | Informar: `📊 Tokens: X/200.000 (Y%) - Z tokens restantes` |
| "Onde paramos?" | Ler e resumir `PROGRESSO_SESSAO.md` |
| "O que falta fazer?" | Listar seção "TAREFAS PLANEJADAS" do `PROGRESSO_SESSAO.md` |
| "Documentar tudo" | Atualizar `PROGRESSO_SESSAO.md` com resumo da sessão |

### 6. Documentação Obrigatória (CRÍTICO 🔥)

**Toda criação ou modificação DEVE ser documentada seguindo o padrão da pasta `docs/`.**

#### Quando criar/modificar código:
| O que mudou | Onde documentar |
|-------------|-----------------|
| Nova tabela mapeada | `docs/de-para/sankhya/[modulo].md` |
| Novo script de extração | `docs/scripts/README.md` |
| Nova estrutura no Data Lake | `docs/data-lake/estrutura.md` |
| Mudança na API Sankhya | `docs/api/sankhya.md` |
| Novo agente criado | `docs/agentes/[nome].md` |
| Qualquer mudança | `PROGRESSO_SESSAO.md` + `CHANGELOG.md`|

#### Padrão de Documentação Data Hub:

```markdown
# 📊 Título do Documento

**Versão:** x.x.x
**Data:** YYYY-MM-DD
**Status:** ✅ ou 🔄

---

## 🎯 Seção Principal

### Subseção
- Item 1
- Item 2

#### Se for correção/mudança:
- **Problema**: O que estava errado
- **Solução**: O que foi feito
- **Motivo/Aprendizado**: Por que essa solução

---
```

#### Regras de Formatação:
- ✅ Usar emojis nos títulos (📊 🔥 🔧 ✅ 🔄 ⭐ 🎯)
- ✅ Tabelas para resumos e comparações
- ✅ Blocos de código com linguagem especificada
- ✅ Separadores `---` entre seções
- ✅ Estrutura Problema → Solução → Motivo para correções
- ✅ Versão e data atualizados no cabeçalho
- ❌ NUNCA deixar mudança sem documentar

---

## 🤖 ARQUITETURA DOS AGENTES (CRÍTICO 🔥)

### ⚠️ IMPORTANTE: Leia isto ANTES de criar qualquer agente

**Agentes do Data Hub são MÓDULOS PYTHON PERMANENTES que rodam em produção.**

| ❌ NÃO É | ✅ É |
|----------|------|
| Comando `/agent` do Claude Code | Código Python em `src/agents/` |
| Sub-agente temporário | Módulo permanente do sistema |
| Ferramenta de debug | Componente de produção |
| Dependente de LLM (exceto Agente LLM) | Python puro com requests, pandas, SQLAlchemy |

### 📊 Agentes Planejados

| Agente | Função | Usa LLM? | Fase | Status |
|--------|--------|----------|------|--------|
| **Engenheiro** | ETL: extrai do Sankhya, transforma, carrega no Data Lake | ❌ Não | 1-2 | 🔄 Parcial |
| **Analista** | Gera dashboards, KPIs, relatórios automatizados | ❌ Não | 3 | 📋 Futuro |
| **Cientista** | Previsões de demanda, detecção de anomalias, ML | ❌ Não | 5 | 📋 Futuro |
| **LLM** | Chat em linguagem natural, geração de SQL, RAG | ✅ Sim | 4 | 📋 Futuro |

### 📁 Estrutura Obrigatória dos Agentes

```
src/agents/
├── __init__.py
│
├── engineer/                  # 🔧 Agente Engenheiro de Dados
│   ├── __init__.py
│   ├── config.py              # Configurações específicas do agente
│   ├── extractors/            # Extratores por entidade
│   │   ├── __init__.py
│   │   ├── base.py            # Classe base abstrata
│   │   ├── vendas.py          # Extrator de vendas
│   │   ├── compras.py         # Extrator de compras
│   │   ├── estoque.py         # Extrator de estoque
│   │   └── financeiro.py      # Extrator financeiro
│   ├── transformers/          # Transformações de dados
│   │   ├── __init__.py
│   │   ├── cleaner.py         # Limpeza e validação
│   │   └── mapper.py          # De-para pro star schema
│   ├── loaders/               # Carga no destino
│   │   ├── __init__.py
│   │   ├── datalake.py        # Carrega no Azure Data Lake
│   │   └── warehouse.py       # Carrega no DW (futuro)
│   ├── orchestrator.py        # Coordena E-T-L
│   └── scheduler.py           # Agenda execuções
│
├── analyst/                   # 📈 Agente Analista (futuro)
│   ├── __init__.py
│   ├── kpis.py                # Cálculo de indicadores
│   ├── reports.py             # Geração de relatórios
│   └── dashboards.py          # Dados para dashboards
│
├── scientist/                 # 🔬 Agente Cientista (futuro)
│   ├── __init__.py
│   ├── forecasting.py         # Previsão de demanda
│   ├── anomaly.py             # Detecção de anomalias
│   └── clustering.py          # Segmentação
│
└── llm/                       # 🤖 Agente LLM (futuro, COM LLM)
    ├── __init__.py
    ├── config.py              # API keys, modelo, etc
    ├── chat.py                # Interface conversacional
    ├── sql_generator.py       # Gera SQL a partir de texto
    └── rag/                   # Retrieval Augmented Generation
        ├── __init__.py
        ├── embeddings.py
        └── retriever.py
```

### 🔧 Tecnologias por Agente

| Agente | Bibliotecas | Dependências Externas |
|--------|-------------|----------------------|
| **Engenheiro** | requests, pandas, pyarrow, sqlalchemy | API Sankhya, Azure Data Lake |
| **Analista** | pandas, plotly, jinja2 | Data Lake/DW |
| **Cientista** | scikit-learn, prophet, numpy | Data Lake/DW |
| **LLM** | langchain, openai/anthropic | API de LLM (OpenAI/Azure/Anthropic) |

### ❌ O que NÃO fazer ao criar agentes

1. **NÃO usar LLM** nos agentes Engenheiro, Analista ou Cientista
2. **NÃO usar frameworks** como CrewAI, AutoGen, ou LangChain (exceto no Agente LLM)
3. **NÃO confundir** `/agent` (comando do Claude Code) com agentes do sistema
4. **NÃO criar** agentes de "debug" ou "investigação" — isso é tarefa de desenvolvimento
5. **NÃO importar** openai, anthropic, langchain nos agentes sem LLM

### ✅ O que FAZER ao criar agentes

1. **Reutilizar** código existente em `src/utils/` (sankhya_client, azure_storage)
2. **Seguir** o padrão de extractors já existente em `src/extractors/`
3. **Documentar** em `docs/agentes/[nome].md`
4. **Testar** com dados reais antes de considerar pronto
5. **Usar** logging para rastreabilidade
6. **Tratar** erros e implementar retry quando necessário

### 📝 Checklist para Criar um Agente

Antes de criar qualquer agente, verificar:

- [ ] Entendi que é código Python permanente (não /agent)
- [ ] Sei qual fase do projeto esse agente pertence
- [ ] Verifiquei se precisa ou não de LLM
- [ ] Li a documentação existente em `docs/`
- [ ] Vou reutilizar código de `src/utils/` e `src/extractors/`
- [ ] Vou criar documentação em `docs/agentes/`
- [ ] Vou atualizar `PROGRESSO_SESSAO.md` ao finalizar

---

## 📚 Documentação do Projeto

| Arquivo | Propósito | Quando Atualizar |
|---------|-----------|------------------|
| `PROGRESSO_SESSAO.md` | **CONTEXTO** - Onde paramos | Sempre, ao final de cada tarefa |
| `CHANGELOG.md` | Histórico de versões | A cada nova versão |
| `README.md` | Documentação principal | Mudanças significativas |

### Pasta `docs/` - Documentação Técnica

| Arquivo | Propósito | Quando Atualizar |
|---------|-----------|------------------|
| `docs/de-para/sankhya/*.md` | Mapeamento de tabelas | Novo campo/tabela descoberto |
| `docs/data-lake/estrutura.md` | Estrutura do Data Lake | Nova pasta/formato criado |
| `docs/api/sankhya.md` | Endpoints da API | Novo endpoint usado |
| `docs/agentes/*.md` | Documentação dos agentes | Novo agente criado/modificado |
| `docs/scripts/README.md` | Scripts Python | Novo script criado |

---

## 🎯 Como Iniciar uma Sessão

```
Oi Claude! Leia PROGRESSO_SESSAO.md e me diga onde paramos.
Quero continuar com [descrição da tarefa].
```

### Ou para tarefas específicas:

```
Claude, leia docs/de-para/sankhya/compras.md e me ajude a [tarefa].
```

```
Claude, preciso criar o script de extração de compras.
```

---

## ⚠️ Avisos de Contexto Longo

Quando a conversa estiver longa, Claude deve:

1. **Avisar proativamente:**
   > "⚠️ Estamos com bastante contexto acumulado. Sugiro salvarmos o progresso no PROGRESSO_SESSAO.md antes de continuar."

2. **Salvar o estado atual:**
   - Atualizar seção "✅ O QUE JÁ FOI FEITO"
   - Atualizar seção "🎯 PRÓXIMOS PASSOS"
   - Atualizar "Mensagem para o Próximo Claude"

3. **Dar comando para continuar:**
   > "Para continuar em nova sessão, diga: 'Claude, leia PROGRESSO_SESSAO.md e continue de onde paramos.'"

---

## 🧩 Padrões do Projeto

### Tecnologias
- **Fonte de Dados**: Sankhya ERP (API REST + Oracle DB)
- **Armazenamento**: Azure Data Lake Gen2 (Parquet)
- **Extração**: Python 3.11+ (pandas, requests, pyarrow)
- **Documentação**: Postman Collections
- **Versionamento**: Git + GitHub

### 📁 Estrutura de Pastas

```
mmarra-data-hub/
├── README.md                    # Documentação principal
├── CLAUDE.md                    # Este arquivo (instruções)
├── PROGRESSO_SESSAO.md         # Contexto da sessão
├── CHANGELOG.md                # Histórico de versões
├── .env                        # Credenciais (NÃO COMMITAR!)
├── .env.example                # Exemplo de configuração
├── .gitignore
│
├── docs/                       # Documentação técnica
│   ├── agentes/               # Documentação dos agentes
│   │   ├── README.md          # Visão geral
│   │   ├── engineer.md        # Agente Engenheiro
│   │   ├── analyst.md         # Agente Analista
│   │   └── llm.md             # Agente LLM
│   ├── api/
│   │   └── sankhya.md         # Endpoints da API
│   ├── data-lake/
│   │   └── estrutura.md       # Estrutura do Data Lake
│   ├── de-para/
│   │   └── sankhya/
│   │       ├── compras.md     # Mapeamento Compras
│   │       ├── vendas.md      # Mapeamento Vendas
│   │       ├── estoque.md     # Mapeamento Estoque
│   │       └── wms.md         # Mapeamento WMS
│   └── pipelines/
│       └── README.md          # Documentação dos pipelines
│
├── postman/                    # Collections Postman
│   ├── LEIA-ME.md
│   └── *.postman_collection.json
│
├── src/                        # Código Python
│   ├── __init__.py
│   ├── config.py              # Configurações globais
│   ├── main.py                # Entry point
│   │
│   ├── agents/                # 🤖 AGENTES DO SISTEMA
│   │   ├── __init__.py
│   │   ├── engineer/          # Agente Engenheiro
│   │   ├── analyst/           # Agente Analista (futuro)
│   │   ├── scientist/         # Agente Cientista (futuro)
│   │   └── llm/               # Agente LLM (futuro)
│   │
│   ├── extractors/            # Extractors legados (migrar para agents/engineer)
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── vendas.py
│   │   ├── compras.py
│   │   ├── clientes.py
│   │   └── estoque.py
│   │
│   ├── pipelines/             # Orquestração de pipelines
│   │   ├── __init__.py
│   │   └── extracao.py
│   │
│   ├── utils/                 # Funções auxiliares compartilhadas
│   │   ├── __init__.py
│   │   ├── sankhya_client.py  # Cliente da API Sankhya
│   │   └── azure_storage.py   # Cliente do Azure Data Lake
│   │
│   └── data/                  # Dados locais (dev/teste)
│       ├── raw/
│       └── processed/
│
├── queries/                    # SQLs reutilizáveis
│   └── *.sql
│
├── scripts/                    # Scripts utilitários
│   └── investigacao/          # Scripts de investigação (dev)
│
├── tests/                      # Testes automatizados
│   └── *.py
│
└── mcp_sankhya/               # MCP Server (integração VS Code)
    ├── server.py
    └── README.md
```

### Comandos Frequentes

```bash
# Ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Rodar extração manual
python src/main.py --extract vendas --date 2026-01-27

# Rodar agente engenheiro
python -m src.agents.engineer.orchestrator --full-load

# Testar conexão com Sankhya
python -c "from src.utils.sankhya_client import SankhyaClient; print(SankhyaClient().test_connection())"
```

### Regras de Código
- **Sempre** usar variáveis de ambiente para credenciais
- **Sempre** logar operações (logging)
- **Sempre** tratar erros de API (try/except)
- **Sempre** validar dados antes de salvar no Data Lake
- **Nunca** commitar arquivos .env ou credenciais

---

## 🎯 Fluxo de Trabalho Ideal

```
1. Ler PROGRESSO_SESSAO.md
   ↓
2. Ler docs/ relevantes
   ↓
3. Fazer tarefa (um passo por vez)
   ↓
4. Testar com dados reais (pequena amostra)
   ↓
5. DOCUMENTAR (ver checklist abaixo)
   ↓
6. Atualizar PROGRESSO_SESSAO.md
   ↓
7. Sugerir próximos passos
```

### ✅ Checklist de Documentação (OBRIGATÓRIO)

Antes de finalizar qualquer tarefa, verificar:

- [ ] `PROGRESSO_SESSAO.md` atualizado com o que foi feito
- [ ] `CHANGELOG.md` atualizado (se nova versão)
- [ ] Documento correto em `docs/` atualizado (ver tabela acima)
- [ ] Versão e data atualizados nos arquivos modificados
- [ ] Código documentado com comentários quando necessário

**NUNCA encerrar sessão sem documentar!**

---

## 🔐 Segurança e Credenciais

### Sankhya API

**Autenticação OAuth 2.0:**
```bash
POST https://api.sankhya.com.br/gateway/v1/authenticate

Headers:
  Content-Type: application/x-www-form-urlencoded
  X-Token: {token_gateway}

Body:
  client_id: {client_id}
  client_secret: {client_secret}
  grant_type: client_credentials
```

**Token retornado:**
- Validade: 24 horas
- Formato: Bearer token
- Uso: `Authorization: Bearer {access_token}`

### Azure Data Lake

**Credenciais:**
- Storage Account Name
- Access Key (ou SAS Token)
- Container: `datahub`

**IMPORTANTE:**
- ❌ NUNCA commitar credenciais no git
- ✅ Usar `.env` para variáveis sensíveis
- ✅ Adicionar `.env` no `.gitignore`
- ✅ Documentar variáveis no `.env.example`

---

## 📊 Estrutura de Dados Sankhya

### Tabelas Principais

| Módulo | Tabelas | Status |
|--------|---------|--------|
| **Compras** | TGFCAB, TGFITE, TGFPAR, TGFPRO, TGWREC | 🔄 Mapeado |
| **Vendas** | TGFCAB, TGFITE, TGFPAR | 🔄 Mapeado |
| **Estoque** | TGFEST, TGFSAL, TGFEND | 📋 Futuro |
| **Financeiro** | TGFFIN, TGFREC | 📋 Futuro |

### Campos Customizados (AD_*)

O Sankhya permite campos customizados prefixados com `AD_`.

**Importante:**
- Sempre verificar se há campos `AD_*` nas tabelas
- Documentar o significado de cada campo customizado
- Consultar com o usuário se não souber o propósito

---

## 🔥 Problemas Comuns e Soluções

### 1. Token Expirado

**Problema:** API retorna 401 Unauthorized

**Solução:**
```python
# Implementar renovação automática do token
if response.status_code == 401:
    token = renovar_token()
    # Tentar novamente
```

### 2. Timeout na Query

**Problema:** Query muito grande trava

**Solução:**
- Dividir extração por períodos menores (1 dia de cada vez)
- Usar paginação se a API suportar
- Adicionar LIMIT na query para testes

### 3. Dados Faltando

**Problema:** Registros não aparecem na extração

**Solução:**
- Verificar filtros (TIPMOV, CODTIPOPER, etc)
- Verificar JOINs (LEFT vs INNER)
- Logar quantidade de registros em cada etapa

---

## 💡 Boas Práticas

### Durante Extração
1. **Sempre** testar com 1 dia de dados antes de rodar período grande
2. **Sempre** logar início, fim e quantidade de registros
3. **Sempre** validar schema do Parquet gerado
4. **Sempre** salvar metadata da extração

### Durante Desenvolvimento
1. **Commits pequenos** com mensagens claras
2. **Testar** antes de commitar
3. **Documentar** antes de finalizar
4. **Perguntar** se tiver dúvida sobre regra de negócio

### Durante Análise de Dados
1. **Nunca** assumir que campo é obrigatório
2. **Sempre** usar `NVL()` ou `COALESCE()` para campos nullable
3. **Sempre** verificar relacionamentos (FK válidas)

---

## 🎯 Roadmap do Projeto

### Fase 1: Fundação ✅
- [x] Estrutura do projeto
- [x] Cliente Sankhya API (`src/utils/sankhya_client.py`)
- [x] Cliente Azure Data Lake (`src/utils/azure_storage.py`)
- [x] Extractors básicos (`src/extractors/`)
- [x] MCP Server para VS Code

### Fase 2: Agente Engenheiro 🔄
- [ ] Migrar extractors para `src/agents/engineer/`
- [ ] Implementar transformers
- [ ] Implementar loaders
- [ ] Criar orchestrator
- [ ] Agendar execuções (scheduler)

### Fase 3: Agente Analista 📋
- [ ] Definir KPIs principais
- [ ] Criar calculadores de KPIs
- [ ] Gerar relatórios automáticos
- [ ] Preparar dados para dashboards

### Fase 4: Agente LLM 📋
- [ ] Configurar API de LLM (OpenAI/Azure/Anthropic)
- [ ] Implementar chat básico
- [ ] Implementar RAG com metadados do DW
- [ ] Gerador de SQL por linguagem natural

### Fase 5: Agente Cientista 📋
- [ ] Previsão de demanda
- [ ] Detecção de anomalias
- [ ] Segmentação de clientes

---

## 📞 Contato

**Projeto**: MMarra Data Hub
**Responsável**: Ítalo Gomes
**Objetivo**: Integrar Sankhya ERP com Data Lake Azure para análises inteligentes

---

**Última atualização:** 2026-02-03
**Versão do projeto:** v0.2.0 (Agentes em desenvolvimento)