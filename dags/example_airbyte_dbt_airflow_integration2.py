# Required python packages
from airflow.utils.dates import days_ago
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from datetime import datetime
from datetime import timedelta
from airflow import DAG
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor
from airflow_dbt.operators.dbt_operator import DbtRunOperator

# Basic arguments required by the DAG tasks
default_args = {
    "owner": "airflow",                   # owner of the DAG
    "depends_on_past": False,             # no dependence on previous attempts
    "retries": 1,                         # limit to 1 retry
    "dir": "~/dbt/insight_history",       # location of the relevant dbt models
    "retry_delay": timedelta(minutes=1),  # retry failed attempt after 1 minute
    "start_date": days_ago(1),            # initiate the process yesterday
    "schedule_interval": "*/5 * * * *",   # trigger the dag every 5 minutes
}


# Define a DAG
with DAG(
    dag_id="example_airbyte_dbt_airflow_integration",
    default_args=default_args,
) as dag:

		# Airbyte data integration task
    sync_source_destination = AirbyteTriggerSyncOperator(
        task_id="airflow-airbyte-sync",
        airbyte_conn_id="airflow-airbyte",
        connection_id="1d7b8c28-8e09-4ae4-9955-a4a388701f32",
    )

    # dbt data transformation task
    dbt_run = DbtRunOperator(
        task_id="dbt_run",
    )
    # Task sequencing indicating dbt_run must run after sync_source_destination
    sync_source_destination >> dbt_run
