SELECT
    symbol,
    interval,
    open_time,
    COUNT(*) AS duplicate_count

FROM {{ ref('stg_crypto_klines') }}

GROUP BY
    symbol,
    interval,
    open_time

HAVING COUNT(*) > 1
