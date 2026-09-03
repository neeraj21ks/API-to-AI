SELECT
    symbol,
    interval,
    open_time,
    close_time

FROM "neondb"."analytics"."stg_crypto_klines"

WHERE close_time < open_time