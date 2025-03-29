"""
Script para criar o arquivo ZIP final com todos os arquivos do projeto.

Este script compacta todos os arquivos relevantes para entrega à IntuitiveCare.
"""

import os
import zipfile
import datetime
from pathlib import Path
import shutil

def criar_zip_final(nome_candidato):
    """
    Cria um arquivo ZIP com todos os arquivos do projeto
    
    Args:
        nome_candidato (str): Nome do candidato para inclusão no nome do arquivo ZIP
        
    Returns:
        Path: Caminho para o arquivo ZIP criado
    """
    # Data atual para o nome do arquivo
    data_atual = datetime.datetime.now().strftime("%Y%m%d")
    
    # Nome do arquivo ZIP final
    nome_zip = f"IntuitiveCare_Testes_{nome_candidato}_{data_atual}.zip"
    
    # Diretórios e arquivos a incluir
    diretorios_incluir = [
        "src",
        "scripts",
        "static",
        "tests"
    ]
    
    arquivos_incluir = [
        "main.py",
        "requirements.txt",
        "README.md"
    ]
    
    # Diretórios a excluir do ZIP
    diretorios_excluir = [
        "__pycache__",
        ".git",
        ".venv",
        "venv",
        "env",
        ".idea",
        ".vscode"
    ]
    
    # Criar diretório temporário para organizar arquivos
    temp_dir = Path("temp_zip")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    
    # Copiar diretórios relevantes
    for diretorio in diretorios_incluir:
        dir_path = Path(diretorio)
        if dir_path.exists():
            # Copiar para o diretório temporário
            shutil.copytree(
                dir_path, 
                temp_dir / diretorio,
                ignore=shutil.ignore_patterns(*diretorios_excluir)
            )
    
    # Copiar arquivos individuais
    for arquivo in arquivos_incluir:
        file_path = Path(arquivo)
        if file_path.exists():
            shutil.copy2(file_path, temp_dir / arquivo)
    
    # Criar o arquivo ZIP
    with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname=arcname)
    
    # Remover diretório temporário
    shutil.rmtree(temp_dir)
    
    print(f"Arquivo ZIP criado: {nome_zip}")
    return Path(nome_zip)

if __name__ == "__main__":
    # Solicitar nome do candidato
    nome_candidato = input("Digite seu nome (sem espaços): ").strip()
    if not nome_candidato:
        nome_candidato = "Candidato"
    
    # Criar o ZIP final
    zip_path = criar_zip_final(nome_candidato)