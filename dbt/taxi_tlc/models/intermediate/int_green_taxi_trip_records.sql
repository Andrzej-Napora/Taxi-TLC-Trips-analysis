select
lpep_pickup_datetime as pickup_datetime,
lpep_dropoff_datetime as dropOff_datetime,
PU_Location_ID,
DO_Location_ID,
EXTRACT(EPOCH FROM 
(lpep_dropoff_datetime-lpep_pickup_datetime)::interval)::
integer AS trip_time_calc,
equal_pu_do_time,
is_negative,
trip_distance,
congestion_surcharge,
cbd_congestion_fee,
null::dec as Airport_fee,
ratecodeid_corrected as ratecode_id,
null::integer as trip_time_inconsistency,
null::integer as time_inconsistency,
null::integer as trip_time,
null::text as shared_request_flag,
null::text as shared_match_flag,
null::text as access_a_ride_flag,
null::text as wav_request_flag,
null::text as wav_match_flag,
null::text as shared_ride,
'green' as data_type
from {{ref('stg_green_taxi_trip_records')}}
where (lpep_pickup_datetime is not null
    and lpep_dropoff_datetime is not null
    and trip_distance is not null
    and PU_Location_ID is not null
    and DO_Location_ID is not null)
    and lpep_dropoff_datetime>=lpep_pickup_datetime