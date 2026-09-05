# NYC TLC Trip Record Data Download Script
# Downloads Parquet files from NYC TLC trip data and saves to Unity Catalog Volume

import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

# Configuration
CATALOG = "workspace"
SCHEMA = "bronze"
VOLUME = "raw"
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"

# Parameters - modify these to set your download range
START_DATE = "2024-08"  # Format: YYYY-MM
END_DATE = "2025-03"    # Format: YYYY-MM
TAXI_TYPE = ["yellow","green","fhv","fhvhv"]    # Options: yellow, green, fhv, fhvhv

def generate_date_range(start_date_str, end_date_str):
    """
    Generate a list of year-month strings between start and end dates.
    
    Args:
        start_date_str: Start date in YYYY-MM format
        end_date_str: End date in YYYY-MM format
    
    Returns:
        List of date strings in YYYY-MM format
    """
    start = datetime.strptime(start_date_str, "%Y-%m")
    end = datetime.strptime(end_date_str, "%Y-%m")
    
    dates = []
    current = start
    while current <= end:
        dates.append(current.strftime("%Y-%m"))
        current += relativedelta(months=1)
    
    return dates

def download_parquet_file(date_str, taxi_type, target_path):
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
    except Exception as e:
        print(f"✗ Error downloading {filename}: {e}")
        return False

def main():
    """
    Main function to download NYC TLC trip data files.
    """
    # Construct volume path
    volume_path = f"/Volumes/{CATALOG}/{SCHEMA}/{VOLUME}"
    
    for taxi in TAXI_TYPE:
        print("="*60)
        print("NYC TLC Trip Record Data Downloader")
        print("="*60)
        print(f"Source: NYC TLC Trip Record Data")
        print(f"Date range: {START_DATE} to {END_DATE}")
        print(f"Taxi type: {taxi}")
        print(f"Target volume: {volume_path}")
        print("="*60)
        print()
        
        # Generate date range
        dates = generate_date_range(START_DATE, END_DATE)
        total_files = len(dates)
        
        print(f"Will attempt to download {total_files} file(s)\n")
        
        # Download files
        successful = 0
        failed = 0
        
        for i, date_str in enumerate(dates, 1):
            print(f"[{i}/{total_files}] ", end="")
            if download_parquet_file(date_str, taxi, volume_path):
                successful += 1
            else:
                failed += 1
            
            # Be nice to the server - add a small delay between downloads
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