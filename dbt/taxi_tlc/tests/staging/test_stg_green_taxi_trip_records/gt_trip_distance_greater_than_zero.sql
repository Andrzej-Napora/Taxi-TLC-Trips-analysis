select *
from {{ref('stg_green_taxi_trip_records')}}
where trip_distance<0