"""
This is an example dag for using the KubernetesPodOperator.
"""

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago
from airflow.configuration import conf

default_args = {
    'owner': 'airflow'
}

namespace = conf.get("kubernetes", "NAMESPACE")
if namespace == "default":
    in_cluster = False
else:
    in_cluster = True


with DAG(
        dag_id='k8s-example-0',
        default_args=default_args,
        schedule_interval="*/5 * * * *",
        start_date=days_ago(2),
        catchup=False,
        tags=['k8s-pod-operator', 'example'],
) as dag:
    k = KubernetesPodOperator(
        namespace= namespace,
        image="ubuntu:latest",
        cmds=["bash", "-cx"],
        arguments=["echo hello"],
        name="k8s-pod",
        task_id="task",
        is_delete_operator_pod=True,
        hostnetwork=False,
        startup_timeout_seconds=1000
    )
