import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.dataframe import DataFrame


def create_spark_session() -> SparkSession:
    spark = (
        SparkSession.builder.appName("Players Gold")
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3")
        .getOrCreate()
    )

    return spark


def read_postgre_table(
    spark: SparkSession, username: str, password: str, url: str, table: str
) -> DataFrame:
    properties = {
        "user": username,
        "password": password,
        "driver": "org.postgresql.Driver",
    }

    df = spark.read.jdbc(url=url, table=table, properties=properties)

    return df


# optimized for bigger files
def load_to_postgre_db(
    df: DataFrame,
    username: str,
    password: str,
    url: str,
    table: str,
    batch_size: int = 2000,
    num_partitions: int = 1000,
) -> None:
    properties = {
        "user": username,
        "password": password,
        "driver": "org.postgresql.Driver",
        "batchsize": f"{batch_size}",
        "rewriteBatchedStatements": "true",
    }

    df = df.coalesce(num_partitions)
    # fmt: off
    df.write \
      .option("truncate", "true") \
      .option("batchsize", batch_size) \
      .jdbc(url=url, table=table, mode="overwrite", properties=properties)
    # fmt: on

    return


def main():
    # params
    username = os.getenv("DB_USERNAME", "airflow")
    password = os.getenv("DB_PASSWORD", "airflow")
    url_silver = "jdbc:postgresql://postgres:5432/silver"  # locally: 'jdbc:postgresql://localhost:5432/silver'
    url_gold = "jdbc:postgresql://postgres:5432/gold"
    table_silver = "players"
    table_gold = "players"

    spark = create_spark_session()
    df = read_postgre_table(spark, username, password, url_silver, table_silver)

    load_to_postgre_db(df, username, password, url_gold, table_gold)


if __name__ == "__main__":
    main()
