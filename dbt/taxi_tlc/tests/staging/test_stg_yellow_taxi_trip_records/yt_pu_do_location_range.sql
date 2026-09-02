select * from {{ref('stg_yellow_taxi_trip_records')}}
where pulocationid not between 1 and 265
or dolocationid not between 1 and 265