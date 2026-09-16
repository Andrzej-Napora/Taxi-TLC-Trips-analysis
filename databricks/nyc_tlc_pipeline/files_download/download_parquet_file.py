import requests

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"

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