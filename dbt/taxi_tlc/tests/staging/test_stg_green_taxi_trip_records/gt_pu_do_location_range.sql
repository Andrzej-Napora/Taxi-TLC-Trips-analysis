select * from {{ref('stg_green_taxi_trip_records')}}
where PULocationID not between 1 and 265
or dolocationid not between 1 and 265