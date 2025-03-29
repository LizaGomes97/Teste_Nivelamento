"""
Módulo de Banco de Dados para o teste de nivelamento da IntuitiveCare.

Este módulo é responsável por baixar dados de demonstrações contábeis e operadoras
da ANS, analisar sua estrutura e criar scripts SQL para importação e análise.
"""

from src.bancoDeDados.database import (
    extrair_arquivos_zip,
    analisar_estrutura_arquivos,
    preparar_scripts_sql,
    main
)

__all__ = [
    'extrair_arquivos_zip',
    'analisar_estrutura_arquivos',
    'preparar_scripts_sql',
    'main'
]