select *
from {{ref('stg_yellow_taxi_trip_records')}}
where trip_distance<0