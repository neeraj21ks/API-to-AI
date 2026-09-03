SELECT
    symbol,
    interval,
    open_time,
    low,
    close

FROM {{ ref('stg_crypto_klines') }}

WHERE low > close