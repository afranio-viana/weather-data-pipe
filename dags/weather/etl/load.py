
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json


def carregar_dados(uri:str,city:str,database_name:str,collection_name:str):
    client = MongoClient(uri, server_api=ServerApi('1'))
    with open(f"/opt/airflow/data/processed/{city}/dados_processados.json",'r') as jsonfile:
        dados_json = json.load(jsonfile)


    try:
        client.admin.command('ping')
        db = client[database_name]
        collection = db[collection_name]

        if(isinstance(dados_json, list)):
            collection.insert_many(dados_json)
        else:
            collection.insert_one(dados_json)

        print("Dados inseridos no MongoDB!")
    except Exception as e:
        print(e)