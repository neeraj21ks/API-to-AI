SELECT
    symbol,
    interval,
    open_time,
    close_time,
    open,
    high,
    low,
    close,
    volume,
    source,
    batch_id,
    ingested_at
FROM {{ source('crypto', 'clean_events') }}
