"""
Funções para extração e transformação de dados de PDFs.
"""

import tabula
import pandas as pd
import os
import zipfile
from pathlib import Path

# Importar funções do módulo de web scraping
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.webScraping.scraper import criar_zip

def extrair_tabela_pdf(caminho_pdf):
    """
    Extrair todas as tabelas do PDF
    
    Args:
        caminho_pdf (str ou Path): Caminho para o arquivo PDF
        
    Returns:
        list: Lista de DataFrames com as tabelas extraídas
    """
    print(f"Extraindo tabelas do arquivo {caminho_pdf}...")

    # Configuração para encoding
    tabula.environment_info()  # Para verificar a configuração

    # Extrai tabelas de todas as páginas do PDF
    try:
        tabelas = tabula.read_pdf(
            caminho_pdf,
            pages="all",
            multiple_tables=True,
            lattice=True,
            guess=False,
            encoding='latin1'  # Usando Latin-1 ao invés de UTF-8
        )

        print(f"Extração concluída. {len(tabelas)} tabelas encontradas.")
        return tabelas
    except Exception as e:
        print(f"Erro ao extrair tabelas: {e}")
        # Tenta uma abordagem alternativa para caso de erro
        try:
            tabelas = tabula.read_pdf(
                caminho_pdf,
                pages="all",
                multiple_tables=True,
                stream=True,  # Tenta o modo stream em vez de lattice
                guess=True
            )
            print(f"Extração alternativa concluída. {len(tabelas)} tabelas encontradas.")
            return tabelas
        except Exception as e2:
            print(f"Erro na extração alternativa: {e2}")
            return []

def combinar_tabelas(tabelas):
    """
    Combina as tabelas em um único DataFrame
    
    Args:
        tabelas (list): Lista de DataFrames com as tabelas extraídas
        
    Returns:
        DataFrame: DataFrame combinado com todas as tabelas
    """
    # Inicia com a primeira tabela se existir
    if not tabelas:
        return pd.DataFrame()
    
    df_combinado = pd.DataFrame()

    # Percorre todas as tabelas e as combina
    for i, tabela in enumerate(tabelas):
        # Limpa a atual
        tabela_limpa = limpar_tabela(tabela)

        # Usa a primeira tabela válida como base
        if df_combinado.empty and not tabela_limpa.empty:
            df_combinado = tabela_limpa
        
        # Caso contrário, concatenamos com a tabela combinada
        elif not tabela_limpa.empty:
            # Verificamos se as colunas são compatíveis
            if set(df_combinado.columns) == set(tabela_limpa.columns):
                df_combinado = pd.concat([df_combinado, tabela_limpa], ignore_index=True)
            else:
                print(f"Aviso: Tabela {i+1} tem estrutura diferente e será ignorada.")

    return df_combinado
    
def limpar_tabela(tabela):
    """
    Remove as linhas vazias e normaliza os dados
    
    Args:
        tabela (DataFrame): DataFrame com a tabela extraída
        
    Returns:
        DataFrame: DataFrame limpo e normalizado
    """
    # Remove linhas onde todas as colunas são NaN
    tabela = tabela.dropna(how='all')

    # Converte colunas para string e remove espaços extras
    tabela = tabela.astype(str)
    for col in tabela.columns:
        tabela[col] = tabela[col].str.strip()

    return tabela
    
def substituir_abreviacoes(df):
    """
    Substitui as abreviações OD e AMB pelas descrições completas
    
    Args:
        df (DataFrame): DataFrame com os dados extraídos
        
    Returns:
        DataFrame: DataFrame com as abreviações substituídas
    """
    mapeamento = {
        'OD': 'Seg. Odontológica',
        'AMB': 'Seg. Ambulatorial'
    }

    # Verifica se as colunas existem antes de substituir
    for abrev, descricao in mapeamento.items():
        if abrev in df.columns:
            df = df.rename(columns={abrev: descricao})

    return df
    
def salvar_csv(df, caminho_csv):
    """
    Salvar DataFrame em um arquivo CSV
    
    Args:
        df (DataFrame): DataFrame com os dados a serem salvos
        caminho_csv (str ou Path): Caminho onde o CSV será salvo
        
    Returns:
        bool: True se os dados foram salvos com sucesso, False caso contrário
    """
    print(f'Salvando dados em {caminho_csv}...')
    
    try:
        # Garantir que o diretório exista
        if isinstance(caminho_csv, str):
            caminho_csv = Path(caminho_csv)
        caminho_csv.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(caminho_csv, index=False, encoding='utf-8')
        print(f'Dados salvos com sucesso')
        return True
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")
        return False
    
def compactar_csv(caminho_csv, nome_zip):
    """
    Compactar CSV em ZIP
    
    Args:
        caminho_csv (str ou Path): Caminho do arquivo CSV a ser compactado
        nome_zip (str ou Path): Caminho onde o ZIP será salvo
        
    Returns:
        bool: True se a compactação foi bem-sucedida, False caso contrário
    """
    print(f"Compactando {caminho_csv} em {nome_zip}...")
    
    try:
        # Garantir que o diretório exista
        if isinstance(nome_zip, str):
            nome_zip = Path(nome_zip)
        nome_zip.parent.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(nome_zip, 'w') as arquivo_zip:
            arquivo_zip.write(caminho_csv, arcname=os.path.basename(caminho_csv))
        print(f'Compactação concluída com sucesso!')
        return True
    except Exception as e:
        print(f"Erro ao compactar CSV: {e}")
        return False
    
def principal():
    """
    Função principal para o teste de Transformação de Dados
    
    1. Extrai dados da tabela Rol de Procedimentos do PDF do Anexo I
    2. Salva os dados em formato CSV
    3. Compacta o CSV em um arquivo ZIP
    4. Substitui abreviações por descrições completas
    """
    # Define os caminhos dos arquivos
    meu_nome = "Lizandra"  

    diretorio_base = Path('.')
    diretorio_anexos = Path('data/anexos')
    caminho_pdf = diretorio_anexos / "Anexo_I.pdf"
    
    diretorio_saida = Path('output')
    diretorio_saida.mkdir(parents=True, exist_ok=True)
    
    caminho_csv = diretorio_saida / "tabela_rol_procedimentos.csv"
    nome_zip = diretorio_saida / f"Teste_{meu_nome}.zip"

    print("=== TESTE 2: TRANSFORMAÇÃO DE DADOS ===")

    # Verificando se o PDF existe
    if not caminho_pdf.exists():
        print(f"Erro: O arquivo {caminho_pdf} não existe.")
        print("Execute primeiro o Teste 1 (Web Scraping) para baixar os anexos.")
        return False
        
    # Extrai as tabelas do PDF
    tabelas = extrair_tabela_pdf(caminho_pdf)

    if not tabelas:
        print("Nenhuma tabela encontrada no PDF.")
        return False

    # Combina as tabelas em um único DataFrame
    df_combinado = combinar_tabelas(tabelas)

    if df_combinado.empty:
        print("Não foi possível combinar as tabelas extraídas.")
        return False

    # Substitui as abreviações pelas descrições completas
    df_limpo = substituir_abreviacoes(df_combinado)

    # Salva os dados em um arquivo CSV
    if salvar_csv(df_limpo, caminho_csv):
        # Compacta o CSV
        if compactar_csv(caminho_csv, nome_zip):
            print(f"Processo concluído com sucesso! Arquivo final: {nome_zip}")
            return True
        else:
            print("Erro ao compactar o arquivo CSV.")
            return False
    else:
        print("Erro ao salvar dados em CSV.")
        return False

if __name__ == "__main__":
    principal()