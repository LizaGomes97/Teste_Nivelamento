"""
Testes unitários para o módulo de API.
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import json
from pathlib import Path
import os
import sys

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.server import app, buscar_operadoras

class TestAPI(unittest.TestCase):
    """Classe de testes para o módulo de API"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Configurar o cliente de teste
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        # Criar um DataFrame de exemplo para simular os dados
        self.df_exemplo = pd.DataFrame({
            'Registro_ANS': ['123456', '789012'],
            'Razao_Social': ['Operadora A', 'Operadora B'],
            'Nome_Fantasia': ['Plano A', 'Plano B'],
            'CNPJ': ['12345678901234', '98765432109876'],
            'Modalidade': ['Cooperativa', 'Medicina de Grupo'],
            'UF': ['SP', 'RJ']
        })
    
    @patch('pandas.read_csv')
    @patch('os.path.exists')
    def test_buscar_operadoras_sem_termo(self, mock_exists, mock_read_csv):
        """Testa a busca de operadoras sem termo de busca"""
        # Configurar mocks
        mock_exists.return_value = True
        mock_read_csv.return_value = self.df_exemplo
        
        # Executar a função
        resultado = buscar_operadoras()
        
        # Verificações
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0]['Registro_ANS'], '123456')
        self.assertEqual(resultado[1]['Registro_ANS'], '789012')
        mock_read_csv.assert_called_once()
    
    @patch('pandas.read_csv')
    @patch('os.path.exists')
    def test_buscar_operadoras_com_termo(self, mock_exists, mock_read_csv):
        """Testa a busca de operadoras com termo de busca"""
        # Configurar mocks
        mock_exists.return_value = True
        mock_read_csv.return_value = self.df_exemplo
        
        # Executar a função
        resultado = buscar_operadoras('Plano A')
        
        # Verificações
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]['Nome_Fantasia'], 'Plano A')
        mock_read_csv.assert_called_once()
    
    @patch('os.path.exists')
    def test_buscar_operadoras_arquivo_inexistente(self, mock_exists):
        """Testa a busca quando o arquivo não existe"""
        # Configurar mock
        mock_exists.return_value = False
        
        # Executar a função
        resultado = buscar_operadoras()
        
        # Verificações
        self.assertIn('erro', resultado)
        self.assertEqual(resultado['erro'], 'Arquivo de operadoras não encontrado')
    
    def test_rota_api_operadoras(self):
        """Testa a rota /api/operadoras"""
        # Configurar mock para a função buscar_operadoras
        with patch('src.api.server.buscar_operadoras') as mock_buscar:
            # Configurar retorno do mock
            mock_buscar.return_value = [
                {
                    'Registro_ANS': '123456',
                    'Razao_Social': 'Operadora A',
                    'Nome_Fantasia': 'Plano A',
                    'CNPJ': '12345678901234',
                    'Modalidade': 'Cooperativa',
                    'UF': 'SP'
                }
            ]
            
            # Fazer requisição para a API
            response = self.client.get('/api/operadoras?q=Plano&limite=10')
            
            # Verificações
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['Registro_ANS'], '123456')
            mock_buscar.assert_called_once_with('Plano', 10)
    
    def test_rota_api_status(self):
        """Testa a rota /api"""
        # Fazer requisição para a API
        response = self.client.get('/api')
        
        # Verificações
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertIn('endpoints', data)
        self.assertEqual(data['status'], 'Servidor funcionando')

if __name__ == '__main__':
    unittest.main()