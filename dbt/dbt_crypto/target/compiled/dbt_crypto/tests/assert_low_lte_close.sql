SELECT
    symbol,
    interval,
    open_time,
    low,
    close

FROM "neondb"."analytics"."stg_crypto_klines"

WHERE low > close