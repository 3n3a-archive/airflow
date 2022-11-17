import json
from datetime import datetime
from airflow.models import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator

def save_locally(ti) -> None:
    posts = ti.xcom_pull(task_ids=['get_posts'])
    with open('/opt/airflow/logs/posts.json', 'w') as f:
        json.dump(posts[0], f)

with DAG(
    dag_id='api_dag',
    schedule_interval='@daily',
    start_date=datetime(2022, 3, 1),
    catchup=False
) as dag:

    # 1) Check if API is up
    task_is_api_active = HttpSensor(
        task_id='is_api_active',
        http_conn_id='api_posts',
        endpoint='posts/'
    )

    # 2) Extract the posts
    task_get_posts = SimpleHttpOperator(
        task_id='get_posts',
        http_conn_id='api_posts',
        endpoint='posts/',
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    # 3) Save locally
    task_save = PythonOperator(
        task_id='save_posts',
        python_callable=save_locally
    )

    task_is_api_active >> task_get_posts >> task_save