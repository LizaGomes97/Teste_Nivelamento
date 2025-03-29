"""
Funções para baixar, processar e analisar dados da ANS e gerar scripts SQL.
"""

import os
from pathlib import Path
import datetime
import zipfile
import pandas as pd

# Importar funções do módulo de web scraping
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.webScraping.scraper import baixar_arquivo, criar_zip, baixar_multiplos_arquivos

def extrair_arquivos_zip(arquivos_zip, diretorio_destino):
    """
    Extrai os arquivos ZIP para o diretório de destino
    
    Args:
        arquivos_zip (list): Lista de caminhos para arquivos ZIP a serem extraídos
        diretorio_destino (str ou Path): Diretório onde os arquivos serão extraídos
        
    Returns:
        list: Lista de caminhos dos arquivos extraídos
    """
    print(f"Extraindo arquivos ZIP para {diretorio_destino}...")
    
    # Converter para Path se for string
    if isinstance(diretorio_destino, str):
        diretorio_destino = Path(diretorio_destino)
    
    # Criar diretório se não existir
    diretorio_destino.mkdir(parents=True, exist_ok=True)
    
    arquivos_extraidos = []
    
    for arquivo_zip in arquivos_zip:
        print(f"Extraindo {arquivo_zip}...")
        
        with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
            zip_ref.extractall(diretorio_destino)
            arquivos_extraidos.extend([diretorio_destino / nome for nome in zip_ref.namelist()])
    
    return arquivos_extraidos

def analisar_estrutura_arquivos(diretorio_dados):
    """
    Analisa a estrutura dos arquivos baixados para ajudar a criar os scripts SQL
    
    Args:
        diretorio_dados (str ou Path): Diretório contendo os arquivos a serem analisados
        
    Returns:
        dict: Dicionário com informações sobre a estrutura dos arquivos
    """
    print("\nAnalisando estrutura dos arquivos...")
    
    if isinstance(diretorio_dados, str):
        diretorio_dados = Path(diretorio_dados)
    
    arquivos_csv = list(diretorio_dados.glob("**/*.csv"))
    
    if not arquivos_csv:
        print("Nenhum arquivo CSV encontrado para análise.")
        return {}
    
    print(f"Encontrados {len(arquivos_csv)} arquivos CSV:")
    
    estrutura = {}
    
    for arquivo in arquivos_csv:
        try:
            df = pd.read_csv(arquivo, sep=';', encoding='latin1', nrows=5)
            
            print(f"\nArquivo: {arquivo}")
            print(f"Dimensões: {df.shape[0]} linhas x {df.shape[1]} colunas")
            print("Colunas:")
            for col in df.columns:
                print(f"  - {col}")
            
            estrutura[str(arquivo)] = {
                'colunas': list(df.columns),
                'linhas': df.shape[0],
                'encoding': 'latin1'
            }
        except Exception as e:
            print(f"Erro ao analisar {arquivo}: {e}")
    
    return estrutura

