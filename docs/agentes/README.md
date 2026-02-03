# 🤖 Agentes de IA - MMarra Data Hub

**Versão:** 1.0.0
**Data:** 2026-02-03
**Status:** ✅ Estrutura criada | ⏳ Aguardando API Key

---

## 📋 Visão Geral

Os agentes de IA são assistentes inteligentes que ajudam a analisar dados, investigar problemas e fornecer insights sobre o ERP Sankhya.

### Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    USUÁRIO                               │
│              "Por que o pedido X está travado?"         │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                AGENTE INVESTIGADOR                       │
│  - Interpreta a pergunta                                │
│  - Decide quais tools usar                              │
│  - Analisa resultados                                   │
│  - Formula diagnóstico                                  │
└─────────────────────┬───────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  SankhyaQuery   │     │   DataLake      │
│     Tool        │     │     Tool        │
│                 │     │                 │
│ Consulta banco  │     │ Consulta dados  │
│ em tempo real   │     │ extraídos       │
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│   SANKHYA ERP   │     │  AZURE DATA     │
│   (API REST)    │     │     LAKE        │
└─────────────────┘     └─────────────────┘
```

---

## 🎯 Agentes Disponíveis

### 1. Agente Investigador

**Arquivo:** `src/agents/investigador.py`

**Função:** Investigar problemas no ERP como pedidos travados, divergências de estoque, empenhos não concluídos.

**Capacidades:**
- Consultar banco Sankhya em tempo real
- Consultar dados do Data Lake
- Manter contexto de conversa
- Gerar diagnósticos formatados

**Exemplo de uso:**
```python
from src.agents import AgenteInvestigador

agente = AgenteInvestigador()

# Investigar pedido
resposta = agente.investigar("Por que o pedido 1192177 está travado?")
print(resposta)

# Investigar estoque
resposta = agente.investigar("Qual o estoque do produto 261302?")
print(resposta)
```

---

## 🔧 Tools Disponíveis

### SankhyaQueryTool

**Arquivo:** `src/agents/tools/sankhya_tool.py`

**Função:** Executar queries SQL no banco Sankhya via API.

**Tabelas acessíveis:**
| Tabela | Descrição | Campos principais |
|--------|-----------|-------------------|
| TGFCAB | Pedidos/Notas | NUNOTA, CODPARC, VLRNOTA, DTNEG |
| TGFITE | Itens dos pedidos | NUNOTA, CODPROD, QTDNEG, VLRTOT |
| TGFPAR | Parceiros/Clientes | CODPARC, NOMEPARC, CGC_CPF |
| TGFPRO | Produtos | CODPROD, DESCRPROD, REFERENCIA |
| TGFEST | Estoque | CODPROD, ESTOQUE, RESERVADO |
| TGWEMPE | Empenho WMS | NUWMSSEP, NUNOTAPEDVEN, STATUS |
| TGFVEN | Vendedores | CODVEND, APELIDO |

### DataLakeTool

**Arquivo:** `src/agents/tools/datalake_tool.py`

**Função:** Consultar dados extraídos no Azure Data Lake.

**Datasets disponíveis:**
- `clientes` - Dados de clientes/parceiros
- `produtos` - Catálogo de produtos
- `estoque` - Posição de estoque
- `vendedores` - Equipe comercial

**Filtros suportados:**
```
clientes                    # Todos os clientes
produtos CODPROD=123456     # Produto específico
estoque DISPONIVEL>100      # Estoque maior que 100
```

---

## ⚙️ Configuração

### Requisitos

1. **OpenAI API Key** (obrigatório)
   ```bash
   # Adicionar ao arquivo mcp_sankhya/.env
   OPENAI_API_KEY=sk-...
   ```

2. **Dependências Python**
   ```bash
   pip install langchain langchain-openai openai
   ```

### Modelos Suportados

| Modelo | Custo | Velocidade | Qualidade |
|--------|-------|------------|-----------|
| gpt-4o-mini | $0.01/investigação | Rápido | Bom |
| gpt-4o | $0.05/investigação | Médio | Excelente |
| gpt-4-turbo | $0.10/investigação | Lento | Excelente |

---

## 🚀 Como Usar

### Via Linha de Comando

```bash
cd mmarra-data-hub
python src/agents/investigador.py
```

### Via Código Python

```python
from src.agents import AgenteInvestigador

# Criar agente
agente = AgenteInvestigador(model="gpt-4o-mini", verbose=True)

# Fazer perguntas
resposta = agente.investigar("Quantos clientes ativos temos?")

# Limpar histórico
agente.limpar_memoria()
```

---

## 📝 Exemplos de Investigações

### 1. Pedido Travado

```
🔍 Você: Por que o pedido 1192177 está travado?

🤖 Agente:
## Resumo do Problema
O pedido 1192177 está com empenho pendente no WMS.

## Dados Encontrados
- Pedido: 1192177 | Cliente: RIMA | Valor: R$ 15.000,00
- Status do empenho: P (Pendente)
- Itens empenhados: 3 de 5

## Diagnóstico
O empenho não foi concluído porque 2 itens não têm estoque disponível.

## Sugestão de Ação
1. Verificar estoque dos produtos 261302 e 263340
2. Liberar reserva ou aguardar reposição
```

### 2. Estoque Divergente

```
🔍 Você: Qual o estoque real do produto 261302?

🤖 Agente:
## Dados do Produto 261302

| Local | Estoque | Reservado | Disponível |
|-------|---------|-----------|------------|
| 1     | 150     | 45        | 105        |
| 2     | 30      | 0         | 30         |
| TOTAL | 180     | 45        | 135        |

## Diagnóstico
Estoque total: 180 unidades
Reservado: 45 unidades (possivelmente para pedidos em separação)
Disponível para venda: 135 unidades
```

---

## 🔮 Roadmap

- [x] Agente Investigador básico
- [ ] Agente de Monitoramento (alertas automáticos)
- [ ] Agente de Análise (tendências, relatórios)
- [ ] Agente de Consulta (perguntas simples sobre dados)
- [ ] Interface web para agentes

---

## 📚 Referências

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Documentação Sankhya](docs/de-para/sankhya/)
