select * from {{ref('stg_green_taxi_trip_records')}}
where PU_Location_ID not between 1 and 265
or do_location_id not between 1 and 265