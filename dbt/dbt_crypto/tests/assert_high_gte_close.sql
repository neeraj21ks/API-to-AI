SELECT
    symbol,
    interval,
    open_time,
    open,
    high,
    close

FROM {{ ref('stg_crypto_klines') }}

WHERE high < close
