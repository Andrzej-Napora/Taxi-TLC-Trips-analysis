select * from {{ref('stg_yellow_taxi_trip_records')}}
where pu_location_id not between 1 and 265
or do_location_id not between 1 and 265