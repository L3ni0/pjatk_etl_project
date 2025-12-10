import os
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StringType,
    StructField,
    StructType,
)
from pyspark.sql import functions as F
from pyspark.sql.dataframe import DataFrame


def create_spark_session() -> SparkSession:
    spark = (
        SparkSession.builder.appName("Purchased Silver")
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


def add_platform_prefix(df: DataFrame, column: str, prefix: str):
    df = df.withColumn(column, F.concat(F.lit(prefix), F.col(column)))
    return df


def main():
    username = os.getenv("DB_USERNAME", "airflow")
    password = os.getenv("DB_PASSWORD", "airflow")
    url_bronze = "jdbc:postgresql://postgres:5432/bronze"  # locally: 'jdbc:postgresql://localhost:5432/silver'
    url_silver = "jdbc:postgresql://postgres:5432/silver"
    table = "players"
    schema = StructType(
        [
            StructField("player_id", StringType(), False),
            StructField("country", StringType(), True),
        ]
    )

    spark = create_spark_session()
    df_merged = spark.createDataFrame([], schema=schema)

    for platform in ["playstation", "steam", "xbox"]:
        df = read_postgre_table(
            spark, username, password, url_bronze, f"{table}_{platform}"
        )
        df = add_platform_prefix(df, "player_id", platform[0])
        df_merged = df_merged.unionByName(df, allowMissingColumns=True)

    df_merged = df_merged.fillna("Undefined", subset="country")
    df_merged = df_merged.drop("nickname", "created_date")
    load_to_postgre_db(df_merged, username, password, url_silver, table)


if __name__ == "__main__":
    main()
