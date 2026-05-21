from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, max, min


builder = (
    SparkSession.builder
    .appName("DeltaWeatherTransformation")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)

spark = configure_spark_with_delta_pip(builder).getOrCreate()

bronze_df = spark.read.parquet("data/bronze/real_weather.parquet")

silver_df = bronze_df.dropna()

silver_df.write.format("delta").mode("overwrite").save("data/silver/delta_weather")

gold_df = (
    silver_df.groupBy("city")
    .agg(
        avg("temperature").alias("avg_temperature"),
        min("temperature").alias("min_temperature"),
        max("temperature").alias("max_temperature"),
    )
)

gold_df.write.format("delta").mode("overwrite").save("data/gold/delta_weather_summary")

print("Delta Lake transformation completed successfully")

spark.stop()
