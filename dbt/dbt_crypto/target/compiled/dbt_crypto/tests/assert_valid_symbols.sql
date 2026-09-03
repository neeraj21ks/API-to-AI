SELECT
    symbol,
    interval,
    open_time

FROM "neondb"."analytics"."stg_crypto_klines"

WHERE symbol NOT IN ('BTCUSDT', 'ETHUSDT', 'SOLUSDT')