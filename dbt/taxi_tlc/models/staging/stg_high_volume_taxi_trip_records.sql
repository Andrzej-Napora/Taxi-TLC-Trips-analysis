select
hvfhs_license_num,
dispatching_base_num,
originating_base_num,
request_datetime,
on_scene_datetime,
pickup_datetime,
dropoff_datetime,
PULocationID as PU_Location_ID,
DOLocationID as DO_Location_ID,
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
case 
    when driver_pay < 0
    or base_passenger_fare < 0 
        then 1
        else 0
end as is_negative,
case
    when PULocationID = DOLocationID
        then 1
        else 0
end as equal_pu_do_time,
case 
    when request_datetime>=on_scene_datetime
    then 1
    else 0
end as time_inconsistency
from {{source('raw','fhvhv_trip_records')}}
where pickup_datetime<=dropoff_datetime
and access_a_ride_flag in ('Y','N')
and on_scene_datetime is not null
and dropoff_datetime is not null