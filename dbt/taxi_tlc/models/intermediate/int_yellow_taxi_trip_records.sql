select
tpep_pickup_datetime as pickup_datetime,
tpep_dropoff_datetime as dropOff_datetime,
PULocationID,
DOLocationID,
EXTRACT(EPOCH FROM 
(tpep_dropoff_datetime-tpep_pickup_datetime)::interval)::
integer AS trip_time_calc,
equal_pu_do_time,
is_negative,
trip_distance,
congestion_surcharge,
cbd_congestion_fee,
Airport_fee,
RatecodeID,
ratecodeid_corrected,
null::integer as trip_time_inconsistency,
null::integer as time_inconsistency,
null::integer as trip_time,
null::text as shared_request_flag,
null::text as shared_match_flag,
null::text as access_a_ride_flag,
null::text as wav_request_flag,
null::text as wav_match_flag,
null::integer as shared_ride
from {{ref('stg_yellow_taxi_trip_records')}}
where (tpep_pickup_datetime is not null
    and tpep_dropoff_datetime is not null
    and trip_distance is not null
    and PULocationID is not null
    and DOLocationID is not null)
    and tpep_dropoff_datetime>=tpep_pickup_datetime