WITH ordered_candles AS (
    SELECT
        symbol,
        interval,
        batch_id,
        open_time,
        LAG(open_time) OVER (
            PARTITION BY symbol, interval, batch_id
            ORDER BY open_time
        ) AS previous_open_time
    FROM {{ ref('stg_crypto_klines') }}
)

SELECT
    symbol,
    interval,
    batch_id,
    previous_open_time,
    open_time,
    open_time - previous_open_time AS gap

FROM ordered_candles

WHERE previous_open_time IS NOT NULL
  AND open_time - previous_open_time > INTERVAL '1 minute'
