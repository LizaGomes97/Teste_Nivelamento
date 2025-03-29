"""
Funções para web scraping do site da ANS e download de arquivos.
"""

import requests
import os 
import zipfile
from pathlib import Path

def baixar_arquivo(url, nome_arquivo):
    """
    Baixa um arquivo da URL especificada e salva com o nome especificado
    
    Args:
        url (str): URL do arquivo para download
        nome_arquivo (str ou Path): Caminho onde o arquivo será salvo
    
    Returns:
        Path ou bool: Caminho do arquivo se o download foi bem-sucedido, False caso contrário
    """
    print(f"Baixando {nome_arquivo}...")
    try:
        resposta = requests.get(url, stream=True, timeout=30)
        
        # Verificação da requisição
        if resposta.status_code == 200:
            # Garantir que o diretório exista
            if isinstance(nome_arquivo, str):
                nome_arquivo = Path(nome_arquivo)
            nome_arquivo.parent.mkdir(parents=True, exist_ok=True)
            
            # Baixar arquivo em pedaços
            with open(nome_arquivo, 'wb') as arquivo:
                # Reúne os pedaços
                for pedaco in resposta.iter_content(chunk_size=8192):
                    arquivo.write(pedaco)
            print(f"Download de {nome_arquivo} concluído!")
            return nome_arquivo  # Retorna o Path para compatibilidade com o resto do código
        else:
            print(f"Erro ao baixar {nome_arquivo}. Código do erro: {resposta.status_code}")
            return False
    except Exception as e:
        print(f"Erro durante o download de {nome_arquivo}: {str(e)}")
        return False
    
def criar_zip(lista_arquivos, nome_arquivo_zip):
    """
    Cria um arquivo ZIP com os arquivos da lista

    Args:
        lista_arquivos (list): Lista de caminhos dos arquivos a serem compactados
        nome_arquivo_zip (str ou Path): Caminho onde o arquivo ZIP será salvo

    Returns:
        Path ou bool: Caminho do arquivo ZIP se a compactação foi bem-sucedida, False caso contrário
    """
    print(f"Criando arquivo ZIP {nome_arquivo_zip}...")
    try:
        if isinstance(nome_arquivo_zip, str):
            nome_arquivo_zip = Path(nome_arquivo_zip)
        nome_arquivo_zip.parent.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(nome_arquivo_zip, 'w') as arquivo_zip:
            for arquivo in lista_arquivos:
                arquivo_zip.write(arquivo, arcname=os.path.basename(arquivo))
        print(f"Arquivo ZIP {nome_arquivo_zip} criado!")
        return nome_arquivo_zip
    except Exception as e:
        print(f"Erro ao criar ZIP: {e}")
        return False
    
def baixar_multiplos_arquivos(urls, diretorio_destino, nomes_arquivos=None):
    """
    Baixa múltiplos arquivos e retorna a lista de arquivos baixados

    Args:
        urls (list): Lista de URLs dos arquivos para download
        diretorio_destino (str ou Path): Diretório onde os arquivos serão salvos
        nome_arquivos (list, optional): Lista de nomes para os arquivos.
                                        Se None, usa os nomes originais das URLs.

    Returns:
        list: Lista de caminhos dos arquivos baixados com sucesso
    """
    # Converter para Path se for string
    if isinstance(diretorio_destino, str):
        diretorio_destino = Path(diretorio_destino)

    # Criar diretório se não existir
    diretorio_destino.mkdir(parents=True, exist_ok=True)

    arquivos_baixados = []

    for i, url in enumerate(urls):
        # Determinar o nome do arquivo
        if nomes_arquivos and i < len(nomes_arquivos):
            nome_arquivo = nomes_arquivos[i]
        else:
            nome_arquivo = url.split('/')[-1]

        caminho_destino = diretorio_destino / nome_arquivo

        arquivo_baixado = baixar_arquivo(url, caminho_destino)
        if arquivo_baixado:
            arquivos_baixados.append(caminho_destino)

    return arquivos_baixados

def principal():
    """
    Função principal para o teste de Web Scraping
    
    1. Acessa o site da ANS
    2. Baixa os Anexos I e II em formato PDF
    3. Compacta os anexos em um único arquivo ZIP
    """
    # URL's dos anexos
    url_1 = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
    url_2 = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"

    # Diretório e nomes dos arquivos
    diretorio_saida = Path('data/anexos')
    urls = [url_1, url_2]
    nomes_arquivos = ['Anexo_I.pdf', 'Anexo_II.pdf']
    nome_arquivo_zip = diretorio_saida / "Anexos.zip"

    print("=== TESTE 1: WEB SCRAPING ===")
    print("Baixando anexos da ANS...")

    # Baixar os arquivos usando a nova função
    arquivos_baixados = baixar_multiplos_arquivos(urls, diretorio_saida, nomes_arquivos)

    # Verificar se todos os arquivos foram baixados
    if len(arquivos_baixados) == len(urls):
        criar_zip(arquivos_baixados, nome_arquivo_zip)
        print(f"Processo concluído com sucesso! Arquivos baixados e compactados em {nome_arquivo_zip}")
        return True
    else:
        print(f"Erro: Não foi possível baixar todos os arquivos.")
        return False

if __name__ == "__main__":
    principal()