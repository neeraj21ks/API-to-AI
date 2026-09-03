SELECT
    symbol,
    interval,
    open_time

FROM "neondb"."analytics"."stg_crypto_klines"

WHERE interval <> '1m'