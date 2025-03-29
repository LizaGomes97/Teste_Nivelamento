"""
Testes unitários para o módulo de transformação de dados.
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from pathlib import Path
import os
import sys
import tempfile
import shutil

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.transformacoesDados.extrator_pdf import (
    extrair_tabela_pdf, 
    combinar_tabelas, 
    limpar_tabela, 
    substituir_abreviacoes,
    salvar_csv, 
    compactar_csv
)

class TestTransformacaoDados(unittest.TestCase):
    """Classe de testes para o módulo de transformação de dados"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar diretório temporário para os testes
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Limpeza após os testes"""
        # Remover diretório temporário
        shutil.rmtree(self.temp_dir)
    
    @patch('tabula.read_pdf')
    def test_extrair_tabela_pdf(self, mock_read_pdf):
        """Testa a extração de tabelas de PDFs"""
        # Configurar o mock
        mock_df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        mock_df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
        mock_read_pdf.return_value = [mock_df1, mock_df2]
        
        # Arquivo PDF para extrair
        caminho_pdf = Path(self.temp_dir) / "documento.pdf"
        
        # Executar a função
        resultado = extrair_tabela_pdf(caminho_pdf)
        
        # Verificações
        self.assertEqual(len(resultado), 2)
        pd.testing.assert_frame_equal(resultado[0], mock_df1)
        pd.testing.assert_frame_equal(resultado[1], mock_df2)
        mock_read_pdf.assert_called_once()
    
    def test_combinar_tabelas(self):
        """Testa a combinação de tabelas"""
        # Criar tabelas de teste
        tabela1 = pd.DataFrame({'A': ['1', '2'], 'B': ['3', '4']})
        tabela2 = pd.DataFrame({'A': ['5', '6'], 'B': ['7', '8']})
        
        # Executar a função
        resultado = combinar_tabelas([tabela1, tabela2])
        
        # Verificações
        self.assertEqual(len(resultado), 4)  # 2 linhas de cada tabela
        self.assertEqual(list(resultado.columns), ['A', 'B'])
        self.assertEqual(resultado['A'].tolist(), ['1', '2', '5', '6'])
        self.assertEqual(resultado['B'].tolist(), ['3', '4', '7', '8'])
    
    def test_limpar_tabela(self):
        """Testa a limpeza de tabelas"""
        # Criar tabela de teste com valores nulos e espaços
        tabela = pd.DataFrame({
            'A': [1, None, 3],
            'B': [' valor1 ', 'valor2', ' valor3']
        })
        
        # Executar a função
        resultado = limpar_tabela(tabela)
        
        # Verificações
        self.assertEqual(len(resultado), 3)  # Deve remover a linha com None
        #verifica se espaços extras foram removidos
        self.assertEqual(resultado['B'][0], 'valor1')
    
    def test_substituir_abreviacoes(self):
        """Testa a substituição de abreviações"""
        # Criar tabela de teste com abreviações
        df = pd.DataFrame(columns=['OD', 'AMB', 'Outra'])
        
        # Executar a função
        resultado = substituir_abreviacoes(df)
        
        # Verificações
        self.assertIn('Seg. Odontológica', resultado.columns)
        self.assertIn('Seg. Ambulatorial', resultado.columns)
        self.assertIn('Outra', resultado.columns)  # Não deve alterar esta coluna
    
    def test_salvar_csv(self):
        """Testa o salvamento de DataFrames em CSV"""
        # Criar DataFrame de teste
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        
        # Caminho para salvar o CSV
        caminho_csv = Path(self.temp_dir) / "dados.csv"
        
        # Executar a função
        resultado = salvar_csv(df, caminho_csv)
        
        # Verificações
        self.assertTrue(resultado)
        self.assertTrue(caminho_csv.exists())
        
        # Verificar o conteúdo do CSV
        df_lido = pd.read_csv(caminho_csv)
        pd.testing.assert_frame_equal(df_lido, df)
    
    def test_compactar_csv(self):
        """Testa a compactação de arquivos CSV"""
        # Criar arquivo CSV de teste
        caminho_csv = Path(self.temp_dir) / "dados.csv"
        with open(caminho_csv, 'w') as f:
            f.write("A,B\n1,2\n3,4\n")
        
        # Caminho para o arquivo ZIP
        caminho_zip = Path(self.temp_dir) / "dados.zip"
        
        # Executar a função
        resultado = compactar_csv(caminho_csv, caminho_zip)
        
        # Verificações
        self.assertTrue(resultado)
        self.assertTrue(caminho_zip.exists())
        
        # Verificar o conteúdo do ZIP
        import zipfile
        with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
            self.assertEqual(len(zip_ref.namelist()), 1)
            self.assertIn(caminho_csv.name, zip_ref.namelist())

if __name__ == '__main__':
    unittest.main()