#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved. This is the one that works
#

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago
import logging

# Kubernetes parameters
namespace = 'default'
image = 'kubernetesetlcontainerregistry.azurecr.io/jaffe-shop-duckdb:1.0'
connection_id = '5872a75d-68ef-4009-9b5c-047f118d2185'  # Variable.get("AIRBYTE_CONNECTION_ID")
airbyte_connection_id = 'airflow-call-to-airbyte-example'
in_cluster = True

# get the airflow.task logger
task_logger = logging.getLogger("airflow.task")

with DAG(
        dag_id="another_airbyte_dbt_transformation",
        default_args={"owner": "airflow"},
        schedule_interval="@daily",
        start_date=days_ago(1)
) as dag:
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

    def print_success_message():
        print("All tasks completed successfully")

    run_airbyte_job >> run_dbt_transformations

    print_success_message = PythonOperator(
        task_id='print_success_message',
        python_callable=print_success_message,
    )

    run_dbt_transformations >> print_success_message
