from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# # to import module from another file
# import sys
# sys.path.append('./scripts/')
# from main import *
from main import run_spotify_etl

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 11, 2),
    # 'end_date': datetime(),
    'depends_on_past': False,
    # 'email': ['airflow@example.com'],
    # 'email_on_failure': False,
    # 'email_on_retry': False,
    # If a task fails, retry it once after waiting
    # at least 5 minutes
    'schedule_interval': '@hourly',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'spotify_de_dag',  # name
    default_args=default_args,
    description='First DAG for spotify de project.',
    # schedule_interval=timedelta(days=1)  # run it daily
)


def print_hello():
    print("Hellowww")


run_etl = PythonOperator(
    task_id='spotify_etl',
    python_callable=run_spotify_etl,
    dag=dag
)

run_etl


# faire en sorte d'importer la focntion run etl de scripts > main (faire des tests entre scripts prython dans deux dossiers diff pour voir)
