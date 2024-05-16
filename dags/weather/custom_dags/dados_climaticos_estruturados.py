from airflow import DAG
import pendulum
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.macros import ds_add
from weather.etl.extract import extrair_dados

#import pandas as pd
from pathlib import Path


def pegar_data_e_criar_pasta():
    # Obter a data atual
    data_atual = pendulum.now(tz="America/Manaus").strftime("%Y-%m-%d %H:%M")
    caminho = f"/opt/airflow/data/semana={data_atual}"
    Path(caminho).mkdir(parents=True, exist_ok=True)
    

with DAG (
    "dados_climaticos_estruturados",
    description='Essa dag vai pegar os dados climaticos de uma determinada cidade.',
    start_date=pendulum.datetime(2024,5,16, hour=17, minute=25, tz="America/Manaus"),
    schedule_interval='*/5 * * * *',
) as dag:
    task_1 = PythonOperator(
        task_id = "criar_pasta",
        python_callable = pegar_data_e_criar_pasta,
        #bash_command='mkdir -p "/opt/airflow/data/semana=$(date +\%Y-\%m-\%d)"'
    )

    task_2 = PythonOperator(
        task_id = "extrair_dados",
        python_callable = extrair_dados,
    )

    task_1 >> task_2