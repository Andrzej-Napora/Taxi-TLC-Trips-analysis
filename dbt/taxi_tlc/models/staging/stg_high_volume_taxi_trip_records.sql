select
hvfhs_license_num,
dispatching_base_num,
originating_base_num,
request_datetime,
on_scene_datetime,
pickup_datetime,
dropoff_datetime,
"PULocationID" as PULocationID,
"DOLocationID" as DOLocationID,
trip_miles,
trip_time,
base_passenger_fare,
tolls,
bcf,
sales_tax,
congestion_surcharge,
airport_fee,
tips,
driver_pay,
shared_request_flag,
shared_match_flag,
access_a_ride_flag,
wav_request_flag,
wav_match_flag,
cbd_congestion_fee,
case 
    when driver_pay < 0
    or base_passenger_fare < 0 
    then True
    else False
end as is_negative,
case 
    when request_datetime>=on_scene_datetime
    then True
    else False
end as time_inconsistency
from {{source('raw','high_volume_taxi_trip_records')}}