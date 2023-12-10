from airflow import DAG
from airflow.utils.dates import days_ago

from airflow.configuration import conf

from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

# Constants
KUBE_CONFIG = '/usr/local/airflow/dags/kube_config.yaml'


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
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

with DAG(
        dag_id="dbt_kubernetes_pod_operator_example",
        default_args={"owner": "airflow"},
        schedule_interval="@daily",
        start_date=days_ago(1),
) as dag:
    # Task
    migrate_data = KubernetesPodOperator(
        namespace='default',
        image='kubernetesetlcontainerregistry.azurecr.io/my-dbt-image:1.0',
        cmds=["dbt", "run"],
        arguments=[
            "--profiles-dir", "profiles"
        ],
        name="dbt_transformations",
        task_id="dbt_transformations",
        get_logs=True
    )
