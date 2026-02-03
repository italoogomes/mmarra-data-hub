# -*- coding: utf-8 -*-
"""
Agente Engenheiro de Dados

Responsável pelo pipeline ETL:
- Extract: Extrai dados do Sankhya ERP via API
- Transform: Limpa, valida e transforma os dados
- Load: Carrega no Azure Data Lake em formato Parquet

Uso básico:
    from src.agents.engineer import Orchestrator

    orchestrator = Orchestrator()
    orchestrator.run_full_pipeline()

Uso avançado:
    from src.agents.engineer import Orchestrator, Scheduler
    from src.agents.engineer.extractors import ClientesExtractor
    from src.agents.engineer.transformers import DataCleaner, DataMapper
    from src.agents.engineer.loaders import DataLakeLoader

    # Extração manual
    extractor = ClientesExtractor()
    df = extractor.extract(apenas_ativos=True)

    # Limpeza
    cleaner = DataCleaner()
    df = cleaner.clean(df, entity="clientes")

    # Carga
    loader = DataLakeLoader()
    loader.load(df, entity="clientes", layer="raw")

Linha de comando:
    # Pipeline completo
    python -m src.agents.engineer.orchestrator

    # Entidades específicas
    python -m src.agents.engineer.orchestrator --entities clientes produtos

    # Scheduler
    python -m src.agents.engineer.scheduler --run-once
"""

from .orchestrator import Orchestrator
from .scheduler import Scheduler

__all__ = ['Orchestrator', 'Scheduler']
