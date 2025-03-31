"""
Servidor Flask para API de busca de operadoras.
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd
import os
from pathlib import Path
from src.api.filtros import aplicar_filtros, extrair_opcoes_unicas

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Isso garante que caracteres não-ASCII sejam preservados
CORS(app)  # Permitir solicitações cross-origin

# Caminho para o arquivo CSV das operadoras
CSV_PATH = Path('data/dados_ans/operadoras/Relatorio_cadop.csv')

def buscar_operadoras(termo_busca='', limite=10, uf='', modalidade='', ordenacao='razao_social', ordem='asc'):
    """
    Busca e filtra operadoras com base em diversos criterios
    """
    # Verificar se o arquivo existe
    if not os.path.exists(CSV_PATH):
        return {'erro': 'Arquivo de operadoras não encontrado'}
    
    try:
        # Carregar o CSV
        df = pd.read_csv(CSV_PATH, sep=';', encoding='utf-8')
        
        # Aplicar filtros avançados
        df_filtrado = aplicar_filtros(df, termo_busca, uf, modalidade, ordenacao, ordem)
        
        # Limitar quantidade de resultados
        resultados = df_filtrado.head(limite)
        
        return resultados.to_dict('records')
    except Exception as e:
        return {'error': str(e)}

# Adicionar rota para obter opções de filtro
@app.route('/api/opcoes-filtro', methods=['GET'])
def api_opcoes_filtro():
    """API endpoint para obter opções de filtro"""
    if not os.path.exists(CSV_PATH):
        return jsonify({'erro': 'Arquivo de operadoras não encontrado'})
    
    try:
        df = pd.read_csv(CSV_PATH, sep=';', encoding='utf-8')
        opcoes = extrair_opcoes_unicas(df)
        return jsonify(opcoes)
    except Exception as e:
        return jsonify({'error': str(e)})

# Rota de API para buscar operadoras
@app.route('/api/operadoras', methods=['GET'])
def api_buscar_operadoras():
    termo_busca = request.args.get('q', '')
    limite = int(request.args.get('limite', 10))
    uf = request.args.get('uf', '')
    modalidade = request.args.get('modalidade', '')
    ordenacao = request.args.get('ordenacao', 'razao_social')
    ordem = request.args.get('ordem', 'asc')

    resultados = buscar_operadoras(termo_busca, limite, uf, modalidade, ordenacao, ordem)
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