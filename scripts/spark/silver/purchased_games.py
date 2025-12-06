from pyspark.sql import SparkSession
from pyspark.sql.types import (
    ArrayType,
    IntegerType,
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


def add_pratform_prefix(df: DataFrame, column: str, prefix: str):
    df = df.withColumn(column, F.concat(F.lit(prefix), F.col(column)))
    return df


def main():
    username = "airflow"
    password = "airflow"
    url_bronze = "jdbc:postgresql://postgres:5432/bronze"  # without airlow: 'jdbc:postgresql://localhost:5432/bronze'
    url_silver = "jdbc:postgresql://postgres:5432/silver"
    table = "purchased_games"
    schema = StructType(
        [
            StructField("player_id", StringType(), False),
            StructField("games", ArrayType(IntegerType()), True),
        ]
    )

    spark = create_spark_session()
    df_merged = spark.createDataFrame([], schema=schema)

    for platform in ["playstation", "steam", "xbox"]:
        df = read_postgre_table(
            spark, username, password, url_bronze, f"{table}_{platform}"
        )
        df = add_pratform_prefix(df, "player_id", platform[0])
        df_merged = df_merged.union(df)

    load_to_postgre_db(df_merged, username, password, url_silver, table)


if __name__ == "__main__":
    main()
