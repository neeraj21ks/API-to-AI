SELECT
    symbol,
    interval,
    open_time,
    high,
    low

FROM "neondb"."analytics"."stg_crypto_klines"

WHERE high < low