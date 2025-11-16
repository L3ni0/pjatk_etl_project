from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.models import Variable


@dag(schedule=None, catchup=False)
def test_dag():
    start = PythonOperator(
        task_id="test_start", python_callable=lambda: print("Jobs started")
    )

    test = SparkSubmitOperator(
        task_id="test_dags",
        application="include/scripts/test.py",
        conn_id="spark-conn",
    )

    start >> test


test_dag()
