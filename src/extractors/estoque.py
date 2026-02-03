# -*- coding: utf-8 -*-
"""
Extrator de Estoque (TGFEST + TGWEST)
"""

from typing import Optional, List

from .base import BaseExtractor


class EstoqueExtractor(BaseExtractor):
    """Extrai dados de estoque do Sankhya (ERP + WMS)"""

    def __init__(self):
        super().__init__("estoque")

    def get_colunas(self) -> List[str]:
        """Colunas do resultado"""
        return [
            "CODEMP",
            "CODPROD",
            "DESCRPROD",
            "CODLOCAL",
            "CODLOCAL_DESCR",
            "CONTROLE",
            # Estoque ERP
            "ESTOQUE",
            "RESERVADO",
            "DISPONIVEL"
        ]

    def get_query(
        self,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        codemp: int = 1,
        codlocal: Optional[int] = None,
        apenas_com_estoque: bool = True,
        **kwargs
    ) -> str:
        """
        Gera query de extracao de estoque.

        Args:
            data_inicio: Nao utilizado (estoque e posicao atual)
            data_fim: Nao utilizado (estoque e posicao atual)
            codemp: Codigo da empresa (default: 1)
            codlocal: Codigo do local (filtro opcional)
            apenas_com_estoque: Filtrar apenas produtos com estoque > 0
        """
        query = f"""
        SELECT
            e.CODEMP,
            e.CODPROD,
            p.DESCRPROD,
            e.CODLOCAL,
            l.DESCRLOCAL AS CODLOCAL_DESCR,
            e.CONTROLE,
            NVL(e.ESTOQUE, 0) AS ESTOQUE,
            NVL(e.RESERVADO, 0) AS RESERVADO,
            NVL(e.ESTOQUE, 0) - NVL(e.RESERVADO, 0) AS DISPONIVEL
        FROM TGFEST e
        LEFT JOIN TGFPRO p ON p.CODPROD = e.CODPROD
        LEFT JOIN TGFLOC l ON l.CODLOCAL = e.CODLOCAL
        WHERE e.CODEMP = {codemp}
        """

        # Filtros
        if codlocal:
            query += f"\n  AND e.CODLOCAL = {codlocal}"

        if apenas_com_estoque:
            query += "\n  AND NVL(e.ESTOQUE, 0) > 0"

        query += "\nORDER BY e.CODPROD, e.CODLOCAL, e.CONTROLE"

        return query


# Para uso direto via linha de comando
if __name__ == "__main__":
    import logging
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    parser = argparse.ArgumentParser(description="Extrai estoque do Sankhya")
    parser.add_argument("--empresa", type=int, default=1, help="Codigo da empresa")
    parser.add_argument("--local", type=int, help="Codigo do local")
    parser.add_argument("--incluir-zerados", action="store_true", help="Incluir produtos sem estoque")
    parser.add_argument("--limite", type=int, help="Limite de registros")
    parser.add_argument("--formato", default="parquet", choices=["parquet", "csv"])

    args = parser.parse_args()

    extractor = EstoqueExtractor()
    arquivo = extractor.executar(
        codemp=args.empresa,
        codlocal=args.local,
        apenas_com_estoque=not args.incluir_zerados,
        limite=args.limite,
        formato=args.formato
    )

    if arquivo:
        print(f"\nArquivo gerado: {arquivo}")
    else:
        print("\nFalha na extracao")
