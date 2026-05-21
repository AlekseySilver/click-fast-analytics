CREATE TABLE nyc_taxi (
    trip_id Int64,
    vendor_id Nullable(Int64),
    pickup_date Nullable(Date),
    pickup_datetime DateTime,
    dropoff_date Nullable(Date),
    dropoff_datetime Nullable(DateTime),
    store_and_fwd_flag Nullable(Int64),
    rate_code_id Nullable(Int64),
    pickup_longitude Nullable(Float64),
    pickup_latitude Nullable(Float64),
    dropoff_longitude Nullable(Float64),
    dropoff_latitude Nullable(Float64),
    passenger_count Nullable(Int64),
    trip_distance Nullable(String),
    fare_amount Nullable(String),
    extra Nullable(String),
    mta_tax Nullable(String),
    tip_amount Nullable(String),
    tolls_amount Nullable(Float64),
    ehail_fee Nullable(Int64),
    improvement_surcharge Nullable(String),
    total_amount Nullable(String),
    payment_type Nullable(String),
    trip_type Nullable(Int64),
    pickup Nullable(String),
    dropoff Nullable(String),
    cab_type Nullable(String),
    pickup_nyct2010_gid Nullable(Int64),
    pickup_ctlabel Nullable(Float64),
    pickup_borocode Nullable(Int64),
    pickup_ct2010 Nullable(String),
    pickup_boroct2010 Nullable(String),
    pickup_cdeligibil Nullable(String),
    pickup_ntacode Nullable(String),
    pickup_ntaname Nullable(String),
    pickup_puma Nullable(Int64),
    dropoff_nyct2010_gid Nullable(Int64),
    dropoff_ctlabel Nullable(Float64),
    dropoff_borocode Nullable(Int64),
    dropoff_ct2010 Nullable(String),
    dropoff_boroct2010 Nullable(String),
    dropoff_cdeligibil Nullable(String),
    dropoff_ntacode Nullable(String),
    dropoff_ntaname Nullable(String),
    dropoff_puma Nullable(Int64)
) ENGINE = MergeTree()
ORDER BY (pickup_datetime, trip_id);


-- https://clickhouse.com/docs/getting-started/quick-start/oss
INSERT INTO nyc_taxi
SELECT * FROM s3(
'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_0.gz',
'TabSeparatedWithNames'
)
SETTINGS input_format_allow_errors_num=25000;


select count(*)
from nyc_taxi;