from pendulum import datetime
from airflow.decorators import dag, task
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
import logging

# Kubernetes parameters
namespace = 'default'
image = 'kubernetesetlcontainerregistry.azurecr.io/jaffe-shop-duckdb:1.0'
airbyte_connection_id = '55ac2529-7881-4059-b82b-203a30d408cc'  # Variable.get("AIRBYTE_CONNECTION_ID")
in_cluster = True

# get the airflow.task logger
task_logger = logging.getLogger("airflow.task")


@dag(
    start_date=datetime(2023, 1, 1),
    catchup=False,
    schedule_interval="@daily",
)
def my_combined_airbyte_dbt_tasks():
    run_airbyte_job = AirbyteTriggerSyncOperator(
        task_id="run_airbyte_job",
        airbyte_conn_id="airbyte_default",
        connection_id=airbyte_connection_id,
        asynchronous=False,
        timeout=3600,
        wait_seconds=3,
    )

    run_dbt_transformations = KubernetesPodOperator(
        namespace=namespace,
        image=image,
        cmds=["/bin/bash", "-c"],  # use bash to run multiple commands
        arguments=["dbt deps && dbt build --profiles-dir ."],
        name="dbt_transformations",
        task_id="run_dbt_transformations",
        get_logs=True,
        log_events_on_failure=True,
        in_cluster=in_cluster,
        is_delete_operator_pod=True,  # don't delete the pod after task completion (only for testing)
    )

    @task
    def print_success_message():
        print("All tasks completed successfully")

    run_airbyte_job >> run_dbt_transformations >> print_success_message()


combined_tasks_dag = my_combined_airbyte_dbt_tasks()  # needed to instantiate the DAG and make it discoverable by the
# Airflow scheduler.
