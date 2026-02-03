# -*- coding: utf-8 -*-
"""
Classe base para todos os extratores
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

import pandas as pd

from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR
from src.utils import SankhyaClient

logger = logging.getLogger(__name__)


class BaseExtractor(ABC):
    """Classe base abstrata para extratores de dados"""

    def __init__(self, nome: str):
        """
        Args:
            nome: Nome do extrator (ex: 'vendas', 'clientes')
        """
        self.nome = nome
        self.client = SankhyaClient()
        self.output_dir = RAW_DATA_DIR / nome
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def get_query(self, **kwargs) -> str:
        """Retorna a query SQL para extracao. Deve ser implementado."""
        pass

    @abstractmethod
    def get_colunas(self) -> List[str]:
        """Retorna lista de nomes das colunas. Deve ser implementado."""
        pass

    def extrair(
        self,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        limite: Optional[int] = None,
        **kwargs
    ) -> Optional[pd.DataFrame]:
        """
        Executa a extracao de dados.

        Args:
            data_inicio: Data inicial (YYYY-MM-DD)
            data_fim: Data final (YYYY-MM-DD)
            limite: Limite de registros (para testes)
            **kwargs: Argumentos adicionais para a query

        Returns:
            DataFrame com os dados extraidos
        """
        logger.info(f"Iniciando extracao: {self.nome}")

        # Autenticar
        if not self.client.autenticar():
            logger.error("Falha na autenticacao")
            return None

        # Montar query
        query = self.get_query(
            data_inicio=data_inicio,
            data_fim=data_fim,
            **kwargs
        )

        # Adicionar limite se especificado
        if limite:
            query = f"{query}\nFETCH FIRST {limite} ROWS ONLY"

        logger.info(f"Executando query...")

        # Executar
        result = self.client.executar_query(query, timeout=300)

        if not result:
            logger.error("Falha ao executar query")
            return None

        rows = result.get("rows", [])

        if not rows:
            logger.warning("Nenhum registro encontrado")
            return pd.DataFrame(columns=self.get_colunas())

        # Criar DataFrame
        df = pd.DataFrame(rows, columns=self.get_colunas())

        logger.info(f"Extraidos {len(df)} registros")

        return df

    def salvar_parquet(
        self,
        df: pd.DataFrame,
        sufixo: str = ""
    ) -> Path:
        """
        Salva DataFrame em formato Parquet.

        Args:
            df: DataFrame a salvar
            sufixo: Sufixo opcional para o nome do arquivo

        Returns:
            Path do arquivo salvo
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"{self.nome}_{timestamp}"

        if sufixo:
            nome_arquivo += f"_{sufixo}"

        nome_arquivo += ".parquet"

        caminho = self.output_dir / nome_arquivo

        df.to_parquet(caminho, index=False, engine='pyarrow')

        logger.info(f"Arquivo salvo: {caminho}")

        return caminho

    def salvar_csv(
        self,
        df: pd.DataFrame,
        sufixo: str = ""
    ) -> Path:
        """
        Salva DataFrame em formato CSV.

        Args:
            df: DataFrame a salvar
            sufixo: Sufixo opcional para o nome do arquivo

        Returns:
            Path do arquivo salvo
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"{self.nome}_{timestamp}"

        if sufixo:
            nome_arquivo += f"_{sufixo}"

        nome_arquivo += ".csv"

        caminho = self.output_dir / nome_arquivo

        df.to_csv(caminho, index=False, encoding='utf-8-sig')

        logger.info(f"Arquivo salvo: {caminho}")

        return caminho

    def executar(
        self,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        formato: str = "parquet",
        limite: Optional[int] = None,
        **kwargs
    ) -> Optional[Path]:
        """
        Executa extracao completa e salva arquivo.

        Args:
            data_inicio: Data inicial (YYYY-MM-DD)
            data_fim: Data final (YYYY-MM-DD)
            formato: 'parquet' ou 'csv'
            limite: Limite de registros
            **kwargs: Argumentos adicionais

        Returns:
            Path do arquivo salvo
        """
        df = self.extrair(
            data_inicio=data_inicio,
            data_fim=data_fim,
            limite=limite,
            **kwargs
        )

        if df is None or df.empty:
            return None

        # Sufixo com periodo
        sufixo = ""
        if data_inicio and data_fim:
            sufixo = f"{data_inicio}_a_{data_fim}"
        elif data_inicio:
            sufixo = f"desde_{data_inicio}"
        elif data_fim:
            sufixo = f"ate_{data_fim}"

        if formato == "csv":
            return self.salvar_csv(df, sufixo)
        else:
            return self.salvar_parquet(df, sufixo)
