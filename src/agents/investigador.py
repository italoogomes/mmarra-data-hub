# -*- coding: utf-8 -*-
"""
Agente Investigador - Analisa problemas no ERP Sankhya

Este agente é especializado em investigar:
- Pedidos travados ou com problemas
- Divergências de estoque
- Empenhos não concluídos
- Relacionamentos entre entidades
"""

import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

from src.agents.tools.sankhya_tool import SankhyaQueryTool
from src.agents.tools.datalake_tool import DataLakeTool
from src.config import OPENAI_API_KEY


SYSTEM_PROMPT = """Você é um Agente Investigador especializado no ERP Sankhya da MMarra Distribuidora.

Seu papel é investigar problemas, analisar dados e fornecer diagnósticos claros.

## Suas Capacidades:

1. **Consultar Banco de Dados Sankhya** (tempo real)
   - Pedidos (TGFCAB): NUNOTA, CODPARC, CODVEND, VLRNOTA, DTNEG, STATUSNOTA
   - Itens (TGFITE): NUNOTA, CODPROD, QTDNEG, VLRTOT
   - Parceiros (TGFPAR): CODPARC, NOMEPARC, CGC_CPF
   - Produtos (TGFPRO): CODPROD, DESCRPROD, REFERENCIA
   - Estoque (TGFEST): CODPROD, ESTOQUE, RESERVADO
   - Empenho WMS (TGWEMPE): NUWMSSEP, NUNOTAPEDVEN, STATUS
   - Vendedores (TGFVEN): CODVEND, APELIDO

2. **Consultar Data Lake** (dados extraídos)
   - clientes, produtos, estoque, vendedores

## Tabelas Importantes:

| Tabela | Descrição | Chave |
|--------|-----------|-------|
| TGFCAB | Cabeçalho de notas/pedidos | NUNOTA |
| TGFITE | Itens das notas | NUNOTA + SEQUENCIA |
| TGFPAR | Parceiros (clientes/fornecedores) | CODPARC |
| TGFPRO | Produtos | CODPROD |
| TGFEST | Estoque ERP | CODPROD + CODEMP + CODLOCAL |
| TGWEMPE | Empenho WMS | NUWMSSEP |
| TGFVEN | Vendedores | CODVEND |

## Status de Empenho (TGWEMPE.STATUS):
- P = Pendente
- L = Liberado
- S = Em Separação
- E = Empenhado
- C = Concluído
- X = Cancelado

## Como Investigar:

1. **Pedido Travado**: Verificar TGFCAB, TGFITE, TGWEMPE
2. **Estoque Divergente**: Comparar TGFEST com TGWEMPE
3. **Empenho Não Concluído**: Analisar STATUS e QTDATEND em TGWEMPE

## Formato de Resposta:

Sempre forneça:
1. **Resumo do Problema**
2. **Dados Encontrados** (com queries executadas)
3. **Diagnóstico**
4. **Sugestão de Ação**

Seja objetivo e técnico. Use formatação markdown.
"""


class AgenteInvestigador:
    """Agente de IA para investigar problemas no Sankhya"""

    def __init__(self, model: str = "gpt-4o-mini", verbose: bool = True):
        """
        Inicializa o agente investigador.

        Args:
            model: Modelo OpenAI a usar (gpt-4o-mini, gpt-4o, gpt-4-turbo)
            verbose: Se True, mostra detalhes da execução
        """
        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY não configurada. "
                "Adicione ao arquivo mcp_sankhya/.env"
            )

        # Inicializar LLM
        self.llm = ChatOpenAI(
            model=model,
            temperature=0,
            api_key=OPENAI_API_KEY
        )

        # Inicializar tools
        self.tools = [
            SankhyaQueryTool(),
            DataLakeTool()
        ]

        # Criar prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        # Criar agente
        agent = create_openai_tools_agent(self.llm, self.tools, self.prompt)

        # Memória para conversação
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # Executor
        self.executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=verbose,
            max_iterations=10,
            handle_parsing_errors=True
        )

    def investigar(self, pergunta: str) -> str:
        """
        Investiga uma questão sobre o ERP.

        Args:
            pergunta: Pergunta ou problema a investigar

        Returns:
            Resposta do agente com diagnóstico
        """
        try:
            result = self.executor.invoke({"input": pergunta})
            return result.get("output", "Sem resposta")
        except Exception as e:
            return f"Erro na investigação: {str(e)}"

    def limpar_memoria(self):
        """Limpa o histórico de conversação"""
        self.memory.clear()


def main():
    """Exemplo de uso do agente"""
    print("=" * 60)
    print("AGENTE INVESTIGADOR - MMarra Data Hub")
    print("=" * 60)
    print("Digite 'sair' para encerrar")
    print("Digite 'limpar' para limpar histórico")
    print("-" * 60)

    try:
        agente = AgenteInvestigador(verbose=True)
    except ValueError as e:
        print(f"\n[ERRO] {e}")
        print("\nPara usar o agente, adicione sua OPENAI_API_KEY no arquivo:")
        print("  mcp_sankhya/.env")
        print("\nExemplo:")
        print("  OPENAI_API_KEY=sk-...")
        return 1

    while True:
        try:
            pergunta = input("\n🔍 Você: ").strip()

            if not pergunta:
                continue

            if pergunta.lower() == "sair":
                print("Até logo!")
                break

            if pergunta.lower() == "limpar":
                agente.limpar_memoria()
                print("Histórico limpo!")
                continue

            print("\n🤖 Investigando...\n")
            resposta = agente.investigar(pergunta)
            print(f"\n📋 Agente:\n{resposta}")

        except KeyboardInterrupt:
            print("\n\nAté logo!")
            break

    return 0


if __name__ == "__main__":
    sys.exit(main())
