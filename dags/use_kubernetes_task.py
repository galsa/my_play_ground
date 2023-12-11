# This code defines an Apache Airflow Directed Acyclic Graph (DAG) using the TaskFlow API, which is a programming
# model where tasks are defined as Python functions and passed directly into the DAG’s operators. Here's a step by
# step breakdown: 1. **Imports and Configurations:** The necessary libraries and modules are imported. The `conf.get(
# "kubernetes", "NAMESPACE")` retrieves the Kubernetes namespace in which Airflow is running. 2. **DAG Definition:**
# A new DAG is created using the `@dag` decorator, with the start date specified as January 1, 2023, no catchup runs,
# and a daily schedule. 3. **Tasks:** Three tasks are defined using the `@task` decorator: - `extract_data`: This
# function simulates the extraction of data by generating a random integer between 0 and 100. - `transform`: This
# function is decorated with `@task.kubernetes`, which means it will be executed as a Kubernetes pod. It takes the
# data point from `extract_data`, multiplies it by 23, and returns the result. The decorator parameters specify the
# Docker image to use, the Kubernetes cluster and namespace to run in, the pod's configuration, and enable pushing
# the return value to XCom. - `load_data`: This function retrieves the transformed data from XCom using the
# `xcom_pull` function and prints it. The `**context` argument allows this function to access the Airflow task
# instance context, which contains the XCom data. 4. **Task Dependencies:** The parentheses at the end of the
# `load_data(transform(extract_data()))` line define the dependencies between the tasks. This line is equivalent to
# `extract_data() >> transform() >> load_data()` in the classic Airflow style. 5. **DAG Instance:** The
# `kubernetes_decorator_example_dag()` call at the end of the script is necessary to create an instance of the DAG.
# Without this line, Airflow would not be able to find and schedule the DAG. XCom (short for "cross-communication")
# is a feature of Airflow that allows tasks to exchange messages or small amounts of data. It's used here to pass the
# transformed data from the `transform` task to the `load_data` task. The `do_xcom_push=True` parameter in the
# `@task.kubernetes` decorator enables pushing the return value of the `transform` function to XCom.
from pendulum import datetime
from airflow.configuration import conf
from airflow.decorators import dag, task
import random
import logging

# get the current Kubernetes namespace Airflow is running in
namespace = conf.get("kubernetes", "NAMESPACE")
image = 'kubernetesetlcontainerregistry.azurecr.io/jaffe-shop-duckdb:1.0'

# get the airflow.task logger
task_logger = logging.getLogger("airflow.task")


@dag(
    start_date=datetime(2023, 1, 1),
    catchup=False,
    schedule="@daily",
)
def kubernetes_decorator_example_dag():
    @task
    def extract_data():
        task_logger.warning("entering: extract_data()")
        # simulating querying from a database
        data_point = random.randint(0, 100)
        return data_point

    @task.kubernetes(
        # specify the Docker image to launch, it needs to be able to run a Python script
        image=image,
        # launch the Pod on the same cluster as Airflow is running on
        in_cluster=True,
        # launch the Pod in the same namespace as Airflow is running in
        namespace=namespace,
        # Pod configuration
        # naming the Pod
        name="my_pod",
        # log stdout of the container as task logs
        get_logs=True,
        # log events in case of Pod failure
        log_events_on_failure=True,
        # enable pushing to XCom
        do_xcom_push=True,
    )
    def transform(data_point):
        task_logger.warning("entering: transform(data_point)")
        multiplied_data_point = 23 * int(data_point)
        return multiplied_data_point

    @task
    def load_data(transformed_data_point: int):
        task_logger.warning("entering: load_data(transformed_data_point)")
        print(transformed_data_point)
        task_logger.warning("transformed_data_point: " + str(transformed_data_point))

    extract_data() >> transform() >> load_data()


kubernetes_decorator_example_dag = kubernetes_decorator_example_dag()
