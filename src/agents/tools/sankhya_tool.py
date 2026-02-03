# -*- coding: utf-8 -*-
"""
Tool para consultar o banco Sankhya via API
"""

from typing import Optional
from langchain.tools import BaseTool
from pydantic import Field

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.utils.sankhya_client import SankhyaClient


class SankhyaQueryTool(BaseTool):
    """Tool para executar queries SQL no Sankhya"""

    name: str = "sankhya_query"
    description: str = """
    Executa uma query SQL no banco de dados Sankhya ERP.
    Use para buscar informações sobre:
    - Pedidos (TGFCAB): NUNOTA, CODPARC, CODVEND, VLRNOTA, DTNEG
    - Itens de pedido (TGFITE): NUNOTA, CODPROD, QTDNEG, VLRTOT
    - Parceiros/Clientes (TGFPAR): CODPARC, NOMEPARC, CGC_CPF
    - Produtos (TGFPRO): CODPROD, DESCRPROD, REFERENCIA
    - Estoque (TGFEST): CODPROD, ESTOQUE, RESERVADO
    - Empenho WMS (TGWEMPE): NUWMSSEP, NUNOTAPEDVEN, STATUS
    - Vendedores (TGFVEN): CODVEND, APELIDO

    Input: Query SQL válida para Oracle
    Output: Resultado da query em formato JSON

    IMPORTANTE:
    - Use NVL() para campos que podem ser NULL
    - Limite resultados com ROWNUM <= 100 para queries exploratórias
    - Use JOINs para relacionar tabelas
    """

    client: Optional[SankhyaClient] = Field(default=None, exclude=True)

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self.client = SankhyaClient()
        if not self.client.autenticar():
            raise Exception("Falha na autenticação com Sankhya")

    def _run(self, query: str) -> str:
        """Executa a query e retorna resultado"""
        try:
            # Limitar resultados para segurança
            if "ROWNUM" not in query.upper() and "FETCH" not in query.upper():
                # Adicionar limite se não existir
                if query.strip().upper().startswith("SELECT"):
                    query = f"SELECT * FROM ({query}) WHERE ROWNUM <= 100"

            result = self.client.executar_query(query, timeout=60)

            if not result:
                return "Erro: Nenhum resultado retornado"

            if result.get("error"):
                return f"Erro na query: {result.get('error')}"

            rows = result.get("rows", [])
            if not rows:
                return "Query executada com sucesso, mas retornou 0 registros"

            # Formatar resultado
            return f"Encontrados {len(rows)} registros:\n{rows}"

        except Exception as e:
            return f"Erro ao executar query: {str(e)}"

    async def _arun(self, query: str) -> str:
        """Versão assíncrona (usa síncrona)"""
        return self._run(query)


# Queries prontas para investigação
QUERIES_INVESTIGACAO = {
    "pedido_completo": """
        SELECT
            c.NUNOTA, c.NUMNOTA, c.DTNEG, c.CODPARC, p.NOMEPARC,
            c.CODVEND, v.APELIDO AS VENDEDOR, c.VLRNOTA, c.STATUSNOTA,
            c.TIPMOV, c.CODTIPOPER, c.STATUSNFE
        FROM TGFCAB c
        LEFT JOIN TGFPAR p ON p.CODPARC = c.CODPARC
        LEFT JOIN TGFVEN v ON v.CODVEND = c.CODVEND
        WHERE c.NUNOTA = {nunota}
    """,

    "itens_pedido": """
        SELECT
            i.NUNOTA, i.SEQUENCIA, i.CODPROD, pr.DESCRPROD,
            i.QTDNEG, i.VLRUNIT, i.VLRTOT, i.CODLOCALORIG
        FROM TGFITE i
        LEFT JOIN TGFPRO pr ON pr.CODPROD = i.CODPROD
        WHERE i.NUNOTA = {nunota}
        ORDER BY i.SEQUENCIA
    """,

    "empenho_pedido": """
        SELECT
            e.NUWMSSEP, e.NUNOTAPEDVEN, e.CODPROD, pr.DESCRPROD,
            e.QTDPEDIDO, e.QTDATEND, e.STATUS, e.DHINCLUSAO, e.DHALTERACAO
        FROM TGWEMPE e
        LEFT JOIN TGFPRO pr ON pr.CODPROD = e.CODPROD
        WHERE e.NUNOTAPEDVEN = {nunota}
        ORDER BY e.CODPROD
    """,

    "estoque_produto": """
        SELECT
            e.CODEMP, e.CODPROD, pr.DESCRPROD, e.CODLOCAL,
            NVL(e.ESTOQUE, 0) AS ESTOQUE,
            NVL(e.RESERVADO, 0) AS RESERVADO,
            NVL(e.ESTOQUE, 0) - NVL(e.RESERVADO, 0) AS DISPONIVEL
        FROM TGFEST e
        LEFT JOIN TGFPRO pr ON pr.CODPROD = e.CODPROD
        WHERE e.CODPROD = {codprod} AND e.CODEMP = 1
    """,

    "cliente_info": """
        SELECT
            p.CODPARC, p.NOMEPARC, p.RAZAOSOCIAL, p.CGC_CPF,
            p.TIPPESSOA, p.ATIVO, p.EMAIL, p.TELEFONE,
            p.CODVEND, v.APELIDO AS VENDEDOR, p.LIMCRED
        FROM TGFPAR p
        LEFT JOIN TGFVEN v ON v.CODVEND = p.CODVEND
        WHERE p.CODPARC = {codparc}
    """
}
