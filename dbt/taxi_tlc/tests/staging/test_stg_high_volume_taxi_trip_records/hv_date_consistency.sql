select *
from {{ref('stg_high_volume_taxi_trip_records')}}
where pickup_datetime>dropoff_datetime