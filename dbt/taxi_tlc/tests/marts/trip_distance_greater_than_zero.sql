select * from {{ref('unioned_taxi_trip_records')}}
where trip_distance<0