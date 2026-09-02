select *
from {{ref('stg_high_volume_taxi_trip_records')}}
where trip_miles < 0
    or trip_time < 0
    or tolls < 0
    or bcf < 0
    or sales_tax < 0
    or congestion_surcharge < 0
    or airport_fee < 0
    or tips < 0