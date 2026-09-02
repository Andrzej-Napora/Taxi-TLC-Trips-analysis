select
pickup_datetime,
dropOff_datetime,
PULocationID,
DOLocationID,
EXTRACT(EPOCH FROM 
(dropoff_datetime-pickup_datetime)::interval)::
integer AS trip_time_calc,
equal_pu_do_time,
null::integer as is_negative,
null::integer as trip_distance,
null::integer as congestion_surcharge,
null::integer as cbd_congestion_fee,
null::integer as airport_fee,
null::integer as RatecodeID,
null::integer as ratecodeid_corrected,
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
        and dispatching_base_num in ('B02510','B02844')
        then 'likely_shared_ride'
    when SR_Flag = 1
        and dispatching_base_num not in ('B02510','B02844')
        then 'requested/shared_ride'
    else 'not_shared_ride'
end as shared_ride
from {{ref('stg_for_hire_taxi_trip_records')}}
where (pickup_datetime is not null
    and dropOff_datetime is not null
    and PULocationID is not null
    and DOLocationID is not null)
    and dropOff_datetime>=pickup_datetime