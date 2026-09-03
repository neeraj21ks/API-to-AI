SELECT
    symbol,
    interval,
    open_time,
    volume

FROM "neondb"."analytics"."stg_crypto_klines"

WHERE volume < 0