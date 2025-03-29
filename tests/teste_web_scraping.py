"""
Testes unitários para o módulo de web scraping.
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

from src.webScraping.scraper import baixar_arquivo, criar_zip, baixar_multiplos_arquivos

class TestWebScraping(unittest.TestCase):
    """Classe de testes para o módulo de web scraping"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar diretório temporário para os testes
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Limpeza após os testes"""
        # Remover diretório temporário
        shutil.rmtree(self.temp_dir)
    
    @patch('requests.get')
    def test_baixar_arquivo(self, mock_get):
        """Testa o download de arquivos"""
        # Configurar o mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content.return_value = [b"conteudo do arquivo"]
        mock_get.return_value = mock_response
        
        # Arquivo para baixar
        url = "https://exemplo.com/arquivo.pdf"
        caminho_destino = Path(self.temp_dir) / "arquivo.pdf"
        
        # Executar a função
        resultado = baixar_arquivo(url, caminho_destino)
        
        # Verificações
        self.assertEqual(resultado, caminho_destino)
        mock_get.assert_called_once_with(url, stream=True)
        self.assertTrue(caminho_destino.exists())
    
    @patch('requests.get')
    def test_baixar_arquivo_erro(self, mock_get):
        """Testa o download de arquivos com erro"""
        # Configurar o mock
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Arquivo para baixar
        url = "https://exemplo.com/arquivo_inexistente.pdf"
        caminho_destino = Path(self.temp_dir) / "arquivo_inexistente.pdf"
        
        # Executar a função
        resultado = baixar_arquivo(url, caminho_destino)
        
        # Verificações
        self.assertFalse(resultado)
        mock_get.assert_called_once_with(url, stream=True)
        self.assertFalse(caminho_destino.exists())
    
    def test_criar_zip(self):
        """Testa a criação de arquivos ZIP"""
        # Criar arquivos de teste
        arquivo1 = Path(self.temp_dir) / "arquivo1.txt"
        arquivo2 = Path(self.temp_dir) / "arquivo2.txt"
        
        with open(arquivo1, 'w') as f:
            f.write("Conteúdo do arquivo 1")
        
        with open(arquivo2, 'w') as f:
            f.write("Conteúdo do arquivo 2")
        
        # Arquivo ZIP para criar
        arquivo_zip = Path(self.temp_dir) / "arquivos.zip"
        
        # Executar a função
        resultado = criar_zip([arquivo1, arquivo2], arquivo_zip)
        
        # Verificações
        self.assertEqual(resultado, arquivo_zip)
        self.assertTrue(arquivo_zip.exists())
        
        # Verificar o conteúdo do ZIP
        import zipfile
        with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
            self.assertEqual(len(zip_ref.namelist()), 2)
            self.assertIn(arquivo1.name, zip_ref.namelist())
            self.assertIn(arquivo2.name, zip_ref.namelist())
    
    @patch('src.webScraping.scraper.baixar_arquivo')
    def test_baixar_multiplos_arquivos(self, mock_baixar_arquivo):
        """Testa o download de múltiplos arquivos"""
        # Configurar o mock
        def side_effect(url, nome_arquivo):
            return nome_arquivo
        
        mock_baixar_arquivo.side_effect = side_effect
        
        # URLs e destinos
        urls = ["https://exemplo.com/arquivo1.pdf", "https://exemplo.com/arquivo2.pdf"]
        diretorio_destino = Path(self.temp_dir)
        
        # Executar a função
        resultado = baixar_multiplos_arquivos(urls, diretorio_destino)
        
        # Verificações
        self.assertEqual(len(resultado), 2)
        self.assertEqual(mock_baixar_arquivo.call_count, 2)
        for i, url in enumerate(urls):
            self.assertEqual(resultado[i], diretorio_destino / url.split('/')[-1])

if __name__ == '__main__':
    unittest.main()