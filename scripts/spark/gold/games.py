import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.dataframe import DataFrame


def create_spark_session() -> SparkSession:
    spark = (
        SparkSession.builder.appName("Games Gold")
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3")
        .getOrCreate()
    )

    return spark


def read_postgre_table(
    spark: SparkSession, username: str, password: str, url: str, table: str
):
    properties = {
        "user": username,
        "password": password,
        "driver": "org.postgresql.Driver",
    }

    df = spark.read.jdbc(url=url, table=table, properties=properties)

    return df


def load_to_postgre_db(
    df: DataFrame, username: str, password: str, url: str, table: str
):
    properties = {
        "user": username,
        "password": password,
        "driver": "org.postgresql.Driver",
    }
    df.write.jdbc(url=url, table=table, mode="overwrite", properties=properties)

    return


def main():
    username = os.getenv("DB_USERNAME", "airflow")
    password = os.getenv("DB_PASSWORD", "airflow")
    url_silver = "jdbc:postgresql://postgres:5432/silver"  # locally: 'jdbc:postgresql://localhost:5432/silver'
    url_gold = "jdbc:postgresql://postgres:5432/gold"
    table = "games"
    spark = create_spark_session()

    df = read_postgre_table(spark, username, password, url_silver, table)
    df = df.select("game_id", "publishers", "title")
    load_to_postgre_db(df, username, password, url_gold, table)


if __name__ == "__main__":
    main()
