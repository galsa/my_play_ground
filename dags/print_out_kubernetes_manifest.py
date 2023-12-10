from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.utils.dates import days_ago

with DAG(
        dag_id="kpo_mapped",
        default_args={"owner": "airflow"},
        schedule_interval="@daily",
        start_date=days_ago(1),
) as dag:
    k = KubernetesPodOperator(
        name="hello-dry-run",
        image="debian",
        cmds=["bash", "-cx"],
        arguments=["echo", "10"],
        labels={"foo": "bar"},
        task_id="dry_run_demo",
        do_xcom_push=True,
    )

    k2 = KubernetesPodOperator(
        task_id="test_error_message",
        image="alpine",
        cmds=["/bin/sh"],
        arguments=["-c", "echo hello world; echo Custom error > /dev/termination-log; exit 1;"],
        name="test-error-message",
        email="airflow@example.com",
        email_on_failure=True,
    )

