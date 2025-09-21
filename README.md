# Explorador de Pontos Turísticos

### Projeto avaliativo da disciplina de Tendências em Ciência da Computação com o tema Persistência Poliglota

### Aluno: **Emerson de Azevedo Silva Bezerra**

### RGM: **44968132**

## Descrição Geral

Aplicação web para cadastro, exploração e visualização de pontos turísticos utilizando persistência
poliglota:

- Cadastro de cidades (SQLite)
- Cadastro de locais de interesse com coordenadas e descrição (MongoDB)
- Visualização por cidade em mapa interativo (pydeck)
- Busca de locais próximos com cálculo de distância geográfica
- Geolocalização automática do usuário para pesquisa por proximidade
- Interface simples via Streamlit

### Tela inicial
![Tela inicial](/docs/images/tela-inicial.png)

### Cadastro de cidade
![Cadastro de cidade](/docs/images/cadastro-cidade.png)

### Cadastro de local
![Cadastro de local](/docs/images/cadastro-local.png)

### Mapa por cidade
![Mapa por cidade](/docs/images/mapa-cidade.png)

### Busca por proximidade
![Busca por proximidade](/docs/images/busca-proximidade.png)

## Ferramentas Utilizadas

- Linguagem: Python 3.13+
- Framework Web: Streamlit
- Banco Relacional: SQLite (cities)
- Banco NoSQL: MongoDB (locais turísticos)
- Bibliotecas:
    - pymongo (acesso MongoDB)
    - sqlite3 (nativo Python)
    - pandas (estrutura tabular)
    - pydeck (mapa interativo)
    - geopy (cálculo de distâncias)
    - dotenv (variáveis ambiente)
- Docker + Docker Compose (infraestrutura MongoDB)
- Arquivo JSON + script com carga inicial de dados turísticos

## Arquitetura

Camadas e módulos principais:

- `app.py`: Interface Streamlit, orquestra fluxo e visualizações
- `db_sqlite.py`: Operações sobre cidades e estados
- `db_mongo.py`: Gestão de locais turísticos
- `geoprocessamento.py`: Funções de distância geográfica
- `docker/`: Infra de dados (compose + import JSON)
- `docker/pontos_turisticos.json`: Carga inicial da coleção locais
- `.env`: Credenciais Mongo (para testes locais apenas)

Fluxo:

1. Usuário cadastra cidade (SQLite) ou ponto turístico (MongoDB)
2. Seleciona cidade => carrega locais => normaliza coordenadas => mostra tabela + mapa pydeck
3. Busca por proximidade => pega geolocalização (JS) => filtra por raio => exibe lista + mapa simples

## Como Executar o Projeto

Pré-requisitos:

- Python 3.11+
- Docker
- Portas livres: 8501 (Streamlit) e 27017 (MongoDB)

Passo a passo:

1. Clonar repositório:
   ```bash
   git clone https://github.com/emersonazbezerra/persistencia-poliglota.git \n
   cd persistencia-poliglota
   ```

2. Subir infraestrutura (MongoDB + carga inicial):
    ```bash
    cd docker
    docker compose up -d
    ```

3. Voltar à raiz do projeto:
    ```bash   
    cd ..
    ```

4. Criar ambiente virtual (opcional):
    ```bash
   python -m venv .venv
   source .venv/bin/activate # Linux/macOS
   # ou .venv\Scripts\activate no Windows
   ```

5. Instalar dependências:
    ```bash
   pip install -r requirements.txt
    ```

6. Executar aplicação:
    ```bash
   streamlit run app.py
   ```

7. Acessar no navegador:
   http://localhost:8501
