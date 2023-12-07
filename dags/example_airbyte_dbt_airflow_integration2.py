# Required python packages
from airflow.utils.dates import days_ago
# from airflow.sensors.external_task_sensor import ExternalTaskSensor
from datetime import datetime
from datetime import timedelta
from airflow import DAG
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor
from airflow_dbt.operators.dbt_operator import DbtRunOperator


AIRBYTE_CONNECTION_ID = "4032a1e1-c8ad-4fbf-a6ef-92d7e9a5931f"

# Basic arguments required by the DAG tasks
default_args = {
    "owner": "airflow",  # owner of the DAG
    "depends_on_past": False,  # no dependence on previous attempts
    "retries": 1,  # limit to 1 retry
    # "dir": "~/dbt/insight_history",  # location of the relevant dbt models
    "retry_delay": timedelta(minutes=1),  # retry failed attempt after 1 minute
    "start_date": days_ago(1),  # initiate the process yesterday
    "schedule_interval": "*/5 * * * *",  # trigger the dag every 5 minutes
}

# Define a DAG
with DAG(
        dag_id="example_airbyte_dbt_airflow_integration2",
        default_args=default_args,
) as dag:
    # Airbyte data integration task
    sync_source_destination = AirbyteTriggerSyncOperator(
        task_id="airbyte_trigger_sync",
        airbyte_conn_id="airflow-call-to-airbyte-example",
        connection_id=AIRBYTE_CONNECTION_ID,
    )

    # dbt data transformation task
    dbt_run = DbtRunOperator(
        task_id="dbt_run",
    )
    # Task sequencing indicating dbt_run must run after sync_source_destination
    sync_source_destination >> dbt_run
