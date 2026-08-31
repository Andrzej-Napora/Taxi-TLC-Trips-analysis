select * from {{ref('stg_green_taxi_trip_records')}}
where pickup_location_id not between 1 and 265
or dropoff_location_id not between 1 and 265