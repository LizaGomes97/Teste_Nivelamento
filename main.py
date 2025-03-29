"""
Script principal para executar todos os testes da IntuitiveCare.

Este script permite executar cada teste individualmente ou todos em sequência.
Uso:
    python main.py             # Executa todos os testes em sequência
    python main.py --teste 1   # Executa apenas o teste de Web Scraping
    python main.py --teste 2   # Executa apenas o teste de Transformação de Dados
    python main.py --teste 3   # Executa apenas o teste de Banco de Dados
    python main.py --teste 4   # Executa apenas o teste de API
"""

import os
import argparse
import sys

# Adicionar caminho para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar funções principais de cada teste
from src.webScraping.scraper import principal as web_scraping
from src.transformacoesDados.extrator_pdf import principal as transformacao_dados
from src.bancoDeDados.database import main as banco_dados
from src.api.server import app as servidor_api

def executar_todos():
    """Executa todos os testes em sequência"""
    print("\n" + "="*60)
    print("TESTES DE NIVELAMENTO - INTUITIVE CARE")
    print("="*60 + "\n")
    
    print("\n===== TESTE 1: WEB SCRAPING =====")
    web_scraping()
    
    print("\n===== TESTE 2: TRANSFORMAÇÃO DE DADOS =====")
    transformacao_dados()
    
    print("\n===== TESTE 3: BANCO DE DADOS =====")
    banco_dados()
    
    print("\n===== TESTE 4: API =====")
    print("Iniciando servidor API...")
    print("Para acessar a interface, abra http://localhost:5000 no navegador")
    print("Pressione CTRL+C para encerrar o servidor")
    servidor_api.run(debug=True, host='0.0.0.0', port=5000)

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="IntuitiveCare Testes de Nivelamento")
    parser.add_argument('--teste', type=int, choices=[1, 2, 3, 4], 
                        help='Escolha qual teste executar (1-4)')
    args = parser.parse_args()
    
    if args.teste == 1:
        print("\n===== TESTE 1: WEB SCRAPING =====")
        web_scraping()
    elif args.teste == 2:
        print("\n===== TESTE 2: TRANSFORMAÇÃO DE DADOS =====")
        transformacao_dados()
    elif args.teste == 3:
        print("\n===== TESTE 3: BANCO DE DADOS =====")
        banco_dados()
    elif args.teste == 4:
        print("\n===== TESTE 4: API =====")
        print("Iniciando servidor API...")
        print("Para acessar a interface, abra http://localhost:5000 no navegador")
        print("Pressione CTRL+C para encerrar o servidor")
        servidor_api.run(debug=True, host='0.0.0.0', port=5000)
    else:
        executar_todos()

if __name__ == "__main__":
    main()