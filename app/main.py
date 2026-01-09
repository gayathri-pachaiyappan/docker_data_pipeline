from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, to_date

def main():
    spark = (
        SparkSession.builder
        .appName("LocalCSVToParquet")
        .master("local[*]")  # run Spark in local mode
        .config("spark.sql.shuffle.partitions", "1")
        .getOrCreate()
    )

    input_path = "/app/data/input.csv"
    output_path = "/app/output/parquet"

    # Read CSV
    df = spark.read.option("header", True).option("inferSchema", True).csv(input_path)

    # Transform: normalize name, cast date, filter positive amounts
    transformed = (
        df
        .withColumn("name_upper", upper(col("name")))
        .withColumn("date", to_date(col("date")))
        .filter(col("amount") > 0)
    )

    # Write Parquet (overwrite for repeatable runs)
    transformed.write.mode("overwrite").parquet(output_path)

    # Show small sample in logs
    transformed.show(truncate=False)

    spark.stop()

if __name__ == "__main__":
    main()

