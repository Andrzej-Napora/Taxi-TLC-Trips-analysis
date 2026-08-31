select * from {{ref('stg_yellow_taxi_trip_records')}}
where tpep_pickup_datetime > tpep_dropoff_datetime