"""
Módulo de API para o teste de nivelamento da IntuitiveCare.

Este módulo implementa uma API RESTful com Flask que permite buscar
operadoras de saúde a partir de dados baixados da ANS, com uma
interface web construída com Vue.js.
"""

from src.api.server import app, buscar_operadoras

__all__ = [
    'app',
    'buscar_operadoras'
]