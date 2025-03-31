"""
Funçoes para filtragem avançada de operadoras
"""

import pandas as pd
import numpy as np

def  aplicar_filtros(df, termo_busca='',uf='',modalidade='',ordenacao='razao_social', ordem ='asc'):
    """
    Aplicaçao de filtros avançados

    Args:
        df (DataFrame): DataFrame com dados das operadoras
        termo_busca (str): Termo a ser buscado nos dados
        uf (str): UF para filtrar
        modalidade (str): Modalidade para filtrar
        ordenacao (str): Campo para ordenar
        ordem (str): Direção da ordenação ('asc' ou 'desc')
        
    Returns:
        DataFrame: DataFrame filtrado e ordenado
    """
    #normalizar colinas para string
    for col in df.columns:
        if df[col].dtype == np.float64 or df[col].dtype == np.int64:
            df[col]=df[col].astype(str)
        df[col] = df[col].fillna('')

    #aplicar filtro de texto se houver ter,p de busca
    if termo_busca:
        df = df[
            df['Razao_Social'].str.contains(termo_busca, case=False, na=False) |
            df['Nome_Fantasia'].str.contains(termo_busca, case=False, na=False) |
            df['Registro_ANS'].str.contains(termo_busca, case=False, na=False) |
            df['CNPJ'].str.contains(termo_busca, case=False, na=False)
        ]

    #aplicar filtro UF
    if uf:
        df = df[df['UF'].str.upper() == uf.upper()]

    #aplicar filtro de modalidade
    if modalidade:
        df = df[df['Modalidade'].str.contains(modalidade, case=False, na=False)]

    #mapear coluna de ordenaçao (normalizar nomes de colunas)
    mapeamento_colunas = {
        'razao_social': 'Razao_Social',
        'nome_fantasia': 'Nome_Fantasia',
        'registro_ans': 'Registro_ANS',
        'uf': 'UF'
    }
    coluna_ordenacao = mapeamento_colunas.get(ordenacao.lower(), 'Razao_Social')
    
    #aplicar ordenaçao
    asceding= ordem.lower() =='asc'
    df = df.sort_values(by=coluna_ordenacao, ascending=asceding)

    return df

def extrair_opcoes_unicas(df):
    """
    Extrair opcoes unicas e modalidades
    
    Args:
        df (DataFrame): DataFrame com dados das operadoras
        
    Returns:
        dict: Dicionário com listas de UFs e Modalidades únicas
    """
    ufs = df['UF'].dropna().unique().tolist()
    ufs = [uf for uf in ufs if uf and str(uf).strip()]
    ufs.sort()
    
    modalidades = df['Modalidade'].dropna().unique().tolist()
    modalidades = [m for m in modalidades if m and str(m).strip()]
    modalidades.sort()
    
    return {
        'ufs': ufs,
        'modalidades': modalidades
    }