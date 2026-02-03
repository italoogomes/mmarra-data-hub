# -*- coding: utf-8 -*-
"""
Extrator de Clientes/Parceiros (TGFPAR)
"""

from typing import Optional, List

from .base import BaseExtractor


class ClientesExtractor(BaseExtractor):
    """Extrai dados de clientes/parceiros do Sankhya"""

    def __init__(self):
        super().__init__("clientes")

    def get_colunas(self) -> List[str]:
        """Colunas do resultado"""
        return [
            "CODPARC",
            "NOMEPARC",
            "RAZAOSOCIAL",
            "CGC_CPF",
            "IDENTINSCESTAD",
            "TIPPESSOA",
            "CLIENTE",
            "FORNECEDOR",
            "VENDEDOR",
            "TRANSPORTADORA",
            "ATIVO",
            "DTCAD",
            "DTALTER",
            "EMAIL",
            "TELEFONE",
            "FAX",
            "CEP",
            "CODEND",
            "NUMEND",
            "COMPLEMENTO",
            "CODBAI",
            "NOMEBAI",
            "CODCID",
            "NOMECID",
            "UF",
            "CODVEND",
            "APELIDO_VEND",
            "CODTAB",
            "LIMCRED",
            "CODREG"
        ]

    def get_query(
        self,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        apenas_clientes: bool = False,
        apenas_fornecedores: bool = False,
        apenas_ativos: bool = True,
        **kwargs
    ) -> str:
        """
        Gera query de extracao de parceiros.

        Args:
            data_inicio: Data inicial de cadastro (YYYY-MM-DD)
            data_fim: Data final de cadastro (YYYY-MM-DD)
            apenas_clientes: Filtrar apenas clientes
            apenas_fornecedores: Filtrar apenas fornecedores
            apenas_ativos: Filtrar apenas ativos (default: True)
        """
        query = """
        SELECT
            p.CODPARC,
            p.NOMEPARC,
            p.RAZAOSOCIAL,
            p.CGC_CPF,
            p.IDENTINSCESTAD,
            p.TIPPESSOA,
            p.CLIENTE,
            p.FORNECEDOR,
            p.VENDEDOR,
            p.TRANSPORTADORA,
            p.ATIVO,
            p.DTCAD,
            p.DTALTER,
            p.EMAIL,
            p.TELEFONE,
            p.FAX,
            p.CEP,
            p.CODEND,
            p.NUMEND,
            p.COMPLEMENTO,
            p.CODBAI,
            b.NOMEBAI,
            p.CODCID,
            c.NOMECID,
            c.UF,
            p.CODVEND,
            v.APELIDO AS APELIDO_VEND,
            p.CODTAB,
            p.LIMCRED,
            p.CODREG
        FROM TGFPAR p
        LEFT JOIN TSIBAI b ON b.CODBAI = p.CODBAI
        LEFT JOIN TSICID c ON c.CODCID = p.CODCID
        LEFT JOIN TGFVEN v ON v.CODVEND = p.CODVEND
        WHERE 1=1
        """

        # Filtros
        if data_inicio:
            query += f"\n  AND p.DTCAD >= TO_DATE('{data_inicio}', 'YYYY-MM-DD')"

        if data_fim:
            query += f"\n  AND p.DTCAD <= TO_DATE('{data_fim}', 'YYYY-MM-DD')"

        if apenas_clientes:
            query += "\n  AND p.CLIENTE = 'S'"

        if apenas_fornecedores:
            query += "\n  AND p.FORNECEDOR = 'S'"

        if apenas_ativos:
            query += "\n  AND p.ATIVO = 'S'"

        query += "\nORDER BY p.CODPARC"

        return query


# Para uso direto via linha de comando
if __name__ == "__main__":
    import logging
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    parser = argparse.ArgumentParser(description="Extrai clientes do Sankhya")
    parser.add_argument("--data-inicio", help="Data inicial de cadastro (YYYY-MM-DD)")
    parser.add_argument("--data-fim", help="Data final de cadastro (YYYY-MM-DD)")
    parser.add_argument("--apenas-clientes", action="store_true")
    parser.add_argument("--apenas-fornecedores", action="store_true")
    parser.add_argument("--incluir-inativos", action="store_true")
    parser.add_argument("--limite", type=int, help="Limite de registros")
    parser.add_argument("--formato", default="parquet", choices=["parquet", "csv"])

    args = parser.parse_args()

    extractor = ClientesExtractor()
    arquivo = extractor.executar(
        data_inicio=args.data_inicio,
        data_fim=args.data_fim,
        apenas_clientes=args.apenas_clientes,
        apenas_fornecedores=args.apenas_fornecedores,
        apenas_ativos=not args.incluir_inativos,
        limite=args.limite,
        formato=args.formato
    )

    if arquivo:
        print(f"\nArquivo gerado: {arquivo}")
    else:
        print("\nFalha na extracao")