def obter_script_sql(nome_script):
    """
    Lê o conteúdo de um arquivo SQL
    
    Args:
        nome_script (str): Nome do arquivo SQL (sem caminho)
        
    Returns:
        str: Conteúdo do arquivo SQL ou None se o arquivo não existir
    """
    # Caminhos para scripts SQL
    diretorio_base = Path(__file__).parent.parent.parent  # Raiz do projeto
    diretorio_scripts = diretorio_base / "scripts" / "sql"
    caminho_script = diretorio_scripts / nome_script
    
    if not caminho_script.exists():
        print(f"Aviso: Script SQL {nome_script} não encontrado em {diretorio_scripts}")
        return None
    
    try:
        with open(caminho_script, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        return conteudo
    except Exception as e:
        print(f"Erro ao ler script {nome_script}: {e}")
        return None

def executar_script_sql(nome_script, conexao=None):
    """
    Lê e opcionalmente executa um script SQL
    
    Args:
        nome_script (str): Nome do arquivo SQL (sem caminho)
        conexao (objeto de conexão, opcional): Conexão com o banco de dados
        
    Returns:
        str: Conteúdo do script SQL
    """
    conteudo = obter_script_sql(nome_script)
    
    if conteudo is None:
        return None
    
    # Se foi fornecida uma conexão, executa o script
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute(conteudo)
            conexao.commit()
            print(f"Script {nome_script} executado com sucesso")
        except Exception as e:
            print(f"Erro ao executar script {nome_script}: {e}")
    
    return conteudo

def preparar_scripts_sql(diretorio_sql):
    """
    Prepara scripts SQL para o banco de dados, lendo dos arquivos de template
    
    Args:
        diretorio_sql (str ou Path): Diretório onde os scripts SQL serão salvos
        
    Returns:
        dict: Dicionário com o conteúdo dos scripts SQL
    """
    print("Preparando scripts SQL para análise...")
    
    # Garantir que o diretório de saída existe
    if isinstance(diretorio_sql, str):
        diretorio_sql = Path(diretorio_sql)
    
    diretorio_sql.mkdir(parents=True, exist_ok=True)
    
    # Nomes dos scripts
    nomes_scripts = {
        "criar_tabelas.sql": diretorio_sql / "1_criar_tabelas.sql",
        "importar_dados.sql": diretorio_sql / "2_importar_dados.sql",
        "consultas_analiticas.sql": diretorio_sql / "3_consultas_analiticas.sql"
    }
    
    scripts = {}
    
    # Ler o conteúdo de cada script
    for nome_script, caminho_destino in nomes_scripts.items():
        conteudo = obter_script_sql(nome_script)
        
        if conteudo:
            # Salvar o script no diretório de destino
            with open(caminho_destino, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            
            scripts[nome_script] = conteudo
            print(f"  ✓ Script {caminho_destino.name} preparado")
        else:
            print(f"  ✗ Script {nome_script} não disponível")
    
    print(f"{len(scripts)} scripts SQL preparados em {diretorio_sql}")
    
    return scripts

def main():
    """
    Função principal para o teste de Banco de Dados
    
    1. Baixa os arquivos dos últimos 2 anos do repositório público da ANS
    2. Baixa os dados cadastrais das operadoras ativas
    3. Cria queries para estruturar tabelas
    4. Elabora queries para importar o conteúdo dos arquivos
    5. Desenvolve queries analíticas
    """
    # Obter o ano e mês atual
    data_atual = datetime.datetime.now()
    ano_atual = data_atual.year
    mes_atual = data_atual.month
    
    # Determinar os anos para download com base no mês atual
    if mes_atual < 6:  # Primeiro semestre
        anos = [ano_atual-2, ano_atual-1]
    else:  # Segundo semestre
        anos = [ano_atual-1, ano_atual]
    
    # Diretórios para dados
    diretorio_base = Path("data/dados_ans")
    diretorio_demonstracoes = diretorio_base / "demonstracoes"
    diretorio_operadoras = diretorio_base / "operadoras"
    diretorio_sql = Path("scripts/sql")
    
    # Criar diretórios
    diretorio_base.mkdir(parents=True, exist_ok=True)
    diretorio_demonstracoes.mkdir(parents=True, exist_ok=True)
    diretorio_operadoras.mkdir(parents=True, exist_ok=True)
    
    print(f"=== TESTE 3: BANCO DE DADOS ANS ===")
    print(f"Data atual: {data_atual.strftime('%Y-%m-%d')}")
    print(f"Anos para análise: {', '.join(map(str, anos))}")
    
    # Download do arquivo de operadoras
    url_operadoras = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
    arquivo_operadoras = baixar_arquivo(url_operadoras, diretorio_operadoras / "Relatorio_cadop.csv")
    
    # Para as demonstrações contábeis, vamos baixar os arquivos trimestrais de cada ano
    arquivos_demonstracoes = []
    for ano in anos:
        # Diretório específico para cada ano
        diretorio_ano = diretorio_demonstracoes / str(ano)
        diretorio_ano.mkdir(exist_ok=True)
        
        # URLs de arquivos trimestrais (arquivos ZIP)
        urls_arquivos = [
            f"https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/{ano}/1T{ano}.zip",
            f"https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/{ano}/2T{ano}.zip",
            f"https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/{ano}/3T{ano}.zip",
            f"https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/{ano}/4T{ano}.zip"
        ]
        
        # Tentar baixar cada arquivo trimestral
        for url in urls_arquivos:
            nome_arquivo = url.split('/')[-1]
            arquivo_baixado = baixar_arquivo(url, diretorio_ano / nome_arquivo)
            if arquivo_baixado:
                arquivos_demonstracoes.append(arquivo_baixado)
    
    # Extrair arquivos ZIP
    arquivos_extraidos = []
    if arquivos_demonstracoes:
        diretorio_extraidos = diretorio_demonstracoes / "extraidos"
        arquivos_extraidos = extrair_arquivos_zip(arquivos_demonstracoes, diretorio_extraidos)
    
    # Analisar estrutura dos arquivos
    estrutura = analisar_estrutura_arquivos(diretorio_base)
    
    # Preparar scripts SQL
    scripts = preparar_scripts_sql(diretorio_sql)
    
    print("\n=== RESUMO ===")
    if arquivo_operadoras and len(arquivos_demonstracoes) > 0:
        print("✅ Downloads concluídos com sucesso!")
        print(f"✅ {len(arquivos_demonstracoes)} arquivos de demonstrações contábeis baixados")
        print(f"✅ {len(arquivos_extraidos)} arquivos extraídos dos ZIPs")
        print(f"✅ Scripts SQL preparados: {', '.join(scripts.keys())}")
        print("\nPróximos passos:")
        print("1. Verifique os arquivos baixados")
        print("2. Revise os scripts SQL gerados e ajuste-os conforme necessário")
        print("3. Execute os scripts em seu banco de dados MySQL ou PostgreSQL")
        return True
    else:
        print("❌ Ocorreram problemas durante o download.")
        if not arquivo_operadoras:
            print("  - Falha ao baixar dados das operadoras")
        if len(arquivos_demonstracoes) == 0:
            print("  - Falha ao baixar demonstrações contábeis")
        return False

if __name__ == "__main__":
    main()