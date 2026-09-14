# NYC TLC Trip Record Data Download Script
# Downloads Parquet files from NYC TLC trip data and saves to Unity Catalog Volume

import time
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from date_utils import generate_date_range
from dateutil.relativedelta import relativedelta

# Configuration
CATALOG = spark.conf.get("project.catalog_name")
BRONZE_SCHEMA = spark.conf.get("project.bronze_schema")
RAW_PATH = spark.conf.get("project.raw_path")
VOLUME = "raw"
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
TIME_ZONE = ZoneInfo(spark.conf.get("project.user_time_zone"))

# Parameters - modify these to set your download range
START_DATE = spark.conf.get("project.initial_date")  # Format: YYYY-MM
END_DATE = (datetime.now(tz=TIME_ZONE)-relativedelta(months=1)).strftime("%Y-%m")    # Format: YYYY-MM
TAXI_TYPE = ["yellow","green","fhv","fhvhv"]


def download_parquet_file(date_str, taxi_type, target_path,files_set):
    """
    Download a single parquet file for the specified date and taxi type.
    
    Args:
        date_str: Date in YYYY-MM format
        taxi_type: Type of taxi data (yellow, green, fhv, fhvhv)
        target_path: Target path in Unity Catalog volume
    
    Returns:
        True if successful, False otherwise
    """
    filename = f"{taxi_type}_tripdata_{date_str}.parquet"
    if filename in files_set:
        print(f"File already exists: {filename}")
        return False
    
    else:
        url = f"{BASE_URL}/{filename}"
        target_file = f"{target_path}/{filename}"
        print(f"Downloading {filename}...")
    
        try:
            response = requests.get(url, stream=True, timeout=300)
            response.raise_for_status()
            
            # Write to Unity Catalog Volume
            with open(target_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size_mb = response.headers.get('content-length')
            if file_size_mb:
                file_size_mb = int(file_size_mb) / (1024 * 1024)
                print(f"✓ Successfully downloaded {filename} ({file_size_mb:.2f} MB)")
            else:
                print(f"✓ Successfully downloaded {filename}")
            
            return True
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"✗ File not found: {filename} (might not be available yet)")
            else:
                print(f"✗ HTTP error downloading {filename}: {e}")
            return False
        except requests.exceptions.ConnectionError as e:
            print(f"✗ Error downloading {filename}: {e}")
            return False

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