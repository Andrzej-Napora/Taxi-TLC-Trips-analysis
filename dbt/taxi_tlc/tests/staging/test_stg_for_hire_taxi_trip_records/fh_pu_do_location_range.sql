select * from {{ref('stg_for_hire_taxi_trip_records')}}
where PULocationID not between 1 and 265
or DOLocationID not between 1 and 265