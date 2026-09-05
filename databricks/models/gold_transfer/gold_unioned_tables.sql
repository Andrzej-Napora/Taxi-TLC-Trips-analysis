create or replace table workspace.gold.unioned_tables
using delta as(

    (
    select
      pickup_datetime,
      dropoff_datetime,
      cast(pu_location_id as bigint) as pu_location_id,
      cast(do_location_id as bigint) as do_location_id,
      cast(trip_distance as double) as trip_distance,
      cast(congestion_surcharge as double) as congestion_surcharge,
      cast(cbd_congestion_fee as double) as cbd_congestion_fee,
      cast(airport_fee as double) as airport_fee,
      time_inconsistency,
      cast(trip_time as bigint) as trip_time,
      shared_request_flag,
      shared_match_flag,
      access_a_ride_flag,
      wav_request_flag,
      wav_match_flag,
      shared_ride,
      is_negative,
      cast(ratecode_id_corrected as bigint) as ratecode_id_corrected,
      equal_pu_do_time,
      data_type,
      trip_time_calc,
      inconsistent_total_amount
    from workspace.silver.yellow_trip_records
    )
    union all
    (
    select
      pickup_datetime,
      dropoff_datetime,
      cast(pu_location_id as bigint) as pu_location_id,
      cast(do_location_id as bigint) as do_location_id,
      cast(trip_distance as double) as trip_distance,
      cast(congestion_surcharge as double) as congestion_surcharge,
      cast(cbd_congestion_fee as double) as cbd_congestion_fee,
      cast(airport_fee as double) as airport_fee,
      time_inconsistency,
      cast(trip_time as bigint) as trip_time,
      shared_request_flag,
      shared_match_flag,
      access_a_ride_flag,
      wav_request_flag,
      wav_match_flag,
      shared_ride,
      is_negative,
      cast(ratecode_id_corrected as bigint) as ratecode_id_corrected,
      equal_pu_do_time,
      data_type,
      trip_time_calc,
      inconsistent_total_amount
    from workspace.silver.green_trip_records
    )
    union all
    (
    select
      pickup_datetime,
      dropoff_datetime,
      cast(pu_location_id as bigint) as pu_location_id,
      cast(do_location_id as bigint) as do_location_id,
      cast(trip_distance as double) as trip_distance,
      cast(congestion_surcharge as double) as congestion_surcharge,
      cast(cbd_congestion_fee as double) as cbd_congestion_fee,
      cast(airport_fee as double) as airport_fee,
      time_inconsistency,
      cast(trip_time as bigint) as trip_time,
      shared_request_flag,
      shared_match_flag,
      access_a_ride_flag,
      wav_request_flag,
      wav_match_flag,
      shared_ride,
      is_negative,
      cast(ratecode_id_corrected as bigint) as ratecode_id_corrected,
      equal_pu_do_time,
      data_type,
      trip_time_calc,
      inconsistent_total_amount
    from workspace.silver.fhv_trip_records
    )
    union all
    (
    select
      pickup_datetime,
      dropoff_datetime,
      cast(pu_location_id as bigint) as pu_location_id,
      cast(do_location_id as bigint) as do_location_id,
      cast(trip_distance as double) as trip_distance,
      cast(congestion_surcharge as double) as congestion_surcharge,
      cast(cbd_congestion_fee as double) as cbd_congestion_fee,
      cast(airport_fee as double) as airport_fee,
      time_inconsistency,
      cast(trip_time as bigint) as trip_time,
      shared_request_flag,
      shared_match_flag,
      access_a_ride_flag,
      wav_request_flag,
      wav_match_flag,
      shared_ride,
      is_negative,
      cast(ratecode_id_corrected as bigint) as ratecode_id_corrected,
      equal_pu_do_time,
      data_type,
      trip_time_calc,
      inconsistent_total_amount
    from workspace.silver.fhvhv_trip_records
    )
    
)