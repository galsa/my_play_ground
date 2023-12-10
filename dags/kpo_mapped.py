from datetime import datetime

from airflow import DAG
from airflow.configuration import conf
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator


namespace = conf.get("kubernetes", "NAMESPACE")
# This will detect the default namespace locally and read the
# environment namespace when deployed to Astronomer.
if namespace == "default":
    config_file = "/usr/local/airflow/include/.kube/config"
    in_cluster = False
else:
    in_cluster = True
    config_file = None


with DAG(
    dag_id="kpo_mapped",
    start_date=datetime(1970, 1, 1),
    schedule_interval=None,
) as dag:

    KubernetesPodOperator(
        task_id="moo",
        name="moo",
        namespace=namespace,
        config_file=config_file,
        in_cluster=False,
        image="docker.io/rancher/cowsay",
        cmds=["cowsay"],
        arguments=["moo"],
    )