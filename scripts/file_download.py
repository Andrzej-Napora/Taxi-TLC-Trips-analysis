import requests
from pathlib import Path

yt_path = Path('app/data/raw/yellow_taxi_trip_records.parquet')
if not yt_path.exists():
    yellow_taxi = requests.get('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet')
    yellow_taxi.raise_for_status()
    with open(yt_path,'wb') as yt_file:
        yt_file.write(yellow_taxi.content)
    print('yellow_taxi_trip_records download complete')

gt_path = Path('app/data/raw/green_taxi_trip_records.parquet')
if not gt_path.exists():
    green_taxi = requests.get('https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2026-01.parquet')
    green_taxi.raise_for_status()
    with open(gt_path,'wb') as gt_file:
        gt_file.write(green_taxi.content)
    print('green_taxi_trip_records download complete')

fh_path = Path('app/data/raw/for_hire_taxi_trip_records.parquet')
if not fh_path.exists():
    for_hire = requests.get('https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2026-01.parquet')
    for_hire.raise_for_status()
    with open(fh_path,'wb') as fh_file:
        fh_file.write(for_hire.content)
    print('for_hire_taxi_trip_records download complete')

hv_path = Path('app/data/raw/high_volume_taxi_trip_records.parquet')
if not hv_path.exists():
    high_volume = requests.get('https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_2026-01.parquet')
    high_volume.raise_for_status()
    with open(hv_path,'wb') as hv_file:
        hv_file.write(high_volume.content)
    print('high_volume_taxi_trip_records download complete')

