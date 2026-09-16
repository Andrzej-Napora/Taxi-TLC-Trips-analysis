# NYC TLC Trip Record Data Download Script
# Downloads Parquet files from NYC TLC trip data and saves to Unity Catalog Volume

import time
from datetime import datetime
from zoneinfo import ZoneInfo

from date_utils import generate_date_range
from dateutil.relativedelta import relativedelta
from download_parquet_file import download_parquet_file

# Configuration
CATALOG = spark.conf.get("project.catalog_name")
BRONZE_SCHEMA = spark.conf.get("project.bronze_schema")
RAW_PATH = spark.conf.get("project.raw_path")
VOLUME = "raw"
TIME_ZONE = ZoneInfo(spark.conf.get("project.user_time_zone"))

# Parameters - modify these to set your download range
START_DATE = spark.conf.get("project.initial_date")  # Format: YYYY-MM
END_DATE = (datetime.now(tz=TIME_ZONE)-relativedelta(months=1)).strftime("%Y-%m")    # Format: YYYY-MM
TAXI_TYPE = ["yellow","green","fhv","fhvhv"]


def main():
    """
    Main function to download NYC TLC trip data files.
    """
    # Construct volume path
    volume_path = f"/Volumes/{CATALOG}/{BRONZE_SCHEMA}/{VOLUME}"
    
    for taxi in TAXI_TYPE:
        print("="*60)
        print("NYC TLC Trip Record Data Downloader")
        print("="*60)
        print("Source: NYC TLC Trip Record Data")
        print(f"Date range: {START_DATE} to {END_DATE}")
        print(f"Taxi type: {taxi}")
        print(f"Target volume: {volume_path}")
        print("="*60)
        print()
        
        # Generate date range
        dates = generate_date_range(START_DATE,END_DATE)
        total_files = len(dates)
        
        print(f"Will attempt to download {total_files} file(s)\n")
        
        # Download files
        successful = 0
        failed = 0
        
        files_set = set()
        files = dbutils.fs.ls(RAW_PATH)
        for file in files:
            files_set.add(file.name)

        for i, date_str in enumerate(dates, 1):
            print(f"[{i}/{total_files}] ", end="")
            if download_parquet_file(date_str, taxi, volume_path,files_set):
                successful += 1
            else:
                failed += 1
            
            # add a small delay between downloads
            if i < total_files:
                time.sleep(1)
            print()
        
        # Summary
        print("="*60)
        print("Download Summary")
        print("="*60)
        print(f"Total files processed: {total_files}")
        print(f"Successful downloads: {successful}")
        print(f"Failed downloads: {failed}")
        print(f"\nFiles saved to: {volume_path}")
        print("="*60)

if __name__ == "__main__":
    main()