from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.decorators import task

with DAG(
    dag_id="example_kubernetes_decorator",
    schedule=None,
    start_date=datetime(2021, 1, 1),
    tags=["example", "cncf", "kubernetes"],
    catchup=False,
) as dag:
    # [START howto_operator_kubernetes]
    @task.kubernetes(
        image="python:3.8-slim-buster",
        name="k8s_test",
        namespace="default",
        in_cluster=False,
        config_file="/path/to/.kube/config",
    )
    def execute_in_k8s_pod():
        import time

        print("Hello from k8s pod")
        time.sleep(2)

    @task.kubernetes(image="python:3.8-slim-buster", namespace="default", in_cluster=False)
    def print_pattern():
        n = 5
        for i in range(n):
            # inner loop to handle number of columns
            # values changing acc. to outer loop
            for j in range(i + 1):
                # printing stars
                print("* ", end="")

            # ending line after each row
            print("\r")

    execute_in_k8s_pod_instance = execute_in_k8s_pod()
    print_pattern_instance = print_pattern()

    execute_in_k8s_pod_instance >> print_pattern_instance