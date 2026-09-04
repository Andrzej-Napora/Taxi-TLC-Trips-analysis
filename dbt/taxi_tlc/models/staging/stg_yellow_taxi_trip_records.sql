
with yellow_taxi_trip_records_cleaned as(
    select
        vendorid AS vendor_id,
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        passenger_count,
        trip_distance,
        ratecodeid AS ratecode_id,
        store_and_fwd_flag,
        pulocationid AS PU_Location_ID,
        dolocationid AS DO_Location_ID,
        payment_type,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        improvement_surcharge,
        total_amount,
        congestion_surcharge,
        cbd_congestion_fee,
        airport_fee,
        
        coalesce(fare_amount,0)
        +coalesce(extra,0)
        +coalesce(tip_amount,0)
        +coalesce(tolls_amount,0)
        +coalesce(mta_tax,0)
        +coalesce(congestion_surcharge,0)
        +coalesce(improvement_surcharge,0)
        +coalesce(airport_fee,0)
        as raw_total
    from {{source('raw' , 'yellow_trip_records')}}
),

yellow_taxi_trip_records_additional_columns as(
select
    vendor_id,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
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
            ratecode_id is null then 99
            else ratecode_id
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
where (vendor_id is null or vendor_id in (1,2,6,7))
and (payment_type is null or payment_type in (0,1,2,3,4,5,6))
and (ratecode_id is null or ratecode_id in (1,2,3,4,5,6,99))
and (store_and_fwd_flag is null or store_and_fwd_flag in ('y','n'))