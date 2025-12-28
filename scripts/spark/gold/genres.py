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
) -> DataFrame:
    properties = {
        "user": username,
        "password": password,
        "driver": "org.postgresql.Driver",
    }
    return spark.read.jdbc(url=url, table=table, properties=properties)


def load_to_postgre_db(
    df: DataFrame, username: str, password: str, url: str, table: str
):
    properties = {
        "user": username,
        "password": password,
        "driver": "org.postgresql.Driver",
    }

    df.write.jdbc(url=url, table=table, mode="overwrite", properties=properties)


def create_id(df: DataFrame, id_col_name: str) -> DataFrame:
    return df.withColumn(id_col_name, F.monotonically_increasing_id())


def main():
    username = os.getenv("DB_USERNAME", "airflow")
    password = os.getenv("DB_PASSWORD", "airflow")
    url_silver = "jdbc:postgresql://postgres:5432/silver"
    table_silver = "games"
    url_gold = "jdbc:postgresql://postgres:5432/gold"

    spark = create_spark_session()

    df = read_postgre_table(spark, username, password, url_silver, table_silver)

    sample = df.select("genres").limit(1).collect()[0]["genres"]
    if isinstance(sample, list):
        genres = df.select(F.explode("genres").alias("genre_name")).distinct()
    else:
        genres = df.select(F.split(F.col("genres"), ",").alias("genres"))
        genres = genres.select(F.explode("genres").alias("genre_name")).distinct()

    genres = genres.withColumn("genre_name", F.trim(F.col("genre_name")))
    genres = create_id(genres, "genre_id")
    if isinstance(sample, list):
        relations = df.select("game_id", F.explode("genres").alias("genre_name"))
    else:
        relations = df.select("game_id", F.split(F.col("genres"), ",").alias("genres"))
        relations = relations.select("game_id", F.explode("genres").alias("genre_name"))

    relations = relations.withColumn("genre_name", F.trim(F.col("genre_name")))
    relations = relations.join(genres, "genre_name", "left")
    relations = relations.select("game_id", "genre_id")

    genres = genres.select("genre_id", "genre_name")
    load_to_postgre_db(genres, username, password, url_gold, "genres")

    load_to_postgre_db(relations, username, password, url_gold, "game_genres")


if __name__ == "__main__":
    main()
