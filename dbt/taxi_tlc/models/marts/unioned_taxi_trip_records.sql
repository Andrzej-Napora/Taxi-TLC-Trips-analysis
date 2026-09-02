(
select * from {{ref('int_yellow_taxi_trip_records')}} 
)
union all
(
select * from {{ref('int_green_taxi_trip_records')}} 
)
union all
(
select * from {{ref('int_for_hire_taxi_trip_records')}} 
)
union all
(
select * from {{ref('int_high_volume_taxi_trip_records')}} 
)
