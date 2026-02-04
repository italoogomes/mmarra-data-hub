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
| Novo modelo de ML | `docs/modelos/[nome].md` |
| Qualquer mudança | `PROGRESSO_SESSAO.md` + `CHANGELOG.md`|

---

## 🤖 ARQUITETURA DOS AGENTES (CRÍTICO 🔥)

### ⚠️ IMPORTANTE: Leia isto ANTES de criar qualquer agente

**Agentes do Data Hub são MÓDULOS PYTHON PERMANENTES que rodam em produção.**

| ❌ NÃO É | ✅ É |
|----------|------|
| Comando `/agent` do Claude Code | Código Python em `src/agents/` |
| Sub-agente temporário | Módulo permanente do sistema |
| Ferramenta de debug | Componente de produção |

### 📊 Agentes Planejados

| Agente | Função | Usa LLM? | Fase | Status |
|--------|--------|----------|------|--------|
| **Engenheiro** | ETL: extrai do Sankhya, transforma, carrega no Data Lake | ❌ Não | 1-2 | ✅ Concluído |
| **Analista** | Gera dashboards, KPIs, relatórios automatizados | ❌ Não | 3 | 📋 Futuro |
| **Cientista** | Previsões de demanda, detecção de anomalias, ML | ❌ Não | 4 | 📋 Futuro |
| **LLM** | Chat em linguagem natural, orquestra outros agentes | ✅ Sim | 5 | 📋 Futuro |

---

## 🧠 INTEGRAÇÃO ML + LLM (CRÍTICO 🔥)

### Como os Agentes Trabalham Juntos

O **Agente LLM** é o orquestrador que chama os outros agentes quando necessário:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FLUXO DE INTEGRAÇÃO                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Usuário: "Quanto vou vender de pastilha de freio mês que vem?"    │
│                              │                                      │
│                              ▼                                      │
│                    ┌──────────────────┐                             │
│                    │   AGENTE LLM     │                             │
│                    │   (entende a     │                             │
│                    │    pergunta)     │                             │
│                    └────────┬─────────┘                             │
│                             │                                       │
│              "Preciso de previsão de demanda"                       │
│                             │                                       │
│                             ▼                                       │
│         ┌─────────────────────────────────────┐                     │
│         │            TOOLS (Ponte)            │                     │
│         │  forecast_tool.py ← chama ML        │                     │
│         └─────────────────┬───────────────────┘                     │
│                           │                                         │
│                           ▼                                         │
│                ┌─────────────────────┐                              │
│                │  AGENTE CIENTISTA   │                              │
│                │     (Prophet)       │                              │
│                │                     │                              │
│                │  Retorna: 450 un.   │                              │
│                │  Tendência: alta    │                              │
│                └──────────┬──────────┘                              │
│                           │                                         │
│                           ▼                                         │
│                    ┌──────────────────┐                             │
│                    │   AGENTE LLM     │                             │
│                    │   (explica o     │                             │
│                    │    resultado)    │                             │
│                    └────────┬─────────┘                             │
│                             │                                       │
│                             ▼                                       │
│   "Baseado no histórico, a previsão é de ~450 unidades,             │
│    com tendência de alta. Picos nas sextas-feiras."                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 🔧 Tools: A Ponte entre LLM e ML

O Agente LLM usa **tools** (funções Python) para chamar os modelos de ML:

| Tool | Chama | Quando usar |
|------|-------|-------------|
| `forecast_demand` | Agente Cientista → Prophet | "quanto vou vender", "previsão", "demanda" |
| `detect_anomalies` | Agente Cientista → Isolation Forest | "algo estranho", "anomalia", "fora do normal" |
| `segment_customers` | Agente Cientista → K-Means | "clientes parecidos", "segmentação", "perfil" |
| `get_kpis` | Agente Analista | "KPIs", "indicadores", "métricas" |
| `run_query` | Data Lake / Sankhya | consultas diretas de dados |

### 📁 Estrutura de Pastas com Integração

