def main():
    raw_path = '/Volumes/workspace/bronze/raw'
    files_list = dbutils.fs.ls(raw_path)
    for file in files_list:
        if file.size == 0:
            print(f"File {file.name} is empty")
            return 1
    taxi_type = ['yellow','green','fhv','fhvhv']
    for taxi in taxi_type:
        spark.sql(fr"""
            CREATE TABLE IF NOT EXISTS workspace.bronze.{taxi}_trip_records
        """)
        
        spark.sql(fr"""
            ALTER TABLE workspace.bronze.{taxi}_trip_records 
            SET TBLPROPERTIES ('delta.feature.timestampNtz' = 'supported')
        """)

        spark.sql(fr"""
            COPY INTO workspace.bronze.{taxi}_trip_records
            FROM '/Volumes/workspace/bronze/raw'
            FILEFORMAT = PARQUET
            PATTERN = '{taxi}_tripdata_*.parquet'
            FORMAT_OPTIONS ('mergeSchema' = 'true')
            COPY_OPTIONS ('mergeSchema' = 'true')
        """)


if __name__ == "__main__":
    main()