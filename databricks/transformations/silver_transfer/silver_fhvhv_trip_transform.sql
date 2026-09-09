create or replace table workspace.silver.fhvhv_trip_records
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

from workspace.bronze.fhvhv_trip_records
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
`PULocationID` as pu_location_id,
`DOLocationID` as do_location_id,
cast(null as int) as ratecode_id,
case
    when
    pickup_datetime = dropoff_datetime
    then 1
    else 0
end as equal_pu_do_time,
case 
    when driver_pay < 0
    or base_passenger_fare < 0
    or airport_fee < 0
    or cbd_congestion_fee < 0
    or sales_tax < 0
    or tips < 0
    or bcf < 0
    or tolls < 0
    or congestion_surcharge < 0
        then 1
        else 0
end as is_negative,
trip_miles as trip_distance,
congestion_surcharge,
cbd_congestion_fee,
airport_fee,
cast(null as int) as ratecode_id_corrected,
case 
    when request_datetime>=on_scene_datetime
    then 1
    else 0
end as time_inconsistency,
trip_time,
shared_request_flag,
shared_match_flag,
access_a_ride_flag,
wav_request_flag,
wav_match_flag,
cast(null as string) as shared_ride,
'high_volume' as data_type
from time_change
where pickup_datetime is not null
and dropoff_datetime is not null
and PULocationID is not null
and DOLocationID is not null
and trip_miles is not null
and (shared_request_flag in ('y','n','Y','N') or shared_request_flag is null)
and (shared_match_flag in ('y','n','Y','N') or shared_match_flag is null)
and (access_a_ride_flag in ('y','n','Y','N') or access_a_ride_flag is null)
and (wav_request_flag in ('y','n','Y','N') or wav_request_flag is null)
and (wav_match_flag in ('y','n','Y','N') or wav_match_flag is null)
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
where ((trip_distance<0 and is_negative=1) or (trip_distance>=0 and is_negative=0))
and dropoff_datetime >= pickup_datetime