```
src/agents/
├── __init__.py
│
├── engineer/                  # 🔧 Agente Engenheiro de Dados
│   ├── __init__.py
│   ├── config.py
│   ├── extractors/
│   ├── transformers/
│   ├── loaders/
│   ├── orchestrator.py
│   └── scheduler.py
│
├── analyst/                   # 📈 Agente Analista
│   ├── __init__.py
│   ├── config.py
│   ├── kpis/
│   ├── reports/
│   └── dashboards/
│
├── scientist/                 # 🔬 Agente Cientista (ML - SEM LLM)
│   ├── __init__.py
│   ├── config.py
│   ├── forecasting/           # Previsão de demanda
│   │   ├── __init__.py
│   │   ├── demand_model.py    # Prophet
│   │   ├── preprocessor.py
│   │   └── predictor.py
│   ├── anomaly/               # Detecção de anomalias
│   │   ├── __init__.py
│   │   ├── detector.py        # Isolation Forest
│   │   └── alerts.py
│   ├── clustering/            # Segmentação
│   │   ├── __init__.py
│   │   ├── customers.py       # K-Means
│   │   └── products.py
│   ├── models/                # Modelos treinados (.pkl)
│   │   ├── demand/
│   │   ├── anomaly/
│   │   └── clustering/
│   └── utils/
│       ├── holidays.py        # Feriados brasileiros
│       └── metrics.py         # MAPE, MAE, etc
│
└── llm/                       # 🤖 Agente LLM (COM LLM - Orquestrador)
    ├── __init__.py
    ├── config.py              # API keys, modelo, temperatura
    ├── chat.py                # Interface de chat principal
    ├── tools/                 # 🆕 FERRAMENTAS QUE CHAMAM OUTROS AGENTES
    │   ├── __init__.py
    │   ├── forecast_tool.py   # Chama scientist/forecasting
    │   ├── anomaly_tool.py    # Chama scientist/anomaly
    │   ├── cluster_tool.py    # Chama scientist/clustering
    │   ├── kpi_tool.py        # Chama analyst/kpis
    │   └── query_tool.py      # Consultas diretas
    ├── prompts/               # Templates de prompt
    │   ├── system.py          # Prompt de sistema
    │   └── templates/
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
| **Cientista** | prophet, scikit-learn, numpy, pandas | Data Lake/DW |
| **LLM** | langchain, openai/anthropic | API de LLM + **chama os outros agentes** |

### ❌ O que NÃO fazer

1. **NÃO colocar LLM** nos agentes Engenheiro, Analista ou Cientista
2. **NÃO fazer** o Cientista responder em linguagem natural (quem faz isso é o LLM)
3. **NÃO duplicar** lógica — ML fica no Cientista, explicação fica no LLM
4. **NÃO chamar** Prophet direto do LLM — sempre passar pela tool

### ✅ O que FAZER

1. **Cientista retorna dados estruturados** (dict/JSON), não texto
2. **LLM interpreta e explica** os dados pro usuário
3. **Tools são a ponte** — funções simples que conectam LLM aos outros agentes
4. **Cada agente faz UMA coisa bem** — separação de responsabilidades

### 📝 Exemplo de Tool

```python
# src/agents/llm/tools/forecast_tool.py

def forecast_demand(codprod: int, periods: int = 30) -> dict:
    """
    Tool que o LLM chama para obter previsão de demanda.

    Args:
        codprod: Código do produto
        periods: Dias para prever

    Returns:
        Dict com previsão formatada para o LLM interpretar
    """
    from ...scientist.forecasting.demand_model import DemandForecastModel

    model = DemandForecastModel()
    return model.get_forecast_summary(codprod, periods)

