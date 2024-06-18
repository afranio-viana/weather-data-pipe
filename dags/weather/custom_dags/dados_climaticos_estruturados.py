from airflow import DAG
from airflow.models import Variable
import pendulum
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.macros import ds_add
from weather.etl.extract import extrair_dados
from weather.etl.transform import transformar_dados
from weather.etl.load import carregar_dados
from pathlib import Path

#import pandas as pd
env = {
    "city_requisition": Variable.get("CITY"),
    "key_api": Variable.get("KEY"),
    "uri": Variable.get("URI"),
    "database_name": Variable.get("DTBASE"),
    "collection_name": Variable.get("COLLECTION"),
}

def pegar_data_e_criar_pasta(city):
    # Obter a data atual
    #caminho = f"/opt/airflow/data/raw/{city}"
    caminho = f"/opt/airflow/data/raw/{city}"
    Path(caminho).mkdir(parents=True, exist_ok=True)
    caminho2 = f"/opt/airflow/data/processed/{city}"
    Path(caminho2).mkdir(parents=True, exist_ok=True)
    

with DAG (
    "dados_climaticos_estruturados",
    description='Essa dag vai pegar os dados climaticos de uma determinada cidade.',
    start_date=pendulum.datetime(2024,6,17, hour=22, minute=20, tz="America/Manaus"),
    schedule_interval='*/5 * * * *',
) as dag:
    task_1 = PythonOperator(
        task_id = "criar_pasta",
        python_callable = pegar_data_e_criar_pasta,
        op_kwargs = {
            "city": env["city_requisition"],
        },
    )

    task_2 = PythonOperator(
        task_id = "extrair_dados",
        python_callable = extrair_dados,
        op_kwargs = {
            "city": env["city_requisition"],
            "key": env["key_api"],
        },
    )

    task_3 = PythonOperator(
        task_id = "transformar_dados",
        python_callable = transformar_dados,
        op_kwargs = {
            "city" : env["city_requisition"],
        }
    )

    task_4 = PythonOperator(
        task_id = "carregar_dados",
        python_callable = carregar_dados,
        op_kwargs = {
            "uri" : env["uri"],
            "city" : env["city_requisition"],
            "database_name": env["database_name"],
            "collection_name": env["collection_name"],
        }
    )

    task_1 >> task_2 >> task_3 >> task_4