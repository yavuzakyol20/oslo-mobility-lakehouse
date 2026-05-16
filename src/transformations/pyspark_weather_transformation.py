from pyspark.sql import SparkSession
from pyspark.sql.functions import avg


spark = (
    SparkSession.builder
    .appName("WeatherTransformation")
    .getOrCreate()
)

df = spark.read.csv(
    "data/bronze/weather.csv",
    header=True,
    inferSchema=True
)

print("Raw Bronze Data")
df.show()

summary_df = (
    df.groupBy("city")
    .agg(
        avg("temperature").alias("avg_temperature")
    )
)

print("Aggregated Weather Data")
summary_df.show()

summary_df.write.mode("overwrite").csv(
    "data/gold/pyspark_weather_summary",
    header=True
)

print("PySpark transformation completed")

spark.stop()
