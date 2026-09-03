SELECT
    symbol,
    interval,
    open_time,
    high,
    low

FROM {{ ref('stg_crypto_klines') }}

WHERE high < low
