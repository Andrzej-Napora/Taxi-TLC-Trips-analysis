select
tpep_pickup_datetime as pickup_datetime,
 -- time shift in new york
case 
    when
        EXTRACT(MONTH FROM tpep_pickup_datetime) = 11
        AND EXTRACT(DAY FROM tpep_pickup_datetime) BETWEEN 1 AND 7
        AND EXTRACT(DOW FROM tpep_pickup_datetime) = 0
        AND EXTRACT(HOUR FROM tpep_pickup_datetime) = 1
        AND tpep_dropoff_datetime + INTERVAL '1 hour' > tpep_pickup_datetime
    then tpep_dropoff_datetime + interval '1 hour'
    else tpep_dropoff_datetime
end as dropOff_datetime,
PU_Location_ID,
DO_Location_ID,
EXTRACT(EPOCH FROM 
(tpep_dropoff_datetime-tpep_pickup_datetime)::interval)::
integer AS trip_time_calc,
equal_pu_do_time,
is_negative,
trip_distance,
congestion_surcharge,
Airport_fee,
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
'yellow' as data_type
from {{ref('stg_yellow_taxi_trip_records')}}
where (tpep_pickup_datetime is not null
    and tpep_dropoff_datetime is not null
    and trip_distance is not null
    and PU_Location_ID is not null
    and DO_Location_ID is not null)
    and ((trip_distance<0 and is_negative=1) or (trip_distance>=0 and is_negative=0))
    and tpep_dropoff_datetime >= tpep_pickup_datetime
