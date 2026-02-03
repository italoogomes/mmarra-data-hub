# -*- coding: utf-8 -*-
"""
Extrator de Vendas (TGFCAB + TGFITE)
"""

from typing import Optional, List

from .base import BaseExtractor


class VendasExtractor(BaseExtractor):
    """Extrai dados de vendas do Sankhya"""

    def __init__(self):
        super().__init__("vendas")

    def get_colunas(self) -> List[str]:
        """Colunas do resultado"""
        return [
            # Cabecalho
            "NUNOTA",
            "NUMNOTA",
            "CODEMP",
            "CODPARC",
            "NOMEPARC",
            "DTNEG",
            "DTFATUR",
            "VLRNOTA",
            "PENDENTE",
            "STATUSNOTA",
            "TIPMOV",
            "CODTIPOPER",
            "DESCROPER",
            "CODVEND",
            "APELIDO_VEND",
            "CODCENCUS",
            # Item
            "SEQUENCIA",
            "CODPROD",
            "DESCRPROD",
            "QTDNEG",
            "VLRUNIT",
            "VLRTOT",
            "VLRDESC",
            "CODLOCALORIG",
            "CONTROLE",
            "REFERENCIA"
        ]

    def get_query(
        self,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        codemp: Optional[int] = None,
        codparc: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Gera query de extracao de vendas.

        Args:
            data_inicio: Data inicial (YYYY-MM-DD)
            data_fim: Data final (YYYY-MM-DD)
            codemp: Codigo da empresa (filtro opcional)
            codparc: Codigo do parceiro (filtro opcional)
        """
        query = """
        SELECT
            -- Cabecalho
            c.NUNOTA,
            c.NUMNOTA,
            c.CODEMP,
            c.CODPARC,
            p.NOMEPARC,
            c.DTNEG,
            c.DTFATUR,
            c.VLRNOTA,
            c.PENDENTE,
            c.STATUSNOTA,
            c.TIPMOV,
            c.CODTIPOPER,
            t.DESCROPER,
            c.CODVEND,
            v.APELIDO AS APELIDO_VEND,
            c.CODCENCUS,
            -- Item
            i.SEQUENCIA,
            i.CODPROD,
            pr.DESCRPROD,
            i.QTDNEG,
            i.VLRUNIT,
            i.VLRTOT,
            i.VLRDESC,
            i.CODLOCALORIG,
            i.CONTROLE,
            pr.REFERENCIA
        FROM TGFCAB c
        INNER JOIN TGFITE i ON i.NUNOTA = c.NUNOTA
        LEFT JOIN TGFPAR p ON p.CODPARC = c.CODPARC
        LEFT JOIN TGFPRO pr ON pr.CODPROD = i.CODPROD
        LEFT JOIN TGFVEN v ON v.CODVEND = c.CODVEND
        LEFT JOIN (
            SELECT CODTIPOPER, DESCROPER,
                   ROW_NUMBER() OVER (PARTITION BY CODTIPOPER ORDER BY DHALTER DESC) AS RN
            FROM TGFTOP
        ) t ON t.CODTIPOPER = c.CODTIPOPER AND t.RN = 1
        WHERE c.TIPMOV = 'V'
        """

        # Filtros
        if data_inicio:
            query += f"\n  AND c.DTNEG >= TO_DATE('{data_inicio}', 'YYYY-MM-DD')"

        if data_fim:
            query += f"\n  AND c.DTNEG <= TO_DATE('{data_fim}', 'YYYY-MM-DD')"

        if codemp:
            query += f"\n  AND c.CODEMP = {codemp}"

        if codparc:
            query += f"\n  AND c.CODPARC = {codparc}"

        query += "\nORDER BY c.DTNEG DESC, c.NUNOTA, i.SEQUENCIA"

        return query


# Para uso direto via linha de comando
if __name__ == "__main__":
    import logging
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    parser = argparse.ArgumentParser(description="Extrai vendas do Sankhya")
    parser.add_argument("--data-inicio", help="Data inicial (YYYY-MM-DD)")
    parser.add_argument("--data-fim", help="Data final (YYYY-MM-DD)")
    parser.add_argument("--limite", type=int, help="Limite de registros")
    parser.add_argument("--formato", default="parquet", choices=["parquet", "csv"])

    args = parser.parse_args()

    extractor = VendasExtractor()
    arquivo = extractor.executar(
        data_inicio=args.data_inicio,
        data_fim=args.data_fim,
        limite=args.limite,
        formato=args.formato
    )

    if arquivo:
        print(f"\nArquivo gerado: {arquivo}")
    else:
        print("\nFalha na extracao")
