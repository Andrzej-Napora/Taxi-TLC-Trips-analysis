import requests
from pathlib import Path


def file_download_process(url,name,file_dict,taxi_type):
    path = Path(f'/app/data/raw/{name}.parquet')
    if not path.exists():
        response = requests.get(url)
        response.raise_for_status()
        with open(path, 'wb') as file:
            file.write(response.content)
        print(f'{name} download complete')
    file_dict[name]=(path,taxi_type)

def download_files(start_month,start_year,end_month,end_year):
    downloaded_files = {}
    taxi_type_list = ['yellow','green','fhv','fhvhv']

    for year in list(range(start_year,end_year+1,1)):
        first_month = start_month if year==start_year else 1
        last_month = end_month if year==end_year else 12

        for month in list(range(first_month,last_month+1,1)):

            for taxi_type in taxi_type_list:
                url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year}-{month:02d}.parquet"
                file_download_process(
                    url,
                    f"{taxi_type}_taxi_records_{year}_{month:02d}",
                    downloaded_files,
                    taxi_type
                    )

    return downloaded_files
