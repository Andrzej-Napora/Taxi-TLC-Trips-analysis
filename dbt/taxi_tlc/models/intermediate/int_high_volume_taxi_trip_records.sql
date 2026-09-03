select
pickup_datetime,
 -- time shift in new york
case 
    when
        EXTRACT(MONTH FROM pickup_datetime) = 11
        AND EXTRACT(DAY FROM pickup_datetime) BETWEEN 1 AND 7
        AND EXTRACT(DOW FROM pickup_datetime) = 0
        AND EXTRACT(HOUR FROM pickup_datetime) = 1
        AND dropoff_datetime + INTERVAL '1 hour' > pickup_datetime
    then dropOff_datetime + interval '1 hour'
    else dropoff_datetime
end as dropOff_datetime,
PU_Location_ID,
DO_Location_ID,
EXTRACT(EPOCH FROM 
(dropoff_datetime-pickup_datetime)::interval)::
integer AS trip_time_calc,
equal_pu_do_time,
is_negative,
trip_miles as trip_distance,
congestion_surcharge,
airport_fee,
null::integer as ratecode_id,
case
    when 
    abs(EXTRACT(EPOCH FROM 
    (dropoff_datetime-pickup_datetime)::interval)::
    integer-trip_time) > 1
    then 1
    else 0
end as trip_time_inconsistency,
time_inconsistency,
trip_time,
shared_request_flag,
shared_match_flag,
access_a_ride_flag,
wav_request_flag,
wav_match_flag,
null::text as shared_ride,
'high_volume' as data_type
from {{ref('stg_high_volume_taxi_trip_records')}}
where (pickup_datetime is not null
and dropoff_datetime is not null
and PU_Location_ID is not null
and DO_Location_ID is not null
and trip_miles is not null)
and ((trip_miles<0 and is_negative=1) or (trip_miles>=0 and is_negative=0))
and dropoff_datetime >= pickup_datetime
