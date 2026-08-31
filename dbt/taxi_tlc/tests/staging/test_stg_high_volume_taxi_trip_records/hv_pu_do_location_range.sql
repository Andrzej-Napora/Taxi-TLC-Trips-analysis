select * from {{ref('stg_high_volume_taxi_trip_records')}}
where PULocationID not between 1 and 265
or DOLocationID not between 1 and 265