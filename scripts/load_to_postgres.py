from sqlalchemy import create_engine,text
from file_download import download_files
from pathlib import Path
import pyarrow.parquet as pq
import pandas as pd
import os

engine = create_engine(
    f"postgresql+psycopg2://" \
    f"{os.getenv('POSTGRES_USER')}:" \
    f"{os.getenv('POSTGRES_PASSWORD')}"
    f"@PostgreSQL:5432/" \
    f"{os.getenv('POSTGRES_DB')}"
                        )

with engine.begin() as connection:
    connection.execute(text('create schema if not exists raw'))

files_dict = download_files()

for name,path in files_dict.items():

    parquet_file = pq.ParquetFile(path)
    parquet_file_first_batch = next(parquet_file.iter_batches(10))
    df_empty = parquet_file_first_batch.to_pandas(types_mapper=pd.ArrowDtype).head(0)
    df_empty.to_sql(
        name = name,
        con = engine,
        schema ='raw',
        if_exists = 'replace',
        index = False,
    )

    taxi_csv_path = Path(f"/app/data/raw/{name}.csv")

    if not taxi_csv_path.exists():

        for batch_number,batch in enumerate(parquet_file.iter_batches(50000)):
            file_dataframe = batch.to_pandas(types_mapper=pd.ArrowDtype)
            file_dataframe.to_csv(taxi_csv_path,
                                  mode = 'w' if batch_number==0 else 'a',
                                  header = True if batch_number==0 else False,
                                  index=False)


    
        with open(taxi_csv_path,'r',encoding='utf-8') as taxi_csv_file:
            raw_connection = engine.raw_connection()
            try:
                with raw_connection.cursor() as psy_cursor:
                    psy_cursor.copy_expert(f"""COPY raw.{name} FROM STDIN with (format csv, header true)""",taxi_csv_file)
                    raw_connection.commit()
            finally:
                raw_connection.close()