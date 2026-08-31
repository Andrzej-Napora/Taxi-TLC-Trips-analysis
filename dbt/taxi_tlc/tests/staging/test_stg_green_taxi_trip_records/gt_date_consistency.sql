select * from {{ref('stg_green_taxi_trip_records')}}
where lpep_pickup_datetime > lpep_dropoff_datetime