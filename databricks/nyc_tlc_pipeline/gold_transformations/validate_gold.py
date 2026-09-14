CATALOG_NAME=spark.conf.get("project.catalog_name")
SILVER_SCHEMA = spark.conf.get("project.silver_schema")
GOLD_SCHEMA = spark.conf.get("project.gold_schema")


dfy = spark.table(f'{CATALOG_NAME}.{SILVER_SCHEMA}.yellow_trip_records')
dfg = spark.table(f'{CATALOG_NAME}.{SILVER_SCHEMA}.green_trip_records')
dffhv = spark.table(f'{CATALOG_NAME}.{SILVER_SCHEMA}.fhv_trip_records')
dfhv = spark.table(f'{CATALOG_NAME}.{SILVER_SCHEMA}.fhvhv_trip_records')
dfgold = spark.table(f'{CATALOG_NAME}.{GOLD_SCHEMA}.unioned_tables')

error = False

# test 1 - record count consistency
silver = [dfy,dfg,dffhv,dfhv]

silver_count = sum(table.count() for table in silver)
gold_count = dfgold.count()

if silver_count == gold_count:
    print("test finished successfully")
else:
    print("records count do not match")
    error = True

# test 2 - data_type content

silver_data_type = set()
for df in silver:
    silver_data_type.update(row['data_type'] for row in df.select('data_type').distinct().collect())

gold_data_type = {row['data_type'] for row in dfgold.select('data_type').distinct().collect()}

if silver_data_type == gold_data_type:
    print("test finished successfully")
else:
    print("data_type content do not match")
    error = True

# test 3 - schema consistency

for df in silver:
    if df.schema != dfgold.schema:
        print("schema content do not match")
        error = True
    else:
        print("test finished successfully")

# test 4 - datetime consistency

row_count = dfgold.filter("pickup_datetime>dropoff_datetime").count()

if row_count==0:
    print("test finished successfully")
else:
    print("pickup_datetime is greater than dropoff_datetime")
    error = True

# test 5 - factual values not null

row_count_fv = dfgold.filter(
        """pickup_datetime is null
        or dropoff_datetime is null
        or trip_distance is null
        or pu_location_id is null
        or do_location_id is null"""
    ).count()

if row_count_fv==0:
    print("test finished successfully")
else:
    print("factual value is null")
    error = True

# test 6 - valid location code

location_code_count = dfgold.filter(
    "pu_location_id not between 1 and 265 or do_location_id not between 1 and 265"
    ).count()

if location_code_count==0:
    print("test finished successfully")
else:
    print("invalid location code")
    error = True


assert error == False, 'gold test failed'