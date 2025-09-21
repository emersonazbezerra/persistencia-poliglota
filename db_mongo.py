import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from dotenv import load_dotenv

load_dotenv()


def obter_colecao():
    try:
        usuario = os.getenv('MONGO_USER')
        senha = os.getenv('MONGO_PASS')
        uri = f"mongodb://{usuario}:{senha}@localhost:27017/"
        cliente = MongoClient(uri)
        banco_de_dados = cliente['pontos_turisticos_db']
        colecao = banco_de_dados['locais']
        return colecao
    except ConnectionFailure as e:
        print(f"Erro de conexão com o MongoDB: {e}")
        return None


def adicionar_local(dados_local):
    colecao = obter_colecao()
    if colecao is not None:
        try:
            # Insere o dicionário como um documento na coleção
            colecao.insert_one(dados_local)
            print(f"Local '{dados_local.get('nome_local')}' adicionado com sucesso!")
            return True
        except OperationFailure as e:
            print(f"Erro ao adicionar local no MongoDB: {e}")
            return False
    return False


def listar_locais_por_cidade(nome_cidade):
    colecao = obter_colecao()
    if colecao is not None:
        try:
            locais = list(colecao.find({"cidade": nome_cidade}))
            return locais
        except OperationFailure as e:
            print(f"Erro ao buscar locais por cidade: {e}")
            return []
    return []


def listar_todos_os_locais():
    colecao = obter_colecao()
    if colecao is not None:
        try:
            locais = list(colecao.find({}))
            return locais
        except OperationFailure as e:
            print(f"Erro ao buscar todos os locais: {e}")
            return []
    return []
