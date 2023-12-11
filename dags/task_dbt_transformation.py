# The `KubernetesPodOperator` in the code above will create a new pod in your Kubernetes cluster using the image
# specified by the `image` variable. It will then run the command specified in the `cmds` variable with the arguments
# provided in the `arguments` variable inside that pod. In this case, the command being run is `/bin/bash -c`,
# and the argument is `"dbt deps && dbt build --profiles-dir ."`. This means that the pod will start a bash shell and
# execute the command `dbt deps && dbt build --profiles-dir .` inside that shell. Once the command has finished
# executing, the pod will be terminated. The logs of the command execution will be fetched and displayed in the
# Airflow's logging system because `get_logs=True` is set. Here's a simplified explanation of what each parameter
# does: - `namespace`: The Kubernetes namespace where the pod will be created. - `image`: The Docker image to use for
# the pod. - `cmds`: The command to run inside the pod. - `arguments`: The arguments to pass to the command. -
# `name`: The name of the pod. - `task_id`: The ID of the Airflow task. - `get_logs`: Whether to fetch the logs from
# the pod and display them in Airflow's logging system. - `log_events_on_failure`: Whether to log events when a
# failure occurs. - `config_file`: The path to your Kubernetes configuration file (kubeconfig). - `in_cluster`:
# Whether Airflow is running inside the Kubernetes cluster or not.
from pendulum import datetime
from airflow.decorators import dag, task
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
import logging

# Kubernetes parameters
namespace = 'default'
image = 'kubernetesetlcontainerregistry.azurecr.io/jaffe-shop-duckdb:1.0'
# config_file = '<path_to_your_kube_config>'
in_cluster = True

# get the airflow.task logger
task_logger = logging.getLogger("airflow.task")


@dag(
    start_date=datetime(2023, 1, 1),
    catchup=False,
    schedule="@daily",
)
def task_dbt_transformation():
    dbt_task = KubernetesPodOperator(
        namespace=namespace,
        image=image,
        cmds=["/bin/bash", "-c"],  # use bash to run multiple commands
        arguments=["dbt deps && dbt build --profiles-dir . && sleep infinity"],
        name="dbt_transformations",
        task_id="dbt_transformations",
        get_logs=True,
        log_events_on_failure=True,
        # config_file=config_file,
        in_cluster=in_cluster,
    )

    @task
    def print_success_message():
        print("All is well")

    dbt_task >> print_success_message()


kubernetes_decorator_example_dag = task_dbt_transformation()
