import os
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    ArrayType,
    StringType,
    StructField,
    StructType,
    DateType,
)
from pyspark.sql import functions as F
from pyspark.sql.dataframe import DataFrame


def create_spark_session() -> SparkSession:
    spark = (
        SparkSession.builder.appName("Games bronze")
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3")
        .getOrCreate()
    )

    return spark


def read_csv_file(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
    df = spark.read.options(header=True, delimiter=",").schema(schema).csv(path)

    return df


def parse_str_to_array(df: DataFrame, column: str) -> DataFrame:
    df = df.withColumn(
        column,
        F.from_json(F.regexp_replace(df[column], "'", '"'), ArrayType(StringType())),
    )
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
    url = "jdbc:postgresql://postgres:5432/bronze"  # locally: 'jdbc:postgresql://localhost:5432/bronze'
    schema = StructType(
        [
            StructField("game_id", StringType(), False),
            StructField("title", StringType(), True),
            StructField("developer", StringType(), True),
            StructField("publishers", StringType(), True),
            StructField("genres", StringType(), True),
            StructField("supported_languages", StringType(), True),
            StructField("release_date", DateType(), True),
        ]
    )

    spark = create_spark_session()

    for platform in ["playstation", "steam", "xbox"]:
        df = read_csv_file(spark, f"data/{platform}/games.csv", schema=schema)
        df = parse_str_to_array(df, "developer")
        df = parse_str_to_array(df, "publisshers")
        df = parse_str_to_array(df, "genres")
        df = parse_str_to_array(df, "supported_languages")
        load_to_postgre_db(df, username, password, url, f"games_{platform}")


if __name__ == "__main__":
    main()
