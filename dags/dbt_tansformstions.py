from pendulum import datetime, duration
from airflow.decorators import dag, task
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.configuration import conf

# import the logging module
import logging

# get the airflow.task logger
task_logger = logging.getLogger("airflow.task")

# Constants
KUBE_CONFIG = '/usr/local/airflow/dags/kube_config.yaml'

namespace = conf.get("kubernetes", "NAMESPACE")
# This will detect the default namespace locally and read the
# environment namespace when deployed to Astronomer.
if namespace == "default":
    config_file = "/usr/local/airflow/include/.kube/config"
    in_cluster = False
else:
    in_cluster = True
    config_file = None


@task
def run_dbt_transformations():
    KubernetesPodOperator(
        namespace='default',
        image='kubernetesetlcontainerregistry.azurecr.io/my-dbt-image:1.0',
        cmds=["dbt", "run"],
        arguments=[
            "--profiles-dir", "profiles"
        ],
        name="dbt_transformations",
        task_id="dbt_transformations",
        get_logs=True,
        config_file=config_file,
        in_cluster=in_cluster
    )


@dag(
    start_date=datetime(2022, 6, 5),
    schedule_interval="@daily",
    dagrun_timeout=duration(minutes=10),
    catchup=False,
)
def dbt_kubernetes_pod_operator_example():
    task_logger.warning("before call to run_dbt_transformations()")
    run_dbt_transformations()
    task_logger.warning("after call to run_dbt_transformations()")


dag = dbt_kubernetes_pod_operator_example()
