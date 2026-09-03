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
null::integer as is_negative,
null::dec as trip_distance,
null::dec as congestion_surcharge,
null::dec as airport_fee,
null::integer as ratecode_id,
null::integer as trip_time_inconsistency,
null::integer as time_inconsistency,
null::integer as trip_time,
null::text as shared_request_flag,
null::text as shared_match_flag,
null::text as access_a_ride_flag,
null::text as wav_request_flag,
null::text as wav_match_flag,
case
    when SR_Flag = 1 
        and dispatching_base_num in ('b02510','b02844')
        then 'likely_shared_ride'
    when SR_Flag = 1
        and dispatching_base_num not in ('b02510','b02844')
        then 'requested/shared_ride'
    else 'not_shared_ride'
end as shared_ride,
'for_hire' as data_type
from {{ref('stg_for_hire_taxi_trip_records')}}
where (pickup_datetime is not null
    and dropOff_datetime is not null
    and PU_Location_ID is not null
    and DO_Location_ID is not null)
    and dropoff_datetime >= pickup_datetime