from sqlalchemy import create_engine,text,inspect
from file_download import download_files
from io import StringIO
import pyarrow.parquet as pq
import pandas as pd
import os
import csv

dec_columns = set([
    'fare_amount',
    'extra',
    'mta_tax',
    'tip_amount',
    'tolls_amount',
    'improvement_surcharge',
    'total_amount',
    'congestion_surcharge',
    'airport_fee',
    'base_passenger_fare',
    'tolls',
    'bcf',
    'sales_tax',
    'tips',
    'driver_pay',
    'trip_distance',
    'trip_miles',
    'cbd_congestion_fee'
])

int_columns = set([
    'vendorid',
    'passenger_count',
    'ratecodeid',
    'pulocationid',
    'dolocationid',
    'payment_type',
    'trip_time'
])

text_columns = set([
    'store_and_fwd_flag',
    'hvfhs_license_num',
    'dispatching_base_num',
    'originating_base_num',
    'shared_request_flag',
    'shared_match_flag',
    'access_a_ride_flag',
    'wav_request_flag',
    'wav_match_flag'
])

date_columns = set([
    'tpep_pickup_datetime',
    'tpep_dropoff_datetime',
    'request_datetime',
    'on_scene_datetime',
    'pickup_datetime',
    'dropoff_datetime',
    'lpep_pickup_datetime',
    'lpep_dropoff_datetime'
])

#converting columns types in dataframes
def type_conversion(df):

    for col in df.columns:
        if col in dec_columns:
            df[col] = pd.to_numeric(df[col],errors='coerce').astype('float64')
        elif col in int_columns:
            df[col] = pd.to_numeric(df[col],errors='coerce').astype('Int32')
        elif col in date_columns:
            df[col] = pd.to_datetime(df[col],errors='coerce')
        elif col in text_columns:
            df[col] = df[col].str.lower()
        elif col == 'sr_flag':
            df[col] = pd.to_numeric(df['sr_flag'], errors='coerce').fillna(0).astype('Int32')
    return df

#determin col data type
def col_type_conversion(col):
    if col in dec_columns:
        col_type = "DOUBLE PRECISION"
    elif col in int_columns or col == 'sr_flag':
        col_type = "INT"
    elif col in date_columns:
        col_type = "TIMESTAMP"
    else:
        col_type = "TEXT"
    return col_type


engine = create_engine(
    f"postgresql+psycopg2://" \
    f"{os.getenv('POSTGRES_USER')}:" \
    f"{os.getenv('POSTGRES_PASSWORD')}"
    f"@PostgreSQL:5432/" \
    f"{os.getenv('POSTGRES_DB')}"
                        )

# creating raw schema
schema_name = 'raw'
with engine.begin() as connection:
    connection.execute(text(f'create schema if not exists {schema_name}'))

#reading file containing all processsed files names
files_processed = set()
files_processed_path = "/app/data/files_processed.csv"
os.makedirs("/app/data/", exist_ok=True)
if os.path.exists(files_processed_path):
    with open(files_processed_path,"r") as file:
        reader = csv.reader(file)
        for row in reader:
            for item in row:
                files_processed.add(item)

#looping through all downloaded files
#this is where you set up which months you want to process
files_dict = download_files(11,2025,12,2025)
for name,url_tableName in files_dict.items():

    parquet_file = pq.ParquetFile(url_tableName[0])
    table_name=f"{url_tableName[1]}_trip_records"

    #processing file if not already processed
    if name not in files_processed:

        #creating new empty table if not exists
        table_exists = inspect(engine).has_table(table_name=table_name,schema=schema_name )
        if not table_exists:
            parquet_file_first_batch = next(parquet_file.iter_batches(1))
            df_empty = parquet_file_first_batch.to_pandas(types_mapper=pd.ArrowDtype).head(0)

            df_empty.columns = [col.lower() for col in df_empty.columns]
            df_empty = type_conversion(df_empty)
            df_empty.to_sql(
                name = table_name,
                con = engine,
                schema =schema_name,
                if_exists = 'replace',
                index = False,
            )
            
        rows_processed = 0
        raw_connection = engine.raw_connection()

        #adding new columns from file to raw.table
        db_columns = [col['name'] for col in inspect(engine).get_columns(table_name,schema=schema_name)]
        files_columns = [col.lower() for col in parquet_file.schema.names]
        if files_columns != db_columns:
            with engine.connect() as connection:
                col_difference = set(files_columns)-set(db_columns)
                for col in col_difference:
                    col = col.lower()
                    connection.execute(text(f"alter table {schema_name}.{table_name}\
                                            add column if not exists {col} {col_type_conversion(col)}"))
                    db_columns = [col['name'] for col in inspect(engine).get_columns(table_name,schema=schema_name)]
                    connection.commit()

        try:
            with raw_connection.cursor() as psy_cursor:
                #looping through parquet file by batches
                for batch in parquet_file.iter_batches(100000):

                    #counting processed rows for finding file end
                    rows_processed += len(batch)

                    #creating buffer accepting csv format data
                    batch_csv_buffer = StringIO()

                    batch_dataframe = batch.to_pandas(types_mapper=pd.ArrowDtype)
                    batch_dataframe.columns = [col.lower() for col in batch_dataframe.columns]

                    #fixing data frame columns order
                    batch_dataframe = batch_dataframe.reindex(columns=db_columns)
                    batch_dataframe = type_conversion(batch_dataframe)

                    #sending batches in csv format into buffer
                    batch_dataframe.to_csv(batch_csv_buffer,
                                            header = False,
                                            index=False)
                    batch_csv_buffer.seek(0)

                    #copying content from buffer to table in database
                    psy_cursor.copy_expert(f"""COPY {schema_name}.{table_name}\
                         ({','.join(batch_dataframe.columns)})
                           FROM STDIN with (format csv)""",batch_csv_buffer)
                raw_connection.commit()
        except Exception:
            raw_connection.rollback()
            raise

        finally:
            raw_connection.close()

        #writing processed file into files_processed
        if rows_processed==parquet_file.metadata.num_rows:
            with open(files_processed_path,"a") as file:
                file.write(f"{name},")
                files_processed.add(name)