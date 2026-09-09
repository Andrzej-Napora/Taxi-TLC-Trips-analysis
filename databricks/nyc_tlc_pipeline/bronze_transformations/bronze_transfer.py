from pyspark import pipelines as dp



@dp.table(
    name="workspace.bronze.yellow_trip_records",
    table_properties={"delta.feature.timestampNtz": "supported"}
)

def yellow_trip_records():
    return (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "parquet")
    .option("pathGlobFilter", "yellow_tripdata_*.parquet")
    .load("/Volumes/workspace/bronze/raw")
    )

@dp.table(
    name="workspace.bronze.green_trip_records",
    table_properties={"delta.feature.timestampNtz": "supported"}
)
def green_trip_records():
    return (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "parquet")
    .option("pathGlobFilter", "green_tripdata_*.parquet")
    .load("/Volumes/workspace/bronze/raw")
    )

@dp.table(
    name="workspace.bronze.fhv_trip_records",
    table_properties={"delta.feature.timestampNtz": "supported"}
)
def fhv_trip_records():
    return (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "parquet")
    .option("pathGlobFilter", "fhv_tripdata_*.parquet")
    .load("/Volumes/workspace/bronze/raw")
    )

@dp.table(
    name="workspace.bronze.fhvhv_trip_records",
    table_properties={"delta.feature.timestampNtz": "supported"}
)
def fhvhv_trip_records():
    return (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "parquet")
    .option("pathGlobFilter", "fhvhv_tripdata_*.parquet")
    .load("/Volumes/workspace/bronze/raw")
    )
