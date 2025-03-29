"""
Módulo de Web Scraping para o teste de nivelamento da IntuitiveCare.

Este módulo é responsável por acessar o site da ANS, baixar anexos em PDF
e compactar esses arquivos em um único arquivo ZIP.
"""

from src.webScraping.scraper import (
    baixar_arquivo,
    criar_zip,
    baixar_multiplos_arquivos,
    principal
)

__all__ = [
    'baixar_arquivo',
    'criar_zip',
    'baixar_multiplos_arquivos',
    'principal'
]