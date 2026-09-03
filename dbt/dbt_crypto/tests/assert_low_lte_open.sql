SELECT
    symbol,
    interval,
    open_time,
    open,
    low

FROM {{ ref('stg_crypto_klines') }}

WHERE low > open
