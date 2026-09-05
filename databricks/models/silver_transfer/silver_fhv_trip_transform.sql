create or replace table workspace.silver.fhv_trip_records
using delta as

with time_change as(
select *,

--the date of time rollback in new york - first sunday of november 2AM
next_day(
make_date(year(pickup_datetime), 10, 31),
'SUN'
) + INTERVAL 2 HOURS as winter_time_change,

--the date of time change in new york - second sunday of march 2AM
next_day(
    make_date(year(pickup_datetime), 3, 7),
    'SUN'
) + INTERVAL 2 HOURS as summer_time_change

from workspace.bronze.fhv_trip_records
),

transform as (select
pickup_datetime,
 -- time shift in new york
case 
    when (pickup_datetime<=winter_time_change 
    and winter_time_change<dropoff_datetime+ interval 1 hour)
    then dropoff_datetime + interval 1 hour

    when pickup_datetime < summer_time_change 
    and dropoff_datetime >= summer_time_change + interval 1 hour
    then dropoff_datetime - interval 1 hour

    else dropoff_datetime
end as dropoff_datetime,
`PUlocationID` as pu_location_id,
`DOlocationID` as do_location_id,
cast(null as INT) as ratecode_id,
cast(null as DEC) as trip_distance,
cast(null as DEC) as congestion_surcharge,
cast(null as DEC) as cbd_congestion_fee,
cast(null as DEC) as airport_fee,
cast(null as INT) as time_inconsistency,
cast(null as INT) as trip_time,
cast(null as string) as shared_request_flag,
cast(null as string) as shared_match_flag,
cast(null as string) as access_a_ride_flag,
cast(null as string) as wav_request_flag,
cast(null as string) as wav_match_flag,
case
    when `SR_Flag` = 1 
        and dispatching_base_num in ('b02510','b02844')
        then 'likely_shared_ride'
    when `SR_Flag` = 1
        and dispatching_base_num not in ('b02510','b02844')
        then 'shared_ride'
    else 'not_shared_ride'
end as shared_ride,
cast(null as INT) as is_negative,
cast(null as INT) as ratecode_id_corrected,
case
    when
    pickup_datetime = dropoff_datetime
    then 1
    else 0
end as equal_pu_do_time,
cast(null as INT) as inconsistent_total_amount,
'for_hire' as data_type
from time_change
where pickup_datetime is not null
    and dropOff_datetime is not null
    and `PUlocationID` is not null
    and `DOlocationID` is not null
) 

select
pickup_datetime,
dropoff_datetime,
pu_location_id,
do_location_id,
trip_distance,
congestion_surcharge,
cbd_congestion_fee,
airport_fee,
time_inconsistency,
trip_time,
shared_request_flag,
shared_match_flag,
access_a_ride_flag,
wav_request_flag,
wav_match_flag,
shared_ride,
is_negative,
ratecode_id_corrected,
equal_pu_do_time,
data_type,
cast(
    timestampdiff(SECOND, pickup_datetime, dropoff_datetime) as INT
) AS trip_time_calc,
cast(null as int) as inconsistent_total_amount
from transform
where dropoff_datetime >= pickup_datetime
