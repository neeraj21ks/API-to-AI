SELECT
    symbol,
    interval,
    open_time,
    COUNT(*) AS record_count

FROM {{ ref('fact_crypto_klines') }}

GROUP BY
    symbol,
    interval,
    open_time

HAVING COUNT(*) > 1