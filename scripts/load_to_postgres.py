from sqlalchemy import create_engine,text,inspect
from file_download import download_files
from io import StringIO
import pyarrow.parquet as pq
import pandas as pd
import os
import csv

engine = create_engine(
    f"postgresql+psycopg2://" \
    f"{os.getenv('POSTGRES_USER')}:" \
    f"{os.getenv('POSTGRES_PASSWORD')}"
    f"@PostgreSQL:5432/" \
    f"{os.getenv('POSTGRES_DB')}"
                        )

schema_name = 'raw'

with engine.begin() as connection:
    connection.execute(text(f'create schema if not exists {schema_name}'))

files_dict = download_files(1,2020,2,2020)

files_processed = set()
files_processed_path = "/app/data/files_processed.csv"
os.makedirs("/app/data/", exist_ok=True)
if os.path.exists(files_processed_path):
    with open(files_processed_path,"r") as file:
        reader = csv.reader(file)
        for row in reader:
            for item in row:
                files_processed.add(item)
for name,taxi_tuple in files_dict.items():

    parquet_file = pq.ParquetFile(taxi_tuple[0])

    table_name=f"{taxi_tuple[1]}_trip_records"

    if table_name not in files_processed:

        db_inspector = inspect(engine)
        table_exists = db_inspector.has_table(table_name=table_name,schema=schema_name )
        if not table_exists:
            parquet_file_first_batch = next(parquet_file.iter_batches(1))
            df_empty = parquet_file_first_batch.to_pandas(types_mapper=pd.ArrowDtype).head(0)

            df_empty.columns = [col.lower() for col in df_empty.columns]

            df_empty.to_sql(
                name = table_name,
                con = engine,
                schema =schema_name,
                if_exists = 'replace',
                index = False,
            )
            
        rows_processed = 0
        raw_connection = engine.raw_connection()
        db_columns = [col['name'] for col in db_inspector.get_columns(table_name,schema=schema_name)]

        try:
            with raw_connection.cursor() as psy_cursor:
                for batch in parquet_file.iter_batches(100000):

                    rows_processed += len(batch)
                    batch_csv_buffer = StringIO()
                    batch_dataframe = batch.to_pandas(types_mapper=pd.ArrowDtype)

                    batch_dataframe.columns = [col.lower() for col in batch_dataframe.columns]
                    batch_dataframe = batch_dataframe.reindex(columns=db_columns)

                    batch_dataframe.to_csv(batch_csv_buffer,
                                            header = False,
                                            index=False,
                                            mode='a')

                    batch_csv_buffer.seek(0)

                    psy_cursor.copy_expert(f"""COPY {schema_name}.{table_name} FROM STDIN with (format csv)""",batch_csv_buffer)
                    raw_connection.commit()

        finally:
            raw_connection.close()
        if rows_processed==parquet_file.metadata.num_rows:
            with open(files_processed_path,"a") as file:
                file.write(f"{table_name},")
                files_processed.add(table_name)