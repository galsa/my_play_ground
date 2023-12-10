from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
}

with DAG('hello_world_kubernetes_dag',
         default_args=default_args,
         schedule_interval='@daily',
         ) as dag:
    task_hello = KubernetesPodOperator(
        namespace='default',
        image="python:3.6",
        cmds=["python", "-c"],
        arguments=["print('Hello World')"],
        labels={"foo": "bar"},
        name="hello-world",
        task_id="hello-world-task",
        is_delete_operator_pod=True,
        get_logs=True
    )
