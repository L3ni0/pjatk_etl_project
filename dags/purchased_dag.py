from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.models import Variable


@dag(schedule=None, catchup=False)
def purchased_dag():

    # for debug
    start = PythonOperator(
        task_id="test_start", python_callable=lambda: print("Jobs started")
    )

    load_data = SparkSubmitOperator(
        task_id="load_purchased_to_bronze",
        application="scripts/spark/bronze/purchased_games.py",
        conn_id='spark_conn',
        packages="org.postgresql:postgresql:42.7.3"
    )

    start  >> load_data


purchased_dag()
