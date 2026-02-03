# -*- coding: utf-8 -*-
"""
Extrator de Produtos (TGFPRO)
"""

from typing import Optional, List

from .base import BaseExtractor


class ProdutosExtractor(BaseExtractor):
    """Extrai dados de produtos do Sankhya"""

    def __init__(self):
        super().__init__("produtos")

    def get_colunas(self) -> List[str]:
        """Colunas do resultado"""
        return [
            "CODPROD",
            "DESCRPROD",
            "COMPLDESC",
            "REFERENCIA",
            "MARCA",
            "CODGRUPOPROD",
            "DESCRGRUPOPROD",
            "ATIVO",
            "USOPROD",
            "ORIGPROD",
            "NCM",
            "CODVOL",
            "PESOBRUTO",
            "PESOLIQ",
            "LARGURA",
            "ALTURA",
            "ESPESSURA",
            "DTALTER"
        ]

    def get_query(
        self,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        apenas_ativos: bool = True,
        codgrupoprod: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Gera query de extracao de produtos.

        Args:
            data_inicio: Data inicial de cadastro (YYYY-MM-DD)
            data_fim: Data final de cadastro (YYYY-MM-DD)
            apenas_ativos: Filtrar apenas ativos (default: True)
            codgrupoprod: Codigo do grupo de produtos (filtro opcional)
        """
        query = """
        SELECT
            p.CODPROD,
            p.DESCRPROD,
            p.COMPLDESC,
            p.REFERENCIA,
            p.MARCA,
            p.CODGRUPOPROD,
            g.DESCRGRUPOPROD,
            p.ATIVO,
            p.USOPROD,
            p.ORIGPROD,
            p.NCM,
            p.CODVOL,
            p.PESOBRUTO,
            p.PESOLIQ,
            p.LARGURA,
            p.ALTURA,
            p.ESPESSURA,
            p.DTALTER
        FROM TGFPRO p
        LEFT JOIN TGFGRU g ON g.CODGRUPOPROD = p.CODGRUPOPROD
        WHERE 1=1
        """

        # Filtros por data de alteracao
        if data_inicio:
            query += f"\n  AND p.DTALTER >= TO_DATE('{data_inicio}', 'YYYY-MM-DD')"

        if data_fim:
            query += f"\n  AND p.DTALTER <= TO_DATE('{data_fim}', 'YYYY-MM-DD')"

        if apenas_ativos:
            query += "\n  AND p.ATIVO = 'S'"

        if codgrupoprod:
            query += f"\n  AND p.CODGRUPOPROD = {codgrupoprod}"

        query += "\nORDER BY p.CODPROD"

        return query


# Para uso direto via linha de comando
if __name__ == "__main__":
    import logging
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    parser = argparse.ArgumentParser(description="Extrai produtos do Sankhya")
    parser.add_argument("--data-inicio", help="Data inicial de cadastro (YYYY-MM-DD)")
    parser.add_argument("--data-fim", help="Data final de cadastro (YYYY-MM-DD)")
    parser.add_argument("--incluir-inativos", action="store_true")
    parser.add_argument("--grupo", type=int, help="Codigo do grupo de produtos")
    parser.add_argument("--limite", type=int, help="Limite de registros")
    parser.add_argument("--formato", default="parquet", choices=["parquet", "csv"])

    args = parser.parse_args()

    extractor = ProdutosExtractor()
    arquivo = extractor.executar(
        data_inicio=args.data_inicio,
        data_fim=args.data_fim,
        apenas_ativos=not args.incluir_inativos,
        codgrupoprod=args.grupo,
        limite=args.limite,
        formato=args.formato
    )

    if arquivo:
        print(f"\nArquivo gerado: {arquivo}")
    else:
        print("\nFalha na extracao")
