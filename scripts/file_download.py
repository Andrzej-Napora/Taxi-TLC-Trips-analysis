import requests
from pathlib import Path


def file_download_process(url,name,file_dict):
    path = Path(f'/app/data/raw/{name}.parquet')
    if not path.exists():
        response = requests.get(url)
        response.raise_for_status()
        with open(path, 'wb') as file:
            file.write(response.content)
        print(f'{name} download complete')
    file_dict[name]=path

def download_files():

    downloaded_files = {}
    yellow_taxi_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet'
    green_taxi_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2026-01.parquet'
    fir_hire_taxi_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2026-01.parquet'
    high_volume_taxi_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_2026-01.parquet'

    file_download_process(yellow_taxi_url,'yellow_taxi_trip_records',downloaded_files)
    file_download_process(green_taxi_url,'green_taxi_trip_records',downloaded_files)
    file_download_process(fir_hire_taxi_url,'for_hire_taxi_trip_records',downloaded_files)
    file_download_process(high_volume_taxi_url,'high_volume_taxi_trip_records',downloaded_files)

    return downloaded_files
