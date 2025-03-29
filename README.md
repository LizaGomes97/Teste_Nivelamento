# Testes de Nivelamento IntuitiveCare

Este projeto contém a implementação dos testes de nivelamento solicitados pela IntuitiveCare, organizados em uma estrutura modular de fácil manutenção.

## Estrutura do Projeto

```
intuitive_care_testes/
│
├── src/                        # Código fonte principal
│   ├── web_scraping/           # Módulo de web scraping (Teste 1)
│   ├── transformacao_dados/    # Módulo de transformação de dados (Teste 2)
│   ├── banco_dados/            # Módulo de banco de dados (Teste 3)
│   └── api/                    # Módulo para o teste de API (Teste 4)
│
├── tests/                      # Testes unitários
│
├── data/                       # Para armazenar dados
│   ├── anexos/                 # Anexos baixados
│   └── dados_ans/              # Dados da ANS
│
├── scripts/                    # Scripts SQL e outros
│   └── sql/                    # Scripts SQL gerados
│
├── static/                     # Arquivos estáticos para a web
│
├── output/                     # Arquivos de saída gerados
│
├── requirements.txt            # Dependências do projeto
├── README.md                   # Este arquivo
└── main.py                     # Arquivo principal para executar todos os testes
```

## Testes Implementados

### Teste 1: Web Scraping

- Acessa o site da ANS
- Baixa os Anexos I e II em formato PDF
- Compacta os anexos em um único arquivo ZIP

### Teste 2: Transformação de Dados

- Extrai dados da tabela "Rol de Procedimentos e Eventos em Saúde" do PDF do Anexo I
- Salva os dados em um arquivo CSV estruturado
- Compacta o CSV em um arquivo ZIP
- Substitui abreviações por descrições completas

### Teste 3: Banco de Dados

- Baixa arquivos de demonstrações contábeis dos últimos 2 anos
- Baixa dados cadastrais das operadoras ativas
- Cria scripts SQL para estruturar tabelas e importar dados
- Desenvolve queries analíticas para responder às perguntas do teste

### Teste 4: API

- Implementa uma interface web com Vue.js
- Cria um servidor Python com Flask
- Disponibiliza uma rota para busca textual de operadoras
- Permite visualizar e filtrar os resultados em uma tabela

## Requisitos

- Python 3.8+
- Bibliotecas listadas no arquivo `requirements.txt`

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/intuitive_care_testes.git
cd intuitive_care_testes
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Uso

### Executar todos os testes em sequência:

```bash
python main.py
```

### Executar um teste específico:

```bash
python main.py --teste 1  # Executa apenas o Teste 1 (Web Scraping)
python main.py --teste 2  # Executa apenas o Teste 2 (Transformação de Dados)
python main.py --teste 3  # Executa apenas o Teste 3 (Banco de Dados)
python main.py --teste 4  # Executa apenas o Teste 4 (API)
```

## Estrutura de Diretórios e Arquivos

### src/web_scraping/

- `__init__.py`: Define os imports do módulo
- `scraper.py`: Funções para baixar e compactar arquivos

### src/transformacao_dados/

- `__init__.py`: Define os imports do módulo
- `extrator_pdf.py`: Funções para extrair e processar dados de PDFs

### src/banco_dados/

- `__init__.py`: Define os imports do módulo
- `database.py`: Funções para baixar, processar e gerar scripts SQL

### src/api/

- `__init__.py`: Define os imports do módulo
- `server.py`: Implementação do servidor Flask e API

### static/

- `index.html`: Interface web para interagir com a API

## Diferenciais Implementados

- **Organização modular**: Código estruturado em módulos independentes
- **Documentação detalhada**: Comentários explicativos e documentação em formato markdown
- **Tratamento de erros**: Validações e tratamentos de exceções
- **Interface amigável**: Interface web responsiva e intuitiva
- **Arquitetura robusta**: Separação de responsabilidades e reuso de código
