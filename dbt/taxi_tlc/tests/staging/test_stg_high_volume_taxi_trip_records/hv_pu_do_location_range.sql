select * from {{ref('stg_high_volume_taxi_trip_records')}}
where PU_Location_ID not between 1 and 265
or DO_Location_ID not between 1 and 265