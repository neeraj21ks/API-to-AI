SELECT
    symbol,
    interval,
    open_time,
    open,
    high

FROM "neondb"."analytics"."stg_crypto_klines"

WHERE high < open