# Definição para LangChain/OpenAI Functions
FORECAST_TOOL = {
    'name': 'forecast_demand',
    'description': 'Faz previsão de demanda. Use quando perguntarem sobre vendas futuras.',
    'parameters': {
        'type': 'object',
        'properties': {
            'codprod': {'type': 'integer', 'description': 'Código do produto'},
            'periods': {'type': 'integer', 'description': 'Dias para prever', 'default': 30}
        },
        'required': ['codprod']
    }
}
```

---

## 📁 Estrutura Completa do Projeto

```
mmarra-data-hub/
├── README.md
├── CLAUDE.md                    # Este arquivo
├── PROGRESSO_SESSAO.md
├── CHANGELOG.md
├── .env
├── .env.example
├── .gitignore
│
├── docs/                        # Documentacao tecnica
│   ├── agentes/                 # Documentacao dos agentes
│   │   ├── README.md
│   │   ├── engineer.md
│   │   ├── analyst.md
│   │   ├── scientist.md
│   │   └── llm.md
│   ├── data-lake/               # Estrutura do Data Lake
│   ├── de-para/                 # Mapeamentos de tabelas
│   │   ├── sankhya/             # Mapeamentos Sankhya
│   │   ├── ANALISE_ESTRUTURA.md
│   │   ├── PLANO_MAPEAMENTO.md
│   │   └── schema-banco-sankhya.md
│   ├── guias/                   # Guias de uso
│   │   ├── GUIA_NGROK.md
│   │   └── GUIA_RAPIDO_MCP.md
│   ├── pipelines/               # Documentacao de pipelines
│   ├── relatorios/              # Documentacao de relatorios
│   │   └── README_RELATORIO.md
│   ├── tabelas/                 # Templates de tabelas
│   │   └── TEMPLATE.md
│   └── wms/                     # Documentacao WMS
│       ├── CHECKLIST_EXPLORACAO_WMS.md
│       └── CURLS_EXPLORACAO_WMS.md
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── agents/                  # Agentes do sistema
│   ├── extractors/              # Legado (migrar para agents/engineer)
│   ├── pipelines/
│   ├── utils/
│   └── data/
│
├── queries/                     # SQLs reutilizaveis
│
├── scripts/                     # Scripts utilitarios
│   ├── extracao/                # Scripts de extracao de dados
│   ├── investigacao/            # Scripts de investigacao
│   ├── manutencao/              # Scripts de manutencao
│   ├── sql/                     # Scripts SQL especificos
│   └── testes/                  # Scripts de teste
│
├── tests/                       # Testes automatizados
└── mcp_sankhya/                 # MCP Server
```

---

## 🎯 Roadmap do Projeto

### Fase 1: Fundação ✅
- [x] Estrutura do projeto
- [x] Cliente Sankhya API
- [x] Cliente Azure Data Lake
- [x] Extractors básicos
- [x] MCP Server

### Fase 2: Agente Engenheiro ✅
- [x] Migrar extractors para `src/agents/engineer/`
- [x] Implementar transformers
- [x] Implementar loaders
- [x] Criar orchestrator
- [x] Agendar execuções

### Fase 3: Agente Analista 📋
- [ ] Definir KPIs principais
- [ ] Criar calculadores de KPIs
- [ ] Gerar relatórios automáticos

### Fase 4: Agente Cientista (ML) 📋
- [ ] Implementar previsão de demanda (Prophet)
- [ ] Implementar detecção de anomalias
- [ ] Implementar segmentação de clientes
- [ ] Criar pipeline de retreino

### Fase 5: Agente LLM (Orquestrador) 📋
- [ ] Configurar API de LLM
- [ ] Criar tools que chamam Cientista
- [ ] Criar tools que chamam Analista
- [ ] Implementar chat
- [ ] Implementar RAG

---

## 🔐 Segurança e Credenciais

### Variáveis de Ambiente (.env)

```bash
# Sankhya
SANKHYA_BASE_URL=https://api.sankhya.com.br/gateway/v1
SANKHYA_TOKEN=seu_token
SANKHYA_APP_KEY=sua_app_key

# Azure Data Lake
AZURE_STORAGE_ACCOUNT=sua_conta
AZURE_STORAGE_KEY=sua_chave
AZURE_CONTAINER=datahub

# LLM (Fase 5)
LLM_PROVIDER=openai  # ou anthropic, azure
LLM_API_KEY=sua_chave
LLM_MODEL=gpt-4  # ou claude-3-opus
```

**IMPORTANTE:**
- ❌ NUNCA commitar credenciais
- ✅ Usar `.env` para variáveis sensíveis
- ✅ Documentar em `.env.example`

---

## 💡 Boas Práticas

### Para ML
1. **Retreinar** modelos periodicamente (semanal/mensal)
2. **Monitorar** métricas (MAPE, MAE) em produção
3. **Versionar** modelos treinados
4. **Logar** previsões vs realidade para avaliar performance

### Para LLM
1. **Tools simples** — cada tool faz uma coisa
2. **Retornar dados estruturados** — LLM formata pro usuário
3. **Tratar erros** — tool deve retornar erro amigável
4. **Cachear** quando possível — LLM é caro

---

## 🎯 Fluxo de Trabalho

```
1. Ler PROGRESSO_SESSAO.md
   ↓
2. Ler docs/ relevantes
   ↓
3. Fazer tarefa (um passo por vez)
   ↓
4. Testar com dados reais
   ↓
5. DOCUMENTAR
   ↓
6. Atualizar PROGRESSO_SESSAO.md
   ↓
7. Sugerir próximos passos
```

---

## 📞 Contato

**Projeto**: MMarra Data Hub
**Responsável**: Ítalo Gomes
**Objetivo**: Integrar Sankhya ERP com Data Lake Azure + IA para análises inteligentes

---

**Última atualização:** 2026-02-04
**Versão do projeto:** v0.3.0 (Agente Engenheiro concluído)
