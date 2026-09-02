from sqlalchemy import create_engine,text,inspect
from file_download import download_files
from io import StringIO
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

schema_name = 'raw'
db_inspector = inspect(engine)
marts_exist = db_inspector.has_table(table_name='unioned_taxi_trip_records',schema=schema_name)
if not marts_exist:

    with engine.begin() as connection:
        connection.execute(text(f'create schema if not exists {schema_name}'))

    files_dict = download_files()

    for name,path in files_dict.items():

        table_exists = db_inspector.has_table(table_name=name,schema=schema_name )
        if not table_exists:

            parquet_file = pq.ParquetFile(path)
            parquet_file_first_batch = next(parquet_file.iter_batches(1))
            df_empty = parquet_file_first_batch.to_pandas(types_mapper=pd.ArrowDtype).head(0)
            df_empty.to_sql(
                name = name,
                con = engine,
                schema =schema_name,
                if_exists = 'replace',
                index = False,
            )

            taxi_csv_path = f"/app/data/raw/{name}.csv"


            for batch_number,batch in enumerate(parquet_file.iter_batches(100000)):
                batch_csv_buffer = StringIO()
                batch_dataframe = batch.to_pandas(types_mapper=pd.ArrowDtype)
                batch_dataframe.to_csv(batch_csv_buffer,
                                        header = False,
                                        index=False)

                batch_csv_buffer.seek(0)
                raw_connection = engine.raw_connection()
                try:
                    with raw_connection.cursor() as psy_cursor:
                        psy_cursor.copy_expert(f"""COPY {schema_name}.{name} FROM STDIN with (format csv)""",batch_csv_buffer)
                        raw_connection.commit()
                finally:
                    raw_connection.close()
        else:
            print(f"table {name}, building terminated")
else:
    print(f"table unioned_taxi_trip_records found, building terminated")