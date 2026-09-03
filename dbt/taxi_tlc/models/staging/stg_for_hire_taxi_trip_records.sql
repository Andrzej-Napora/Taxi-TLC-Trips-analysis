select
    dispatching_base_num,
    pickup_datetime,
    dropOff_datetime,
    pulocationid as PU_Location_ID,
    pulocationid as DO_Location_ID,
    sr_flag,
    affiliated_base_number,
    case
        when PUlocationID = DOlocationID
            then 1
            else 0
    end as equal_pu_do_time
    from {{source('raw','fhv_trip_records')}}
    where sr_flag in (0,1)