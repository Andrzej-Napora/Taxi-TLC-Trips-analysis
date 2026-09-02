select
    dispatching_base_num,
    pickup_datetime,
    "dropOff_datetime" as dropOff_datetime,
    "PUlocationID" as PULocationID,
    "DOlocationID" as DOLocationID,
    "SR_Flag" as SR_Flag,
    "Affiliated_base_number" as Affiliated_base_number,
    case
        when "PUlocationID" = "DOlocationID"
            then 1
            else 0
    end as equal_pu_do_time
    from {{source('raw','for_hire_taxi_trip_records')}}
    where pickup_datetime <= "dropOff_datetime"