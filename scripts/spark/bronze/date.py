import os
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructField,
    StructType,
    DateType,
    IntegerType
)
from pyspark.sql import functions as F
from pyspark.sql.dataframe import DataFrame


def create_spark_session() -> SparkSession:
    spark = (
        SparkSession.builder.appName("Date bronze")
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3")
        .getOrCreate()
    )

    return spark


def read_csv_file(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
    df = (
        spark.read
        .options(header=True, delimiter=",")
        .option("dateFormat", "d.MM.yyyy")
        .schema(schema)
        .csv(path)
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
            StructField("date_id", IntegerType(), False),
            StructField("transaction_date", DateType(), True),
        ]
    )

    spark = create_spark_session()

    df = read_csv_file(spark, f"data/date.csv", schema=schema)
    load_to_postgre_db(df, username, password, url, f"date")


if __name__ == "__main__":
    main()
