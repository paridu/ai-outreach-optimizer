import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, from_unixtime, to_timestamp, current_timestamp
from pyspark.sql.types import StructType, StringType, DoubleType, LongType, MapType

# --- CONFIGURATION ---
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_SERVERS", "kafka:9092")
KAFKA_TOPIC = "customer.interactions.raw"
CHECKPOINT_LOCATION = "/mnt/datalake/checkpoints/interaction_ingestion"
OUTPUT_PATH = "/mnt/datalake/bronze/customer_interactions"

def build_spark_session():
    return SparkSession.builder \
        .appName("ETL-RealTime-Customer-Interactions") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

def run_pipeline():
    spark = build_spark_session()

    # Define schema matching the Avro/Protobuf blueprint
    schema = StructType() \
        .add("event_id", StringType()) \
        .add("customer_id", StringType()) \
        .add("event_type", StringType()) \
        .add("timestamp", LongType()) \
        .add("platform", StringType()) \
        .add("page_url", StringType()) \
        .add("product_id", StringType()) \
        .add("action_value", DoubleType()) \
        .add("metadata", MapType(StringType(), StringType()))

    # 1. EXTRACT: Stream from Kafka
    raw_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", KAFKA_TOPIC) \
        .option("startingOffsets", "latest") \
        .load()

    # 2. TRANSFORM: Parse JSON and cast types
    # (Note: Using JSON for demo, would use from_avro in production per Architecture)
    transformed_df = raw_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*") \
        .withColumn("event_time", to_timestamp(from_unixtime(col("timestamp") / 1000))) \
        .withColumn("ingestion_at", current_timestamp())

    # 3. LOAD: Write to Delta Lakehouse (Bronze Layer)
    query = transformed_df.writeStream \
        .format("delta") \
        .outputMode("append") \
        .option("checkpointLocation", CHECKPOINT_LOCATION) \
        .partitionBy("event_type") \
        .start(OUTPUT_PATH)

    query.awaitTermination()

if __name__ == "__main__":
    run_pipeline()