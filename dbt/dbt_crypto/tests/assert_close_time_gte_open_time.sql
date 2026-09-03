SELECT
    symbol,
    interval,
    open_time,
    close_time

FROM {{ ref('stg_crypto_klines') }}

WHERE close_time < open_time
