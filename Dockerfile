FROM apache/airflow:2.9.1

#COPY requirements.txt .

USER root
RUN apt-get update

USER airflow
RUN pip install --no-cache-dir --upgrade pip \
    pip install --force --no-cache-dir pandas \
    pip install --force --no-cache-dir "pymongo[srv]"