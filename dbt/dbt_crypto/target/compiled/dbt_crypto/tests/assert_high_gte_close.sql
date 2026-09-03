SELECT
    symbol,
    interval,
    open_time,
    open,
    high,
    close

FROM "neondb"."analytics"."stg_crypto_klines"

WHERE high < close