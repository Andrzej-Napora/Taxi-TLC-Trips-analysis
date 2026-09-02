select * from {{ref('unioned_taxi_trip_records')}}
where pickup_datetime>dropoff_datetime