"""
Módulo de Transformação de Dados para o teste de nivelamento da IntuitiveCare.

Este módulo é responsável por extrair dados das tabelas do PDF do Anexo I, 
salvar em formato CSV estruturado e compactar o resultado.
"""

from src.transformacoesDados.extrator_pdf import (
    extrair_tabela_pdf,
    combinar_tabelas,
    limpar_tabela,
    substituir_abreviacoes,
    salvar_csv,
    compactar_csv,
    principal
)

__all__ = [
    'extrair_tabela_pdf',
    'combinar_tabelas',
    'limpar_tabela',
    'substituir_abreviacoes',
    'salvar_csv',
    'compactar_csv',
    'principal'
]