from pyspark import pipelines as dp
from pyspark.sql import functions as F

raw_path = spark.conf.get("project.raw_volume_path")
catalog_name = spark.conf.get("project.catalog_name")
bronze_schema = spark.conf.get("project.bronze_schema")


@dp.table(
    name=f"{catalog_name}.{bronze_schema}.yellow_trip_records",
    table_properties={"delta.feature.timestampNtz": "supported"}
)

def yellow_trip_records():
    return (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "parquet")
    .option("pathGlobFilter", "yellow_tripdata_*.parquet")
    .load(raw_path)
    .select("*",
            F.col("_metadata.file_name").alias("_source_file"),
            F.current_timestamp().alias("_ingested_at"),
            F.col("_metadata.file_size").alias("_file_size")
            )
    )

@dp.table(
    name=f"{catalog_name}.{bronze_schema}.green_trip_records",
    table_properties={"delta.feature.timestampNtz": "supported"}
)
def green_trip_records():
    return (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "parquet")
    .option("pathGlobFilter", "green_tripdata_*.parquet")
    .load(raw_path)
    .select("*",
            F.col("_metadata.file_name").alias("_source_file"),
            F.current_timestamp().alias("_ingested_at"),
            F.col("_metadata.file_size").alias("_file_size")
            )
    )

@dp.table(
    name=f"{catalog_name}.{bronze_schema}.fhv_trip_records",
    table_properties={"delta.feature.timestampNtz": "supported"}
)
def fhv_trip_records():
    return (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "parquet")
    .option("pathGlobFilter", "fhv_tripdata_*.parquet")
    .load(raw_path)
    .select("*",
            F.col("_metadata.file_name").alias("_source_file"),
            F.current_timestamp().alias("_ingested_at"),
            F.col("_metadata.file_size").alias("_file_size")
            )
    )

@dp.table(
    name=f"{catalog_name}.{bronze_schema}.fhvhv_trip_records",
    table_properties={"delta.feature.timestampNtz": "supported"}
)
def fhvhv_trip_records():
    return (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "parquet")
    .option("pathGlobFilter", "fhvhv_tripdata_*.parquet")
    .load(raw_path)
    .select("*",
            F.col("_metadata.file_name").alias("_source_file"),
            F.current_timestamp().alias("_ingested_at"),
            F.col("_metadata.file_size").alias("_file_size")
            )
    )



    
