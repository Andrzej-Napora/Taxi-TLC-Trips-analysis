select
    dispatching_base_num,
    pickup_datetime,
    dropOff_datetime,
    PUlocationID as PU_Location_ID,
    DOlocationID as DO_Location_ID,
    coalesce(nullif(SR_Flag, '')::integer, 0) as sr_flag,
    Affiliated_base_number,
    case
        when PUlocationID = DOlocationID
            then 1
            else 0
    end as equal_pu_do_time
    from {{source('raw','fhv_trip_records')}}
    where pickup_datetime <= dropOff_datetime