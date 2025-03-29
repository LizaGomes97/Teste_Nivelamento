"""
Testes unitários para o módulo de banco de dados.
"""

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import os
import sys
import tempfile
import shutil

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bancoDeDados.database import preparar_scripts_sql, extrair_arquivos_zip, obter_script_sql

class TestBancoDados(unittest.TestCase):
    """Classe de testes para o módulo de banco de dados"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar diretório temporário para os testes
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Limpeza após os testes"""
        # Remover diretório temporário
        shutil.rmtree(self.temp_dir)
    
    @patch('src.bancoDeDados.database.obter_script_sql')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="-- SQL script content")
    @patch('pathlib.Path.exists')
    def test_preparar_scripts_sql_com_templates(self, mock_exists, mock_open, mock_obter_script):
        """Testa a preparação de scripts SQL a partir de templates"""
        # Configurar os mocks
        mock_exists.return_value = True
        mock_obter_script.return_value = "-- SQL script content"
        
        # Diretório destino para os scripts SQL
        diretorio_sql = Path(self.temp_dir) / 'sql'
        
        # Executar a função
        scripts_preparados = preparar_scripts_sql(diretorio_sql)
        
        # Verificações
        self.assertIsInstance(scripts_preparados, dict)
        self.assertEqual(len(scripts_preparados), 3)  # Deve ter 3 scripts no dicionário
        mock_open.assert_called()  # Verifica se tentou abrir arquivos
        
        # Verifica se os scripts foram obtidos
        mock_obter_script.assert_called()
    
    @patch('src.bancoDeDados.database.obter_script_sql')
    @patch('pathlib.Path.exists')
    def test_preparar_scripts_sql_sem_templates(self, mock_exists, mock_obter_script):
        """Testa a preparação de scripts SQL quando não há templates disponíveis"""
        # Configurar os mocks
        mock_exists.return_value = True
        mock_obter_script.return_value = None  # Simulando que nenhum script foi encontrado
        
        # Diretório destino para os scripts SQL
        diretorio_sql = Path(self.temp_dir) / 'sql'
        
        # Executar a função
        scripts_preparados = preparar_scripts_sql(diretorio_sql)
        
        # Verificações
        self.assertEqual(len(scripts_preparados), 0)  # Não deve encontrar nenhum script
        mock_obter_script.assert_called()
    
    @patch('pathlib.Path.exists')
    def test_obter_script_sql(self, mock_exists):
        """Testa a obtenção de scripts SQL"""
        # Caso 1: Script existe
        mock_exists.return_value = True
        
        # Mockando a função open para retornar um conteúdo fictício
        with patch('builtins.open', unittest.mock.mock_open(read_data="-- SQL test script")) as mock_file:
            conteudo = obter_script_sql("test.sql")
            self.assertEqual(conteudo, "-- SQL test script")
            mock_file.assert_called_once()
        
        # Caso 2: Script não existe
        mock_exists.return_value = False
        conteudo = obter_script_sql("nonexistent.sql")
        self.assertIsNone(conteudo)
    
    @patch('zipfile.ZipFile')
    def test_extrair_arquivos_zip(self, mock_zipfile):
        """Testa a extração de arquivos ZIP"""
        # Configurar o mock
        mock_zip_instance = MagicMock()
        mock_zip_instance.namelist.return_value = ['arquivo1.csv', 'arquivo2.csv']
        mock_zipfile.return_value.__enter__.return_value = mock_zip_instance
        
        # Arquivos ZIP para extrair
        arquivos_zip = [Path(self.temp_dir) / 'arquivo1.zip', Path(self.temp_dir) / 'arquivo2.zip']
        
        # Diretório de destino
        diretorio_destino = Path(self.temp_dir) / 'extraidos'
        
        # Executar a função
        arquivos_extraidos = extrair_arquivos_zip(arquivos_zip, diretorio_destino)
        
        # Verificações
        self.assertEqual(len(arquivos_extraidos), 4)  # 2 arquivos por ZIP
        mock_zipfile.assert_called()
        mock_zip_instance.extractall.assert_called()

if __name__ == '__main__':
    unittest.main()