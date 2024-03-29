#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

from airflow import DAG
from airflow.models import Variable
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.utils.dates import days_ago

connection_id = '5872a75d-68ef-4009-9b5c-047f118d2185'  # Variable.get("AIRBYTE_CONNECTION_ID")
airbyte_connection_id = 'airflow-call-to-airbyte-example'

with DAG(
        dag_id="trigger_airbyte_job_example2",
        default_args={"owner": "airflow"},
        schedule_interval="@daily",
        start_date=days_ago(1)
) as dag:
    example_sync = AirbyteTriggerSyncOperator(
        task_id="airbyte_example",
        airbyte_conn_id=airbyte_connection_id,
        connection_id=connection_id,
        asynchronous=False,
        timeout=3600,
        wait_seconds=3,
    )
