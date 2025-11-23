from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder.appName("test spark").getOrCreate()

    test_data = [[1, 2], [3, 4]]
    df = spark.createDataFrame(test_data)
    df.show()

    spark.stop()


if __name__ == "__main__":
    main()
