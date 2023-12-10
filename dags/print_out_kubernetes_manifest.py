from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.utils.dates import days_ago

with DAG(
        dag_id="print_out_kubernetes_manifest",
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
