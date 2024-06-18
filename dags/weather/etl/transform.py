import csv
import json


def transformar_dados(city:str):
    dados_csv = []
    with open(f"/opt/airflow/data/raw/{city}/dados_brutos.csv",'r') as csvfile:
            reader = csv.DictReader(csvfile,delimiter=",")
            for row in reader:
                dados_csv.append(row)

    with open(f"/opt/airflow/data/processed/{city}/dados_processados.json","w") as jsonfile:
        json.dump(dados_csv,jsonfile,indent=4)