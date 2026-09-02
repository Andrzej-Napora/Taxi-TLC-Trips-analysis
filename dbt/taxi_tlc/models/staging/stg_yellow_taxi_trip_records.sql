
with yellow_taxi_trip_records_cleaned as(
    select
        "VendorID" AS VendorID,
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        passenger_count,
        trip_distance,
        "RatecodeID" AS RatecodeID,
        store_and_fwd_flag,
        "PULocationID" AS PULocationID,
        "DOLocationID" AS DOLocationID,
        payment_type,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        improvement_surcharge,
        total_amount,
        congestion_surcharge,
        "Airport_fee" AS airport_fee,
        cbd_congestion_fee,
        fare_amount
        +extra
        +tip_amount
        +tolls_amount
        +mta_tax
        +coalesce(congestion_surcharge,0)
        +cbd_congestion_fee
        +improvement_surcharge
        +"Airport_fee"
        as raw_total
    from {{source('raw' , 'yellow_taxi_trip_records')}}
),

yellow_taxi_trip_records_additional_columns as(
select
    vendorid,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    store_and_fwd_flag,
    ratecodeid,
    PULocationID,
    DOLocationID,
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
    airport_fee,
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
        or airport_fee < 0 
        then 1
        else 0
    end as is_negative,
    case
        when
            ratecodeid is null then 99
            else ratecodeid
        end as ratecodeid_corrected,
    case
        when
        tpep_pickup_datetime = tpep_dropoff_datetime
    then 1
    else 0
    end as equal_pu_do_time
from yellow_taxi_trip_records_cleaned
)
select * from yellow_taxi_trip_records_additional_columns
where tpep_pickup_datetime <= tpep_dropoff_datetime