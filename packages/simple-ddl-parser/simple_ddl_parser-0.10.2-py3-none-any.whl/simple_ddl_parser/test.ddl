CREATE EXTERNAL TABLE IF NOT EXISTS database.table_name
(
    day_long_nm     string,
    calendar_dt     date,
    source_batch_id string,
    field_qty       decimal(10, 0),
    field_bool      boolean,
    field_float     float,
    create_tmst     timestamp,
    field_double    double,
    field_long      bigint
) PARTITIONED BY (batch_id int) STORED AS PARQUET LOCATION 's3://datalake/table_name/v1'
