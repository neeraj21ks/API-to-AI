SELECT
    symbol,
    interval,
    open_time,
    open,
    high

FROM {{ ref('stg_crypto_klines') }}

WHERE high < open