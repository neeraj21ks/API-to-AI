SELECT
    symbol,
    interval,
    open_time

FROM {{ ref('stg_crypto_klines') }}

WHERE symbol NOT IN ('BTCUSDT', 'ETHUSDT', 'SOLUSDT')
