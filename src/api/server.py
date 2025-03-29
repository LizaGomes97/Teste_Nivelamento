"""
Servidor Flask para API de busca de operadoras.
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd
import os
from pathlib import Path

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Isso garante que caracteres não-ASCII sejam preservados
CORS(app)  # Permitir solicitações cross-origin

# Caminho para o arquivo CSV das operadoras
CSV_PATH = Path('data/dados_ans/operadoras/Relatorio_cadop.csv')

def buscar_operadoras(termo_busca='', limite=10):
    """
    Busca e filtra operadoras com base em um termo de busca
    
    Args:
        termo_busca (str): Termo a ser buscado nos dados das operadoras
        limite (int): Número máximo de resultados a retornar
        
    Returns:
        list: Lista de dicionários com os dados das operadoras encontradas
    """
    # Verificar se o arquivo existe
    if not os.path.exists(CSV_PATH):
        return {'erro': 'Arquivo de operadoras não encontrado'}
    
    try:
        # Carregar o CSV
        df = pd.read_csv(CSV_PATH, sep=';', encoding='utf-8')

        # Se não houver termo de busca, retornar as primeiras operadoras
        if not termo_busca:
            resultado = df.head(limite)
            # Converter todas as colunas para strings
            resultado = resultado.astype(str)
            # Substituir 'nan' por string vazia
            resultado = resultado.replace('nan', '')
            return resultado.to_dict('records')

        # Convertendo colunas para string para evitar erros
        for col in df.columns:
            df[col] = df[col].astype(str)
            df[col] = df[col].replace('nan', '')

        # Filtrar os dados por diferentes colunas
        resultados = df[
            df['Razao_Social'].str.contains(termo_busca, case=False, na=False) |
            df['Nome_Fantasia'].str.contains(termo_busca, case=False, na=False) |
            df['Registro_ANS'].str.contains(termo_busca, case=False, na=False) |
            df['CNPJ'].str.contains(termo_busca, case=False, na=False)
        ]

        # Limitar quantidade de resultados
        return resultados.head(limite).to_dict('records')

    except Exception as e:
        return {'error': str(e)}

# Rota de API para buscar operadoras
@app.route('/api/operadoras', methods=['GET'])
def api_buscar_operadoras():
    """API endpoint para buscar operadoras"""
    termo_busca = request.args.get('q', '')
    limite = int(request.args.get('limite', 10))

    resultados = buscar_operadoras(termo_busca, limite)
    response = jsonify(resultados)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

# Rota principal para verificar se o servidor está funcionando
@app.route('/api')
def api_status():
    """Rota para verificar status da API"""
    return jsonify({
        "status": "Servidor funcionando", 
        "endpoints": ["/api/operadoras"]
    })

# Rota para servir o HTML da interface
@app.route('/')
def serve_index():
    """Rota para servir a página principal"""
    # Obtém o caminho absoluto para o diretório static
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../static'))
    return send_from_directory(static_dir, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Rota para servir arquivos estáticos"""
    # Obtém o caminho absoluto para o diretório static
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../static'))
    return send_from_directory(static_dir, path)
def main():
    """
    Função principal para o teste de API
    
    1. Implementa uma API para busca textual de operadoras
    2. Serve a interface web para interagir com a API
    """
    print("=== TESTE 4: API ===")
    print("Iniciando servidor em http://localhost:5000")
    print("Para encerrar o servidor, pressione CTRL+C")
    
    app.run(debug=True)

if __name__ == '__main__':
    main()