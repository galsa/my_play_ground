from airflow import DAG
from datetime import datetime

from airflow.configuration import conf

# from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

# Constants
KUBE_CONFIG = '/usr/local/airflow/dags/kube_config.yaml'
KUBE_SERVICE_ACCOUNT = 'mwaa-sa'

# DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
    'provide_context': True
}

namespace = conf.get("kubernetes", "NAMESPACE")
# This will detect the default namespace locally and read the
# environment namespace when deployed to Astronomer.
if namespace == "default":
    config_file = "/usr/local/airflow/include/.kube/config"
    in_cluster = False
else:
    in_cluster = True
    config_file = None

dag = DAG('dbt_example', default_args=default_args, schedule_interval=None)

# Task
# dbt_test = KubernetesPodOperator(
#                        task_id="dbt-test",
#                        name="dbt-test",
#                        namespace=namespace,
#                        image="my-dbt-image:1.0",
#                        cmds=["dbt"],
#                        arguments=["run", "--profiles-dir", ".", "--fail-fast", "-m", "your_model"],
#                        ## no change on below
#                        get_logs=True,
#                        dag=dag,
#                        is_delete_operator_pod=False,
#                        config_file=KUBE_CONFIG,
#                        in_cluster=False,
#                        service_account_name=KUBE_SERVICE_ACCOUNT,
#                        get_logs=True,
#                        )
