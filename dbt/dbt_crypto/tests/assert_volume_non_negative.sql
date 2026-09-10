SELECT
    symbol,
    interval,
    open_time,
    volume

FROM {{ ref('stg_crypto_klines') }}

WHERE volume < 0
