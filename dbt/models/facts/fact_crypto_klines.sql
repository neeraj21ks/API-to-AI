SELECT
    d.symbol_key,
    s.symbol,
    s.interval,
    s.open_time,
    s.close_time,
    s.open,
    s.high,
    s.low,
    s.close,
    s.volume,
    s.source,
    s.batch_id,
    s.ingested_at
FROM {{ ref('stg_crypto_klines') }} s
JOIN {{ ref('dim_symbol') }} d
    ON s.symbol = d.symbol
