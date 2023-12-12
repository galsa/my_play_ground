from pendulum import datetime
from airflow.decorators import dag, task
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
import logging

# Kubernetes parameters
namespace = 'default'
image = 'kubernetesetlcontainerregistry.azurecr.io/jaffe-shop-duckdb:1.0'
connection_id = '5872a75d-68ef-4009-9b5c-047f118d2185'  # Variable.get("AIRBYTE_CONNECTION_ID")
airbyte_connection_id = 'airflow-call-to-airbyte-example'
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
        task_id="run_combined_airbyte_dbt_job",
        airbyte_conn_id=airbyte_connection_id,
        connection_id=connection_id,
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
        get_logs=False,
        log_events_on_failure=True,
        in_cluster=in_cluster,
        is_delete_operator_pod=False,  # don't delete the pod after task completion (only for testing)
    )

    @task
    def print_success_message():
        print("All tasks completed successfully")

    run_airbyte_job >> run_dbt_transformations >> print_success_message()


combined_tasks_dag = my_combined_airbyte_dbt_tasks()  # needed to instantiate the DAG and make it discoverable by the
# Airflow scheduler.
