select * from {{ref('stg_for_hire_taxi_trip_records')}}
where pickup_datetime > dropOff_datetime