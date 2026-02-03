# -*- coding: utf-8 -*-
"""
Tool para consultar dados no Azure Data Lake
"""

from typing import Optional
from langchain.tools import BaseTool
from pydantic import Field
import pandas as pd

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.utils.azure_storage import AzureDataLakeClient
from src.config import RAW_DATA_DIR


class DataLakeTool(BaseTool):
    """Tool para consultar dados no Data Lake"""

    name: str = "datalake_query"
    description: str = """
    Consulta dados armazenados no Azure Data Lake (arquivos Parquet).
    Útil para análises em lote e dados históricos.

    Datasets disponíveis:
    - clientes: CODPARC, NOMEPARC, CGC_CPF, EMAIL, CODVEND, LIMCRED
    - produtos: CODPROD, DESCRPROD, REFERENCIA, MARCA, CODGRUPOPROD
    - estoque: CODPROD, DESCRPROD, ESTOQUE, RESERVADO, DISPONIVEL
    - vendedores: CODVEND, APELIDO, ATIVO, TIPVEND, EMAIL

    Input: Nome do dataset (clientes, produtos, estoque, vendedores)
           Opcionalmente: filtro no formato "coluna=valor" ou "coluna>valor"
    Output: Dados em formato tabular

    Exemplos:
    - "clientes" -> Lista todos os clientes
    - "produtos CODPROD=123456" -> Busca produto específico
    - "estoque DISPONIVEL>100" -> Produtos com estoque > 100
    """

    azure_client: Optional[AzureDataLakeClient] = Field(default=None, exclude=True)

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self.azure_client = AzureDataLakeClient()

    def _run(self, input_str: str) -> str:
        """Consulta o Data Lake"""
        try:
            # Parse input
            parts = input_str.strip().split(" ", 1)
            dataset = parts[0].lower()
            filtro = parts[1] if len(parts) > 1 else None

            # Datasets disponíveis
            datasets = {
                "clientes": RAW_DATA_DIR / "clientes" / "clientes.parquet",
                "produtos": RAW_DATA_DIR / "produtos" / "produtos.parquet",
                "estoque": RAW_DATA_DIR / "estoque" / "estoque.parquet",
                "vendedores": RAW_DATA_DIR / "vendedores" / "vendedores.parquet"
            }

            if dataset not in datasets:
                return f"Dataset '{dataset}' não encontrado. Disponíveis: {list(datasets.keys())}"

            arquivo = datasets[dataset]

            if not arquivo.exists():
                return f"Arquivo não encontrado: {arquivo}. Execute a extração primeiro."

            # Carregar dados
            df = pd.read_parquet(arquivo)

            # Aplicar filtro se existir
            if filtro:
                df = self._aplicar_filtro(df, filtro)

            # Limitar resultado
            if len(df) > 50:
                return f"Encontrados {len(df)} registros. Mostrando primeiros 50:\n{df.head(50).to_string()}"

            return f"Encontrados {len(df)} registros:\n{df.to_string()}"

        except Exception as e:
            return f"Erro ao consultar Data Lake: {str(e)}"

    def _aplicar_filtro(self, df: pd.DataFrame, filtro: str) -> pd.DataFrame:
        """Aplica filtro ao DataFrame"""
        try:
            # Suporta: coluna=valor, coluna>valor, coluna<valor, coluna>=valor, coluna<=valor
            for op in [">=", "<=", "!=", "=", ">", "<"]:
                if op in filtro:
                    coluna, valor = filtro.split(op, 1)
                    coluna = coluna.strip().upper()
                    valor = valor.strip()

                    if coluna not in df.columns:
                        # Tentar case insensitive
                        for col in df.columns:
                            if col.upper() == coluna:
                                coluna = col
                                break

                    if coluna not in df.columns:
                        return df

                    # Converter valor se necessário
                    try:
                        valor_num = float(valor)
                        valor = valor_num
                    except:
                        pass

                    # Aplicar filtro
                    if op == "=":
                        df = df[df[coluna] == valor]
                    elif op == "!=":
                        df = df[df[coluna] != valor]
                    elif op == ">":
                        df = df[df[coluna] > valor]
                    elif op == "<":
                        df = df[df[coluna] < valor]
                    elif op == ">=":
                        df = df[df[coluna] >= valor]
                    elif op == "<=":
                        df = df[df[coluna] <= valor]

                    break

            return df

        except Exception as e:
            return df

    async def _arun(self, input_str: str) -> str:
        """Versão assíncrona"""
        return self._run(input_str)
