import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.dataframe import DataFrame


def create_spark_session() -> SparkSession:
    spark = (
        SparkSession.builder.appName("Date Silver")
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
    url_bronze = "jdbc:postgresql://postgres:5432/bronze"  # locally: 'jdbc:postgresql://localhost:5432/silver'
    url_silver = "jdbc:postgresql://postgres:5432/silver"
    table = "date"
    
    spark = create_spark_session()

    df = read_postgre_table(
        spark, username, password, url_bronze, f"{table}"
    )

    df_silver = df.select(
        F.col("date_id"),
        F.year(F.col("transaction_date")).alias("year"),
        F.month(F.col("transaction_date")).alias("month")
    )

    load_to_postgre_db(df_silver, username, password, url_silver, table)


if __name__ == "__main__":
    main()
