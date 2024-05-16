from os.path import join
import pendulum
from airflow.macros import ds_add
import pandas as pd
def extrair_dados():
    data_interval_end = pendulum.now(tz="America/Manaus").strftime("%Y-%m-%d")
    data_interval_path =pendulum.now(tz="America/Manaus").strftime("%Y-%m-%d %H:%M")
    city = 'Itacoatiara'

    key = '5E5XLKVBF6CAMA5HT783FVJZT'

    url = join("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/",
            f"{city}%2CUK/{data_interval_end}/{ds_add(data_interval_end,7)}?unitGroup=metric&include=days&key={key}&contentType=csv")


    dados = pd.read_csv(url)

    file_path = f"/opt/airflow/data/semana={data_interval_path}/"

    dados.to_csv(file_path+'dados_brutos.csv')
    dados[['datetime','tempmin', 'temp', 'tempmax']].to_csv(file_path + 'temperaturas.csv')
    dados[['datetime', 'description', 'icon']].to_csv(file_path + 'condicoes.csv')