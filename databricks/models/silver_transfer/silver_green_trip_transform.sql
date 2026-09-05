create or replace table workspace.silver.green_trip_records
using delta as

with time_change as(
select *,

--the date of time rollback in new york - first sunday of november 2AM
next_day(
make_date(year(lpep_pickup_datetime), 10, 31),
'SUN'
) + INTERVAL 2 HOURS as winter_time_change,

--the date of time change in new york - second sunday of march 2AM
next_day(
    make_date(year(lpep_pickup_datetime), 3, 7),
    'SUN'
) + INTERVAL 2 HOURS as summer_time_change

from workspace.bronze.green_trip_records
),

transform as(
select
lpep_pickup_datetime as pickup_datetime,
 -- time shift in new york
case 
    when (lpep_pickup_datetime<=winter_time_change 
    and winter_time_change<lpep_dropoff_datetime+ interval 1 hour)
    then lpep_dropoff_datetime + interval 1 hour

    when lpep_pickup_datetime < summer_time_change 
    and lpep_dropoff_datetime >= summer_time_change + interval 1 hour
    then lpep_dropoff_datetime - interval 1 hour

    else lpep_dropoff_datetime
end as dropoff_datetime,
`PULocationID` as pu_location_id,
`DOLocationID` as do_location_id,
try_cast(`RatecodeID` as BIGINT) as ratecode_id,
trip_distance,
congestion_surcharge,
cbd_congestion_fee,
cast(null as DEC) as airport_fee,
CAST(NULL AS INT) as time_inconsistency,
CAST(NULL AS INT) as trip_time,
CAST(NULL AS STRING) as shared_request_flag,
CAST(NULL AS STRING) as shared_match_flag,
CAST(NULL AS STRING) as access_a_ride_flag,
CAST(NULL AS STRING) as wav_request_flag,
CAST(NULL AS STRING) as wav_match_flag,
CAST(NULL AS STRING) as shared_ride,

coalesce(fare_amount,0)
+coalesce(extra,0)
+coalesce(tip_amount,0)
+coalesce(tolls_amount,0)
+coalesce(mta_tax,0)
+coalesce(congestion_surcharge,0)
+coalesce(improvement_surcharge,0)
as raw_total,

case 
    when
    fare_amount < 0
    or mta_tax < 0
    or improvement_surcharge < 0
    or total_amount < 0
    or extra < 0
    or tip_amount < 0
    or tolls_amount < 0
    or congestion_surcharge < 0
    then 1
    else 0
end as is_negative,
case
    when
        `RatecodeID` is null then 99
        else `RatecodeID`
    end as ratecode_id_corrected,
case
    when
    lpep_pickup_datetime = lpep_dropoff_datetime
    then 1
    else 0
end as equal_pu_do_time,
'green' as data_type,
total_amount
from time_change
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
CAST(
    timestampdiff( SECOND, pickup_datetime, dropoff_datetime) as INT
) AS trip_time_calc,
case
    when
    abs(total_amount-raw_total)>0.0001 then 1
    else 0
end as inconsistent_total_amount

from transform

where (pickup_datetime is not null
and dropOff_datetime is not null
and trip_distance is not null
and pu_location_id is not null
and do_location_id is not null)
and ((trip_distance<0 and is_negative=1) or (trip_distance>=0 and is_negative=0))
and dropOff_datetime >= pickup_datetime;
