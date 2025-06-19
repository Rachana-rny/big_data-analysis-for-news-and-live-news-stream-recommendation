from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType

spark = SparkSession.builder.appName("NewsConsumer").getOrCreate()
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "news") \
    .load()

schema = StructType().add("title", StringType()).add("description", StringType()).add("url", StringType()).add("publishedAt", StringType())
json_df = df.selectExpr("CAST(value AS STRING)").select(from_json(col("value"), schema).alias("data")).select("data.*")

query = json_df.writeStream.outputMode("append").format("csv").option("path", "../data/recommended_news.csv").option("checkpointLocation", "/tmp/checkpoint").start()
query.awaitTermination()