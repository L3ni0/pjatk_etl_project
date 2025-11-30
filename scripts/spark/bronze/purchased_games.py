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
        SparkSession.builder.appName("Purchased bronze")
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3")
        .getOrCreate()
    )

    return spark


def read_csv_file(spark: SparkSession, path: str, schema: StructType) -> DataFrame:
    df = spark.read.options(header=True, delimiter=",").schema(schema).csv(path)

    df = df.withColumn("games", F.from_json(F.col("library"), ArrayType(IntegerType())))
    df = df.drop("library")

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
    username = "airflow"
    password = "airflow"
    url = "jdbc:postgresql://postgresql:5432/bronze"  # without airlow: 'jdbc:postgresql://localhost:5432/bronze'
    schema = StructType(
        [
            StructField("player_id", StringType(), False),
            StructField("library", StringType(), True),
        ]
    )

    spark = create_spark_session()

    for platform in ["playstation", "steam", "xbox"]:
        df = read_csv_file(spark, f"data/{platform}/purchased_games.csv", schema=schema)
        load_to_postgre_db(df, username, password, url, f"purchased_games_{platform}")


if __name__ == "__main__":
    main()
