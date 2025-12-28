from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator


@dag(schedule=None, catchup=False)
def games_dag():
    # for debug
    start = PythonOperator(
        task_id="test_start", python_callable=lambda: print("Jobs started")
    )

    load_purchases_data = SparkSubmitOperator(
        task_id="load_purchased_to_bronze",
        application="scripts/spark/bronze/purchased_games.py",
        conn_id="spark_conn",
        packages="org.postgresql:postgresql:42.7.3",
    )

    load_players_data = SparkSubmitOperator(
        task_id="load_players_to_bronze",
        application="scripts/spark/bronze/players.py",
        conn_id="spark_conn",
        packages="org.postgresql:postgresql:42.7.3",
    )

    load_games_data = SparkSubmitOperator(
        task_id="load_games_to_bronze",
        application="scripts/spark/bronze/games.py",
        conn_id="spark_conn",
        packages="org.postgresql:postgresql:42.7.3",
    )

    load_date_data = SparkSubmitOperator(
        task_id="load_date_to_bronze",
        application="scripts/spark/bronze/date.py",
        conn_id="spark_conn",
        packages="org.postgresql:postgresql:42.7.3",
    )

    clear_purchases_data = SparkSubmitOperator(
        task_id="clear_purchased",
        application="scripts/spark/silver/purchased_games.py",
        conn_id="spark_conn",
        packages="org.postgresql:postgresql:42.7.3",
    )

    clear_players_data = SparkSubmitOperator(
        task_id="clear_players",
        application="scripts/spark/silver/players.py",
        conn_id="spark_conn",
        packages="org.postgresql:postgresql:42.7.3",
    )

    clear_games_data = SparkSubmitOperator(
        task_id="clear_games",
        application="scripts/spark/silver/games.py",
        conn_id="spark_conn",
        packages="org.postgresql:postgresql:42.7.3",
    )

    clear_date_data = SparkSubmitOperator(
        task_id="clear_date",
        application="scripts/spark/silver/date.py",
        conn_id="spark_conn",
        packages="org.postgresql:postgresql:42.7.3",
    )

    aggregate_purchases_data = SparkSubmitOperator(
        task_id="aggregate_to_purchases",
        application="scripts/spark/gold/purchases.py",
        conn_id="spark_conn",
        packages="org.postgresql:postgresql:42.7.3",
    )

    aggregate_players_data = SparkSubmitOperator(
        task_id="aggregate_to_players",
        application="scripts/spark/gold/players.py",
        conn_id="spark_conn",
        packages="org.postgresql:postgresql:42.7.3",
    )

    aggregate_games_data = SparkSubmitOperator(
        task_id="aggregate_to_games",
        application="scripts/spark/gold/games.py",
        conn_id="spark_conn",
        packages="org.postgresql:postgresql:42.7.3",
    )

    aggregate_date_data = SparkSubmitOperator(
        task_id="aggregate_to_date",
        application="scripts/spark/gold/date.py",
        conn_id="spark_conn",
        packages="org.postgresql:postgresql:42.7.3",
    )
    start >> load_purchases_data >> clear_purchases_data >> aggregate_purchases_data
    start >> load_players_data >> clear_players_data >> aggregate_players_data
    start >> load_games_data >> clear_games_data >> aggregate_games_data
    start >> load_date_data >> clear_date_data >> aggregate_date_data


games_dag()
