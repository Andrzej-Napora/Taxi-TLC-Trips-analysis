from sqlalchemy import create_engine,text
from file_download import download_files
import pyarrow.parquet as pq
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

for name, path in files_dict.items():
    parquet_file = pq.ParquetFile(path)

    first_batch = True

    for batch in parquet_file.iter_batches(batch_size=50_000):
        df = batch.to_pandas()

        print(df.columns)
        print(df.dtypes)
        df.to_sql(
            name=name,
            con=engine,
            schema='raw',
            if_exists='replace' if first_batch else "append",
            index=False,
            chunksize=10000,
            method='multi'
        )

        first_batch = False
        print(f"Loaded {len(df)} rows into raw.{name}")
        del df
