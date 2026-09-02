with green_taxi_trip_records_cleaned as(
    select
        "VendorID" AS vendor_id,
        lpep_pickup_datetime,
        lpep_dropoff_datetime,
        passenger_count,
        trip_distance,
        "RatecodeID" AS ratecode_id,
        store_and_fwd_flag,
        "PULocationID" AS PU_Location_ID,
        "DOLocationID" AS DO_Location_ID,
        payment_type,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        ehail_fee,
        trip_type,
        improvement_surcharge,
        total_amount,
        congestion_surcharge,
        cbd_congestion_fee,
        fare_amount
        +extra
        +tip_amount
        +tolls_amount
        +mta_tax
        +coalesce(congestion_surcharge,0)
        +cbd_congestion_fee
        +improvement_surcharge
        as raw_total
    from {{source('raw' , 'green_taxi_trip_records')}}
),

green_taxi_trip_records_additional_columns as(
select
    vendor_id,
    lpep_pickup_datetime,
    lpep_dropoff_datetime,
    store_and_fwd_flag,
    ratecode_id,
    PU_Location_ID,
    DO_Location_ID,
    passenger_count,
    trip_distance,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    payment_type,
    congestion_surcharge,
    cbd_congestion_fee,
    total_amount,
    round(
        raw_total::numeric,2
    ) as raw_total,
    total_amount-raw_total as difference,
    case
        when
        abs(total_amount-raw_total)>0.0001 then 1
        else 0
    end as inconsistent_total_amount,
    case 
        when
        fare_amount < 0
        or mta_tax < 0
        or improvement_surcharge < 0
        or total_amount < 0
        or cbd_congestion_fee < 0
        or extra < 0
        or tip_amount < 0
        or tolls_amount < 0
        or congestion_surcharge < 0
        then 1
        else 0
    end as is_negative,
    case
        when
            ratecode_id is null then 99
            else ratecode_id
        end as ratecodeid_corrected,
    case
        when
        lpep_pickup_datetime = lpep_dropoff_datetime
    then 1
    else 0
end as equal_pu_do_time
from green_taxi_trip_records_cleaned
)
select * from green_taxi_trip_records_additional_columns
where lpep_pickup_datetime <= lpep_dropoff_datetime
and PU_Location_ID is not null
and DO_Location_ID is not null