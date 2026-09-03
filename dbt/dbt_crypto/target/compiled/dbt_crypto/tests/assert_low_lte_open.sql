SELECT
    symbol,
    interval,
    open_time,
    open,
    low

FROM "neondb"."analytics"."stg_crypto_klines"

WHERE low > open