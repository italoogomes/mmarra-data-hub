# -*- coding: utf-8 -*-
"""
Extrator de Vendedores/Compradores (TGFVEN)
"""

from typing import Optional, List

from .base import BaseExtractor


class VendedoresExtractor(BaseExtractor):
    """Extrai dados de vendedores/compradores do Sankhya"""

    def __init__(self):
        super().__init__("vendedores")

    def get_colunas(self) -> List[str]:
        """Colunas do resultado"""
        return [
            "CODVEND",
            "APELIDO",
            "ATIVO",
            "TIPVEND",
            "EMAIL",
            "CODGER"
        ]

    def get_query(
        self,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        apenas_ativos: bool = False,
        tipvend: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Gera query de extracao de vendedores/compradores.

        Args:
            data_inicio: Nao utilizado (cadastro)
            data_fim: Nao utilizado (cadastro)
            apenas_ativos: Filtrar apenas ativos
            tipvend: Tipo de vendedor (V=Vendedor, C=Comprador, R=Representante)
        """
        query = """
        SELECT
            v.CODVEND,
            v.APELIDO,
            v.ATIVO,
            v.TIPVEND,
            v.EMAIL,
            v.CODGER
        FROM TGFVEN v
        WHERE 1=1
        """

        if apenas_ativos:
            query += "\n  AND v.ATIVO = 'S'"

        if tipvend:
            query += f"\n  AND v.TIPVEND = '{tipvend}'"

        query += "\nORDER BY v.CODVEND"

        return query


# Para uso direto via linha de comando
if __name__ == "__main__":
    import logging
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    parser = argparse.ArgumentParser(description="Extrai vendedores/compradores do Sankhya")
    parser.add_argument("--apenas-ativos", action="store_true")
    parser.add_argument("--tipo", choices=["V", "C", "R"], help="V=Vendedor, C=Comprador, R=Representante")
    parser.add_argument("--limite", type=int, help="Limite de registros")
    parser.add_argument("--formato", default="parquet", choices=["parquet", "csv"])

    args = parser.parse_args()

    extractor = VendedoresExtractor()
    arquivo = extractor.executar(
        apenas_ativos=args.apenas_ativos,
        tipvend=args.tipo,
        limite=args.limite,
        formato=args.formato
    )

    if arquivo:
        print(f"\nArquivo gerado: {arquivo}")
    else:
        print("\nFalha na extracao")
