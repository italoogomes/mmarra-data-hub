# 🤖 Agentes do MMarra Data Hub

**Versão:** 1.0.0
**Data:** 2026-02-03

---

## 📋 Visão Geral

Agentes são **módulos Python permanentes** que executam tarefas automatizadas no Data Hub.

> ⚠️ **IMPORTANTE:** Agentes NÃO são sub-agentes do Claude Code ou comandos `/agent`. São código Python em `src/agents/`.

---

## 🎯 Agentes Disponíveis

| Agente | Função | Usa LLM? | Status |
|--------|--------|----------|--------|
| [**Engenheiro**](engineer.md) | ETL: Sankhya → Data Lake | ❌ Não | ✅ Operacional |
| **Analista** | KPIs, relatórios, dashboards | ❌ Não | 📋 Futuro |
| **Cientista** | ML, previsões, anomalias | ❌ Não | 📋 Futuro |
| **LLM** | Chat natural, SQL, RAG | ✅ Sim | 📋 Futuro |

---

## 📁 Estrutura

```
src/agents/
├── __init__.py
│
├── engineer/          # 🔧 Agente Engenheiro ✅
│   ├── extractors/
│   ├── transformers/
│   ├── loaders/
│   ├── orchestrator.py
│   └── scheduler.py
│
├── analyst/           # 📈 Agente Analista (futuro)
│   ├── kpis.py
│   ├── reports.py
│   └── dashboards.py
│
├── scientist/         # 🔬 Agente Cientista (futuro)
│   ├── forecasting.py
│   ├── anomaly.py
│   └── clustering.py
│
└── llm/               # 🤖 Agente LLM (futuro)
    ├── chat.py
    ├── sql_generator.py
    └── rag/
```

---

## 🚀 Como Usar

### Agente Engenheiro

```python
from src.agents.engineer import Orchestrator

# Pipeline completo
orchestrator = Orchestrator()
results = orchestrator.run_full_pipeline()
```

### Via CLI

```bash
# Engenheiro
python -m src.agents.engineer.orchestrator
python -m src.agents.engineer.scheduler --run-once
```

---

## 🛠️ Tecnologias

| Agente | Bibliotecas |
|--------|-------------|
| Engenheiro | requests, pandas, pyarrow |
| Analista | pandas, plotly, jinja2 |
| Cientista | scikit-learn, prophet |
| LLM | langchain, openai |

---

## 📚 Documentação

- [Agente Engenheiro](engineer.md)
- Agente Analista (em breve)
- Agente Cientista (em breve)
- Agente LLM (em breve)
