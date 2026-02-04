# -*- coding: utf-8 -*-
"""
Agente Analista - MMarra Data Hub

Gera KPIs, relatorios e dashboards a partir dos dados do Data Lake.
NAO usa LLM - apenas Python puro (pandas, jinja2, plotly).

Componentes:
- kpis/: Calculadores de KPIs (vendas, compras, estoque)
- reports/: Gerador de relatorios HTML
- dashboards/: Preparacao de dados para dashboards

Exemplo de uso:
    from src.agents.analyst import VendasKPI, ComprasKPI, EstoqueKPI
    from src.agents.analyst import ReportGenerator
    from src.agents.analyst import AnalystDataLoader

    # Carregar dados
    loader = AnalystDataLoader()
    df = loader.load("vendas", data_inicio="2026-01-01")

    # Calcular KPIs
    kpi = VendasKPI()
    resultado = kpi.calculate_all(df)

    # Gerar relatorio
    gen = ReportGenerator()
    html = gen.generate({"vendas": resultado})
"""

from .config import KPI_CONFIG, DATA_SOURCES, ANALYST_CONFIG
from .data_loader import AnalystDataLoader
from .kpis import VendasKPI, ComprasKPI, EstoqueKPI, BaseKPI
from .reports import ReportGenerator
from .dashboards import DashboardDataPrep

__all__ = [
    # Configuracao
    'KPI_CONFIG',
    'DATA_SOURCES',
    'ANALYST_CONFIG',
    # Data Loader
    'AnalystDataLoader',
    # KPIs
    'BaseKPI',
    'VendasKPI',
    'ComprasKPI',
    'EstoqueKPI',
    # Reports
    'ReportGenerator',
    # Dashboards
    'DashboardDataPrep',
]
